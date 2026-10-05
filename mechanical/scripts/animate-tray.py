"""Assembly animation of the carrier tray (MEC-17), rendered by Blender.

    openscad -D 'PART="tray"' -o ../cad/carrier-tray.stl ../cad/carrier-tray.scad   # the tray it animates
    blender -b -P animate-tray.py                   # -> ../renders/tray-assembly.mp4
    blender -b -P animate-tray.py -- --preview      # half size, every 4th frame
    blender -b -P animate-tray.py -- --still 20     # one PNG at 20 s, for checking a moment

Two steps, as MEC-17 places it. First the carrier is built on the tray at the bench: nuts into the
four pockets, boards A, B and C onto the tray's own holes, the S6 / S7 splices. Then the tray goes
onto plate 2: its holes over the plate's, the wires up through the window, four screws from below,
and plate 2 lowers onto its standoffs. The Discovery plugs on last.

Read from disk: ../cad/carrier-tray.stl (the tray itself), and ../../hardware/renders/chassis-layout.svg
(plate 2's outline, its holes and slots, so the plate is the survey's and not a drawing of one).
Everything else is a stand-in: the boards, the harness parts under plate 2 at MEC-16's footprints, the
Discovery. The order of work is a PROPOSAL (MEC-17), not a measured procedure.

Coordinates: the layout frame of MEC-15 / MEC-16 (x front to rear, y from the vehicle's right), in
millimetres, z up from plate 1's top face. The layout's y runs the wrong way for a right-handed frame,
so every point is written to Blender with y negated (B() below) and nothing else changes.
"""
import bpy, bmesh, math, os, re, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(HERE, "..", "cad")
RENDERS = os.path.join(HERE, "..", "renders")
SVG = os.path.join(HERE, "..", "..", "hardware", "renders", "chassis-layout.svg")
OUT = os.path.join(RENDERS, "tray-assembly.mp4")
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PREVIEW = "--preview" in ARGS
STILL = float(ARGS[ARGS.index("--still") + 1]) if "--still" in ARGS else None

FPS = 24
S = lambda sec: int(round(sec * FPS)) + 1
END = S(50)

# ---------------------------------------------------------------- the design (mirrors carrier-tray.scad)
PLACE = (85.50, 5.11)
T = 4.0
CORNER_INSET = 2.5
Z_PLATE_TOP, Z_PLATE_BOT = 52.0, 50.0
LIFT = 60.0                              # plate 2 is worked on this far above its standoffs
BOARDS = {'A': (31.50, 101.50, 0.00, 50.00, 6), 'B': (34.04, 104.04, 55.88, 105.88, 6),
          'C': (0.00, 30.00, 20.09, 90.09, 10)}                   # tray frame u0 u1 v0 v1, standoff mm
FIXINGS = {'F1': (148.18, 23.76), 'F2': (148.18, 72.24), 'F5': (99.24, 38.76), 'F6': (99.24, 81.76)}
PLATE_D = {'F1': 3.18, 'F2': 2.71, 'F5': 3.18, 'F6': 3.18}
SPLICES = [(87.7, 106.3, 41.5, 54.5), (87.7, 106.3, 63.5, 76.5)]
BENCH = (0.0, 175.0)                     # where the unit is built, beside plate 2 (layout y negated)

# ---------------------------------------------------------------- timeline (seconds)
NUTS = [3.0, 3.4, 3.8, 4.2]
BOARD_T = {'A': 6.0, 'B': 7.2, 'C': 8.4}
SCREWS_T = 10.5                          # twelve board screws, 0.25 s apart
SPLICE_T = [15.0, 15.6]
CARRY = (18.5, 23.5)                     # lift, across, set down
WIRES_T = 24.0
FIX_T = [26.5, 27.3, 28.1, 28.9]
LOWER = (32.5, 36.5)
DISCO = (38.5, 41.0)
ORBIT = 42.0
DROP = S(0.7) - 1

CAPTIONS = [
    ((0, 3), "Two steps: build the carrier on the tray at the bench, then set the tray on plate 2"),
    ((3, 5.6), "1  An M2.5 nut into each of the tray's four hex pockets - they hold the nut so a screw can turn from below"),
    ((5.6, 10.3), "2  Boards A, B and C lower onto the tray: their nylon standoffs land on the tray's board holes"),
    ((10.3, 14.4), "3  Twelve M2.5 screws from below into the standoffs - the heads sit in the tray's counterbores"),
    ((14.4, 18.5), "4  The S6 and S7 splices go into their outlines under board C"),
    ((18.5, 23.5), "5  Step 2: lift the unit onto plate 2 - its holes are plate 2's holes, its window is the wire opening"),
    ((23.5, 26.2), "6  The Bauer feed comes up through the window to the splices"),
    ((26.2, 32.0), "7  F1, F2, F5, F6: an M2.5 screw from below into each nut pocket (a washer in the three M3 holes)"),
    ((32.0, 36.5), "8  Plate 2 comes off its blocks and lowers onto the chassis standoffs"),
    ((36.5, 41.0), "9  The Discovery plugs onto the sockets of A and B"),
    ((41.0, 50.0), "The tray lifts out as one unit: unscrew four screws from below"),
]

# ---------------------------------------------------------------- scene, materials
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)


MATS = {}


def mat(name, colour, a=1.0):
    if name not in MATS:
        m = bpy.data.materials.new(name)
        m.diffuse_color = hexc(colour, a) if isinstance(colour, str) else colour
        MATS[name] = m
    return MATS[name]


for n, c, a in [('plate', '#4b5563', 1), ('plate1', '#64748b', 0.35), ('standoff', '#cbd5e1', 1), ('tray', '#e5e7eb', 1),
                ('fr4', '#1f7a3a', 1), ('black', '#16181c', 1), ('nylon', '#f1f5f9', 1), ('steel', '#9ca3af', 1),
                ('nut', '#facc15', 1), ('term', '#2563eb', 1), ('cap', '#1e293b', 1), ('splice', '#f97316', 1),
                ('red', '#dc2626', 1), ('blk', '#111827', 1), ('harness', '#a8855a', 0.4), ('fuse', '#b45309', 0.4),
                ('disco', '#243b63', 1), ('usb', '#c0c4ca', 1), ('bench', '#8b6f47', 1), ('block', '#7c5e3c', 1),
                ('module', '#1d4ed8', 1)]:
    mat(n, c, a)


def B(x, y, z):
    return (x, -y, z)


def new_obj(name, bm, material, parent=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.data.materials.append(MATS[material])
    sc.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def prism(name, poly, z0, z1, material, parent=None):
    """An extruded polygon, given in layout coordinates."""
    bm = bmesh.new()
    lo = [bm.verts.new(B(x, y, z0)) for x, y in poly]
    hi = [bm.verts.new(B(x, y, z1)) for x, y in poly]
    bm.faces.new(lo[::-1])
    bm.faces.new(hi)
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([lo[i], lo[j], hi[j], hi[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, material, parent)


def box(name, x0, x1, y0, y1, z0, z1, material, parent=None):
    return prism(name, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1, material, parent)


def cyl(name, x, y, z0, z1, d, material, parent=None, n=20, rot=0.0):
    return prism(name, [(x + d / 2 * math.cos(rot + 2 * math.pi * i / n), y + d / 2 * math.sin(rot + 2 * math.pi * i / n))
                        for i in range(n)], z0, z1, material, parent)


def hexa(name, x, y, z0, z1, af, material, parent=None):
    return cyl(name, x, y, z0, z1, af / math.cos(math.radians(30)), material, parent, n=6)


def rrect_poly(x0, x1, y0, y1, r, steps=8):
    pts = []
    for cx, cy, a0 in [(x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)]:
        for k in range(steps + 1):
            a = math.radians(a0 + 90 * k / steps)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    sc.collection.objects.link(e)
    if parent is not None:
        e.parent = parent
    return e


def show(o, frames):
    """Rendered only inside the given (start, end) frame windows - the object and everything under it."""
    for t in [o] + list(o.children_recursive):
        t.hide_render = True
        t.keyframe_insert("hide_render", frame=1)
        for a, b in frames:
            t.hide_render = False
            t.keyframe_insert("hide_render", frame=a)
            t.hide_render = True
            t.keyframe_insert("hide_render", frame=b)
        for fc in t.animation_data.action.fcurves:
            if fc.data_path == "hide_render":
                for k in fc.keyframe_points:
                    k.interpolation = 'CONSTANT'


def drop(o, sec, dz=30.0, dur=None):
    """Appear dz above (or below, if negative) its place at `sec`, settle onto it."""
    f = S(sec)
    show(o, [(f, END + 1)])
    o.location = (0, 0, dz)
    o.keyframe_insert("location", frame=f)
    o.location = (0, 0, 0)
    o.keyframe_insert("location", frame=f + (DROP if dur is None else S(dur) - 1))


def move(o, keys):
    """keys: [(sec, (x, y, z))] in the object's parent frame."""
    for sec, p in keys:
        o.location = p
        o.keyframe_insert("location", frame=S(sec))


# ---------------------------------------------------------------- plate 2 from the survey
svg = open(SVG, encoding="utf-8").read().split("\n")
top = next(i for i, l in enumerate(svg) if "MIDDLE DECK - plate 2, TOP FACE" in l)
low = next(i for i, l in enumerate(svg) if "LOWER DECK - plate 1" in l)
plan = svg[top:low]
OUTLINE = None
for l in plan:
    if l.startswith("<path") and OUTLINE is None:
        nums = re.findall(r"[ML]([\d.]+) ([\d.]+)", l)
        OUTLINE = [((float(a) - 60.0) / 1.7, (float(b) - 390.0) / 1.7) for a, b in nums]
CUTS = []                                       # (kind, data)
for l in plan:
    if "#eef2f6" not in l:
        continue
    m = re.match(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', l)
    if m:
        cx, cy, r = map(float, m.groups())
        CUTS.append(((cx - 60.0) / 1.7, (cy - 390.0) / 1.7, 2 * r / 1.7))
        continue
    m = re.match(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="([\d.]+)"', l)
    if m:
        x, y, w, h, rx = map(float, m.groups())
        CUTS.append((((x - 60.0) / 1.7, (x + w - 60.0) / 1.7, (y - 390.0) / 1.7, (y + h - 390.0) / 1.7, rx / 1.7)))

# ---------------------------------------------------------------- plate 1, the standoffs, plate 2
P1 = prism("plate1", OUTLINE, 0.0, 2.0, 'plate1')
for (x, y) in [(27.35, 22.18), (27.35, 98.35), (256.82, 22.18), (256.82, 98.35)]:
    cyl("so", x, y, 2.0, Z_PLATE_BOT, 6.0, 'standoff', n=6)

P2 = empty("PLATE2", loc=(0, 0, LIFT))
plate = prism("plate2", OUTLINE, Z_PLATE_BOT, Z_PLATE_TOP, 'plate', P2)
cutters = []
for c in CUTS:
    if len(c) == 3:
        cutters.append(cyl("c", c[0], c[1], Z_PLATE_BOT - 1, Z_PLATE_TOP + 1, c[2], 'plate', n=16))
    else:
        cutters.append(prism("c", rrect_poly(c[0], c[1], c[2], c[3], min(c[4], (c[1] - c[0]) / 2, (c[3] - c[2]) / 2)),
                             Z_PLATE_BOT - 1, Z_PLATE_TOP + 1, 'plate'))
bpy.ops.object.select_all(action='DESELECT')
for o in cutters:
    o.select_set(True)
bpy.context.view_layer.objects.active = cutters[0]
bpy.ops.object.join()
cutter = bpy.context.view_layer.objects.active
mod = plate.modifiers.new("holes", 'BOOLEAN')
mod.object, mod.operation, mod.solver = cutter, 'DIFFERENCE', 'EXACT'
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier="holes")
bpy.data.objects.remove(cutter)

# the harness board under plate 2 (MEC-16): stand-in boxes at the table's footprints, 1 mm foam under plate 2
HARNESS = [("main fuse", 96, 146, 2, 32, 15), ("motor fuse", 152, 202, 2, 32, 15), ("ubec fuse", 152, 202, 88, 118, 15),
           ("(+) bus", 88, 106.6, 40, 70, 12), ("(-) bus", 134, 152.6, 40, 70, 12), ("ina226", 108, 134, 78, 100, 8),
           ("ubec", 100, 135, 100, 112, 20)]
for n, x0, x1, y0, y1, h in HARNESS:
    box(n, x0, x1, y0, y1, Z_PLATE_BOT - 1 - h, Z_PLATE_BOT - 1, 'harness' if 'fuse' not in n else 'fuse', P2)

# ---------------------------------------------------------------- the bench, and the blocks plate 2 stands on
BENCH_Z = LIFT + Z_PLATE_BOT - 24.0            # clear of the harness parts hanging under plate 2
BENCH_B = (BENCH[0], BENCH[1], LIFT)           # the unit's start in Blender coordinates: layout y -175 is Blender y +175
slab2 = box("bench-plate2", 0, 275, -10, 130, BENCH_Z - 3, BENCH_Z, 'bench')
BLOCKS = [box("blk", x - 6, x + 6, y - 6, y + 6, 2.0, LIFT + Z_PLATE_BOT, 'block')    # trestles off plate 1, beside the chassis standoffs
          for x, y in [(27.35, 38.0), (27.35, 82.0), (256.82, 38.0), (256.82, 82.0)]]
show(slab2, [(1, S(WIRES_T))])                 # the bench is pulled out once the unit is down, to work from below
for o in BLOCKS:
    show(o, [(1, S(LOWER[0]))])

# ---------------------------------------------------------------- the unit, built at the bench
ROOT = empty("UNIT")
ROOT.location = BENCH_B

tray = None
bpy.ops.wm.stl_import(filepath=os.path.join(CAD, "carrier-tray.stl"))
tray = bpy.context.selected_objects[0]
tray.name = "tray"
tray.parent = ROOT
tray.location = (PLACE[0], -PLACE[1], Z_PLATE_TOP)
tray.data.materials.append(MATS['tray'])

# the bench slab under the unit
slab = box("bench-unit", 70, 215, -BENCH[1] - 5, -BENCH[1] + 120, BENCH_Z - 3, BENCH_Z, 'bench')
show(slab, [(1, S(CARRY[1]))])
bars = [box("bar", 98, 106, -BENCH[1] + 3, -BENCH[1] + 108, BENCH_Z, LIFT + Z_PLATE_TOP, 'block'),
        box("bar", 152, 160, -BENCH[1] + 3, -BENCH[1] + 108, BENCH_Z, LIFT + Z_PLATE_TOP, 'block')]
for o in bars:
    show(o, [(1, S(CARRY[0]))])


def tp(u, v):
    return PLACE[0] + u, PLACE[1] + v          # tray frame -> plate-2 layout frame


def corners(b):
    u0, u1, v0, v1 = b[:4]
    return [(u0 + CORNER_INSET, v0 + CORNER_INSET), (u1 - CORNER_INSET, v0 + CORNER_INSET),
            (u0 + CORNER_INSET, v1 - CORNER_INSET), (u1 - CORNER_INSET, v1 - CORNER_INSET)]


# nuts into the pockets
nuts = {}
for k, (x, y) in FIXINGS.items():
    o = hexa("nut-" + k, x, y, Z_PLATE_TOP + T - 2.4, Z_PLATE_TOP + T - 0.4, 5.0, 'nut', ROOT)
    nuts[k] = o
for o, t in zip(nuts.values(), NUTS):
    drop(o, t, dz=25.0)

# the boards, each with its standoffs, sockets and a few parts
ZB = {k: Z_PLATE_TOP + T + b[4] for k, b in BOARDS.items()}
assemblies = {}
for k, b in BOARDS.items():
    asm = empty("board-" + k, ROOT)
    assemblies[k] = asm
    u0, u1, v0, v1 = b[:4]
    x0, y0 = tp(u0, v0)
    x1, y1 = tp(u1, v1)
    zb = ZB[k]
    box("fr4-" + k, x0, x1, y0, y1, zb, zb + 1.6, 'fr4', asm)
    for (u, v) in corners(b):
        x, y = tp(u, v)
        cyl("standoff", x, y, Z_PLATE_TOP + T, zb, 5.0, 'nylon', asm, n=6)
    if k in 'AB':                                          # the two 1x24 sockets under the Discovery, 5.1 mm across
        vs = 22.5 if k == 'A' else 73.2
        xs, ys = tp(38.56, vs)
        box("sockets-" + k, xs, xs + 61.0, ys, ys + 5.1, zb + 1.6, zb + 10.1, 'black', asm)
    if k == 'A':
        box("term-6V", x0 + 4, x0 + 14, y1 - 28, y1 - 6, zb + 1.6, zb + 11.6, 'term', asm)
        cyl("c2", x0 + 34, y0 + 7, zb + 1.6, zb + 14.6, 10.0, 'cap', asm)
    if k == 'B':
        box("term-can", x0 + 4, x0 + 14, y0 + 6, y0 + 22, zb + 1.6, zb + 11.6, 'term', asm)
        box("module", x0 + 40, x0 + 68, y1 - 20, y1 - 8, zb + 1.6, zb + 6.0, 'module', asm)
    if k == 'C':
        cyl("c1", x0 + 15, y0 + 18, zb + 1.6, zb + 14.6, 10.0, 'cap', asm)
        box("usbc", x0 + 8, x0 + 22, y0 - 4, y0 + 9, zb + 1.6, zb + 5.0, 'steel', asm)
        box("term-c", x0 + 4, x0 + 24, y1 - 12, y1 - 3, zb + 1.6, zb + 11.0, 'term', asm)
for k, t in BOARD_T.items():
    drop(assemblies[k], t, dz=40.0)

# the board screws, from below
sc_n = 0
for k, b in BOARDS.items():
    for (u, v) in corners(b):
        x, y = tp(u, v)
        zb = ZB[k]
        s = empty("screw", ROOT)
        cyl("head", x, y, Z_PLATE_TOP, Z_PLATE_TOP + 2.0, 4.6, 'steel', s)
        cyl("shaft", x, y, Z_PLATE_TOP + 2.0, zb - 2.0, 2.5, 'steel', s)
        drop(s, SCREWS_T + 0.25 * sc_n, dz=-22.0, dur=0.5)
        sc_n += 1

# the splices
for i, (x0, x1, y0, y1) in enumerate(SPLICES):
    sp = box("splice-s%d" % (6 + i), x0, x1, y0, y1, Z_PLATE_TOP + T, Z_PLATE_TOP + T + 8.5, 'splice', ROOT)
    drop(sp, SPLICE_T[i], dz=25.0)

# carried across: lift, over, set down; then it rides plate 2 down
bx, by, bz = BENCH_B
move(ROOT, [(0, (bx, by, bz)), (CARRY[0], (bx, by, bz)), (CARRY[0] + 1.4, (bx, by, bz + 40)),
            (CARRY[1] - 1.8, (0, 0, bz + 40)), (CARRY[1], (0, 0, bz)),
            (LOWER[0], (0, 0, bz)), (LOWER[1], (0, 0, 0))])
move(P2, [(0, (0, 0, LIFT)), (LOWER[0], (0, 0, LIFT)), (LOWER[1], (0, 0, 0))])
for ob in list(bpy.data.objects):
    if ob.animation_data and ob.animation_data.action:
        for fc in ob.animation_data.action.fcurves:
            if fc.data_path == "location" and ob in (ROOT, P2):
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'

# the Bauer feed up through the window to the splices (under plate 2, then over the tray's top)
for i, (col, zoff) in enumerate([('red', 0.0), ('blk', 1.4)]):
    cu = bpy.data.curves.new("w", 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution = '3D', 1.0, 3
    sp = cu.splines.new('POLY')
    ya = 49.0 + i * 15.0
    pts = [(112.4 + zoff * 0.3, ya, Z_PLATE_BOT - 14.0), (112.4 + zoff * 0.3, ya, Z_PLATE_TOP + T + 3.0 + zoff),
           (109.0, ya - 2, Z_PLATE_TOP + T + 9.0 + zoff), (104.0, SPLICES[i][2] + 6.5, Z_PLATE_TOP + T + 11.0),
           (104.0, SPLICES[i][2] + 6.5, Z_PLATE_TOP + T + 4.5)]
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (*B(*co), 1)
    w = bpy.data.objects.new("wire", cu)
    w.data.materials.append(MATS[col])
    sc.collection.objects.link(w)
    w.parent = P2
    drop(w, WIRES_T + 0.5 * i, dz=-20.0, dur=1.2)

# the four screws and washers from below
for (k, (x, y)), t in zip(FIXINGS.items(), FIX_T):
    s = empty("fix-" + k, P2)
    if PLATE_D[k] > 3.0:                                  # a washer only in the three M3 holes (MEC-11); F2's hole is M2.5
        cyl("washer", x, y, Z_PLATE_BOT - 0.5, Z_PLATE_BOT, 6.0, 'steel', s)
    cyl("head", x, y, Z_PLATE_BOT - 2.5, Z_PLATE_BOT - 0.5, 4.6, 'steel', s)
    cyl("shaft", x, y, Z_PLATE_BOT, Z_PLATE_TOP + T - 0.8, 2.5, 'steel', s)
    drop(s, t, dz=-30.0, dur=0.7)

# the Discovery (a mock: outline from UM1472, USB and chip for recognition)
disco = empty("discovery", ROOT)
dx, dy = tp(35.0, 17.4)
zd = ZB['A'] + 1.6 + 10.1
box("disco-pcb", dx, dx + 97.0, dy, dy + 66.0, zd, zd + 1.6, 'disco', disco)
box("disco-chip", dx + 45, dx + 59, dy + 26, dy + 40, zd + 1.6, zd + 3.4, 'black', disco)
box("disco-usb", dx + 94, dx + 101, dy + 26, dy + 38, zd + 1.6, zd + 5.0, 'usb', disco)
box("disco-usb2", dx + 2, dx + 9, dy + 6, dy + 18, zd + 1.6, zd + 5.0, 'usb', disco)
drop(disco, DISCO[0], dz=45.0, dur=DISCO[1] - DISCO[0])

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
UNIT_C = (137.0, BENCH[1] - 58.0, LIFT + 62.0)             # the bench unit, in Blender coordinates
PL2_C = (137.0, -58.0, LIFT + 52.0)
LOW_C = (150.0, -58.0, 55.0)
KEYS = [(0, (30.0, 400.0, 330.0), (130.0, 110.0, 100.0)),
        (2.4, (50.0, 335.0, 250.0), UNIT_C),
        (17.8, (50.0, 335.0, 250.0), UNIT_C),
        (19.0, (60.0, 330.0, 330.0), (140.0, 60.0, 112.0)),
        (24.0, (110.0, 120.0, 245.0), PL2_C),
        (25.6, (110.0, 120.0, 245.0), PL2_C),
        (27.0, (128.0, -20.0, 6.0), (128.0, -58.0, 110.0)),
        (31.8, (128.0, -20.0, 6.0), (128.0, -58.0, 110.0)),
        (34.0, (60.0, 160.0, 250.0), (150.0, -58.0, 85.0)),
        (38.0, (60.0, 120.0, 190.0), LOW_C),
        (41.5, (60.0, 120.0, 190.0), LOW_C)]
for sec, c, t in KEYS:
    f = S(sec)
    cam.location, target.location = c, t
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
holder = empty("caption-holder", cam)                     # captions keep their size on screen when the lens changes
for sec, lens in [(26.0, 32.0), (27.2, 20.0), (31.8, 20.0), (33.0, 32.0)]:      # wide for the view from below
    cam.data.lens = lens
    cam.data.keyframe_insert("lens", frame=S(sec))
    holder.scale = (32.0 / lens, 32.0 / lens, 1.0)
    holder.keyframe_insert("scale", frame=S(sec))
for i in range(0, 12):                                     # orbit the finished carrier
    f = S(ORBIT) + i * S(0.7)
    a = math.radians(70 - i * 22)
    cam.location = (150 + 230 * math.cos(a), -58 + 230 * math.sin(a), 150 - i * 4)
    target.location = LOW_C
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions, riding with the camera
band_mat = bpy.data.materials.new("caption-band")
band_mat.diffuse_color = (0.02, 0.02, 0.03, 0.72)
bpy.ops.mesh.primitive_plane_add(size=1)
bo = bpy.context.active_object
bo.name = "caption-band"
bo.data.materials.append(band_mat)
bo.parent = holder
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
    t.parent = holder
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
sc.world = bpy.data.worlds.new("bench")
sc.world.color = (0.16, 0.17, 0.19)
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
if STILL is not None:
    sc.frame_set(S(STILL))
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = os.path.join(RENDERS, f"tray-still-{STILL:g}.png")
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
