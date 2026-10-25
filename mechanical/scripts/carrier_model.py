"""The finished STM32 carrier as Blender objects, static: boards A, B and C with every part and wire,
and the NUCLEO-H533RE mock. Shared by animate-carrier-tray.py; animate-stm32-carrier.py builds the same geometry step by step.

Everything is read from ../../hardware/scripts/stm32-carrier.py (`C` below), which owns every hole, part and wire.
This module only gives them bodies. Nothing is hidden or animated here; the caller moves the returned roots.

Frames. The carrier's own frame is the drawing's: X along the vehicle (row 1 at X 0), Y across, Z up from the
board's TOP face, mm. Plate 2's layout frame is x front to rear, y from the vehicle's right. They meet at

    A and B:  plate x = 183.74 + X,  plate y = 28.84 + Y     (grid row 1 at x 183.74, A's outboard edge at y 5.11)
    board C:  its own frame, rotated onto the waist: plate x = 85.5 + (y_l + 3.57), plate y = 25.2 + (x_l + 5.79)

Blender is right-handed with Z up, and the layout's y runs the wrong way, so a point goes in as (x, -y, z).
"""
import bpy, importlib.util, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("carrier", os.path.join(HERE, "..", "..", "hardware", "scripts", "stm32-carrier.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
P = C.P

AB_ORIGIN = (183.74, 28.84)                  # plate-2 (x, y) of the carrier frame's origin
C_ORIGIN = (85.5 + 3.57, 25.2 + 5.79)        # plate-2 (x, y) of board C's frame origin, after its quarter turn
MATS = {}


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)


def mat(name, colour, a=1.0):
    if name not in MATS:
        m = bpy.data.materials.new(name)
        m.diffuse_color = hexc(colour, a) if isinstance(colour, str) else colour
        MATS[name] = m
    return MATS[name]


for _n, _c in [('fr4', '#1f7a3a'), ('pad', '#c9ccd1'), ('hole', '#0b0f0d'), ('black', '#16181c'), ('solder', '#f1f5f9'),
               ('gold', '#d4a52c'), ('brass', '#c8a24a'), ('term2', '#2563eb'), ('term3', '#16a34a'),
               ('screw', '#9ca3af'), ('res', '#d8c28c'), ('band', '#7c2d12'), ('capsleeve', '#1e293b'),
               ('capstripe', '#94a3b8'), ('captop', '#cbd5e1'), ('module', '#1d4ed8'), ('chip', '#111111'),
               ('mterm', '#15803d'), ('jumper', '#dc2626'), ('mark', '#ef4444'), ('silk', '#f8fafc'),
               ('nucleo', '#f2f2ee'), ('usb', '#c0c4ca'), ('led_o', '#f97316'), ('led_g', '#22c55e'),
               ('led_r', '#ef4444'), ('led_b', '#3b82f6'), ('btn_b', '#2563eb'), ('bare', '#e5e7eb')]:
    mat(_n, _c)
for _net, _c in C.NET.items():
    mat('net_' + _net, _c)


class Frame:
    """A carrier frame -> Blender: a point (X, Y, Z) lands at tf(X, Y, Z); proper = the map keeps handedness."""

    def __init__(self, tf, proper, rot=0.0):
        self.tf, self.proper, self.rot = tf, proper, rot


AB = Frame(lambda X, Y, Z: (AB_ORIGIN[0] + X, -(AB_ORIGIN[1] + Y), Z), proper=False)
CF = Frame(lambda X, Y, Z: (C_ORIGIN[0] + Y, -(C_ORIGIN[1] + X), Z), proper=True, rot=-math.pi / 2)


class Mesh:
    """Boxes, cylinders and cones, one material slot per name, in one object."""

    def __init__(self, frame):
        self.f_, self.v, self.f, self.mi, self.names = frame, [], [], [], []

    def _m(self, name):
        if name not in self.names:
            self.names.append(name)
        return self.names.index(name)

    def box(self, x0, x1, y0, y1, z0, z1, m):
        i, k = len(self.v), self._m(m)
        x0, x1, y0, y1, z0, z1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1)
        self.v += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                   (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        for q in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.f.append(tuple(i + a for a in q))
            self.mi.append(k)

    def cone(self, a, b, r0, r1, m, n=16):
        a, b = Vector(a), Vector(b)
        ax = (b - a).normalized()
        u = ax.orthogonal().normalized()
        w = ax.cross(u)
        i, k = len(self.v), self._m(m)
        for j in range(n):
            t = 2 * math.pi * j / n
            d = u * math.cos(t) + w * math.sin(t)
            self.v += [tuple(a + d * r0), tuple(b + d * r1)]
        for j in range(n):
            p, q = 2 * j, 2 * ((j + 1) % n)
            self.f.append((i + p, i + q, i + q + 1, i + p + 1))
            self.mi.append(k)
        self.f.append(tuple(i + 2 * j for j in reversed(range(n))))
        self.mi.append(k)
        self.f.append(tuple(i + 2 * j + 1 for j in range(n)))
        self.mi.append(k)

    def cyl(self, a, b, r, m, n=16):
        self.cone(a, b, r, r, m, n)

    def make(self, name, parent=None):
        me = bpy.data.meshes.new(name)
        faces = [tuple(reversed(f)) if not self.f_.proper else tuple(f) for f in self.f]
        me.from_pydata([self.f_.tf(*v) for v in self.v], [], faces)
        for nm in self.names:
            me.materials.append(MATS[nm])
        for p, k in zip(me.polygons, self.mi):
            p.material_index = k
        me.update()
        o = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(o)
        if parent is not None:
            o.parent = parent
        return o


def wire(name, pts, net, kind, parent, frame, colour=None, z=None):
    """An insulated run on the solder side, pad to pad."""
    r = {'ins': 0.55, 'pwr': 0.9, 'lead': 0.3}[kind]
    z = -1.6 - r if z is None else z
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = '3D', r, 3, True
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = frame.tf(q[0], q[1], q[2] if len(q) > 2 else z) + (1,)
    cu.materials.append(mat('wire' + colour, colour) if colour else MATS['bare' if kind == 'lead' else 'net_' + net])
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    o.parent = parent
    return o


def joints(name, xys, parent, frame):
    m = Mesh(frame)
    for x, y in xys:
        m.cone((x, y, -1.6), (x, y, -2.9), 1.05, 0.3, 'solder', 10)
    return m.make(name, parent)


def label(text, x, y, z, size, parent, frame, rot=0.0, m='silk'):
    cu = bpy.data.curves.new(text, 'FONT')
    cu.body, cu.size, cu.align_x = text, size, 'CENTER'
    cu.materials.append(MATS[m])
    o = bpy.data.objects.new('lab-' + text, cu)
    o.location = frame.tf(x, y, z)
    o.rotation_euler = (0, 0, rot + frame.rot)
    bpy.context.scene.collection.objects.link(o)
    o.parent = parent
    return o


def empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    bpy.context.scene.collection.objects.link(e)
    if parent is not None:
        e.parent = parent
    return e


def perfboard(name, edges_x, edges_y, holes, parent, frame):
    m = Mesh(frame)
    m.box(edges_x[0], edges_x[1], edges_y[0], edges_y[1], -1.6, 0, 'fr4')
    for x, y in holes:
        m.cyl((x, y, 0), (x, y, 0.04), 0.9, 'pad', 8)
        m.cyl((x, y, 0.04), (x, y, 0.05), 0.42, 'hole', 8)
    return m.make(name, parent)


def terminal(name, pins_xy, along_x, entry, parent, frame):
    xs, ys = [p[0] for p in pins_xy], [p[1] for p in pins_xy]
    if along_x:
        X0, X1, Y0, Y1 = min(xs) - 2.5, max(xs) + 2.5, ys[0] - 3.8, ys[0] + 3.8
    else:
        X0, X1, Y0, Y1 = xs[0] - 3.8, xs[0] + 3.8, min(ys) - 2.5, max(ys) + 2.5
    m = Mesh(frame)
    m.box(X0, X1, Y0, Y1, 0, 10, 'term3' if len(pins_xy) == 3 else 'term2')
    for x, y in pins_xy:
        m.cyl((x, y, 10), (x, y, 10.4), 1.6, 'screw', 14)
        m.box(x - 1.3, x + 1.3, y - 0.25, y + 0.25, 10.4, 10.5, 'hole')
        if entry in ('-Y', '+Y'):
            ye = Y0 if entry == '-Y' else Y1
            m.box(x - 1.5, x + 1.5, ye - 0.05, ye + 0.05, 3.2, 6.6, 'hole')
        elif entry in ('-X', '+X'):
            xe = X0 if entry == '-X' else X1
            m.box(xe - 0.05, xe + 0.05, y - 1.5, y + 1.5, 3.2, 6.6, 'hole')
        m.cyl((x, y, 0), (x, y, -2.6), 0.5, 'screw', 6)
    return m.make(name, parent)


def resistor(name, a, b, parent, frame):
    a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
    mid, d = (a + b) / 2, (b - a).normalized()
    m = Mesh(frame)
    zc = 1.6
    m.cyl(tuple(a + Vector((0, 0, zc))), tuple(mid - d * 3.1 + Vector((0, 0, zc))), 0.28, 'screw', 6)
    m.cyl(tuple(b + Vector((0, 0, zc))), tuple(mid + d * 3.1 + Vector((0, 0, zc))), 0.28, 'screw', 6)
    for p in (a, b):
        m.cyl(tuple(p + Vector((0, 0, zc))), tuple(p + Vector((0, 0, -2.6))), 0.28, 'screw', 6)
    m.cyl(tuple(mid - d * 3.1 + Vector((0, 0, zc))), tuple(mid + d * 3.1 + Vector((0, 0, zc))), 1.2, 'res', 14)
    for t in (-1.9, -1.0, 0.0, 1.6):
        m.cyl(tuple(mid + d * (t - 0.3) + Vector((0, 0, zc))), tuple(mid + d * (t + 0.3) + Vector((0, 0, zc))), 1.25, 'band', 14)
    return m.make(name, parent)


def capacitor(name, minus, plus, parent, frame):
    cx, cy = (minus[0] + plus[0]) / 2, (minus[1] + plus[1]) / 2
    m = Mesh(frame)
    m.cyl((cx, cy, 0.3), (cx, cy, 13), 5.0, 'capsleeve', 28)
    m.cyl((cx, cy, 13), (cx, cy, 13.05), 4.6, 'captop', 28)
    dx, dy = minus[0] - cx, minus[1] - cy
    n = math.hypot(dx, dy) or 1
    m.box(cx + dx / n * 4.7 - 1.2, cx + dx / n * 4.7 + 1.2, cy + dy / n * 4.7 - 1.2, cy + dy / n * 4.7 + 1.2, 0.5, 12.8, 'capstripe')
    for x, y in (minus, plus):
        m.cyl((x, y, 0.3), (x, y, -2.6), 0.3, 'screw', 6)
    return m.make(name, parent)


def build_ab(parent, z):
    """Boards A and B, populated and wired, under an empty at height z (the boards' top face). Returns that empty."""
    hole = lambda b, c, r: C.hole(b, c, r)
    car = empty('carrier-ab', parent, (0, 0, z))
    for b in ('A', 'B'):
        cfg = C.BOARD[b]
        perfboard('board-' + b, C.bx(b), cfg['edge'], [hole(b, c, r) for c in range(1, cfg['cols'] + 1) for r in range(1, cfg['rows'] + 1)], car, AB)
    label('A', C.bx('A')[0] + 3.2, C.BOARD['A']['edge'][0] + 2.0, 0.06, 4, car, AB)
    label('B', C.bx('B')[0] + 3.2, C.BOARD['B']['edge'][1] - 5.0, 0.06, 4, car, AB)
    pins = []
    for i, (b, col, lab) in enumerate(C.SOCKETS):             # the four 1x19 sockets under the Nucleo's morpho headers
        y = C.cy(b, C.ci(col))
        m = Mesh(AB)
        m.box(C.NX(C.NUC_ROWS) - 1.27, C.NX(1) + 1.27, y - 1.25, y + 1.25, 0, 8.5, 'black')
        for k in range(1, C.NUC_ROWS + 1):
            m.box(C.NX(k) - 0.5, C.NX(k) + 0.5, y - 0.5, y + 0.5, 8.5, 8.52, 'hole')
            m.cyl((C.NX(k), y, 0), (C.NX(k), y, -2.6), 0.3, 'screw', 6)
            pins.append((C.NX(k), y))
        m.make('socket-' + col + b, car)
    for b, ps, entry, name, colr in C.TERMS:
        xy = [hole(b, C.ci(c), r) for c, r, _ in ps]
        terminal('term-' + name, xy, len({r for _, r, _ in ps}) > 1, entry, car, AB)
        pins += xy
    for b, ps, name in C.MALE:                              # straight, or 90 degrees with the plug lying forward
        m = Mesh(AB)
        for bx_ in C.header_boxes(b, ps, name):
            m.box(*bx_)
        pins += [hole(b, C.ci(c), r) for c, r, _ in ps]
        m.make('header-' + name, car)
    for b, a, c_, lab in C.RES:
        resistor('res-' + lab, hole(b, C.ci(a[0]), a[1]), hole(b, C.ci(c_[0]), c_[1]), car, AB)
    for b, mi, pl, lab in C.CAPS:
        capacitor('cap-' + lab, hole(b, C.ci(mi[0]), mi[1]), hole(b, C.ci(pl[0]), pl[1]), car, AB)
    b, ps = C.XCVR_SOCKET                                    # the module's 1x4 and 1x2 sockets
    xy = [hole(b, C.ci(c), r) for c, r, _ in ps]
    xy2 = [hole(C.CAN_SOCKET[0], C.ci(c), r) for c, r, _ in C.CAN_SOCKET[1]]
    m = Mesh(AB)
    m.box(xy[0][0] - 1.27, xy[0][0] + 1.27, xy[0][1] - 1.27, xy[-1][1] + 1.27, 0, 8.5, 'black')
    m.box(xy2[0][0] - 1.27, xy2[0][0] + 1.27, xy2[0][1] - 1.27, xy2[-1][1] + 1.27, 0, 8.5, 'black')
    m.make('xcvr-socket', car)
    pins += xy + xy2
    # the module lies face down on its sockets: chip and terminal hang underneath
    X0, X1, Y0, Y1 = C.module_box()
    ZB = 11.0
    m = Mesh(AB)
    m.box(X0, X1, Y0, Y1, ZB, ZB + 1.6, 'module')
    m.box(X0, X0 + 2.5, Y0 + 0.3, Y1 - 0.3, ZB - 2.5, ZB, 'black')
    for x, y in [hole(C.XCVR_SOCKET[0], C.ci(c), r) for c, r, _ in C.XCVR_SOCKET[1]]:
        m.box(x - 0.32, x + 0.32, y - 0.32, y + 0.32, 3.0, ZB, 'gold')
    mid, yc = (X0 + X1) / 2, (Y0 + Y1) / 2
    m.box(mid - 4.5, mid - 0.5, yc - 2.5, yc + 2.5, ZB - 1.5, ZB, 'chip')
    m.box(X1 - C.MODULE['terminal'], X1, Y0 + 0.4, Y1 - 0.4, ZB - 9.5, ZB, 'mterm')
    for x, y in [hole(C.CAN_SOCKET[0], C.ci(c), r) for c, r, _ in C.CAN_SOCKET[1]]:
        m.box(x - 1.27, x + 1.27, y - 1.27, y + 1.27, ZB - 2.5, ZB, 'black')
        m.box(x - 0.32, x + 0.32, y - 0.32, y + 0.32, 3.0, ZB, 'gold')
    m.make('module-sn65hvd230', car)
    for net_i, (n, b, ps, kind) in enumerate(C.WIRES):         # the solder side, pad to pad
        xy = [hole(b, c, r) for c, r in ps]
        wire(f'wire-{b}-{n}-{net_i}', xy, n, kind, car, AB)
    for net_i, (n, ps, kind) in enumerate(C.XWIRES):
        xy = [hole(b, c, r) for b, c, r in ps]
        wire(f'bridge-{n}', xy, n, kind, car, AB)
    joints('joints-ab', pins, car, AB)
    return car


def build_c(parent, z):
    """Board C, the 5 V split, populated and wired, with the USB-C socket and its pigtail."""
    cr = empty('carrier-c', parent, (0, 0, z))
    ch = lambda c, r: ((r - 1) * P, (c - 1) * P)
    perfboard('board-C', C.C_EDGE_X, C.C_EDGE_Y, [ch(c, r) for c in range(1, C.C_COLS + 1) for r in range(1, C.C_ROWS + 1)], cr, CF)
    label('C', 29.21, C.C_EDGE_Y[0] + 0.8, 0.06, 2.6, cr, CF)
    pins = []
    for ps, entry, name, note in C.C_TERMS:
        xy = [ch(C.ci(c), r) for c, r, _ in ps]
        terminal('c-term-' + name, xy, False, entry, cr, CF)
        pins += xy
    for a, b_, lab_ in C.C_RES:
        resistor('c-res-' + lab_, ch(C.ci(a[0]), a[1]), ch(C.ci(b_[0]), b_[1]), cr, CF)
        pins += [ch(C.ci(a[0]), a[1]), ch(C.ci(b_[0]), b_[1])]
    capacitor('c-cap-C1', ch(C.ci('c'), 12), ch(C.ci('a'), 12), cr, CF)
    sk = C.C_SOCKET
    Yc = sk['y']
    m = Mesh(CF)
    m.box(sk['flange'][0], sk['flange'][1], Yc - sk['flange_w'] / 2, Yc + sk['flange_w'] / 2, 0, sk['flange_h'], 'black')
    zb = (sk['flange_h'] - sk['body_h']) / 2
    m.box(sk['body'][0], sk['body'][1], Yc - sk['body_w'] / 2, Yc + sk['body_w'] / 2, zb, zb + sk['body_h'], 'black')
    zc = sk['flange_h'] / 2
    m.box(sk['flange'][0] - 0.06, sk['flange'][0], Yc - 4.3, Yc + 4.3, zc - 1.3, zc + 1.3, 'hole')
    m.box(sk['flange'][0] - 0.08, sk['flange'][0] - 0.06, Yc - 3.2, Yc + 3.2, zc - 0.3, zc + 0.3, 'usb')
    m.make('c-usb-socket', cr)
    x1 = sk['body'][1]
    for lab, colour, col, row, ye in C.C_PIGTAIL:
        hx, hy = ch(C.ci(col), row)
        wire('c-pigtail-' + lab, [(x1, ye, zc), (x1 + 2.2, ye, zc), (hx, hy, 3.0), (hx, hy, -2.2)], lab, 'ins', cr, CF, colour=colour)
        pins.append((hx, hy))
    m = Mesh(CF)
    for lab, colour, ye in C.C_CUT:
        m.cyl((x1, ye, zc), (x1 + 1.6, ye, zc), 0.55, 'screw', 8)
        m.cyl((x1 + 1.6, ye, zc), (x1 + 5.0, ye, zc), 0.85, 'capsleeve', 10)
    m.make('c-cut-dplus-dminus', cr)
    m = Mesh(CF)
    yb_, yi_ = (C.ci('b') - 1) * P, (C.ci('i') - 1) * P
    for r in C.C_TIES:
        x = (r - 1) * P
        top = zb + sk['body_h'] if sk['body'][0] < x < x1 else zc + 0.6
        for ya, yb2, z0, z1 in ((yb_, yi_, top, top + 0.4), (yb_, yi_, -2.0, -1.6)):
            m.box(x - 1.25, x + 1.25, ya, yb2, z0, z1, 'captop')
        for y in (yb_, yi_):
            m.box(x - 1.25, x + 1.25, y - 0.2, y + 0.2, -2.0, top + 0.4, 'captop')
        m.box(x - 1.6, x + 1.6, yi_ - 3.2, yi_ - 0.2, top, top + 1.6, 'captop')
    m.make('c-zip-ties', cr)
    for i, (net, ps, kind) in enumerate(C.C_WIRES):
        xy = [ch(c, r) for c, r in ps]
        wire(f'c-wire-{net}-{i}', xy, net, kind, cr, CF)
    joints('c-joints', pins, cr, CF)
    return cr


def build_nucleo(parent, z):
    """The NUCLEO-H533RE mock, seated on A's and B's sockets. Outline and morpho headers are UM3121 Fig. 7; the parts in C.NUC_MOCK
    are read off the same figure, for recognition and clearance only."""
    nx0, nx1 = C.NUC['x']
    ny0, ny1 = C.NUC['y']
    Z0 = 9.0
    Z1 = Z0 + 1.6
    d = Mesh(AB)
    d.box(nx0, nx1, ny0, ny1, Z0, Z1, 'nucleo')
    for b, cols in (('A', ('g', 'h')), ('B', ('i', 'j'))):
        ya, yb = C.cy(b, C.ci(cols[0])), C.cy(b, C.ci(cols[1]))
        d.box(C.NX(C.NUC_ROWS) - 1.27, C.NX(1) + 1.27, min(ya, yb) - 1.27, max(ya, yb) + 1.27, Z1, Z1 + 2.5, 'black')
        for k in range(1, C.NUC_ROWS + 1):
            for y in (ya, yb):
                d.box(C.NX(k) - 0.32, C.NX(k) + 0.32, y - 0.32, y + 0.32, 3.0, Z1 + 3.0, 'gold')
    for side, x0, x1, y0, y1, h, m, _ in C.NUC_MOCK:
        d.box(x0, x1, y0, y1, Z1, Z1 + h, m) if side == 'top' else d.box(x0, x1, y0, y1, Z0 - h, Z0, m)
    o = d.make('nucleo', parent)
    o.location = (0, 0, z)
    label('NUCLEO-H533RE', -27, 42.0, Z1 + 0.05, 3.2, o, AB, m='chip')
    return o
