"""Assembly animation of the STM32 carrier and the 5 V split board (MEC-15, HW-19), by Blender.

    blender -b -P animate-carrier.py                   # -> carrier-animation.mp4, 94 s
    blender -b -P animate-carrier.py -- --preview      # half size, every 4th frame
    blender -b -P animate-carrier.py -- --still 40     # one PNG at 40 s, for checking a moment

Nothing is read from disk but ../hardware/stm32-carrier.py, which owns every hole, part and
wire; this script only gives them bodies. It follows the drawing's build order: the sockets
go in with the Discovery plugged in as the jig, the stack turns over for their joints, the
parts go in, the solder side is wired spine by spine and run by run, the module, jumper and
standoffs go on, and the Discovery drops onto the finished carrier. Board C follows.

Coordinates are the drawing's: X along the vehicle (row 1 at X 0, rear = +X), Y across
(A at -Y, B at +Y), Z up from the boards' top face, millimetres throughout. The drawing puts
+Y DOWN the page, so a right-handed Blender frame with Z up would mirror the board: every
point is written to Blender with Y negated (mirror() below), and nothing else changes.

The STM32F4DISCOVERY is a MOCK: its outline, the P1 / P2 headers and CN1's edge are UM1472
Fig. 10 geometry (the same numbers the drawing uses); every chip, LED, button and connector on
it is placed by eye, for recognition only. Real models (GrabCAD, 3D ContentCentral, DigiKey)
sit behind a login and are not ours to commit.
"""
import bpy, importlib.util, math, os, sys
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "carrier-animation.mp4")
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PREVIEW = "--preview" in ARGS
STILL = float(ARGS[ARGS.index("--still") + 1]) if "--still" in ARGS else None

spec = importlib.util.spec_from_file_location("carrier", os.path.join(HERE, "..", "hardware", "stm32-carrier.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
P = C.P

FPS = 24
S = lambda sec: int(round(sec * FPS)) + 1      # the timeline is written in seconds
END = S(94)

# ---------------------------------------------------------------- timeline (seconds)
SOCKETS_IN = 4.0             # four 1x25 sockets, 0.5 s apart
ROW25 = (6.3, 8.2)           # row 25 marked
DISCO_JIG = (8.2, 10.8)      # the Discovery plugs in as the jig
FLIP1 = (11.0, 13.4)         # over for the socket joints
TACK, SOCK_J = 13.9, 15.3
FLIP1B = (17.0, 19.4)        # back
DISCO_OFF = (19.6, 21.2)
PARTS_T = {'6V IN': 21.6, 'CAN': 22.4, '5V IN': 23.2, 'SERVO': 24.6, 'I2C-B': 25.1, 'I2C-A': 25.6,
           'TERM': 26.3, 'R4 1k': 27.2, 'R3 120R': 27.8, 'C2': 28.6, 'XCVR': 30.2}
FLIP2 = (32.0, 34.4)
PART_J = 34.8
SPINES = (37.2, 42.6)
INSUL = (43.2, 50.6)
BRIDGE = (51.4, 55.0)
FLIP2B = (56.0, 58.4)
MODULE, LINKS, JUMPER, STANDOFFS = 58.8, 60.0, 61.0, 62.0
DISCO_ON = (64.0, 66.6)
C_PARTS = {'terms': 68.4, 'res': 69.6, 'cap': 70.4}
C_FLIP = (72.0, 74.2)
C_J, C_SPINES, C_WIRES = 74.6, (75.4, 77.2), (77.6, 80.2)
C_FLIPB = (81.0, 83.2)
ORBIT = 84.0
DROP = S(0.7) - 1            # how long a part takes to settle
GROW = S(0.9) - 1            # how long a wire takes to run

CAPTIONS = [
    ((0, 4), "Boards A and B: two 5x7 kit boards, 18 x 24 holes, 5.9 mm apart - board C, the 5 V split, beside them"),
    ((4, 8.2), "1  Four 1x25 female sockets: A i/j under P1, B g/h under P2 - row 25 sits on the margin, tail snipped"),
    ((8.2, 11), "2  The Discovery plugs in as the jig: it alone sets the 53.34 mm between the two headers"),
    ((11, 19.4), "3  Turn the stack over and solder the sockets - tack the four corners, check, then the rest"),
    ((19.4, 21.6), "   Lift the Discovery off"),
    ((21.6, 24.6), "4  Screw terminals: 6V IN on A, CAN (3p) and 5V IN on B"),
    ((24.6, 27.2), "5  Male headers: SERVO, I2C-B and I2C-A on A, TERM on B"),
    ((27.2, 30.2), "6  R4 1k in the servo PWM, R3 120R to TERM, C2 470 uF across the servo supply"),
    ((30.2, 32), "7  A 1x4 socket for the SN65HVD230 module"),
    ((32, 37.2), "8  Turn it over: solder every part pin"),
    ((37.2, 43.2), "9  Bare tinned spines: GND col e and 6 V col a on A, GND col j on B"),
    ((43.2, 51.4), "10  Insulated runs: 5 V, 3V3, servo PWM, I2C SCL / SDA, CAN TX / RX, CAN H / L"),
    ((51.4, 56), "11  The bridges: GND along row 1, 3V3 along row 3 - the 3V3 stops at A k3, never j3 (P1-4 VDD)"),
    ((56, 58.8), "   Right way up again"),
    ((58.8, 64), "12  Module in, H / L links to m3 / o3, TERM jumper on, four 10 mm M2.5 standoffs"),
    ((64, 67.4), "13  The Discovery drops onto the carrier"),
    ((67.4, 72), "14  Board C, the 5 V split: four terminals, R1 / R2 10k source Rp for the USB-C, C1 470 uF"),
    ((72, 84), "15  Solder side: 5 V spine col a, GND spine col c, the TO STM32 pair in 18 AWG, the CC network"),
    ((84, 95), "The carrier and the 5 V split, ready for plate 2 (MEC-15, HW-19) - the Discovery is a mock"),
]

# ---------------------------------------------------------------- scene and materials
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)


MATS = {}


def mat(name, colour):
    if name not in MATS:
        m = bpy.data.materials.new(name)
        m.diffuse_color = hexc(colour) if isinstance(colour, str) else colour
        MATS[name] = m
    return MATS[name]


FR4, PAD, HOLE, BLACK = '#1f7a3a', '#c9ccd1', '#0b0f0d', '#16181c'
DISCO_PCB = '#243b63'            # a guess - set to the board on the desk
for n, c in [('fr4', FR4), ('pad', PAD), ('hole', HOLE), ('black', BLACK), ('solder', '#f1f5f9'),
             ('gold', '#d4a52c'), ('brass', '#c8a24a'), ('term2', '#2563eb'), ('term3', '#16a34a'),
             ('screw', '#9ca3af'), ('res', '#d8c28c'), ('band', '#7c2d12'), ('capsleeve', '#1e293b'),
             ('capstripe', '#94a3b8'), ('captop', '#cbd5e1'), ('module', '#1d4ed8'), ('chip', '#111111'),
             ('mterm', '#15803d'), ('jumper', '#dc2626'), ('mark', '#ef4444'), ('silk', '#f8fafc'),
             ('disco', DISCO_PCB), ('usb', '#c0c4ca'), ('led_o', '#f97316'), ('led_g', '#22c55e'),
             ('led_r', '#ef4444'), ('led_b', '#3b82f6'), ('btn_b', '#2563eb'), ('mat', '#2b3a33'),
             ('bare', '#e5e7eb')]:
    mat(n, c)
for net, c in C.NET.items():
    mat('net_' + net, c)


# ---------------------------------------------------------------- mesh building
def mirror(p):
    """Drawing coordinates -> Blender: the drawing's +Y is down the page."""
    return (p[0], -p[1], p[2])


class Mesh:
    """Collects boxes, cylinders and cones, one material slot per name, into one object."""

    def __init__(self):
        self.v, self.f, self.mi, self.names = [], [], [], []

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
        """Frustum from point a (radius r0) to point b (radius r1)."""
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
        me.from_pydata([mirror(v) for v in self.v], [], [tuple(reversed(f)) for f in self.f])
        for nm in self.names:
            me.materials.append(MATS[nm])
        for p, k in zip(me.polygons, self.mi):
            p.material_index = k
        me.update()
        o = bpy.data.objects.new(name, me)
        sc.collection.objects.link(o)
        if parent:
            adopt(o, parent)
        return o


def adopt(o, parent):
    o.parent = parent
    o.matrix_parent_inverse = parent.matrix_world.inverted()


def empty(name, loc):
    e = bpy.data.objects.new(name, None)
    e.location = mirror(loc)
    sc.collection.objects.link(e)
    bpy.context.view_layer.update()
    return e


def show(o, frames):
    """Rendered only inside the given (start, end) frame windows."""
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=1)
    for a, b in frames:
        o.hide_render = False
        o.keyframe_insert("hide_render", frame=a)
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=b)
    for fc in o.animation_data.action.fcurves:
        if fc.data_path == "hide_render":
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT'


def drop(o, sec, dz=30.0, keep=True):
    """Appear at `sec` dz above the place, settle onto it."""
    f = S(sec)
    show(o, [(f, END + 1)])
    o.location = (0, 0, dz)
    o.keyframe_insert("location", frame=f)
    o.location = (0, 0, 0)
    o.keyframe_insert("location", frame=f + DROP)


def flip(root, a, b, back=False, lift=45.0):
    """Turn a board over about its long axis, lifting it clear of the mat."""
    fa, fb = S(a), S(b)
    r0, r1 = (math.pi, 2 * math.pi) if back else (0.0, math.pi)
    base = root.location.copy()
    root.rotation_euler = (r0, 0, 0)
    root.keyframe_insert("rotation_euler", frame=fa)
    root.location = base
    root.keyframe_insert("location", frame=fa)
    root.location = base + Vector((0, 0, lift))
    root.keyframe_insert("location", frame=(fa + fb) // 2)
    root.location = base
    root.keyframe_insert("location", frame=fb)
    root.rotation_euler = (r1, 0, 0)
    root.keyframe_insert("rotation_euler", frame=fb)


def wire(name, pts, net, kind, parent, sec, dur=None, z=None):
    """A run on the solder side (z below the board), grown from its first point."""
    r = {'bare': 0.5, 'ins': 0.55, 'pwr': 0.9}[kind]
    z = -1.6 - r if z is None else z
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = r
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    cu.bevel_factor_mapping_end = 'SPLINE'
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = mirror((q[0], q[1], q[2] if len(q) > 2 else z)) + (1,)
    cu.materials.append(MATS['bare' if kind == 'bare' else 'net_' + net])
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    adopt(o, parent)
    f = S(sec)
    show(o, [(f, END + 1)])
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=f)
    cu.bevel_factor_end = 1.0
    cu.keyframe_insert("bevel_factor_end", frame=f + (dur or GROW))
    return o


def joints(name, xys, parent, sec, board_bottom=-1.6):
    m = Mesh()
    for x, y in xys:
        m.cone((x, y, board_bottom), (x, y, board_bottom - 1.3), 1.05, 0.3, 'solder', 10)
    o = m.make(name, parent)
    show(o, [(S(sec), END + 1)])
    return o


def label(text, x, y, z, size, parent, m='silk', rot=0.0):
    cu = bpy.data.curves.new(text, 'FONT')
    cu.body = text
    cu.size = size
    cu.align_x = 'CENTER'
    cu.materials.append(MATS[m])
    o = bpy.data.objects.new('lab-' + text, cu)
    o.location = mirror((x, y, z))
    o.rotation_euler = (0, 0, rot)
    sc.collection.objects.link(o)
    adopt(o, parent)
    return o


# ---------------------------------------------------------------- the bench
m = Mesh()
m.box(-150, 110, -120, 150, -32, -30, 'mat')
m.make('cutting-mat')

# ---------------------------------------------------------------- carrier boards A and B
PIVOT = Vector((-15.0, 29.0, -0.8))
car = empty('carrier', PIVOT)
hole = lambda b, c, r: C.hole(b, c, r)


def perfboard(name, edges_x, edges_y, holes, parent):
    m = Mesh()
    m.box(edges_x[0], edges_x[1], edges_y[0], edges_y[1], -1.6, 0, 'fr4')
    for x, y in holes:
        for z0, z1, zh in ((0, 0.04, 0.05), (-1.6, -1.64, -1.65)):
            m.cyl((x, y, z0), (x, y, z1), 0.9, 'pad', 10)
            m.cyl((x, y, z1), (x, y, zh), 0.42, 'hole', 8)
    return m.make(name, parent)


for b in ('A', 'B'):
    cfg = C.BOARD[b]
    perfboard('board-' + b, C.BX, cfg['edge'],
              [hole(b, c, r) for c in range(1, cfg['cols'] + 1) for r in range(1, cfg['rows'] + 1)], car)
label('A', C.BX[0] + 3.2, C.BOARD['A']['edge'][0] + 2.0, 0.06, 4, car)
label('B', C.BX[0] + 3.2, C.BOARD['B']['edge'][1] - 5.0, 0.06, 4, car)

# ---- the four 1x25 sockets, row 25 on the margin
SOCKET_XY = []
for i, (b, col, lab) in enumerate(C.SOCKETS):
    y = C.cy(b, C.ci(col))
    m = Mesh()
    m.box(C.RX(25) - 1.27, C.RX(1) + 1.27, y - 1.25, y + 1.25, 0, 8.5, 'black')
    for r in range(1, 26):
        m.box(C.RX(r) - 0.5, C.RX(r) + 0.5, y - 0.5, y + 0.5, 8.5, 8.52, 'hole')
        if r < 25:
            m.cyl((C.RX(r), y, 0), (C.RX(r), y, -2.6), 0.3, 'screw', 6)
            SOCKET_XY.append((C.RX(r), y))
    drop(m.make('socket-' + col + b, car), SOCKETS_IN + 0.5 * i, 40)
m = Mesh()
for b, col, lab in C.SOCKETS:
    y = C.cy(b, C.ci(col))
    m.cone((C.RX(25), y, 22), (C.RX(25), y, 12), 2.2, 0.2, 'mark', 12)
show(m.make('row25-marks', car), [(S(ROW25[0]), S(ROW25[1]))])

corners = [(x, y) for x, y in SOCKET_XY if abs(x - C.RX(1)) < 0.1 or abs(x - C.RX(24)) < 0.1]
joints('joints-tack', corners, car, TACK)
joints('joints-sockets', [p for p in SOCKET_XY if p not in corners], car, SOCK_J)

# ---- screw terminals: 2p blue, 3p green, as in the kit
PART_PINS = []


def terminal(name, pins_xy, along_x, entry, parent, sec, extra=None):
    xs, ys = [p[0] for p in pins_xy], [p[1] for p in pins_xy]
    if along_x:
        X0, X1, Y0, Y1 = min(xs) - 2.5, max(xs) + 2.5, ys[0] - 3.8, ys[0] + 3.8
    else:
        X0, X1, Y0, Y1 = xs[0] - 3.8, xs[0] + 3.8, min(ys) - 2.5, max(ys) + 2.5
    m = Mesh()
    body = 'term3' if len(pins_xy) == 3 else 'term2'
    m.box(X0, X1, Y0, Y1, 0, 10, body)
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
        (extra if extra is not None else PART_PINS).append((x, y))
    drop(m.make(name, parent), sec)


for b, pins, entry, name, colr in C.TERMS:
    xy = [hole(b, C.ci(c), r) for c, r, _ in pins]
    terminal('term-' + name, xy, len({r for _, r, _ in pins}) > 1, entry, car, PARTS_T[name])

# ---- male headers
for b, pins, name in C.MALE:
    m = Mesh()
    for c, r, _ in pins:
        x, y = hole(b, C.ci(c), r)
        m.box(x - 1.27, x + 1.27, y - 1.27, y + 1.27, 0, 2.5, 'black')
        m.box(x - 0.32, x + 0.32, y - 0.32, y + 0.32, -3.0, 8.5, 'gold')
        PART_PINS.append((x, y))
    drop(m.make('header-' + name, car), PARTS_T[name])


# ---- resistors, lying flat
def resistor(name, a, b, parent, sec, extra=None):
    a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
    mid, d = (a + b) / 2, (b - a).normalized()
    m = Mesh()
    zc = 1.6
    m.cyl(tuple(a + Vector((0, 0, zc))), tuple(mid - d * 3.1 + Vector((0, 0, zc))), 0.28, 'screw', 6)
    m.cyl(tuple(b + Vector((0, 0, zc))), tuple(mid + d * 3.1 + Vector((0, 0, zc))), 0.28, 'screw', 6)
    for p in (a, b):
        m.cyl(tuple(p + Vector((0, 0, zc))), tuple(p + Vector((0, 0, -2.6))), 0.28, 'screw', 6)
        (extra if extra is not None else PART_PINS).append((p.x, p.y))
    m.cyl(tuple(mid - d * 3.1 + Vector((0, 0, zc))), tuple(mid + d * 3.1 + Vector((0, 0, zc))), 1.2, 'res', 14)
    for t in (-1.9, -1.0, 0.0, 1.6):
        m.cyl(tuple(mid + d * (t - 0.3) + Vector((0, 0, zc))), tuple(mid + d * (t + 0.3) + Vector((0, 0, zc))), 1.25, 'band', 14)
    drop(m.make(name, parent), sec)


for b, a, c, lab in C.RES:
    resistor('res-' + lab, hole(b, C.ci(a[0]), a[1]), hole(b, C.ci(c[0]), c[1]), car, PARTS_T[lab])


# ---- 470 uF radial, 10 x 13
def capacitor(name, minus, plus, parent, sec, extra=None):
    cx, cy = (minus[0] + plus[0]) / 2, (minus[1] + plus[1]) / 2
    m = Mesh()
    m.cyl((cx, cy, 0.3), (cx, cy, 13), 5.0, 'capsleeve', 28)
    m.cyl((cx, cy, 13), (cx, cy, 13.05), 4.6, 'captop', 28)
    dx, dy = minus[0] - cx, minus[1] - cy
    n = math.hypot(dx, dy) or 1
    m.box(cx + dx / n * 4.7 - 1.2, cx + dx / n * 4.7 + 1.2, cy + dy / n * 4.7 - 1.2, cy + dy / n * 4.7 + 1.2,
          0.5, 12.8, 'capstripe')
    for x, y in (minus, plus):
        m.cyl((x, y, 0.3), (x, y, -2.6), 0.3, 'screw', 6)
        (extra if extra is not None else PART_PINS).append((x, y))
    drop(m.make(name, parent), sec)


for b, mi, pl, lab in C.CAPS:
    capacitor('cap-' + lab, hole(b, C.ci(mi[0]), mi[1]), hole(b, C.ci(pl[0]), pl[1]), car, PARTS_T[lab])

# ---- the module's 1x4 socket
b, pins = C.XCVR_SOCKET
xy = [hole(b, C.ci(c), r) for c, r, _ in pins]
m = Mesh()
m.box(xy[0][0] - 1.27, xy[0][0] + 1.27, xy[0][1] - 1.27, xy[-1][1] + 1.27, 0, 8.5, 'black')
for x, y in xy:
    m.box(x - 0.5, x + 0.5, y - 0.5, y + 0.5, 8.5, 8.52, 'hole')
    PART_PINS.append((x, y))
drop(m.make('xcvr-socket', car), PARTS_T['XCVR'])

joints('joints-parts', PART_PINS, car, PART_J)

# ---------------------------------------------------------------- solder side of A and B
BRIDGE_RUNS = {('GND', 'A', ((9, 1), (18, 1))), ('3V3', 'A', ((11, 3), (18, 3))),
               ('GND', 'B', ((1, 1), (8, 1))), ('3V3', 'B', ((1, 3), (8, 3)))}
spines, insul, bridges = [], [], []
for net, b, pts, kind in C.WIRES:
    xy = [hole(b, c, r) for c, r in pts]
    key = (net, b, tuple(pts))
    (bridges if key in BRIDGE_RUNS else spines if kind == 'bare' else insul).append((net, b, pts, kind, xy))


def wire_ends(pts, xy):
    return [p for (c, r), p in zip((pts[0], pts[-1]), (xy[0], xy[-1]))
            if float(c).is_integer() and float(r).is_integer()]


for group, (a, z) in ((spines, SPINES), (insul, INSUL)):
    step = (z - a) / max(1, len(group))
    for i, (net, b, pts, kind, xy) in enumerate(group):
        t = a + i * step
        wire(f'wire-{b}-{net}-{i}', xy, net, kind, car, t)
        if kind != 'bare':
            joints(f'wj-{b}-{net}-{i}', wire_ends(pts, xy), car, t + GROW / FPS)
# the two bridges: along B's row, across the gap, along A's row - one wire each
for i, (net, (ba, ca, ra), (bb, cb, rb)) in enumerate(C.BRIDGES):
    run = [r for r in bridges if r[0] == net]
    a_run = next(r for r in run if r[1] == 'A')
    b_run = next(r for r in run if r[1] == 'B')
    xy = list(reversed(b_run[4])) + list(reversed(a_run[4]))
    wire(f'bridge-{net}', xy, net, 'bare', car, BRIDGE[0] + 1.8 * i, dur=S(1.6) - 1)

# ---------------------------------------------------------------- module, links, jumper, standoffs
mx0 = C.RX(13) - 1.5
m = Mesh()
m.box(mx0, mx0 + 25, 60.85, 78.85, 11.0, 12.6, 'module')
for x, y in [hole('B', C.ci(c), r) for c, r, _ in C.XCVR_SOCKET[1]]:
    m.box(x - 1.27, x + 1.27, y - 1.27, y + 1.27, 8.5, 11.0, 'black')
    m.box(x - 0.32, x + 0.32, y - 0.32, y + 0.32, 3.0, 13.5, 'gold')
m.box(mx0 + 8, mx0 + 13, 67.5, 72.2, 12.6, 14.1, 'chip')
m.box(mx0 + 25 - 7.5, mx0 + 25, 63.0, 74.0, 12.6, 19.0, 'mterm')
for y in (66.04, 71.12):
    m.cyl((mx0 + 21.2, y, 19.0), (mx0 + 21.2, y, 19.3), 1.4, 'screw', 12)
    m.box(mx0 + 24.95, mx0 + 25.05, y - 1.3, y + 1.3, 14, 17, 'hole')
m.box(mx0 + 2, mx0 + 4, 62.5, 64.5, 12.6, 13.2, 'led_r')
drop(m.make('module-sn65hvd230', car), MODULE, 25)
for net, (b, c, r) in C.LINKS:
    x, y = hole(b, c, r)
    wire('link-' + net, [(mx0 + 25, y, 15.5), (x, y, 15.5), (x, y, 5.0), (x, y, 0.0)], net, 'ins', car, LINKS)
x, y = hole('B', C.ci('m'), 22)              # TERM is m22 / m23, along X
m = Mesh()
m.box(C.RX(23) - 1.3, C.RX(22) + 1.3, y - 1.3, y + 1.3, 2.6, 8.8, 'jumper')
drop(m.make('term-jumper', car), JUMPER, 15)

m_so, m_sc = Mesh(), Mesh()
for b, c, r, lab, _ in C.FIX:
    x, y = hole(b, c, r)
    m_so.cone((x, y, -1.6), (x, y, -11.6), 2.5, 2.5, 'brass', 6)
    m_sc.cyl((x, y, 0), (x, y, 1.6), 2.2, 'screw', 16)
    m_sc.box(x - 1.5, x + 1.5, y - 0.3, y + 0.3, 1.6, 1.65, 'hole')
drop(m_so.make('standoffs', car), STANDOFFS, -30)
drop(m_sc.make('screws', car), STANDOFFS + 0.5, 25)

# ---------------------------------------------------------------- the STM32F4DISCOVERY (mock)
dx0, dx1 = C.DISCO['x']
dy0, dy1 = C.DISCO['y']
Z0 = 9.0                     # the PCB's underside, seated on the sockets
Z1 = Z0 + 1.6
d = Mesh()
d.box(dx0, dx1, dy0, dy1, Z0, Z1, 'disco')
for b, cols in (('A', ('i', 'j')), ('B', ('g', 'h'))):
    ya, yb = C.cy(b, C.ci(cols[0])), C.cy(b, C.ci(cols[1]))
    d.box(C.RX(25) - 1.27, C.RX(1) + 1.27, min(ya, yb) - 1.27, max(ya, yb) + 1.27, Z1, Z1 + 2.5, 'black')
    for r in range(1, 26):
        for y in (ya, yb):
            d.box(C.RX(r) - 0.32, C.RX(r) + 0.32, y - 0.32, y + 0.32, 3.0, Z1 + 6.0, 'gold')
cyc = (dy0 + dy1) / 2
d.box(-37, -23, cyc - 7, cyc + 7, Z1, Z1 + 1.4, 'chip')                # STM32F407VG, LQFP100
d.box(-38, -22, cyc - 8, cyc + 8, Z1, Z1 + 0.3, 'screw')
d.box(12, 19, cyc - 3.5, cyc + 3.5, Z1, Z1 + 1.4, 'chip')              # ST-LINK F103
d.box(11.5, 19.5, cyc - 4, cyc + 4, Z1, Z1 + 0.3, 'screw')
d.box(dx1 - 7, dx1 + 1, cyc - 3.9, cyc + 3.9, Z1, Z1 + 4, 'usb')       # CN1 mini-B, the rear edge
d.box(dx0 - 1, dx0 + 5, cyc + 4, cyc + 11.5, Z1, Z1 + 2.6, 'usb')      # CN5 micro-B, the front edge
d.cyl((dx0 - 1, 8, Z1 + 2.6), (dx0 + 12, 8, Z1 + 2.6), 3.0, 'black', 16)   # CN4 audio jack
d.box(-56, -51, 17, 22, Z1, Z1 + 1.0, 'chip')                          # CS43L22
d.box(-46.5, -43.5, cyc - 1.5, cyc + 1.5, Z1, Z1 + 1.0, 'chip')        # accelerometer
for (ox, oy), mm in (((0, 5.5), 'led_o'), ((-5.5, 0), 'led_g'), ((0, -5.5), 'led_r'), ((5.5, 0), 'led_b')):
    d.box(-45 + ox - 0.8, -45 + ox + 0.8, cyc + oy - 0.5, cyc + oy + 0.5, Z1, Z1 + 0.6, mm)
for yb_, cap in ((44.0, 'btn_b'), (10.0, 'black')):                    # B1 user, B2 reset
    d.box(-54, -48, yb_ - 3, yb_ + 3, Z1, Z1 + 3.4, 'usb')
    d.cyl((-51, yb_, Z1 + 3.4), (-51, yb_, Z1 + 4.8), 1.8, cap, 16)
d.box(22, 23.6, 46, 47.0, Z1, Z1 + 0.6, 'led_r')                       # LD2 PWR
d.box(22, 23.6, 49, 50.0, Z1, Z1 + 0.6, 'led_g')                       # LD1 COM
d.cyl((-13, cyc - 2.5, Z1), (-13, cyc - 2.5, Z1 + 1.2), 1.6, 'usb', 12)  # X2
for i in range(6):                                                     # CN3 SWD
    d.box(26 - 1.27, 26 + 1.27, 6 + i * P - 1.27, 6 + i * P + 1.27, Z1, Z1 + 2.5, 'black')
for jy in (40.0, 45.0):                                                # CN2 jumpers
    d.box(3, 8.1, jy - 1.3, jy + 1.3, Z1, Z1 + 5.5, 'black')
d.box(-9, -6.4, 45, 50.1, Z1, Z1 + 5.5, 'black')                       # JP1 IDD
disco = d.make('discovery', car)
bpy.context.view_layer.update()
labels = [label('STM32F4DISCOVERY', -27, 42.0, Z1 + 0.05, 3.2, disco),
          label('mock', -27, 46.5, Z1 + 0.05, 2.4, disco, 'capstripe')]
f0, f1 = S(DISCO_JIG[0]), S(DISCO_JIG[1])
g0, g1 = S(DISCO_OFF[0]), S(DISCO_OFF[1])
h0, h1 = S(DISCO_ON[0]), S(DISCO_ON[1])
for o in [disco] + labels:
    show(o, [(f0, g1), (h0, END + 1)])
for f, z in ((f0, 60), (f1, 0), (g0, 0), (g1, 60), (h0, 60), (h1, 0)):
    disco.location = (0, 0, z)
    disco.keyframe_insert("location", frame=f)

# ---------------------------------------------------------------- board C, the 5 V split
OXc, OYc = -58.42, -60.0
cpiv = Vector((OXc + 29.21, OYc + 11.43, -0.8))
cr = empty('board-c', cpiv)
ch = lambda c, r: (OXc + (r - 1) * P, OYc + (c - 1) * P)
perfboard('board-C', (OXc + C.C_EDGE_X[0], OXc + C.C_EDGE_X[1]), (OYc + C.C_EDGE_Y[0], OYc + C.C_EDGE_Y[1]),
          [ch(c, r) for c in range(1, C.C_COLS + 1) for r in range(1, C.C_ROWS + 1)], cr)
label('C', OXc + 29.21, OYc + C.C_EDGE_Y[0] + 0.8, 0.06, 2.6, cr)
C_PINS = []
for pins, entry, name, note in C.C_TERMS:
    terminal('c-term-' + name, [ch(C.ci(c), r) for c, r, _ in pins], False, entry, cr, C_PARTS['terms'], C_PINS)
for a, b_, lab_ in C.C_RES:
    resistor('c-res-' + lab_, ch(C.ci(a[0]), a[1]), ch(C.ci(b_[0]), b_[1]), cr, C_PARTS['res'], C_PINS)
capacitor('c-cap-C1', ch(C.ci('c'), 12), ch(C.ci('a'), 12), cr, C_PARTS['cap'], C_PINS)
m = Mesh()
for c, r, _, _ in C.C_FIX:
    x, y = ch(c, r)
    m.cone((x, y, -1.6), (x, y, -11.6), 2.5, 2.5, 'brass', 6)
drop(m.make('c-standoffs', cr), C_PARTS['cap'] + 0.6, -30)
joints('c-joints', C_PINS, cr, C_J)
c_sp = [w_ for w_ in C.C_WIRES if w_[2] == 'bare']
c_ot = [w_ for w_ in C.C_WIRES if w_[2] != 'bare']
for group, (a, z) in ((c_sp, C_SPINES), (c_ot, C_WIRES)):
    step = (z - a) / max(1, len(group))
    for i, (net, pts, kind) in enumerate(group):
        wire(f'c-wire-{net}-{i}', [ch(c, r) for c, r in pts], net, kind, cr, a + i * step)

flip(car, *FLIP1)
flip(car, *FLIP1B, back=True)
flip(car, *FLIP2)
flip(car, *FLIP2B, back=True)
flip(cr, *C_FLIP, lift=35)
flip(cr, *C_FLIPB, back=True, lift=35)

# ---------------------------------------------------------------- camera
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.clip_end = 5000
cam.data.lens = 32
sc.collection.objects.link(cam)
sc.camera = cam
target = bpy.data.objects.new("target", None)
sc.collection.objects.link(target)
tc = cam.constraints.new('TRACK_TO')
tc.target = target
tc.track_axis = 'TRACK_NEGATIVE_Z'
tc.up_axis = 'UP_Y'
# written in drawing coordinates: the camera stands on B's side (+Y), as the drawing's reader does
AB, CC = (-15, 29, 0), (OXc + 29.2, OYc + 11.4, 0)
KEYS = [(0, (-20, 250, 250), (-15, 0, 0)),
        (3.6, (-22, 180, 165), (-15, 38, 0)),
        (10.6, (-22, 180, 165), (-15, 38, 0)),
        (11.4, (-22, 150, 140), (-15, 32, 12)),
        (19.4, (-22, 150, 140), (-15, 32, 12)),
        (21.2, (-25, 170, 160), (-15, 38, 0)),
        (31.8, (-25, 170, 160), (-15, 38, 0)),
        (34.6, (-18, 128, 132), (-15, 31, 0)),
        (56.0, (-18, 128, 132), (-15, 31, 0)),
        (58.6, (-125, 170, 115), (-15, 36, 6)),
        (66.8, (-125, 170, 115), (-15, 36, 6)),
        (68.0, (CC[0] - 4, CC[1] + 62, 125), (CC[0], CC[1] + 4, 0)),
        (83.6, (CC[0] - 4, CC[1] + 62, 125), (CC[0], CC[1] + 4, 0))]
for sec, c, t in KEYS:
    f = S(sec)
    cam.location, target.location = mirror(c), mirror(t)
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
for i in range(0, 15):                      # orbit the finished pair
    f = S(ORBIT) + i * S(0.7)
    a = math.radians(100 - i * 14)
    cam.location = mirror((-15 + 260 * math.cos(a), 5 + 260 * math.sin(a), 175 - i * 3))
    target.location = mirror((-15, 5, 4))
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions, riding with the camera
band_mat = bpy.data.materials.new("caption-band")
band_mat.diffuse_color = (0.02, 0.02, 0.03, 0.72)
MATS['caption-band'] = band_mat
bpy.ops.mesh.primitive_plane_add(size=1)
bo = bpy.context.active_object
bo.name = "caption-band"
bo.data.materials.append(band_mat)
bo.parent = cam
bo.location = (0, -5.62, -20.05)
bo.scale = (24, 1.25, 1)
white = mat('caption', (0.95, 0.95, 0.95, 1))
for (a, b), text in CAPTIONS:
    a, b = S(a), min(S(b), END + 1)
    cu = bpy.data.curves.new("cap", 'FONT')
    cu.body = text
    cu.size = 0.46
    t = bpy.data.objects.new("cap", cu)
    t.data.materials.append(white)
    sc.collection.objects.link(t)
    t.parent = cam
    t.location = (-10.6, -5.8, -20)
    show(t, [(a, b)])

# ---------------------------------------------------------------- render
sc.frame_start, sc.frame_end = 1, END
sc.render.fps = FPS
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.color_type, sh.light = 'MATERIAL', 'STUDIO'
sh.show_cavity = sh.show_object_outline = True
sh.background_type = 'VIEWPORT'
sh.background_color = (0.16, 0.17, 0.19)
sc.world = bpy.data.worlds.new("bench")      # the render reads the world, not the viewport
sc.world.color = (0.16, 0.17, 0.19)
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
if STILL is not None:
    sc.frame_set(S(STILL))
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = os.path.join(HERE, f"carrier-still-{STILL:g}.png")
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath)
    sys.exit(0)
if PREVIEW:
    sc.render.resolution_percentage = 50
    sc.frame_step = 4
sc.render.image_settings.file_format = 'FFMPEG'
sc.render.ffmpeg.format = 'MPEG4'
sc.render.ffmpeg.codec = 'H264'
sc.render.ffmpeg.constant_rate_factor = 'HIGH'
sc.render.filepath = OUT
bpy.ops.render.render(animation=True)
print("wrote", OUT)
