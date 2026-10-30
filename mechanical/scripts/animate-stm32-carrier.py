"""Assembly animation of the STM32 carrier and the 5 V split board (MEC-15, HW-19), by Blender.

    blender -b -P animate-stm32-carrier.py                   # -> ../renders/stm32-carrier-animation.mp4, 47 s
    blender -b -P animate-stm32-carrier.py -- --preview      # half size, every 4th frame
    blender -b -P animate-stm32-carrier.py -- --still 40     # one PNG at 40 s, for checking a moment

Nothing is read from disk but ../../hardware/scripts/stm32-carrier.py, which owns every hole, part and
wire; this script only gives them bodies. It follows the drawing's build order: the sockets
go in with the Nucleo plugged in as the jig, the stack turns over for their joints, the
parts go in, the solder side is wired spine by spine and run by run, the module, jumper and
standoffs go on, and the Nucleo drops onto the finished carrier. Board C follows.

Coordinates are the drawing's: X along the vehicle (row 1 at X 0, rear = +X), Y across
(A at -Y, B at +Y), Z up from the boards' top face, millimetres throughout. The drawing puts
+Y DOWN the page, so a right-handed Blender frame with Z up would mirror the board: every
point is written to Blender with Y negated (mirror() below), and nothing else changes.

The NUCLEO-H533RE is a MOCK: its outline, the CN7 / CN10 morpho headers and CN1's edge are UM3121
Fig. 7 geometry (the same numbers the drawing uses); its taller parts (C.NUC_MOCK) are read off the
same figure, for recognition and clearance only. ST's own model sits behind a login and is not ours
to commit.
"""
import bpy, importlib.util, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blender_compat import fcurves, mp4                              # noqa: E402
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "..", "renders")
OUT = os.path.join(RENDERS, "stm32-carrier-animation.mp4")
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PREVIEW = "--preview" in ARGS
STILL = float(ARGS[ARGS.index("--still") + 1]) if "--still" in ARGS else None

spec = importlib.util.spec_from_file_location("carrier", os.path.join(HERE, "..", "..", "hardware", "scripts", "stm32-carrier.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
P = C.P

FPS = 24
SPEED = 2                    # the timeline is written in seconds and plays SPEED times faster
S = lambda sec: int(round(sec * FPS / SPEED)) + 1
END = S(94)

# ---------------------------------------------------------------- timeline (seconds)
SOCKETS_IN = 4.0             # four 1x19 sockets, 0.5 s apart
NUC_JIG = (8.2, 10.8)        # the Nucleo plugs in as the jig
FLIP1 = (11.0, 13.4)         # over for the socket joints
TACK, SOCK_J = 13.9, 15.3
FLIP1B = (17.0, 19.4)        # back
NUC_OFF = (19.6, 21.2)
PARTS_T = {'CAN': 21.6, '6V IN': 22.4, '5V IN': 23.2, 'SERVO': 24.6, 'I2C-B': 25.4, 'I2C-A': 26.0,
           'R4 1k': 27.4, 'C2': 28.4, 'XCVR': 30.2}
FLIP2 = (32.0, 34.4)
PART_J = 34.8
SPINES = (37.2, 42.6)
INSUL = (43.2, 50.6)
BRIDGE = (51.4, 55.0)
FLIP2B = (56.0, 58.4)
MODULE, LINKS, STANDOFFS = 58.8, 60.0, 62.0
NUC_ON = (64.0, 66.6)
C_PARTS = {'terms': 68.4, 'res': 69.2, 'cap': 69.8, 'screws': 70.5, 'socket': 71.1, 'pigtail': 71.6, 'ties': 72.1}
C_FLIP = (72.8, 75.0)
C_J, C_SPINES, C_WIRES = 75.3, (75.9, 77.5), (77.9, 80.4)
C_FLIPB = (81.0, 83.2)
ORBIT = 84.0
DROP = S(0.7) - 1            # how long a part takes to settle
WIRE_S = 0.9                 # how long a wire takes to run, in timeline seconds
GROW = S(WIRE_S) - 1

CAPTIONS = [
    ((0, 4), "Board A: a 5x7 kit board, 18 x 24 holes; board B: a 3x7, 10 x 24 - board C, the 5 V split, beside them"),
    ((4, 8.2), f"1  Four 1x19 sockets: A {C.silk('A', 'g', 1)[1:]} / {C.silk('A', 'h', 1)[1:]} under CN10, B {C.silk('B', 'i', 1)[1:]} / {C.silk('B', 'j', 1)[1:]} under CN7, rows 5-23 and 6-24"),
    ((8.2, 11), "2  The Nucleo plugs in as the jig, A and B on the tray: it sets the 63.50 mm between the two headers"),
    ((11, 19.4), "3  Turn the stack over and solder the sockets - tack the four corners, check, then the rest"),
    ((19.4, 21.6), "   Lift the Nucleo off"),
    ((21.6, 24.6), "4  Screw terminals: CAN (3p) on A, 6V IN and 5V IN on B"),
    ((24.6, 27.4), "5  SERVO on B; I2C-B and I2C-A are 90 degree headers on A along the gap, pointing forward"),
    ((27.4, 30.2), "6  R4 1k in the servo PWM, C2 470 uF across the servo supply, both on B"),
    ((30.2, 32), "7  A 1x4 and a 1x2 socket on A for the SN65HVD230 module"),
    ((32, 37.2), "8  Turn it over: solder every part pin, then bridge each one onto the free hole its wire lands on"),
    ((37.2, 43.2), "9  The servo loop in 18 AWG on B: 6V IN to C2 to SERVO, on + and on GND"),
    ((43.2, 51.4), "10  22 AWG, each end on a bridged free hole (E5V and 3V3 on B take it direct): 5 V, GND, PWM, I2C, CAN"),
    ((51.4, 56), f"11  One bridge: CN7-16 3V3 to I2C-A VCC ({C.N('A', 'r', 20)}); A's GND comes from CN10-9 and CN10-20"),
    ((56, 58.8), "   Right way up again"),
    ((58.8, 62), f"12  Module in face down on A, CANH / CANL into {C.N('A', 'b', C.CAN_ROW)} / {C.silk('A', 'c', C.CAN_ROW)}; its own 120 R ends the bus"),
    ((62, 64), "    A nylon standoff and screw in the corner holes: four on A, three on B"),
    ((64, 67.4), "13  The NUCLEO-H533RE drops onto the carrier, JP5 on [5-6] for E5V"),
    ((67.4, 70.5), "14  Board C, the 5 V split: IN 5V and TO STM32, C1 470 uF"),
    ((70.5, 72.8), f"    Four corner standoffs and screws, then the USB-C socket: pigtail into {' / '.join(C.silk('C', c, r) for _, _, c, r, _ in C.C_PIGTAIL)}, two zip ties"),
    ((72.8, 84), "15  Solder side: IN 5V to C1 to the socket on each rail in 18 AWG; D-, D+, CC1, CC2 cut short and insulated"),
    ((84, 95), "The carrier and the 5 V split, ready for plate 2 (MEC-15, HW-19) - the Nucleo is a mock"),
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
NUC_PCB = '#f2f2ee'              # the Nucleo-64 board is white
for n, c in [('fr4', FR4), ('pad', PAD), ('hole', HOLE), ('black', BLACK), ('solder', '#f1f5f9'),
             ('gold', '#d4a52c'), ('brass', '#c8a24a'), ('term2', '#2563eb'), ('term3', '#16a34a'),
             ('screw', '#9ca3af'), ('res', '#d8c28c'), ('band', '#7c2d12'), ('capsleeve', '#1e293b'),
             ('capstripe', '#94a3b8'), ('captop', '#cbd5e1'), ('module', '#1d4ed8'), ('chip', '#111111'),
             ('mterm', '#15803d'), ('jumper', '#dc2626'), ('mark', '#ef4444'), ('silk', '#f8fafc'),
             ('nucleo', NUC_PCB), ('usb', '#c0c4ca'), ('led_o', '#f97316'), ('led_g', '#22c55e'),
             ('led_r', '#ef4444'), ('led_b', '#3b82f6'), ('btn_b', '#2563eb'), ('mat', '#2b3a33'),
             ('bare', '#e5e7eb'), ('nylon', '#e8e4d8')]:
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
    for fc in fcurves(o.animation_data.action):
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


TURNED = {}                  # each root's angle so far: every flip adds half a turn


def flip(root, a, b, lift=45.0):
    """Turn a board over about its long axis, lifting it clear of the mat.

    The angle only ever grows. Starting a flip back at 0 after the last one ended at
    360 deg would make Blender spin the board through the half turn in between.
    """
    fa, fb = S(a), S(b)
    r0 = TURNED.get(root.name, 0.0)
    r1 = TURNED[root.name] = r0 + math.pi
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


def wire(name, pts, net, kind, parent, sec, dur=None, z=None, colour=None):
    """A run on the solder side (z below the board), grown from its first point."""
    r = {'ins': 0.55, 'pwr': 0.9, 'lead': 0.3, 'bridge': 0.6}[kind]
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
    cu.materials.append(mat('wire' + colour, colour) if colour else MATS['bare' if kind == 'lead' else 'net_' + net])
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
    perfboard('board-' + b, C.bx(b), cfg['edge'],
              [hole(b, c, r) for c in range(cfg['c0'], cfg['cols'] + 1) for r in range(1, cfg['rows'] + 1)], car)
label('A', C.bx('A')[0] + 3.2, C.BOARD['A']['edge'][0] + 2.0, 0.06, 4, car)
label('B', C.bx('B')[0] + 3.2, C.BOARD['B']['edge'][1] - 5.0, 0.06, 4, car)

# ---- the four 1x19 sockets, every tail in a hole
SOCKET_XY = []
for i, (b, col, lab) in enumerate(C.SOCKETS):
    y = C.cy(b, C.ci(col))
    m = Mesh()
    m.box(C.NX(C.NUC_ROWS) - 1.27, C.NX(1) + 1.27, y - 1.25, y + 1.25, 0, 8.5, 'black')
    for k in range(1, C.NUC_ROWS + 1):
        m.box(C.NX(k) - 0.5, C.NX(k) + 0.5, y - 0.5, y + 0.5, 8.5, 8.52, 'hole')
        m.cyl((C.NX(k), y, 0), (C.NX(k), y, -2.6), 0.3, 'screw', 6)
        SOCKET_XY.append((C.NX(k), y))
    drop(m.make('socket-' + col + b, car), SOCKETS_IN + 0.5 * i, 40)

xs = sorted({round(x, 2) for x, _ in SOCKET_XY})
corners = [(x, y) for x, y in SOCKET_XY if round(x, 2) in (xs[0], xs[-1])]
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
for b, pins, name in C.MALE:                               # straight, or 90 degrees with the plug lying forward
    m = Mesh()
    for bx_ in C.header_boxes(b, pins, name):
        m.box(*bx_)
    PART_PINS.extend(hole(b, C.ci(c), r) for c, r, _ in pins)
    drop(m.make('header-' + name, car), PARTS_T[name], 40)


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
xy2 = [hole(C.CAN_SOCKET[0], C.ci(c), r) for c, r, _ in C.CAN_SOCKET[1]]
m.box(xy2[0][0] - 1.27, xy2[0][0] + 1.27, xy2[0][1] - 1.27, xy2[-1][1] + 1.27, 0, 8.5, 'black')
for x, y in xy + xy2:
    m.box(x - 0.5, x + 0.5, y - 0.5, y + 0.5, 8.5, 8.52, 'hole')
    PART_PINS.append((x, y))
drop(m.make('xcvr-socket', car), PARTS_T['XCVR'])

joints('joints-parts', PART_PINS, car, PART_J)

# ---------------------------------------------------------------- solder side of A and B
# the solder bridges first: each joins a pin to the free hole beside it, where its wire lands (no wire goes on a pin)
for k, (b, run) in enumerate(C.SOLDER):
    wire(f'solder-{b}-{k}', [hole(b, c, r) for c, r in run], 'GND', 'bridge', car, 34.6 + k * 2.4 / len(C.SOLDER), z=-1.9, colour='#cbd5e1')
heavy = [(n, b, pts, k) for n, b, pts, k in C.WIRES if k == 'pwr']
light = [(n, b, pts, k) for n, b, pts, k in C.WIRES if k != 'pwr']


def wire_ends(pts, xy):
    return [p for (c, r), p in zip((pts[0], pts[-1]), (xy[0], xy[-1]))
            if float(c).is_integer() and float(r).is_integer()]


# every wire is insulated and runs pad to pad; its two joints appear as it lands
for group, (a, z) in ((heavy, SPINES), (light, INSUL)):
    step = (z - a) / max(1, len(group))
    for i, (net, b, pts, kind) in enumerate(group):
        t = a + i * step
        xy = [hole(b, c, r) for c, r in pts]
        wire(f'wire-{b}-{net}-{i}', xy, net, kind, car, t)
        joints(f'wj-{b}-{net}-{i}', wire_ends(pts, xy), car, t + WIRE_S)
# the one bridge between the boards: 3V3 from CN7 on B to I2C-A on A
for i, (net, pts, kind) in enumerate(C.XWIRES):
    xy = [hole(b, c, r) for b, c, r in pts]
    t = BRIDGE[0] + 1.8 * i
    wire(f'bridge-{net}', xy, net, kind, car, t, dur=S(1.6) - 1)
    joints(f'bj-{net}', [xy[0], xy[-1]], car, t + 1.6)

# ---------------------------------------------------------------- module, links, jumper, standoffs
# the module lies flat and FACE DOWN, its pins bent 90 deg toward its components, into the 1x4
# socket; its chip and screw terminal hang underneath (BOM 4.1, MEC-15 2026-10-03)
X0, X1, Y0, Y1 = C.module_box()
ZB = 11.0                                 # underside of the module's board (its component side)
m = Mesh()
m.box(X0, X1, Y0, Y1, ZB, ZB + 1.6, 'module')
m.box(X0, X0 + 2.5, Y0 + 0.3, Y1 - 0.3, ZB - 2.5, ZB, 'black')          # header spacer, on the socket
for x, y in [hole(C.XCVR_SOCKET[0], C.ci(c), r) for c, r, _ in C.XCVR_SOCKET[1]]:
    m.box(x - 0.32, x + 0.32, y - 0.32, y + 0.32, 3.0, ZB, 'gold')
mid = (X0 + X1) / 2
yc = (Y0 + Y1) / 2
m.box(mid - 4.5, mid - 0.5, yc - 2.5, yc + 2.5, ZB - 1.5, ZB, 'chip')
tx0 = X1 - C.MODULE['terminal']
m.box(tx0, X1, Y0 + 0.4, Y1 - 0.4, ZB - 9.5, ZB, 'mterm')                # hangs to ~1.5 mm off B
for x, y in [hole(C.CAN_SOCKET[0], C.ci(c), r) for c, r, _ in C.CAN_SOCKET[1]]:      # the 2-pin CANH / CANL header,
    m.box(x - 1.27, x + 1.27, y - 1.27, y + 1.27, ZB - 2.5, ZB, 'black')     # pointing down into its socket
    m.box(x - 0.32, x + 0.32, y - 0.32, y + 0.32, 3.0, ZB, 'gold')
drop(m.make('module-sn65hvd230', car), MODULE, 25)

m_so, m_sc = Mesh(), Mesh()
CORNER_INSET = 2.5           # the kit boards' own four corner holes, as animate-carrier-tray.py (MEC-17)


def corners(x0, x1, y0, y1):
    return [(x, y) for x in (x0 + CORNER_INSET, x1 - CORNER_INSET) for y in (y0 + CORNER_INSET, y1 - CORNER_INSET)]


for b in ('A', 'B'):
    for x, y in C.fixings(b):                     # B, a 3x7, leaves its front inboard corner free (MEC-17)
        m_so.cone((x, y, -1.6), (x, y, -9.6), 2.5, 2.5, 'nylon', 6)           # 8 mm, as the tray sets them
        m_sc.cyl((x, y, 0), (x, y, 1.6), 2.2, 'screw', 16)
        m_sc.box(x - 1.5, x + 1.5, y - 0.3, y + 0.3, 1.6, 1.65, 'hole')
drop(m_so.make('standoffs', car), STANDOFFS, -30)
drop(m_sc.make('screws', car), STANDOFFS + 0.5, 25)

# ---------------------------------------------------------------- the NUCLEO-H533RE (mock)
nx0, nx1 = C.NUC['x']
ny0, ny1 = C.NUC['y']
Z0 = 9.0                     # the PCB's underside, seated on the sockets
Z1 = Z0 + 1.6
d = Mesh()
d.box(nx0, nx1, ny0, ny1, Z0, Z1, 'nucleo')
for b, cols in (('A', ('g', 'h')), ('B', ('i', 'j'))):
    ya, yb = C.cy(b, C.ci(cols[0])), C.cy(b, C.ci(cols[1]))
    d.box(C.NX(C.NUC_ROWS) - 1.27, C.NX(1) + 1.27, min(ya, yb) - 1.27, max(ya, yb) + 1.27, Z1, Z1 + 2.5, 'black')
    for k in range(1, C.NUC_ROWS + 1):
        for y in (ya, yb):
            d.box(C.NX(k) - 0.32, C.NX(k) + 0.32, y - 0.32, y + 0.32, 3.0, Z1 + 3.0, 'gold')
for side, x0, x1, y0, y1, h, mm, _ in C.NUC_MOCK:
    d.box(x0, x1, y0, y1, Z1, Z1 + h, mm) if side == 'top' else d.box(x0, x1, y0, y1, Z0 - h, Z0, mm)
nucleo = d.make('nucleo', car)
bpy.context.view_layer.update()
labels = [label('NUCLEO-H533RE', -27, 42.0, Z1 + 0.05, 3.2, nucleo, 'chip'),
          label('mock', -27, 46.5, Z1 + 0.05, 2.4, nucleo, 'capstripe')]
f0, f1 = S(NUC_JIG[0]), S(NUC_JIG[1])
g0, g1 = S(NUC_OFF[0]), S(NUC_OFF[1])
h0, h1 = S(NUC_ON[0]), S(NUC_ON[1])
for o in [nucleo] + labels:
    show(o, [(f0, g1), (h0, END + 1)])
for f, z in ((f0, 60), (f1, 0), (g0, 0), (g1, 60), (h0, 60), (h1, 0)):
    nucleo.location = (0, 0, z)
    nucleo.keyframe_insert("location", frame=f)

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
for x, y in corners(OXc + C.C_EDGE_X[0], OXc + C.C_EDGE_X[1], OYc + C.C_EDGE_Y[0], OYc + C.C_EDGE_Y[1]):
    m.cone((x, y, -1.6), (x, y, -9.6), 2.5, 2.5, 'nylon', 6)
drop(m.make('c-standoffs', cr), C_PARTS['cap'] + 0.6, -30)

# ---- the four corner screws, then the USB-C socket, its pigtail and two ties
m = Mesh()
for x, y in corners(OXc + C.C_EDGE_X[0], OXc + C.C_EDGE_X[1], OYc + C.C_EDGE_Y[0], OYc + C.C_EDGE_Y[1]):
    m.cyl((x, y, 0), (x, y, 1.7), 2.25, 'screw', 16)
    m.box(x - 1.5, x + 1.5, y - 0.3, y + 0.3, 1.7, 1.75, 'hole')
drop(m.make('c-screws', cr), C_PARTS['screws'], 20)
sk = C.C_SOCKET
X = lambda x: OXc + x
Yc = OYc + sk['y']
m = Mesh()
m.box(X(sk['flange'][0]), X(sk['flange'][1]), Yc - sk['flange_w'] / 2, Yc + sk['flange_w'] / 2, 0, sk['flange_h'], 'black')
zb = (sk['flange_h'] - sk['body_h']) / 2
m.box(X(sk['body'][0]), X(sk['body'][1]), Yc - sk['body_w'] / 2, Yc + sk['body_w'] / 2, zb, zb + sk['body_h'], 'black')
zc = sk['flange_h'] / 2
m.box(X(sk['flange'][0]) - 0.06, X(sk['flange'][0]), Yc - 4.3, Yc + 4.3, zc - 1.3, zc + 1.3, 'hole')
m.box(X(sk['flange'][0]) - 0.08, X(sk['flange'][0]) - 0.06, Yc - 3.2, Yc + 3.2, zc - 0.3, zc + 0.3, 'usb')
drop(m.make('c-usb-socket', cr), C_PARTS['socket'], 25)
x1 = X(sk['body'][1])
for lab, colour, col, row, ye in C.C_PIGTAIL:
    hx, hy = ch(C.ci(col), row)
    wire('c-pigtail-' + lab, [(x1, OYc + ye, zc), (x1 + 2.2, OYc + ye, zc), (hx, hy, 3.0), (hx, hy, -2.2)],
         lab, 'ins', cr, C_PARTS['pigtail'], colour=colour)
    C_PINS.append((hx, hy))
m = Mesh()
for lab, colour, ye in C.C_CUT:
    m.cyl((x1, OYc + ye, zc), (x1 + 1.6, OYc + ye, zc), 0.55, 'screw', 8)
    m.cyl((x1 + 1.6, OYc + ye, zc), (x1 + 5.0, OYc + ye, zc), 0.85, 'capsleeve', 10)
show(m.make('c-cut-dplus-dminus', cr), [(S(C_PARTS['pigtail']), END + 1)])
m = Mesh()
yb_, yi_ = OYc + (C.ci('b') - 1) * P, OYc + (C.ci('i') - 1) * P
for r in C.C_TIES:
    x = OXc + (r - 1) * P
    top = zb + sk['body_h'] if X(sk['body'][0]) < x < x1 else zc + 0.6
    for ya, yb2, z0, z1 in ((yb_, yi_, top, top + 0.4), (yb_, yi_, -2.0, -1.6)):
        m.box(x - 1.25, x + 1.25, ya, yb2, z0, z1, 'captop')
    for y in (yb_, yi_):
        m.box(x - 1.25, x + 1.25, y - 0.2, y + 0.2, -2.0, top + 0.4, 'captop')
    m.box(x - 1.6, x + 1.6, yi_ - 3.2, yi_ - 0.2, top, top + 1.6, 'captop')      # the lock
drop(m.make('c-zip-ties', cr), C_PARTS['ties'], 15)
joints('c-joints', C_PINS, cr, C_J)
c_sp = [w_ for w_ in C.C_WIRES if w_[2] == 'pwr']
c_ot = [w_ for w_ in C.C_WIRES if w_[2] != 'pwr']
for group, (a, z) in ((c_sp, C_SPINES), (c_ot, C_WIRES)):
    step = (z - a) / max(1, len(group))
    for i, (net, pts, kind) in enumerate(group):
        xy = [ch(c, r) for c, r in pts]
        wire(f'c-wire-{net}-{i}', xy, net, kind, cr, a + i * step)
        if kind != 'lead':
            joints(f'c-wj-{net}-{i}', [xy[0], xy[-1]], cr, a + i * step + WIRE_S)

flip(car, *FLIP1)
flip(car, *FLIP1B)
flip(car, *FLIP2)
flip(car, *FLIP2B)
flip(cr, *C_FLIP, lift=35)
flip(cr, *C_FLIPB, lift=35)

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
        (34.6, (-18, 135, 132), (-15, 37, 0)),
        (56.0, (-18, 135, 132), (-15, 37, 0)),
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
sh.studio_light = 'paint.sl'                                  # lights the undersides too; the default studio light leaves them black
sh.show_cavity = sh.show_object_outline = True
sh.background_type = 'VIEWPORT'
sh.background_color = (0.16, 0.17, 0.19)
sc.world = bpy.data.worlds.new("bench")      # the render reads the world, not the viewport
sc.world.color = (0.16, 0.17, 0.19)
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
if STILL is not None:
    sc.frame_set(S(STILL))
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = os.path.join(RENDERS, f"stm32-carrier-still-{STILL:g}.png")
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath)
    sys.exit(0)
if PREVIEW:
    sc.render.resolution_percentage = 50
    sc.frame_step = 4
mp4(sc)
sc.render.filepath = OUT
bpy.ops.render.render(animation=True)
print("wrote", OUT)
