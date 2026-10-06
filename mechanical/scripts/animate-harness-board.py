"""Assembly animation of the harness-board sandwich (MEC-16), rendered by Blender.

    python3 plate1.py && python3 make-assembly.py      # the model it animates
    blender -b -P animate-harness-board.py                   # -> ../renders/harness-board-animation.mp4, about 1 min 20 s
    blender -b -P animate-harness-board.py -- --preview      # quarter size, every 4th frame

It follows MEC-16's build steps: plate 2 lies upside down beside the chassis, its parts
go on one by one and the wires grow run by run, the lower fascia panel with the
switches joins it, plate 2 flips over, lowers onto its standoffs, the two plugs go in,
and plate 3 closes the stack. Every part and every wire run has its own caption (what it
is, which connector it ends in), and the camera goes to where it is. Parts are the assembly's own groups (P1_* from plate1.py,
the chassis from Hiwonder's CAD); the two wires that cross between the decks come from
plate1/states/, one mesh per position.

The hinge is the one plate1.plate2_move() uses: 180 deg about a line along the
vehicle's right side (vehicle X -85, Z 50.56). The flip goes over the top, so plate 2
never passes through the chassis.
"""
import bpy, math, os, sys
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(HERE, "..", "cad")
OBJ = os.path.join(CAD, "chassis-3deck-fascia.obj")
STATES = os.path.join(CAD, "plate1", "states")
OUT = os.path.join(HERE, "..", "renders", "harness-board-animation.mp4")
PREVIEW = "--preview" in sys.argv
PIVOT = Vector((-85.0, 0.0, 50.56))
LIFT = 60.0

# what stays on plate 1; everything else of ours rides on plate 2
STAY = ("P1_battery", "P1_driver", "P1_tire", "P1_run01a", "P1_run04a", "P1_sm2p-female", "P1_drop-")
PLATE2_CAD = ("obj36_", "obj146_", "obj147_", "obj148_", "obj149_", "FASCIA_LOWER")
DECK3 = ("DECK3", "FASCIA_UPPER")

FPS = 24
SPEED = 2                    # the timeline is written in seconds and plays SPEED times faster
S = lambda sec: int(round(sec * FPS / SPEED)) + 1

# when each part goes onto the upturned plate 2 (seconds), in MEC-16's order
PARTS = [("P1_bus-", 3.0), ("P1_fuse-main", 4.4), ("P1_fuse-motor", 5.6), ("P1_fuse-ubec", 6.8),
         ("P1_ina226", 8.2), ("P1_split-sw1", 9.6), ("P1_ubec", 11.0), ("P1_splice-s1", 12.4),
         ("P1_splice-s2", 13.4), ("P1_splice-s4", 14.2), ("P1_splice-s3", 15.2), ("P1_splice-s5", 16.0), ("P1_splice-s8", 16.8), ("P1_splice-s9", 17.6),
         ("FASCIA_LOWER", 20.5), ("P1_sw1", 21.6), ("P1_sw2", 21.6)]
# S6 and S7 are on plate 2's TOP face, beside the Bauer, which faces the floor while
# plate 2 lies open: a drop-in would push them through the plate. Like the Bauer and
# the carrier, they are simply there from the start.
DROP_IN = S(0.8) - 1         # how long a part takes to settle onto the face

# the wire runs, in building order: key, where the camera goes (layout x, y), then two caption lines.
# Names after the BOM / MEC-16: "bus" is a genuine WAGO 221-415, "splice" and "split" are DOMAXWILL
# lever clips (the 221 look-alike kit, BOM 3.13), "tab" is a 4.8 mm flag receptacle on the switch.
RUN_SEQ = [
    ("run01b", (90, 30), "Wire 1  SM-2P male (+)  to  splice S1", "18 AWG red  -  DOMAXWILL 2-port lever clip"),
    ("run01c", (90, 28), "Wire 2  S1  to  main fuse (7.5 A)", "the holder's own 16 AWG lead, into the same 2-port clip"),
    ("run02",  (125, 55), "Wire 3  main fuse  to  INA226 VIN+", "16 AWG red  -  ferrule, screw terminal"),
    ("run03",  (120, 60), "Wire 4  INA226 VIN-  to  (+) bus, port 1", "18 AWG red  -  ferrule at the module, WAGO 221-415 lever"),
    ("run04b", (115, 50), "Wire 5  SM-2P male (-)  to  (-) bus, port 5", "18 AWG black  -  WAGO 221-415 lever"),
    ("run05",  (150, 62), "Wire 6  (+) bus, port 2  to  S8, the switch feed", "18 AWG red  -  WAGO lever, DOMAXWILL 3-port clip toward the rear"),
    ("run06a", (170, 66), "Wire 7  S8  to  SW1 contact", "the switch's own green wire  -  3-port clip"),
    ("run06b", (170, 66), "Wire 8  S8  to  SW2 contact", "the switch's own green wire  -  same 3-port clip"),
    ("run07a", (205, 55), "Wire 9  SW1 contact out (green)  to  S9", "3-port clip beside the SW1 split"),
    ("run07b", (205, 50), "Wire 10  SW1 LED (+) (red)  to  S9", "thin LED wire, same clip: it is live only when SW1 is on"),
    ("run07c", (190, 50), "Wire 11  S9  to  the SW1 split", "18 AWG orange  -  into the split's second port"),
    ("run08a", (190, 45), "Wire 12  split  to  motor fuse (5 A)", "16 AWG orange  -  the holder's lead, 3-port clip"),
    ("run08b", (170, 35), "Wire 13  motor fuse  to  splice S2", "16 AWG orange  -  DOMAXWILL 2-port lever clip"),
    ("run08c", (160, 40), "Wire 14  driver VM (+) lead  to  S2", "18 AWG orange  -  second wire in the same 2-port clip"),
    ("run12a", (160, 40), "Wire 15  driver VM (-) lead  to  splice S4", "18 AWG black  -  DOMAXWILL 2-port lever clip"),
    ("run12b", (145, 45), "Wire 16  S4  to  (-) bus, port 3", "18 AWG black  -  WAGO 221-415 lever"),
    ("run09a", (190, 85), "Wire 17  split  to  UBEC fuse (5 A)", "16 AWG orange  -  the holder's lead, 3-port clip"),
    ("run09b", (150, 105), "Wire 18  UBEC fuse  to  splice S3", "16 AWG orange  -  DOMAXWILL 2-port lever clip, under S5"),
    ("run09c", (140, 108), "Wire 19  UBEC (+) input lead  to  S3", "18 AWG orange  -  second wire in the same 2-port clip"),
    ("run11a", (140, 108), "Wire 20  UBEC (-) input lead  to  S5", "18 AWG black  -  DOMAXWILL 5-port clip"),
    ("run11b", (140, 85), "Wire 21  S5  to  (-) bus, port 4", "18 AWG black  -  WAGO 221-415 lever"),
    ("run13a", (150, 92), "Wire 22  SW1 LED (-) (black)  to  S5", "thin LED wire  -  the 5-port clip, with the UBEC return"),
    ("run13b", (150, 92), "Wire 23  SW2 LED (-) (black)  to  S5", "thin LED wire  -  same clip: one more (-) bus port stays free"),
    ("run10a", (110, 80), "Wire 24  UBEC 6 V (+)  to  carrier board A", "18 AWG teal  -  up through plate 2's opening, screw terminal"),
    ("run10b", (110, 80), "Wire 25  UBEC 6 V (-)  to  carrier board A", "18 AWG black  -  up through plate 2's opening, screw terminal"),
    ("run15a", (90, 85), "Wire 26  SW2 contact out (green)  to  S6", "to the tray: up the left slot, 3-port clip beside the Bauer"),
    ("run15c", (80, 95), "Wire 27  SW2 LED (+) (red)  to  S6", "thin LED wire  -  same clip: live only when SW2 is on"),
    ("run15b", (60, 100), "Wire 28  Bauer red lead  to  S6", "18 AWG orange  -  third wire in the 3-port clip"),
    ("run16a", (60, 40), "Wire 29  Bauer black lead  to  splice S7", "18 AWG black  -  DOMAXWILL 2-port lever clip"),
    ("run16b", (110, 40), "Wire 30  S7  to  (-) bus, port 1", "18 AWG black  -  WAGO 221-415 lever"),
]
WIRE_SEC = 2.2               # time each run takes, script seconds
W0 = 28.0                    # wiring starts
W1 = W0 + WIRE_SEC * len(RUN_SEQ)
WIRES = (S(W0), S(W1))       # every run grows in this window, in run order
GROW = S(1.6) - 1
FLIP = (S(W1 + 3), S(W1 + 9))            # over the top, lifting LIFT mm
LOWER = (S(W1 + 10.5), S(W1 + 14))       # held a moment at the top, then down onto the standoffs
PLUGS = S(W1 + 15.5)
DECK3_IN = (S(W1 + 19.5), S(W1 + 22.5))
END = S(W1 + 30)
T_FLIP, T_LOWER_END, T_PLUGS, T_DECK3 = W1 + 3, W1 + 14, W1 + 15.5, W1 + 19.5

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=OBJ, use_split_objects=True, use_split_groups=True,
                      forward_axis='Y', up_axis='Z')
sc = bpy.context.scene
for m in bpy.data.materials:              # the workbench reads the viewport colour
    b = m.node_tree.nodes.get("Principled BSDF") if m.use_nodes else None
    if b:
        c = b.inputs["Base Color"].default_value
        m.diffuse_color = (c[0], c[1], c[2], b.inputs["Alpha"].default_value)

meshes = [o for o in sc.objects if o.type == 'MESH']


def on_plate2(o):
    n = o.name
    if n.startswith("P1_"):
        return not n.startswith(STAY)
    return n.startswith(PLATE2_CAD)


def show(o, frames):
    """Visible only inside the given (start, end) frame windows."""
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=1)
    for a, b in frames:
        o.hide_render = False
        o.keyframe_insert("hide_render", frame=a)
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=b)
    for fc in o.animation_data.action.fcurves:
        for k in fc.keyframe_points:
            k.interpolation = 'CONSTANT'


# ---- the hinge: plate 2 and everything on it
hinge = bpy.data.objects.new("hinge", None)
sc.collection.objects.link(hinge)
hinge.location = PIVOT
hinge.rotation_euler = (0, math.pi, 0)
for o in meshes:
    if on_plate2(o):
        o.parent = hinge
        o.matrix_parent_inverse = Matrix.Translation(-PIVOT)
hinge.keyframe_insert("rotation_euler", frame=FLIP[0])
hinge.keyframe_insert("location", frame=FLIP[0])
hinge.rotation_euler = (0, 2 * math.pi, 0)      # the long way round: over the top
hinge.location = PIVOT + Vector((0, 0, LIFT))
hinge.keyframe_insert("rotation_euler", frame=FLIP[1])
hinge.keyframe_insert("location", frame=FLIP[1])
hinge.keyframe_insert("location", frame=LOWER[0])
hinge.location = PIVOT
hinge.keyframe_insert("location", frame=LOWER[1])

# ---- parts go on one by one, dropping onto the face (plate 2's -Z, which is up while open)
for o in meshes:
    n = o.name
    if not n.startswith("P1_") and not n.startswith("FASCIA_LOWER"):
        continue
    for prefix, f in PARTS:
        if n.startswith(prefix):
            f = S(f)
            f = f - S(0.5) + 1 if n.endswith("-tape") else f
            show(o, [(f, END + 1)])
            o.location = (0, 0, -40 if not n.startswith(("FASCIA", "P1_sw")) else -25)
            o.keyframe_insert("location", frame=f)
            o.location = (0, 0, 0)
            o.keyframe_insert("location", frame=f + DROP_IN)
            break

# ---- wires grow, run by run, in RUN_SEQ order
by_key = {o.name[3:].split('-')[0]: o for o in meshes if o.name.startswith("P1_run") and on_plate2(o)}
assert set(by_key) == {k for k, *_ in RUN_SEQ}, set(by_key) ^ {k for k, *_ in RUN_SEQ}
for i, (key, *_r) in enumerate(RUN_SEQ):
    mod = by_key[key].modifiers.new("grow", 'BUILD')
    mod.frame_start = S(W0 + i * WIRE_SEC)
    mod.frame_duration = GROW

# ---- the two crossing wires: tails while open, hanging while lowering, plugged when closed
for o in meshes:
    if o.name.startswith("P1_drop-"):
        show(o, [(PLUGS, END + 1)])


def import_state(state, window):
    d = os.path.join(STATES, state)
    for f in sorted(os.listdir(d)):
        bpy.ops.wm.stl_import(filepath=os.path.join(d, f))
        o = bpy.context.selected_objects[0]
        n = f[:-4]
        m = "connector" if n.endswith("-plug") else (
            "wire_orange" if "vm-plus" in n else ("wire_red" if "plus" in n else "wire_black"))
        o.data.materials.append(bpy.data.materials[m])
        show(o, [window])


import_state("open", (WIRES[1], FLIP[0]))
import_state("raised", (FLIP[1], LOWER[0] + 1))      # while it is held at the top

# ---- plate 3 and the upper panel come down last
for o in meshes:
    if o.name.startswith(DECK3):
        show(o, [(DECK3_IN[0], END + 1)])
        o.location = (0, 0, 90)
        o.keyframe_insert("location", frame=DECK3_IN[0])
        o.location = (0, 0, 0)
        o.keyframe_insert("location", frame=DECK3_IN[1])

# ---- camera: over the bench, then round the car
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
def bench(lx, ly, d=1.0):
    """Camera and target over a spot of plate 2's lower face while it lies open beside the chassis
    (the hinge turns layout (x, y, z) into assembly (-112.2 - y, x - 138.4, 72 - z))."""
    t = (-112.2 - ly, lx - 138.4 - 28 * d, 24)       # a little toward the camera, so the subject sits above the caption band
    return (t[0] + 30 * d, t[1] - 150 * d, t[2] + 165 * d), t


KEYS = [(0, (-140, -430, 390), (-95, 5, 25)), (2.0, *bench(150, 60, 1.3))]
KEYS += [(W0 + i * WIRE_SEC - 0.4, *bench(*(xy), 0.75)) for i, (_k, xy, *_r) in enumerate(RUN_SEQ)]
KEYS += [(T_FLIP - 0.5, *bench(150, 60, 1.3)),
         (T_FLIP + 1.5, (-140, -430, 390), (-95, 5, 25)),
         (T_FLIP + 6, (-420, -330, 300), (-40, 0, 60)),
         (T_LOWER_END + 1.5, (-330, -300, 180), (0, 10, 50))]
for sec, c, t in KEYS:
    f = S(sec)
    cam.location, target.location = c, t
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
for i in range(0, 17):                      # orbit from the front-right round the rear
    f = S(T_DECK3) + i * S(0.75)
    a = math.radians(-130 + i * 11)
    cam.location = (360 * math.cos(a), 360 * math.sin(a), 210 - i * 2)
    target.location = (0, 10, 55)
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions, riding with the camera: a heading line and a detail line
white = bpy.data.materials.new("caption")
white.diffuse_color = (0.95, 0.95, 0.95, 1)
grey = bpy.data.materials.new("caption-detail")
grey.diffuse_color = (0.72, 0.84, 1.0, 1)
CAPTIONS = [((0, 3), "Plate 2 upside down beside the chassis", "pack and driver already on plate 1; the two buses, fuses and splices come from the BOM"),
            ((3.0, 4.4), "1  Both WAGO 221-415 buses, levers down", "(+) bus uses 2 of 5 ports, (-) bus 4 of 5 - the star ground (HW-06)"),
            ((4.4, 5.6), "2  Main fuse holder, 7.5 A", "flat on the face, lid to the side, 3M foam tape"),
            ((5.6, 6.8), "3  Motor fuse holder, 5 A", "its leads reach the driver's splice"),
            ((6.8, 8.2), "4  UBEC fuse holder, 5 A", "lid to the left side"),
            ((8.2, 9.6), "5  INA226 current sensor, upside down", "terminals face plate 2's opening"),
            ((9.6, 11.0), "6  SW1 split: DOMAXWILL 3-port lever clip", "one switched feed becomes the motor and UBEC fuses"),
            ((11.0, 12.4), "7  UBEC (servo supply), jumper set to 6 V first", "35 x 12 x 5 mm, potted - foam tape only"),
            ((12.4, 13.4), "8  Splice S1: SM-2P (+) to the main fuse", "DOMAXWILL 2-port lever clip"),
            ((13.4, 14.2), "9  Splice S2: motor fuse to the driver's VM (+)", "DOMAXWILL 2-port lever clip"),
            ((14.2, 15.2), "10  Splice S4: driver VM (-)", "stacked under S2"),
            ((15.2, 16.0), "11  Splice S3: UBEC fuse to the UBEC (+) input", "DOMAXWILL 2-port lever clip"),
            ((16.0, 16.8), "12  Splice S5: a DOMAXWILL 5-port clip", "UBEC (-), the run to the (-) bus, and both switch LED returns; S3 hangs under it"),
            ((16.8, 17.6), "13  Splice S8: a 3-port clip toward the rear", "one (+) bus port feeds both switches"),
            ((17.6, 20.5), "14  Splice S9: a 3-port clip beside the SW1 split", "S6 (3-port) and S7 for the Bauer already sit on the carrier tray (MEC-17)"),
            ((20.5, 23.5), "15  The lower rear panel, with SW1 and SW2, held to plate 2", "a temporary M3 x 8 into each captive nut (MEC-07)"),
            ((23.5, W0), "16  Wire the whole harness on the bench", "30 runs; each one ends in a clip, a terminal or a plug - no wire is joined to another without one"),
            ((T_FLIP - 0.5, T_FLIP + 7), "17  Flip plate 2 and the panel over", "nothing crosses the decks yet except the two plugs"),
            ((T_FLIP + 7, T_PLUGS), "18  Lower onto the standoffs", "check nothing is pinched against the pack"),
            ((T_PLUGS, T_DECK3), "19  From the right side: driver VM plug, fuses in, SM-2P last", "the battery connector is the disconnect (HW-08)"),
            ((T_DECK3, T_DECK3 + 13), "20  Plate 3 and the upper panel close the stack", "MEC-16")]
CAPTIONS += [((W0 + i * WIRE_SEC, W0 + (i + 1) * WIRE_SEC), l1, l2) for i, (_k, _xy, l1, l2) in enumerate(RUN_SEQ)]
band_mat = bpy.data.materials.new("caption-band")
band_mat.diffuse_color = (0.02, 0.02, 0.03, 0.88)
bpy.ops.mesh.primitive_plane_add(size=1)
band = bpy.context.active_object
band.name = "caption-band"
band.data.materials.append(band_mat)
band.parent = cam
band.location = (0, -5.3, -20.05)           # just behind the text, across the frame
band.scale = (24, 2.0, 1)
for (a, b), head, detail in CAPTIONS:
    a, b = S(a), min(S(b), END + 1)
    for text, size, y, mat in ((head, 0.52, -4.95, white), (detail, 0.4, -5.85, grey)):
        cu = bpy.data.curves.new("cap", 'FONT')
        cu.body = text
        cu.size = size
        t = bpy.data.objects.new("cap", cu)
        t.data.materials.append(mat)
        sc.collection.objects.link(t)
        t.parent = cam
        t.location = (-10.8, y, -20)          # 20 mm in front of the lens: nothing gets closer
        show(t, [(a, b)])

# ---- render
sc.frame_start, sc.frame_end = 1, END
sc.render.fps = FPS
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.color_type, sh.light = 'MATERIAL', 'STUDIO'
sh.studio_light = 'paint.sl'                                  # lights the undersides too; the default studio light leaves them black
sh.show_cavity = sh.show_object_outline = True
sh.background_type = 'VIEWPORT'
sh.background_color = (0.16, 0.17, 0.19)
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
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
