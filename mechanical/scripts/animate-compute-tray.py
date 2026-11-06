"""Assembly animation of the compute tray (MEC-18), rendered by Blender.

    openscad -D 'PART="tray"' -o ../cad/compute-tray.stl ../cad/compute-tray.scad   # the tray it animates
    blender -b -P animate-compute-tray.py                   # -> ../renders/compute-tray-animation.mp4  (1080p)
    blender -b -P animate-compute-tray.py -- --preview      # half size, every 4th frame
    blender -b -P animate-compute-tray.py -- --still 20     # one PNG at 20 s, for checking a moment

The order of work (a PROPOSAL, MEC-18). The tray is built up at a bench: a nut into each of the 14 pockets, the FRDM on its
six metal standoffs, four screws from below through the counterbores, then (a later phase) the Pi 5 on four standoffs. The unit
is carried to plate 3, which is held 60 mm clear of its standoffs, so the 14 fixing screws can go in from below; plate 3 then
lowers onto the chassis. Last, the three cables of the BOM reach the FRDM: J1 power, J11 console, J7 CAN.

Read from disk: ../cad/compute-tray.stl and ../cad/carrier-tray.stl (the two trays), ../cad/plate3-data.scad (plate 3's outline,
holes and slots, exported from the layout drawing). Stand-ins: the FRDM's connectors (positions read off NXP's Quick Start Guide, +-1 mm,
heights guessed), the Pi 5 (indicative), the boards and the Bauer on plate 2, the fascia port.

Coordinates: plate 3's layout frame (x front to rear, y from the vehicle's right, mm, z up from plate 1's underside).
The layout's y runs the wrong way for a right-handed frame, so a point goes to Blender as (x, -y, z).
"""
import bpy, bmesh, math, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blender_compat import fcurves, mp4                              # noqa: E402
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
from carrier_model import Mesh, Frame, MATS, mat, empty        # noqa: E402

CAD = os.path.join(HERE, "..", "cad")
RENDERS = os.path.join(HERE, "..", "renders")
OUT = os.path.join(RENDERS, "compute-tray-animation.mp4")
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PREVIEW = "--preview" in ARGS
STILL = float(ARGS[ARGS.index("--still") + 1]) if "--still" in ARGS else None

FPS = 24
S = lambda sec: int(round(sec * FPS)) + 1
TOTAL = 84.0
END = S(TOTAL)

# ---------------------------------------------------------------- the design (mirrors compute-tray.scad)
T = 4.0
Z3_BOT, Z3_TOP = 121.12, 123.12                  # plate 3
Z2_BOT, Z2_TOP = 79.12, 81.12                    # plate 2
Z1_BOT, Z1_TOP = 27.12, 29.12                    # plate 1
LIFT = 60.0                                      # plate 3 is worked on this far above its standoffs
BENCH_Y = 190.0                                  # the bench stands this far to the vehicle's right (Blender +y)
FX0, FY0, FL, FW = 184.0, 6.75, 95.0, 65.0       # the FRDM: footprint x, y of its corner, long edge (along y), short edge
FRDM_STANDOFF, PI_STANDOFF = 6.0, 8.0
PX0, PY0, PL, PW = 94.0, 17.75, 85.0, 56.0       # the Pi 5
CB_DEPTH = 2.4                                   # counterbore for an M2.5 head, from below
FIX = [(17.82, 53.24, 3.18), (17.82, 67.24, 3.18), (49.0, 35.94, 2.71), (49.0, 84.53, 2.71), (86.94, 40.23, 2.71), (86.94, 80.23, 2.71),
       (120.06, 35.94, 2.71), (120.06, 84.53, 2.71), (143.47, 52.65, 2.71), (143.47, 67.88, 2.71),
       (196.88, 38.76, 3.18), (196.88, 81.77, 3.18), (245.88, 38.76, 3.18), (245.88, 81.77, 3.18)]


def frdm_at(u, v):
    return (FX0 + FW - v, FY0 + u)


def pi_at(a, b):
    return (PX0 + PW - b, PY0 + a)


FRDM_SCREWS = [frdm_at(u, v) for u in (3.5, 52.5) for v in (3.5, 61.5)]
PI_HOLES = [pi_at(a, b) for a in (3.5, 61.5) for b in (3.5, 52.5)]

# ---------------------------------------------------------------- timeline (seconds)
T_NUTS = 6.5                                     # first nut, 0.36 s apart
T_FRDM = 14.0
T_FSCREW = 18.4                                  # four screws from below
T_PISTAND = 24.0
T_PISCREW_LO = 26.0
T_PI = 28.5
T_PISCREW_HI = 31.0
CARRY = (34.0, 38.5, 41.5)                       # lift, across, set down
T_FIXSCREW = 44.0                                # fourteen, 0.5 s apart
T_UNBLOCK = 55.0
LOWER = (56.5, 61.0)
T_J1, T_J11, T_J7 = 63.0, 68.0, 73.0
ORBIT = 78.0
DROP = S(0.7) - 1

CAPTIONS = [
    ((0, 6.5), "The compute tray, 236.6 x 108 x 4 mm PETG: spare pad, Pi 5, plug gap, FRDM"),
    ((6.5, 14), "1  A nut into each of the 14 hex pockets: eight M2.5, six M3"),
    ((14, 18.4), "2  The FRDM-IMX91S on its six 6 mm metal standoffs: four for screws, two just stand"),
    ((18.4, 24), "3  Four M2.5 x 6 from below, each head in its counterbore"),
    ((24, 28.5), "4  Later: four 8 mm standoffs for the Pi 5, a screw from below into each"),
    ((28.5, 34), "5  The Pi 5 lowers on, ports to the vehicle's left; four M2.5 x 6 from above"),
    ((34, 41.5), "The unit is carried to plate 3: every fixing hole lands on a plate hole"),
    ((41.5, 55), "6  Fourteen screws from below, a washer under each: six M3 x 8, eight M2.5 x 8"),
    ((55, 56.5), "The blocks come out"),
    ((56.5, 62), "7  Plate 3, tray and boards lower onto the four chassis standoffs"),
    ((62, 67.5), "8  J1 power: the 20 cm C-to-C from board C, up the slot, along the edge to J1"),
    ((67.5, 72.5), "9  J11 console: the 20 cm USB-C extension from the fascia, round the left edge"),
    ((72.5, 78), "10  J7 CAN: the 2x5 lead from board B, up the cross-slot, onto J7"),
    ((78, 84), "17 mm beside the USB plugs, a 34 mm plug gap for J1, the nose pad free to drill"),
]

# ---------------------------------------------------------------- materials
sc = bpy.context.scene
for n, c, a in [('plate', '#8793a1', 1), ('plate1', '#64748b', 0.35), ('plate2', '#8793a1', 0.55), ('standoff', '#cbd5e1', 1), ('tray', '#eceff3', 1),
                ('steel', '#a3aab4', 1), ('brass', '#c8a24a', 1), ('nut', '#f2c230', 1), ('screwc', '#9aa3ad', 1), ('recess', '#2b3038', 1),
                ('washer', '#c7ccd3', 1), ('blk', '#111827', 1), ('rail', '#475569', 1), ('block', '#64748b', 1),
                ('pcb', '#171c26', 1), ('pcb_g', '#1e7f45', 1), ('hdr', '#2f5bd3', 1), ('hdr_k', '#1c1f26', 1), ('pin', '#d9b24a', 1),
                ('metal', '#c4c8ce', 1), ('metal_d', '#8a9099', 1), ('port', '#0e1218', 1), ('led', '#34d058', 1), ('tan', '#c8a778', 1),
                ('red_s', '#d73a3a', 1), ('mod', '#146b3a', 1), ('chip', '#0d0f12', 1), ('spreader', '#b8bec7', 1), ('sdslot', '#b0b6bf', 1),
                ('hole', '#07090c', 1), ('ring', '#d4a52c', 1), ('white', '#f1f5f9', 1),
                ('carrier', '#3b5b8c', 0.55), ('bauer', '#2f353d', 0.6), ('cable_r', '#d63030', 1), ('cable_b', '#2563eb', 1),
                ('cable_g', '#16a34a', 1), ('fascia', '#a8b4c4', 0.35), ('port_body', '#9ca3af', 0.85), ('sec_bg', '#1b1f24', 1)]:
    mat(n, c, a)
ID = Frame(lambda X, Y, Z: (X, -Y, Z), proper=False)                       # plate layout coordinates -> Blender
FR = Frame(lambda u, v, z: (FX0 + FW - v, -(FY0 + u), z), proper=False)    # the FRDM's own frame (u, v) -> Blender
PF = Frame(lambda a, b, z: (PX0 + PW - b, -(PY0 + a), z), proper=False)    # the Pi's own frame (a, b) -> Blender


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


def hexa(m, x, y, z0, z1, af, material):
    m.cyl((x, y, z0), (x, y, z1), af / 2 / math.cos(math.radians(30)), material, 6)


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
        for fc in fcurves(t.animation_data.action):
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


def cable(name, pts, material, r=1.6, parent=None):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = '3D', r, 4, True
    sp = cu.splines.new('NURBS')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = B(*q) + (1,)
    sp.order_u = 4
    sp.use_endpoint_u = True
    cu.materials.append(MATS[material])
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def text(body, loc, size, material='white', rot=(0, 0, 0), parent=None, align='CENTER'):
    cu = bpy.data.curves.new(body, 'FONT')
    cu.body, cu.size, cu.align_x, cu.align_y = body, size, align, 'CENTER'
    cu.materials.append(MATS[material])
    o = bpy.data.objects.new('lab-' + body, cu)
    o.location, o.rotation_euler = loc, rot
    sc.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def screw(name, x, y, z_head, d, dir_up, shank, head_d, head_h, material='screwc', washer=None, parent=None):
    """A pan-head screw with a cross recess, head at z_head, shank going up (dir_up) or down. Washer = (od, thickness) under the head."""
    m = Mesh(ID)
    s = 1 if dir_up else -1
    zz = z_head
    if washer:
        od, th = washer
        m.cyl((x, y, zz), (x, y, zz + s * th), od / 2, 'washer', 20)
        m.cyl((x, y, zz + s * th * 0.98), (x, y, zz + s * th * 1.02), d * 0.62, 'recess', 12)
        zz += s * th
    m.cyl((x, y, zz), (x, y, zz - s * head_h), head_d / 2, material, 20)                       # head, away from the shank
    zt = zz - s * head_h
    m.box(x - head_d * 0.34, x + head_d * 0.34, y - 0.2, y + 0.2, zt - s * 0.05 - 0.2, zt - s * 0.05 + 0.2, 'recess')
    m.box(x - 0.2, x + 0.2, y - head_d * 0.34, y + head_d * 0.34, zt - s * 0.05 - 0.2, zt - s * 0.05 + 0.2, 'recess')
    m.cyl((x, y, zz), (x, y, zz + s * shank), d / 2, material, 14)
    return m.make(name, parent)


def nutmesh(name, x, y, z0, z1, af, parent=None):
    m = Mesh(ID)
    hexa(m, x, y, z0, z1, af, 'nut')
    m.cyl((x, y, z1 - 0.05), (x, y, z1 + 0.02), af * 0.3, 'recess', 14)
    return m.make(name, parent)


# ---------------------------------------------------------------- the vehicle: plates, standoffs
data = open(os.path.join(CAD, "plate3-data.scad"), encoding="utf-8").read()
PD = {k: json.loads(v) for k, v in re.findall(r"(\w+) = (\[.*?\]);", data, re.S)}
OUTLINE, HOLES, SLOTS = [tuple(p) for p in PD['OUTLINE']], PD['HOLES'], PD['SLOTS']
STANDS = [tuple(p) for p in PD['STANDOFFS']]
CLAMPS = [tuple(p) for p in PD['CLAMPS']]

prism("plate1", OUTLINE, Z1_BOT, Z1_TOP, 'plate1')
prism("plate2", OUTLINE, Z2_BOT, Z2_TOP, 'plate2')
for (x, y) in STANDS:
    m = Mesh(ID)
    hexa(m, x, y, Z1_TOP, Z2_BOT, 6.0, 'standoff')               # lower gap, 50 mm
    hexa(m, x, y, Z2_TOP, Z3_BOT, 6.0, 'standoff')               # upper gap, 40 mm
    m.cyl((x, y, Z3_BOT), (x, y, Z3_BOT + 4.5), 1.9, 'metal_d', 12)       # the male thread through plate 3
    m.make("chassis-standoff")

P3 = empty("PLATE3", loc=(0, 0, LIFT))
plate3 = prism("plate3", OUTLINE, Z3_BOT, Z3_TOP, 'plate', P3)
cutters = []
for (x, y, d) in HOLES:
    m = Mesh(ID)
    m.cyl((x, y, Z3_BOT - 1), (x, y, Z3_TOP + 1), d / 2, 'plate', 16)
    cutters.append(m.make("c"))
for (x, y, w, h) in SLOTS:
    cutters.append(prism("c", rrect_poly(x, x + w, y, y + h, min(w, h) / 2, 6), Z3_BOT - 1, Z3_TOP + 1, 'plate'))
bpy.ops.object.select_all(action='DESELECT')
for o in cutters:
    o.select_set(True)
bpy.context.view_layer.objects.active = cutters[0]
bpy.ops.object.join()
cutter = bpy.context.view_layer.objects.active
mod = plate3.modifiers.new("holes", 'BOOLEAN')
mod.object, mod.operation, mod.solver = cutter, 'DIFFERENCE', 'EXACT'
bpy.context.view_layer.objects.active = plate3
bpy.ops.object.modifier_apply(modifier="holes")
bpy.data.objects.remove(cutter)
bm = bmesh.new()                                                   # a face with a hundred holes in it renders black from below: triangulate
bm.from_mesh(plate3.data)
bmesh.ops.triangulate(bm, faces=bm.faces)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(plate3.data)
for p_ in plate3.data.polygons:
    p_.use_smooth = False
bm.free()
for (x, y) in CLAMPS:                                              # the fascia upper panel's clamp holes, M3
    m = Mesh(ID)
    m.cyl((x, y, Z3_TOP), (x, y, Z3_TOP + 0.2), 3.4, 'ring', 20)
    m.make("clamp", P3)

# plate 3 rests on four blocks until it is lowered
BLOCKS = [box("block", x - 6, x + 6, y - 6, y + 6, Z2_TOP, Z3_BOT + LIFT - 0.1, 'block') for x, y in [(60.0, 34.0), (60.0, 86.0), (225.0, 22.0), (225.0, 98.0)]]
for o in BLOCKS:
    show(o, [(1, S(T_UNBLOCK))])

# ---- plate 2 and what is on it: the carrier tray (MEC-17), boards A, B, C, the Bauer 50 W, board C's USB-C socket
bpy.ops.wm.stl_import(filepath=os.path.join(CAD, "carrier-tray.stl"))
ctray = bpy.context.selected_objects[0]
ctray.name = "carrier-tray"
ctray.location = (8.50, -5.11, Z2_TOP)
for p in ctray.data.polygons:
    p.use_smooth = False
ctray.data.materials.append(MATS['tray'])
for n, (x0, x1, y0, y1, h) in {'A': (117.00, 187.00, 5.11, 55.11, 8), 'B': (119.54, 189.54, 60.99, 110.99, 8), 'C': (85.50, 115.50, 25.20, 95.20, 8)}.items():
    box("board-" + n, x0, x1, y0, y1, Z2_TOP + T + h, Z2_TOP + T + h + 1.6, 'carrier')
box("bauer", 11.0, 75.0, 32.0, 89.0, Z2_TOP + T, Z2_TOP + T + 22, 'bauer')
box("discovery", 117.0, 215.0, 14.0, 98.0, Z2_TOP + T + 14, Z2_TOP + T + 16.6, 'carrier')
SOCK_C = (100.0, 22.0, Z2_TOP + T + 8 + 2.5)                     # board C's USB-C socket, facing the vehicle's right
box("socket-C", 96.0, 106.0, 12.0, 25.2, SOCK_C[2] - 2.6, SOCK_C[2] + 2.6, 'metal')

# the fascia's USB-C port (MEC-13): its 40 mm body ends at x 225.7, y 41.3, z 101
box("fascia-wall", 266.9, 269.9, 20.0, 100.0, Z2_TOP, Z3_BOT, 'fascia')
box("fascia-usbc-body", 225.7, 266.0, 41.3 - 7.0, 41.3 + 7.0, 101.0 - 3.75, 101.0 + 3.75, 'port_body')

# ---------------------------------------------------------------- the unit, built at the bench
ROOT = empty("UNIT")
ROOT.location = (0, BENCH_Y, LIFT)
bpy.ops.wm.stl_import(filepath=os.path.join(CAD, "compute-tray.stl"))
tray = bpy.context.selected_objects[0]
tray.name = "compute-tray"
tray.parent = ROOT
tray.location = (0, 0, Z3_TOP)
for p in tray.data.polygons:
    p.use_smooth = False
tray.data.materials.append(MATS['tray'])
ZT = Z3_TOP + T                                                    # the tray's top face

# the bench: three posts under the tray's underside, clear of every screw
RAILS = [box("post", x - 3, x + 3, y - 3, y + 3, Z3_TOP - 30, Z3_TOP - 0.2, 'rail', ROOT) for x, y in [(30.0, 40.0), (30.0, 82.0), (125.0, 12.0), (125.0, 108.0), (215.0, 106.0)]]
for r in RAILS:
    show(r, [(1, S(CARRY[0]))])

# ---- 1  the nuts (M3: 5.5 across flats, 2.6 thick; M2.5: 5.0, 2.4)
nuts = []
for i, (x, y, d) in enumerate(FIX):
    af, th = (5.5, 2.6) if d > 3 else (5.0, 2.4)
    nuts.append(nutmesh("nut-%d" % (i + 1), x, y, ZT - th, ZT - 0.2, af, ROOT))
for i, o in enumerate(nuts):
    drop(o, T_NUTS + 0.36 * i, dz=26.0)

# ---- 2  the FRDM-IMX91S on its standoffs (built in its own frame: u along the long edge, v along the short one)
FB = empty("FRDM", ROOT)
zf = ZT + FRDM_STANDOFF                                            # the board's underside
m = Mesh(FR)
m.box(0, FL, 0, FW, zf, zf + 1.6, 'pcb')
for (u, v) in [(3.5, 3.5), (3.5, 61.5), (52.5, 3.5), (52.5, 61.5), (FL - 4.0, 3.5), (FL - 4.0, 61.5)]:
    m.cyl((u, v, zf + 1.6), (u, v, zf + 1.65), 2.4, 'ring', 18)
    m.cyl((u, v, zf + 1.65), (u, v, zf + 1.7), 1.4, 'hole', 14)
top = zf + 1.6
m.box(0.5, 6.0, 7.0, 59.0, top, top + 8.5, 'hdr')                                  # 40-pin header, blue housing
for k in range(20):
    for row in (2.0, 4.6):
        m.box(row - 0.3, row + 0.3, 7.0 + 1.3 + k * 2.54 - 0.3, 7.0 + 1.3 + k * 2.54 + 0.3, top + 8.5, top + 11.5, 'pin')
m.box(60.5, 73.5, 1.8, 7.3, top, top + 8.5, 'hdr_k')                               # J7, 2x5 NXP header
for k in range(5):
    for row in (3.2, 5.8):
        m.box(62.2 + k * 2.54 - 0.3, 62.2 + k * 2.54 + 0.3, row - 0.3, row + 0.3, top + 8.5, top + 11.5, 'pin')
m.box(27.0, 47.0, 1.0, 6.0, top, top + 2.0, 'tan')                                  # 30-pin FPC
m.box(27.0, 47.0, 0.4, 1.0, top, top + 2.6, 'hdr_k')
for k in range(3):
    m.box(75.0 + k * 4.5, 78.5 + k * 4.5, 3.0, 6.5, top, top + 3.0, 'red_s' if k == 2 else 'metal_d')    # USER / ONOFF / RESET
m.box(58.5, 64.5, 17.0, 24.0, top, top + 3.0, 'hdr')                                # boot switch
m.box(13.0, 24.0, 6.0, 20.5, top, top + 1.8, 'mod')                                  # IW610 module
m.box(15.0, 22.0, 9.0, 16.0, top + 1.8, top + 2.4, 'metal')
m.box(17.0, 34.0, 25.0, 42.0, top, top + 1.4, 'chip')                                # i.MX 91
m.box(19.0, 32.0, 27.0, 40.0, top + 1.4, top + 1.6, 'spreader')
m.box(36.0, 46.0, 28.0, 38.0, top, top + 1.2, 'chip')                                # LPDDR4
m.box(46.0, 54.0, 17.0, 23.0, top, top + 1.0, 'chip')                                # NAND
m.box(18.0, 22.0, 46.0, 50.0, top, top + 0.8, 'chip')
# the USB group on the u-max edge, hanging 1.8 mm over it: J11 DBG, USB-C, USB-A
for v0, v1 in [(10.3, 18.8), (27.0, 36.0)]:
    m.box(89.0, FL + 0.8, v0, v1, top, top + 3.3, 'metal')
    m.box(90.0, FL + 0.9, v0 + 1.1, v1 - 1.1, top + 0.9, top + 2.4, 'port')
m.box(81.5, FL + 1.8, 43.0, 56.5, top, top + 6.5, 'metal')                          # USB-A
m.box(82.5, FL + 1.9, 44.2, 55.3, top + 1.0, top + 3.0, 'port')
m.box(82.5, FL + 1.9, 44.2, 55.3, top + 3.0, top + 3.6, 'hdr')
# the v-max edge, hanging 2.5 mm over it: RJ45, J1 power, audio
m.box(60.0, 77.0, 44.0, FW + 2.5, top, top + 13.5, 'metal')                         # RJ45
m.box(62.0, 75.0, FW - 1.0, FW + 2.6, top + 1.5, top + 11.0, 'port')
m.box(62.5, 64.0, FW + 2.4, FW + 2.7, top + 9.5, top + 11.0, 'led')
m.box(73.0, 74.5, FW + 2.4, FW + 2.7, top + 9.5, top + 11.0, 'tan')
m.box(30.8, 40.8, 56.8, FW + 1.5, top, top + 3.3, 'metal')                          # J1, USB-C power
m.box(31.8, 39.8, FW - 1.0, FW + 1.6, top + 0.9, top + 2.4, 'port')
m.box(16.0, 23.0, 54.0, FW + 2.0, top, top + 6.0, 'hdr_k')                          # audio jack
m.cyl((19.5, FW + 2.0, top + 3.0), (19.5, FW + 2.4, top + 3.0), 2.4, 'metal_d', 16)
# the underside: the microSD socket opening to the v-0 edge, with a card half in
m.box(29.4, 44.7, -1.0, 14.7, zf - 2.0, zf, 'sdslot')
m.box(31.0, 43.0, -2.0, 6.0, zf - 1.0, zf - 0.4, 'chip')
m.make("frdm-board", FB)
ms = Mesh(FR)                                                                       # the six standoffs, hex 5 across flats
for (u, v) in [(3.5, 3.5), (3.5, 61.5), (52.5, 3.5), (52.5, 61.5), (FL - 4.0, 3.5), (FL - 4.0, 61.5)]:
    hexa(ms, u, v, ZT, zf, 5.0, 'steel')
    ms.cyl((u, v, ZT - 0.01), (u, v, ZT + 0.0), 1.1, 'hole', 10)
ms.make("frdm-standoffs", FB)
for (name, u, v, sz) in [("J1", 35.8, 51.0, 1.7), ("J11", 93.0, 14.5, 1.5), ("USB-C", 93.0, 31.5, 1.5), ("USB-A", 90.0, 50.0, 1.7), ("ETH", 69.0, 56.0, 2.2),
                          ("AUDIO", 19.5, 51.0, 1.5), ("J7 CAN", 67.0, 12.0, 1.7), ("40-pin", 3.3, 33.0, 1.5), ("FPC", 37.0, 9.0, 1.5), ("i.MX 91", 25.5, 33.5, 1.6)]:
    p = frdm_at(u, v)
    rot = (0, 0, math.pi / 2) if name in ("40-pin",) else (0, 0, 0)
    text(name, (p[0], -p[1], top + 0.1 if name not in ("40-pin",) else top + 8.7), sz, 'white', rot, FB)
drop(FB, T_FRDM, dz=44.0, dur=1.4)

# ---- 3  four screws from below, head in the counterbore (M2.5 x 6, head 4.4 x 1.6 against the counterbore's ceiling)
fscr = []
for i, (x, y) in enumerate(FRDM_SCREWS):
    fscr.append(screw("fscrew-%d" % (i + 1), x, y, Z3_TOP + CB_DEPTH, 2.5, True, 6.0, 4.4, 1.6, parent=ROOT))
for i, o in enumerate(fscr):
    drop(o, T_FSCREW + 0.45 * i, dz=-30.0)

# ---- 4  the Raspberry Pi 5 (a later phase): four 8 mm standoffs, then the board
zp = ZT + PI_STANDOFF
PB = empty("PI5", ROOT)
mp = Mesh(PF)
mp.box(0, PL, 0, PW, zp, zp + 1.6, 'pcb_g')
tp = zp + 1.6
mp.box(64.0, 85.0, 2.0, 18.0, tp, tp + 13.5, 'metal')                               # RJ45 (ports on the a = 85 edge)
mp.box(66.0, 85.2, 4.0, 16.0, tp + 1.5, tp + 11.5, 'port')
mp.box(68.0, 85.0, 20.0, 34.0, tp, tp + 16.0, 'metal')                              # two USB stacks
mp.box(68.0, 85.0, 36.0, 50.0, tp, tp + 16.0, 'metal')
for v0 in (22.0, 38.0):
    mp.box(70.0, 85.2, v0, v0 + 10.0, tp + 2.0, tp + 6.0, 'port')
    mp.box(70.0, 85.2, v0, v0 + 10.0, tp + 9.0, tp + 13.0, 'port')
mp.box(8.0, 17.0, 46.0, PW + 0.5, tp, tp + 3.3, 'metal')                            # USB-C power, south edge
mp.box(22.0, 29.5, 46.0, PW + 0.5, tp, tp + 3.2, 'metal')                           # two micro-HDMI
mp.box(34.0, 41.5, 46.0, PW + 0.5, tp, tp + 3.2, 'metal')
mp.box(7.0, 58.0, 0.6, 5.6, tp, tp + 8.5, 'hdr_k')                                  # GPIO header, north edge
for k in range(20):
    for row in (1.9, 4.3):
        mp.box(7.0 + 1.3 + k * 2.54 - 0.3, 7.0 + 1.3 + k * 2.54 + 0.3, row - 0.3, row + 0.3, tp + 8.5, tp + 11.5, 'pin')
mp.box(30.0, 44.0, 20.0, 34.0, tp, tp + 1.6, 'chip')                                # BCM2712 under its heat spreader
mp.box(31.0, 43.0, 21.0, 33.0, tp + 1.6, tp + 2.2, 'spreader')
mp.box(48.0, 58.0, 24.0, 32.0, tp, tp + 1.0, 'chip')
mp.box(3.0, 9.0, 22.0, 32.0, tp, tp + 2.2, 'metal_d')                               # camera / display FFC
for (a, b) in [(3.5, 3.5), (3.5, 52.5), (61.5, 3.5), (61.5, 52.5)]:
    mp.cyl((a, b, tp), (a, b, tp + 0.05), 2.5, 'ring', 18)
mp.box(0, 12, 22, 34, zp - 2.2, zp, 'sdslot')                                      # the microSD socket underneath
mp.make("pi-board", PB)
ps = Mesh(PF)
for (a, b) in [(3.5, 3.5), (3.5, 52.5), (61.5, 3.5), (61.5, 52.5)]:
    hexa(ps, a, b, ZT, zp, 5.0, 'brass')
ps_o = ps.make("pi-standoffs", ROOT)
text("Raspberry Pi 5", (pi_at(30, 10)[0] - 6.0, -pi_at(30, 10)[1], tp + 0.2), 2.6, 'white', (0, 0, 0), PB)
text("later phase", (pi_at(30, 10)[0] - 6.0, -pi_at(30, 10)[1] - 4.0, tp + 0.2), 2.0, 'white', (0, 0, 0), PB)
pscr_lo = [screw("pscrew-lo-%d" % (i + 1), x, y, Z3_TOP + CB_DEPTH, 2.5, True, 6.0, 4.4, 1.6, parent=ROOT) for i, (x, y) in enumerate(PI_HOLES)]
pscr_hi = [screw("pscrew-hi-%d" % (i + 1), x, y, zp + 1.6, 2.5, False, 6.0, 4.4, 1.6, parent=ROOT) for i, (x, y) in enumerate(PI_HOLES)]
drop(ps_o, T_PISTAND, dz=30.0, dur=1.0)
for i, o in enumerate(pscr_lo):
    drop(o, T_PISCREW_LO + 0.4 * i, dz=-30.0)
drop(PB, T_PI, dz=46.0, dur=1.6)
for i, o in enumerate(pscr_hi):
    drop(o, T_PISCREW_HI + 0.4 * i, dz=18.0, dur=0.7)

# ---- 6  the fourteen fixing screws, from below: M3 x 8 with a 7 mm washer, M2.5 x 8 with a 5.5 mm one
fix_scr = []
for i, (x, y, d) in enumerate(FIX):
    if d > 3:
        o = screw("fix-%d" % (i + 1), x, y, Z3_BOT - 0.5 - 2.0, 3.0, True, 8.0 + 2.0 + 0.5, 5.6, 2.0, washer=(7.0, 0.5), parent=ROOT)
    else:
        o = screw("fix-%d" % (i + 1), x, y, Z3_BOT - 0.5 - 1.7, 2.5, True, 8.0 + 1.7 + 0.5, 4.6, 1.7, washer=(5.5, 0.5), parent=ROOT)
    fix_scr.append(o)
for i, o in enumerate(fix_scr):
    drop(o, T_FIXSCREW + 0.5 * i, dz=-34.0, dur=0.8)

# ---------------------------------------------------------------- the carrying and the lowering
move(ROOT, [(0.0, (0, BENCH_Y, LIFT)), (CARRY[0], (0, BENCH_Y, LIFT)), (CARRY[0] + 1.6, (0, BENCH_Y, LIFT + 34)), (CARRY[1], (0, 0, LIFT + 34)),
            (CARRY[2], (0, 0, LIFT)), (LOWER[0], (0, 0, LIFT)), (LOWER[1], (0, 0, 0))])
move(P3, [(0.0, (0, 0, LIFT)), (LOWER[0], (0, 0, LIFT)), (LOWER[1], (0, 0, 0))])
for ob in (ROOT, P3):
    for fc in fcurves(ob.animation_data.action):
        for k in fc.keyframe_points:
            k.interpolation = 'BEZIER'

# ---------------------------------------------------------------- the three cables of the BOM (MEC-18), drawn after the lowering
J1_MOUTH = frdm_at(35.8, FW)
Z_J = Z3_TOP + T + FRDM_STANDOFF + 1.6 + 1.65
c1 = cable("cable-J1", [(100.0, 4.0, SOCK_C[2]), (104.0, 8.0, SOCK_C[2] + 4), (118.0, 12.0, 100.0), (125.0, 12.0, 118.0), (126.0, 12.0, Z3_TOP + 3.0),
                        (150.0, 12.0, Z3_TOP + 4.0), (168.0, 26.0, Z3_TOP + 4.0), (J1_MOUTH[0] - 20.0, J1_MOUTH[1], Z_J), (J1_MOUTH[0] - 3.0, J1_MOUTH[1], Z_J)],
           'cable_r', 1.7, None)
j11 = frdm_at(FL + 18.0, 14.5)
c2 = cable("cable-J11", [(225.7, 41.3, 101.0), (215.0, 80.0, 101.0), (228.0, 121.0, 104.0), (233.0, 126.0, 118.0), (j11[0], j11[1] + 1.0, Z_J + 1.0),
                         (j11[0], frdm_at(FL + 2.0, 14.5)[1], Z_J)], 'cable_b', 1.7, None)
j7 = frdm_at(67.0, 4.5)
c3 = cable("cable-J7", [(190.0, 92.0, Z2_TOP + T + 8 + 1.6 + 2.0), (230.0, 80.0, Z2_TOP + T + 12.0), (262.0, 74.0, Z2_TOP + T + 8.0), (262.5, j7[1], 115.0),
                        (262.5, j7[1], Z3_TOP + 4.0), (255.0, j7[1], Z3_TOP + 8.0), (j7[0] + 6.0, j7[1], Z3_TOP + T + FRDM_STANDOFF + 1.6 + 11.5),
                        (j7[0], j7[1], Z3_TOP + T + FRDM_STANDOFF + 1.6 + 10.0)], 'cable_g', 1.1, None)
grow(c1, T_J1, 4.0)
grow(c2, T_J11, 4.0)
grow(c3, T_J7, 4.0)

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

BEN = (132.0, BENCH_Y - 60.0, LIFT + 126.0)                        # the tray on the bench (Blender coordinates)
K = []
K += [(0.0, (110.0, 470.0, 300.0), (135.0, 50.0, 125.0)), (5.5, (390.0, 400.0, 300.0), (135.0, 50.0, 125.0))]
K += [(6.5, (60.0, BENCH_Y + 150.0, LIFT + 270.0), BEN), (13.5, (180.0, BENCH_Y + 140.0, LIFT + 250.0), BEN)]
K += [(14.2, (300.0, BENCH_Y + 110.0, LIFT + 225.0), (216.0, BENCH_Y - 55.0, LIFT + 128.0)), (18.0, (300.0, BENCH_Y + 110.0, LIFT + 225.0), (216.0, BENCH_Y - 55.0, LIFT + 128.0))]
K += [(18.4, (216.0, BENCH_Y + 80.0, LIFT + 40.0), (216.0, BENCH_Y - 35.0, LIFT + 126.0)), (23.6, (216.0, BENCH_Y + 80.0, LIFT + 40.0), (216.0, BENCH_Y - 35.0, LIFT + 126.0))]
K += [(24.3, (110.0, BENCH_Y + 130.0, LIFT + 250.0), (115.0, BENCH_Y - 60.0, LIFT + 130.0)), (25.9, (110.0, BENCH_Y + 130.0, LIFT + 250.0), (115.0, BENCH_Y - 60.0, LIFT + 130.0))]
K += [(26.4, (122.0, BENCH_Y + 100.0, LIFT + 30.0), (122.0, BENCH_Y - 45.0, LIFT + 126.0)), (28.2, (122.0, BENCH_Y + 100.0, LIFT + 30.0), (122.0, BENCH_Y - 45.0, LIFT + 126.0))]
K += [(28.8, (60.0, BENCH_Y + 170.0, LIFT + 250.0), BEN), (33.6, (-10.0, BENCH_Y + 160.0, LIFT + 240.0), BEN)]
K += [(34.6, (-80.0, 330.0, LIFT + 280.0), (140.0, 70.0, LIFT + 100.0)), (38.0, (-80.0, 330.0, LIFT + 280.0), (140.0, 70.0, LIFT + 100.0))]
K += [(38.6, (140.0, 90.0, LIFT + 400.0), (135.0, -58.0, LIFT + 126.0)), (41.4, (140.0, 90.0, LIFT + 400.0), (135.0, -58.0, LIFT + 126.0))]
K += [(42.4, (60.0, 170.0, 125.0), (80.0, -60.0, LIFT + 120.0)), (47.5, (200.0, 170.0, 125.0), (180.0, -60.0, LIFT + 120.0))]
K += [(48.5, (255.0, 120.0, 135.0), (225.0, -60.0, LIFT + 122.0)), (54.4, (255.0, 120.0, 135.0), (225.0, -60.0, LIFT + 122.0))]
K += [(55.4, (-70.0, 250.0, 190.0), (130.0, -58.0, 120.0)), (60.8, (-70.0, 250.0, 190.0), (130.0, -58.0, 120.0))]
K += [(62.2, (60.0, 80.0, 190.0), (130.0, -22.0, 105.0)), (66.8, (180.0, 60.0, 200.0), (160.0, -30.0, 125.0))]
K += [(67.8, (290.0, 190.0, 200.0), (232.0, -90.0, 112.0)), (72.0, (260.0, 190.0, 210.0), (235.0, -100.0, 118.0))]
K += [(72.8, (320.0, 30.0, 200.0), (240.0, -73.0, 120.0)), (77.0, (330.0, 40.0, 215.0), (245.0, -72.0, 124.0))]
for sec, c, t in K:
    f = S(sec)
    cam.location, target.location = c, t
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
for i in range(0, 12):                                    # orbit the finished plate
    f = S(ORBIT) + i * S(0.5)
    a = math.radians(-30 - i * 28)
    cam.location = (135 + 330 * math.cos(a), -58 + 330 * math.sin(a), 190 - i * 4)
    target.location = (135, -58, 118)
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions: above the player's controls, scaled with the lens so they stay one size on screen
holder = empty("caption-holder", cam)
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
for (a, b), body in CAPTIONS:
    a, b = S(a), min(S(b), END + 1)
    cu = bpy.data.curves.new("cap", 'FONT')
    cu.body = body
    cu.size = 0.42
    t = bpy.data.objects.new("cap", cu)
    t.data.materials.append(white)
    sc.collection.objects.link(t)
    t.parent = holder
    t.location = (-10.4, -4.95, -20)
    show(t, [(a, b)])

# ---------------------------------------------------------------- render
sc.frame_start, sc.frame_end = 1, END
sc.render.fps = FPS
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.color_type, sh.light = 'MATERIAL', 'STUDIO'
sh.studio_light = ARGS[ARGS.index("--light") + 1] if "--light" in ARGS else 'paint.sl'      # lights the undersides too; the default studio light leaves them black
sh.show_cavity = True
sh.cavity_type = 'BOTH'
sh.cavity_ridge_factor, sh.cavity_valley_factor = 1.2, 1.0
sh.show_shadows = True
sh.shadow_intensity = 0.32
sc.display.render_aa = '8'
sh.show_object_outline = True
sh.object_outline_color = (0.06, 0.07, 0.08)
sh.show_specular_highlight = True
sh.use_world_space_lighting = False
sh.background_type = 'VIEWPORT'
sh.background_color = (0.24, 0.26, 0.29)
sc.world = bpy.data.worlds.new("bench")
sc.world.color = (0.24, 0.26, 0.29)
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
if STILL is not None:
    sc.frame_set(S(STILL))
    sc.render.resolution_percentage = 60 if "--small" in ARGS else 100
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = os.path.join(RENDERS, f"compute-tray-still-{STILL:g}.png")
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
