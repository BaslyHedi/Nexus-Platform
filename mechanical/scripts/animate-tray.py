"""Assembly animation of the carrier tray (MEC-17), rendered by Blender.

    openscad -D 'PART="tray"' -o ../cad/carrier-tray.stl ../cad/carrier-tray.scad   # the tray it animates
    blender -b -P animate-tray.py                   # -> ../renders/tray-assembly.mp4
    blender -b -P animate-tray.py -- --preview      # half size, every 4th frame
    blender -b -P animate-tray.py -- --still 20     # one PNG at 20 s, for checking a moment

Two steps, as MEC-17 places it. First the carrier is built on the tray at a jig: nuts into the pockets, the
boards A, B and C on their standoffs, the screws from below, the splices, the Bauer in its rim. Then the tray goes
onto plate 2: its holes over the plate's, the wires up through the window, six screws from below, and plate 2 lowers
onto its standoffs. The Bauer is held to the tray by two M3 screws through its own mounting holes. The Discovery plugs on last.

Read from disk: ../cad/carrier-tray.stl (the tray itself), ../../hardware/renders/chassis-layout.svg (plate 2's
outline, holes and slots) and, through carrier_model.py, ../../hardware/scripts/stm32-carrier.py (the boards as
built: every part and wire). Stand-ins: the harness parts under plate 2 (MEC-16 footprints), the Bauer (64 x 57 x
22 mm; its ears are not modelled, they are not measured), the Discovery. The order of work is a PROPOSAL (MEC-17).

Coordinates: plate 2's layout frame (x front to rear, y from the vehicle's right, mm, z up from plate 1's top).
The layout's y runs the wrong way for a right-handed frame, so a point goes to Blender as (x, -y, z).
"""
import bpy, bmesh, math, os, re, sys
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)           # before carrier_model, which creates the materials

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import carrier_model as CM                                     # noqa: E402
from carrier_model import Mesh, Frame, MATS, mat, empty        # noqa: E402

CAD = os.path.join(HERE, "..", "cad")
RENDERS = os.path.join(HERE, "..", "renders")
SVG = os.path.join(HERE, "..", "..", "hardware", "renders", "chassis-layout.svg")
OUT = os.path.join(RENDERS, "tray-assembly.mp4")
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PREVIEW = "--preview" in ARGS
STILL = float(ARGS[ARGS.index("--still") + 1]) if "--still" in ARGS else None

FPS = 24
S = lambda sec: int(round(sec * FPS)) + 1
END = S(58)

# ---------------------------------------------------------------- the design (mirrors carrier-tray.scad)
PLACE = (8.50, 5.11)
T = 4.0
CORNER_INSET = 2.5
ZP_TOP, ZP_BOT = 52.0, 50.0
LIFT = 60.0                                   # plate 2 is worked on this far above its standoffs
Z_TRAY = ZP_TOP + T                           # the tray's top face
BOARDS = {'A': (117.00, 187.00, 5.11, 55.11, 8), 'B': (119.54, 189.54, 60.99, 110.99, 8),
          'C': (85.50, 115.50, 25.20, 95.20, 8)}          # plate-2 x0 x1 y0 y1, standoff height
FIXINGS = {'F1': (148.18, 23.76, 3.18), 'F2': (148.18, 72.24, 2.71), 'F5': (99.24, 38.76, 3.18), 'F6': (99.24, 81.76, 3.18),
           'F7': (24.82, 60.24, 3.18), 'F8': (52.82, 60.24, 3.18)}
EARS = [(16.0, 63.0), (70.0, 63.0)]            # the Bauer's two 6.8 mm holes: 5 and 59 mm from its front end, 26 mm from its leads edge (y 89)
SPLICES = [(87.7, 106.3, 41.5, 54.5), (87.7, 106.3, 63.5, 76.5)]
BAUER = (11.0, 75.0, 32.0, 89.0, 22.0)         # x0 x1 y0 y1 height: 10.5 mm clear of board C, for its cables
BENCH_Y = 190.0                                # the jig stands this far to the vehicle's right (Blender +y)

# ---------------------------------------------------------------- timeline (seconds)
NUTS = [4.0 + 0.35 * i for i in range(8)]          # six M2.5 and two M3
BAUER_T = 8.0
EARSCREW_T = 9.2
BOARD_T = {'C': 10.5, 'AB': 12.0}
SCREWS_T = 14.5                                # twelve board screws, 0.28 s apart
SPLICE_T = [19.0, 19.6]
CARRY = (22.5, 28.5)                           # lift, across, set down
WIRES_T = 29.5
FIX_T = [32.5 + 0.6 * i for i in range(6)]
SECTION = (37.0, 41.5)                         # the cutaway through one fixing
LOWER = (42.5, 46.5)
DISCO = (48.0, 50.5)
ORBIT = 51.0
DROP = S(0.7) - 1

CAPTIONS = [
    ((0, 4), "The carrier tray: 182 x 106 mm, 4 mm PETG. Plate 2's holes are repeated in it; eight have a nut pocket"),
    ((4, 7.4), "1  A nut into each hex pocket: six M2.5 for plate 2, two M3 under the Bauer's holes"),
    ((7.4, 10.3), "2  The Bauer drops into its rim, two M3 screws through its own holes; its leads get a clear lane"),
    ((10.3, 14.4), "3  Boards C, then A and B, lower on their nylon standoffs onto the tray's board holes"),
    ((14.4, 19), "4  Twelve M2.5 screws from below, one into each standoff; the heads sit in the counterbores"),
    ((19, 22.5), "5  The S6 and S7 splices go into their outlines under board C"),
    ((22.5, 29.5), "Step 2. The unit lifts onto plate 2: every tray hole lands on a plate hole, the window on the wire opening"),
    ((29.5, 32.5), "6  The Bauer's 12 V feed comes up through the window to the splices"),
    ((32.5, 37), "7  F1, F2, F5, F6, F7, F8: a screw from below into each pocket (a washer in the M3 holes)"),
    ((37, 41.5), "Section through one fixing: plate 2, the tray with its captive nut, the screw, the Bauer above"),
    ((41.5, 48), "8  Plate 2 comes off its blocks and lowers onto the chassis standoffs"),
    ((48, 51), "9  The Discovery plugs onto the sockets of A and B"),
    ((51, 58), "The tray lifts out as one unit: six screws from below. The Bauer comes off with two"),
]

# ---------------------------------------------------------------- scene
sc = bpy.context.scene
for n, c, a in [('plate', '#8793a1', 1), ('plate1', '#64748b', 0.35), ('standoff', '#cbd5e1', 1), ('tray', '#eceff3', 1),
                ('nylon', '#f4f6f8', 1), ('steel', '#a3aab4', 1), ('nut', '#f2c230', 1), ('splice', '#f97316', 1),
                ('red', '#dc2626', 1), ('blk', '#111827', 1), ('harness', '#b69668', 0.22), ('fuse', '#c2410c', 0.22),
                ('rail', '#475569', 1), ('block', '#64748b', 1), ('bauer', '#2f353d', 1), ('bauerfin', '#4a525d', 1),
                ('bauerlabel', '#d1d5db', 1), ('lead_r', '#b91c1c', 1), ('lead_k', '#0f172a', 1),
                ('sec_bg', '#1b1f24', 1), ('lead_y', '#eab308', 1)]:
    mat(n, c, a)
ID = Frame(lambda X, Y, Z: (X, -Y, Z), proper=False)           # plate-2 layout coordinates -> Blender


def B(x, y, z):
    return (x, -y, z)


def prism(name, poly, z0, z1, material, parent=None):
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
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.data.materials.append(MATS[material])
    sc.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def box(name, x0, x1, y0, y1, z0, z1, material, parent=None):
    m = Mesh(ID)
    m.box(x0, x1, y0, y1, z0, z1, material)
    return m.make(name, parent)


def cyl(name, x, y, z0, z1, d, material, parent=None, n=24):
    m = Mesh(ID)
    m.cyl((x, y, z0), (x, y, z1), d / 2, material, n)
    return m.make(name, parent)


def hexa(name, x, y, z0, z1, af, material, parent=None):
    return cyl(name, x, y, z0, z1, af / math.cos(math.radians(30)), material, parent, n=6)


def rrect_poly(x0, x1, y0, y1, r, steps=8):
    pts = []
    for cx, cy, a0 in [(x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)]:
        for k in range(steps + 1):
            a = math.radians(a0 + 90 * k / steps)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


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
    """Appear dz above (below, if negative) its place at `sec`, settle onto it."""
    f = S(sec)
    show(o, [(f, END + 1)])
    o.location = (0, 0, dz)
    o.keyframe_insert("location", frame=f)
    o.location = (0, 0, 0)
    o.keyframe_insert("location", frame=f + (DROP if dur is None else S(dur) - 1))


def move(o, keys):
    for sec, p in keys:
        o.location = p
        o.keyframe_insert("location", frame=S(sec))


def grow(o, sec, dur):
    """Draw a curve object from its first point."""
    f = S(sec)
    show(o, [(f, END + 1)])
    cu = o.data
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=f)
    cu.bevel_factor_end = 1.0
    cu.keyframe_insert("bevel_factor_end", frame=f + S(dur) - 1)


# ---------------------------------------------------------------- plate 2 from the survey
svg = open(SVG, encoding="utf-8").read().split("\n")
top = next(i for i, l in enumerate(svg) if "MIDDLE DECK - plate 2, TOP FACE" in l)
low = next(i for i, l in enumerate(svg) if "LOWER DECK - plate 1" in l)
plan = svg[top:low]
OUTLINE = None
for l in plan:
    if l.startswith("<path") and OUTLINE is None:
        OUTLINE = [((float(a) - 60.0) / 1.7, (float(b) - 390.0) / 1.7) for a, b in re.findall(r"[ML]([\d.]+) ([\d.]+)", l)]
CUTS = []
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
        CUTS.append(((x - 60.0) / 1.7, (x + w - 60.0) / 1.7, (y - 390.0) / 1.7, (y + h - 390.0) / 1.7, rx / 1.7))

prism("plate1", OUTLINE, 0.0, 2.0, 'plate1')
for (x, y) in [(27.35, 22.18), (27.35, 98.35), (256.82, 22.18), (256.82, 98.35)]:
    cyl("chassis-standoff", x, y, 2.0, ZP_BOT, 6.0, 'standoff', n=6)

P2 = empty("PLATE2", loc=(0, 0, LIFT))
plate = prism("plate2", OUTLINE, ZP_BOT, ZP_TOP, 'plate', P2)
cutters = []
for c in CUTS:
    if len(c) == 3:
        m = Mesh(ID)
        m.cyl((c[0], c[1], ZP_BOT - 1), (c[0], c[1], ZP_TOP + 1), c[2] / 2, 'plate', 20)
        cutters.append(m.make("c"))
    else:
        cutters.append(prism("c", rrect_poly(c[0], c[1], c[2], c[3], min(c[4], (c[1] - c[0]) / 2, (c[3] - c[2]) / 2)), ZP_BOT - 1, ZP_TOP + 1, 'plate'))
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

# the harness board under plate 2 (MEC-16 footprints, plate1.py), translucent so the screw heads read through it
for n, x0, x1, y0, y1, h in [("main fuse", 96, 146, 2, 32, 15), ("motor fuse", 152, 202, 2, 32, 15), ("ubec fuse", 152, 202, 88, 118, 15),
                             ("(+) bus", 88, 106.6, 40, 70, 12), ("(-) bus", 134, 152.6, 40, 70, 12), ("ina226", 108, 134, 78, 100, 8),
                             ("ubec", 100, 135, 100, 112, 20), ("s1", 83, 96, 21, 40, 8)]:
    box(n, x0, x1, y0, y1, ZP_BOT - 1 - h, ZP_BOT - 1, 'fuse' if 'fuse' in n else 'harness', P2)

# plate 2 rests on four blocks until it is lowered
BLOCKS = [box("block", x - 6, x + 6, y - 6, y + 6, 2.0, LIFT + ZP_BOT, 'block') for x, y in [(27.35, 38.0), (27.35, 82.0), (256.82, 38.0), (256.82, 82.0)]]
for o in BLOCKS:
    show(o, [(1, S(LOWER[0]))])

# ---------------------------------------------------------------- the unit, built on the jig
ROOT = empty("UNIT")
ROOT.location = (0, BENCH_Y, LIFT)
bpy.ops.wm.stl_import(filepath=os.path.join(CAD, "carrier-tray.stl"))
tray = bpy.context.selected_objects[0]
tray.name = "tray"
tray.parent = ROOT
tray.location = (PLACE[0], -PLACE[1], ZP_TOP)
for p in tray.data.polygons:
    p.use_smooth = False
tray.data.materials.append(MATS['tray'])

# the jig: three posts under the tray, clear of every screw and pocket, so the underside is open to view
RAILS = [box("post", x - 3, x + 3, y - 3, y + 3, ZP_TOP - 30, ZP_TOP - 0.2, 'rail', ROOT) for x, y in [(30.0, 14.0), (30.0, 104.0), (150.0, 58.0)]]
for r in RAILS:
    show(r, [(1, S(CARRY[0]))])

nuts = []
for k, (x, y, d) in FIXINGS.items():
    nuts.append(hexa("nut-" + k, x, y, Z_TRAY - 2.4, Z_TRAY - 0.4, 5.0, 'nut', ROOT))
for i, (x, y) in enumerate(EARS):                          # M3: 5.5 across flats, 2.4 thick
    nuts.append(hexa("nut-E%d" % (i + 1), x, y, Z_TRAY - 2.6, Z_TRAY - 0.2, 5.5, 'nut', ROOT))
for o, t in zip(nuts, NUTS):
    drop(o, t, dz=28.0)

# the Bauer 50 W, from the seller's drawing and the photo (2026-10-05): 64 x 57 x 22 mm, corners chamfered 8 x 6.5, two 6.8 mm holes
# INSIDE the outline (5 mm from each end, 26 mm from the leads edge), a raised central plateau with three ridges, two fins each side
# of it running the full length with round bosses on the outer ones, and the four leads leaving through the middle of one long edge.
# The leads edge is put on the vehicle's left (plate y 89). Body coordinates: dx along the vehicle, dy from the right edge (y 32).
bx0, bx1, by0, by1, bh = BAUER
CHX, CHY = 8.0, 6.5


def bp(dx, dy):
    return (bx0 + dx, by0 + dy)


def ins(dy):                                              # how far the chamfer cuts into a fin at dy
    e = min(dy, 57.0 - dy)
    return max(0.0, CHX * (CHY - e) / CHY)


bau = empty("bauer", ROOT)
outline = [bp(CHX, 0), bp(64 - CHX, 0), bp(64, CHY), bp(64, 57 - CHY), bp(64 - CHX, 57), bp(CHX, 57), bp(0, 57 - CHY), bp(0, CHY)]
SHELF = 4.0
shelf = prism("bauer-shelf", outline, Z_TRAY, Z_TRAY + SHELF, 'bauer', bau)
cutters = []
for (dx, dy) in [(5.0, 31.0), (59.0, 31.0)]:               # 26 mm from the leads edge = 31 mm from the right edge
    x, y = bp(dx, dy)
    m = Mesh(ID)
    m.cyl((x, y, Z_TRAY - 1), (x, y, Z_TRAY + 5), 3.4, 'bauer', 28)
    m.cyl((x, y, Z_TRAY + 2.5), (x, y, Z_TRAY + 5), 5.0, 'bauer', 32)
    cutters.append(m.make("ear-cut"))
bpy.ops.object.select_all(action='DESELECT')
for c in cutters:
    c.select_set(True)
bpy.context.view_layer.objects.active = cutters[0]
bpy.ops.object.join()
cut = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = shelf
md = shelf.modifiers.new("ears", 'BOOLEAN')
md.object, md.operation, md.solver = cut, 'DIFFERENCE', 'EXACT'
bpy.ops.object.modifier_apply(modifier="ears")
bpy.data.objects.remove(cut)
m = Mesh(ID)
x0, y0 = bp(13.4, 0)
m.box(x0, bx0 + 50.6, y0, by0 + 57, Z_TRAY, Z_TRAY + 19, 'bauer')                          # the central plateau, full width
for dy in (0.8, 56.2):                                                                      # a thin wall along each edge of it
    x0, y0 = bp(7.0, dy - 0.8)
    m.box(x0, bx0 + 57.0, y0, y0 + 1.6, Z_TRAY, Z_TRAY + 22, 'bauerfin')
for dy in (6.5, 13.3, 43.7, 50.5):                                                          # two fins each side, full length
    i = ins(dy)
    x0, y0 = bp(i, dy - 0.9)
    m.box(x0, bx0 + 64 - i, y0, y0 + 1.8, Z_TRAY + SHELF, Z_TRAY + 22, 'bauerfin')
for dy in (20.6, 28.1, 35.6):                                                               # three thin ridges on the plateau
    x0, y0 = bp(17.0, dy - 0.4)
    m.box(x0, bx0 + 47.0, y0, y0 + 0.8, Z_TRAY + 19, Z_TRAY + 20, 'bauerfin')
for (dx, dy) in [(20.7, 6.5), (43.1, 6.5), (20.7, 50.5), (43.1, 50.5)]:                     # round bosses on the outer fins
    x, y = bp(dx, dy)
    m.cyl((x, y, Z_TRAY + 22), (x, y, Z_TRAY + 23.3), 1.9, 'bauerfin', 16)
x, y = bp(31.9, 28.0)
m.cyl((x, y, Z_TRAY + 20), (x, y, Z_TRAY + 21.3), 1.9, 'bauerfin', 16)                      # and one on the middle ridge
# a black grommet in the leads edge, middle of the plateau; four leads: yellow, black, black, red
gx, gy = bp(24.0, 57.0)
m.box(gx, gx + 18.0, gy, gy + 2.6, Z_TRAY + 6, Z_TRAY + 13, 'lead_k')
m.make("bauer-body", bau)
LEADS = [('lead_y', 27.0), ('lead_k', 31.0), ('lead_k', 35.0), ('lead_r', 39.0)]
for i, (col, dxl) in enumerate(LEADS):
    cu = bpy.data.curves.new("lead", 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = '3D', 1.1, 3, True
    sp = cu.splines.new('POLY')
    xl = bx0 + dxl
    yl = 93.5 + i * 1.9                                    # fanned across the 12 mm lane beside the Bauer
    pts = [(xl, by1 + 2.6, Z_TRAY + 9.5), (xl, by1 + 4.5, Z_TRAY + 8.5), (xl + 3.0, yl, Z_TRAY + 4.0), (xl + 9.0, yl + 1.0, Z_TRAY + 1.3),
           (xl + 24.0, yl + 1.0, Z_TRAY + 1.3), (84.0, yl + 1.0, Z_TRAY + 1.3)]
    sp.points.add(len(pts) - 1)
    for p_, co in zip(sp.points, pts):
        p_.co = B(*co) + (1,)
    lw = bpy.data.objects.new("lead", cu)
    lw.data.materials.append(MATS[col])
    sc.collection.objects.link(lw)
    lw.parent = bau
drop(bau, BAUER_T, dz=40.0)
for i, (x, y) in enumerate(EARS):                          # M3 x 8 through each of the Bauer's own holes into its nut
    sh = empty("ear-screw", ROOT)
    cyl("head", x, y, Z_TRAY + 2.5, Z_TRAY + 4.5, 5.5, 'steel', sh, 20)
    cyl("shaft", x, y, Z_TRAY - 2.2, Z_TRAY + 2.5, 3.0, 'steel', sh, 12)
    drop(sh, EARSCREW_T + 0.5 * i, dz=26.0, dur=0.7)

# the boards, as built (carrier_model.py), each on four nylon standoffs
asm = {'AB': empty("boards-AB", ROOT), 'C': empty("board-C", ROOT)}
zA = Z_TRAY + 8 + 1.6
zC = Z_TRAY + 8 + 1.6
CM.build_ab(asm['AB'], zA)
CM.build_c(asm['C'], zC)
screws_at = []
for k, (x0, x1, y0, y1, hs) in BOARDS.items():
    grp = asm['C'] if k == 'C' else asm['AB']
    zb = Z_TRAY + hs
    for (x, y) in [(x0 + CORNER_INSET, y0 + CORNER_INSET), (x1 - CORNER_INSET, y0 + CORNER_INSET),
                   (x0 + CORNER_INSET, y1 - CORNER_INSET), (x1 - CORNER_INSET, y1 - CORNER_INSET)]:
        hexa("standoff-" + k, x, y, Z_TRAY, zb, 5.0, 'nylon', grp)
        screws_at.append((x, y, zb))
drop(asm['C'], BOARD_T['C'], dz=45.0, dur=1.0)
drop(asm['AB'], BOARD_T['AB'], dz=45.0, dur=1.0)

for i, (x, y, zb) in enumerate(screws_at):                     # M2.5 x 12, heads in the counterbores
    s = empty("screw", ROOT)
    cyl("head", x, y, ZP_TOP, ZP_TOP + 2.0, 4.6, 'steel', s, 16)
    cyl("shaft", x, y, ZP_TOP + 2.0, zb - 1.0, 2.5, 'steel', s, 12)
    drop(s, SCREWS_T + 0.28 * i, dz=-24.0, dur=0.55)

for i, (x0, x1, y0, y1) in enumerate(SPLICES):
    sp = box("splice-s%d" % (6 + i), x0, x1, y0, y1, Z_TRAY, Z_TRAY + 8.5, 'splice', ROOT)
    drop(sp, SPLICE_T[i], dz=25.0)

# the discovery
disco = empty("discovery-root", ROOT)                     # drop() moves this; the board keeps its own height inside it
CM.build_discovery(disco, zA).name = "discovery"
drop(disco, DISCO[0], dz=45.0, dur=DISCO[1] - DISCO[0])

# lifted across, set down on plate 2, then it rides plate 2 down
move(ROOT, [(0, (0, BENCH_Y, LIFT)), (CARRY[0], (0, BENCH_Y, LIFT)), (CARRY[0] + 1.6, (0, BENCH_Y, LIFT + 45)),
            (CARRY[1] - 2.2, (0, 0, LIFT + 45)), (CARRY[1], (0, 0, LIFT)), (LOWER[0], (0, 0, LIFT)), (LOWER[1], (0, 0, 0))])
move(P2, [(0, (0, 0, LIFT)), (LOWER[0], (0, 0, LIFT)), (LOWER[1], (0, 0, 0))])

# ---------------------------------------------------------------- plate-2 side: wires, screws (children of PLATE2)
for i, (col, ya) in enumerate([('red', 49.0), ('blk', 64.0)]):
    cu = bpy.data.curves.new("w", 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = '3D', 1.0, 3, True
    sp = cu.splines.new('POLY')
    pts = [(112.4, ya, ZP_BOT - 16.0), (112.4, ya, ZP_BOT + 2.0), (112.4, ya, Z_TRAY + 3.0), (109.5, ya - 1.0, Z_TRAY + 9.0),
           (104.0, SPLICES[i][2] + 6.5, Z_TRAY + 11.0), (104.0, SPLICES[i][2] + 6.5, Z_TRAY + 4.5)]
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = B(*co) + (1,)
    w = bpy.data.objects.new("wire", cu)
    w.data.materials.append(MATS[col])
    sc.collection.objects.link(w)
    w.parent = P2
    drop(w, WIRES_T + 0.5 * i, dz=-20.0, dur=1.2)

for (k, (x, y, d)), t in zip(FIXINGS.items(), FIX_T):
    s = empty("fix-" + k, P2)
    if d > 3.0:                                           # a washer only in the M3 holes (MEC-11)
        cyl("washer", x, y, ZP_BOT - 0.5, ZP_BOT, 6.0, 'steel', s, 20)
    cyl("head", x, y, ZP_BOT - 2.5, ZP_BOT - 0.5, 4.6, 'steel', s, 16)
    cyl("shaft", x, y, ZP_BOT, Z_TRAY - 0.9, 2.5, 'steel', s, 12)
    drop(s, t, dz=-28.0, dur=0.7)


# ---------------------------------------------------------------- the cutaway through one fixing (a separate model)
SEC_AT = (-170.0, -60.0, 90.0)
SEC = empty("section", loc=B(*SEC_AT))


def sec_cyl(name, z0, z1, d, material, n=48):
    m = Mesh(ID)
    m.cyl((0, 0, z0), (0, 0, z1), d / 2, material, n)
    return m.make(name, SEC)


def sec_hex(name, z0, z1, af, material):
    m = Mesh(ID)
    m.cyl((0, 0, z0), (0, 0, z1), af / math.cos(math.radians(30)) / 2, material, 6)
    return m.make(name, SEC)


def boolean(obj, cutter, op='DIFFERENCE'):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new("b", 'BOOLEAN')
    mod.object, mod.operation, mod.solver = cutter, op, 'EXACT'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter)


def halfcut(obj):
    """Remove the half on the camera's side of the axis, leaving a cut face to look at."""
    m = Mesh(ID)
    m.box(-30, 30, -30, 0, -40, 60, 'steel')                  # layout y < 0 is Blender +y, away from the camera
    boolean(obj, m.make("half", SEC))
    for pp in obj.data.polygons:
        pp.use_smooth = False


R = 11.0
parts_sec = []
o = sec_cyl("sec-plate", -2.0, 0.0, 2 * R, 'plate')
boolean(o, sec_cyl("h", -3, 1, 2.71, 'steel', 24))
parts_sec.append(o)
o = sec_cyl("sec-tray", 0.0, T, 2 * R, 'tray')
boolean(o, sec_cyl("h", -1, 5, 2.8, 'steel', 24))
boolean(o, sec_hex("p", T - 2.4, T + 1, 5.2, 'steel'))
parts_sec.append(o)
o = sec_hex("sec-nut", T - 2.4, T - 0.4, 5.0, 'nut')
boolean(o, sec_cyl("h", T - 3, T + 1, 2.5, 'steel', 16))
parts_sec.append(o)
parts_sec.append(sec_cyl("sec-bauer", T, T + 14, 2 * R, 'bauer'))
sp_screw = empty("sec-screw", SEC)
for nm, z0, z1, d in [("head", -4.5, -2.5, 4.6), ("shaft", -2.5, T - 0.9, 2.5), ("washer", -2.5, -2.0, 6.0)]:
    c = sec_cyl("sec-" + nm, z0, z1, d, 'steel', 24)
    c.parent = sp_screw
    parts_sec.append(c)
for o in parts_sec:
    halfcut(o)
for o in [p for p in parts_sec if p.parent is SEC]:
    show(o, [(S(SECTION[0]), S(SECTION[1]))])
f0 = S(SECTION[0] + 0.6)
sp_screw.location = (0, 0, -22)
sp_screw.keyframe_insert("location", frame=f0)
sp_screw.location = (0, 0, 0)
sp_screw.keyframe_insert("location", frame=f0 + S(1.6))
show(sp_screw, [(S(SECTION[0]), S(SECTION[1]))])
lab_mat = mat('seclabel', (0.95, 0.95, 0.95, 1))
for text, z in [("Bauer 50 W", 9.0), ("nut in its pocket", 3.9), ("tray, 4 mm", 1.4), ("plate 2, 2 mm", -1.2), ("M2.5 screw", -3.6)]:
    cu = bpy.data.curves.new(text, 'FONT')
    cu.body, cu.size, cu.align_x = text, 1.3, 'LEFT'
    cu.materials.append(lab_mat)
    lo = bpy.data.objects.new('lab-' + text, cu)
    lo.parent = SEC
    lo.location = (-(R + 2.5), 0, z - 0.5)
    lo.rotation_euler = (math.pi / 2, 0, math.pi)
    sc.collection.objects.link(lo)
    show(lo, [(S(SECTION[0] + 1.6), S(SECTION[1]))])
bgm = Mesh(ID)
bgm.box(-60, 60, 25, 28, -40, 50, 'sec_bg')
show(bgm.make("section-backdrop", SEC), [(S(SECTION[0]), S(SECTION[1]))])

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

JIG = (105.0, BENCH_Y - 58.0, LIFT + 60.0)                # the tray on the jig, centre (Blender coordinates)
JIG_U = (105.0, BENCH_Y - 58.0, LIFT + 50.0)              # looking up at its underside
PL2 = (105.0, -58.0, LIFT + 60.0)
SECC = (SEC_AT[0] - 9.0, -SEC_AT[1], SEC_AT[2] + 3.0)   # a little to the right of the stack, so the labels fit
KEYS = [(0.0, (-60.0, BENCH_Y + 150.0, LIFT + 250.0), JIG),
        (4.0, (60.0, BENCH_Y + 175.0, LIFT + 230.0), JIG),
        (7.2, (60.0, BENCH_Y + 175.0, LIFT + 230.0), JIG),
        (7.9, (-25.0, 5.0, LIFT + 130.0), (50.0, BENCH_Y - 62.0, LIFT + 66.0)),
        (10.2, (-25.0, 5.0, LIFT + 130.0), (50.0, BENCH_Y - 62.0, LIFT + 66.0)),
        (10.9, (60.0, BENCH_Y + 175.0, LIFT + 230.0), JIG),
        (13.5, (60.0, BENCH_Y + 175.0, LIFT + 230.0), JIG),
        (14.2, (100.0, BENCH_Y + 150.0, LIFT - 60.0), JIG_U),
        (18.6, (100.0, BENCH_Y + 150.0, LIFT - 60.0), JIG_U),
        (19.6, (60.0, BENCH_Y + 175.0, LIFT + 230.0), JIG),
        (22.0, (60.0, BENCH_Y + 175.0, LIFT + 230.0), JIG),
        (23.4, (-80.0, 290.0, LIFT + 250.0), (110.0, 35.0, LIFT + 60.0)),
        (27.2, (-80.0, 290.0, LIFT + 250.0), (110.0, 35.0, LIFT + 60.0)),
        (28.0, (100.0, -20.0, LIFT + 330.0), (105.0, -58.0, LIFT + 54.0)),
        (29.4, (100.0, -20.0, LIFT + 330.0), (105.0, -58.0, LIFT + 54.0)),
        (30.4, (85.0, 110.0, 20.0), (85.0, -53.0, 108.0)),
        (36.6, (85.0, 110.0, 20.0), (85.0, -53.0, 108.0)),
        (37.0, (SECC[0] - 6.0, SECC[1] + 44.0, SECC[2] + 10.0), SECC),
        (41.4, (SECC[0] - 6.0, SECC[1] + 44.0, SECC[2] + 10.0), SECC),
        (42.2, (-20.0, 190.0, 190.0), (110.0, -58.0, 85.0)),
        (46.4, (10.0, 205.0, 215.0), (115.0, -58.0, 62.0)),
        (49.8, (10.0, 205.0, 215.0), (115.0, -58.0, 62.0))]
for sec, c, t in KEYS:
    f = S(sec)
    cam.location, target.location = c, t
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
for i in range(0, 12):                                    # orbit the finished carrier
    f = S(ORBIT) + i * S(0.55)
    a = math.radians(125 - i * 24)
    cam.location = (115 + 260 * math.cos(a), -58 + 260 * math.sin(a), 150 - i * 3)
    target.location = (115, -58, 62)
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions: above the player's controls, scaled with the lens so they stay one size on screen
holder = empty("caption-holder", cam)
for sec, lens in [(29.6, 32.0), (30.4, 24.0), (36.6, 24.0), (37.0, 32.0)]:
    cam.data.lens = lens
    cam.data.keyframe_insert("lens", frame=S(sec))
    holder.scale = (32.0 / lens, 32.0 / lens, 1.0)
    holder.keyframe_insert("scale", frame=S(sec))
band_mat = bpy.data.materials.new("caption-band")
band_mat.diffuse_color = (0.02, 0.02, 0.03, 0.78)
bpy.ops.mesh.primitive_plane_add(size=1)
bo = bpy.context.active_object
bo.name = "caption-band"
bo.data.materials.append(band_mat)
bo.parent = holder
bo.location = (0, -4.85, -20.05)
bo.scale = (24, 1.3, 1)
white = mat('caption', (0.97, 0.97, 0.97, 1))
for (a, b), text in CAPTIONS:
    a, b = S(a), min(S(b), END + 1)
    cu = bpy.data.curves.new("cap", 'FONT')
    cu.body = text
    cu.size = 0.5
    t = bpy.data.objects.new("cap", cu)
    t.data.materials.append(white)
    sc.collection.objects.link(t)
    t.parent = holder
    t.location = (-10.7, -4.95, -20)
    show(t, [(a, b)])

# ---------------------------------------------------------------- render
sc.frame_start, sc.frame_end = 1, END
sc.render.fps = FPS
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.color_type, sh.light = 'MATERIAL', 'STUDIO'
sh.show_cavity = False
sh.show_object_outline = True
sh.object_outline_color = (0.08, 0.09, 0.1)
sh.show_specular_highlight = False
sh.use_world_space_lighting = False
sh.background_type = 'VIEWPORT'
sh.background_color = (0.17, 0.18, 0.2)
sc.world = bpy.data.worlds.new("bench")
sc.world.color = (0.17, 0.18, 0.2)
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
