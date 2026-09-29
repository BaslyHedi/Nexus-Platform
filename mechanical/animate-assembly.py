"""Assembly animation of the harness-board sandwich (MEC-16), rendered by Blender.

    python3 plate1.py && python3 make-assembly.py      # the model it animates
    blender -b -P animate-assembly.py                   # -> assembly-animation.mp4
    blender -b -P animate-assembly.py -- --preview      # quarter size, every 4th frame

It follows MEC-16's build steps: plate 2 lies upside down beside the chassis, its parts
go on one by one and the wires grow run by run, the lower fascia panel with the
switches joins it, plate 2 flips over, lowers onto its standoffs, the two plugs go in,
and plate 3 closes the stack. Parts are the assembly's own groups (P1_* from plate1.py,
the chassis from Hiwonder's CAD); the two wires that cross between the decks come from
plate1/states/, one mesh per position.

The hinge is the one plate1.plate2_move() uses: 180 deg about a line along the
vehicle's right side (vehicle X -85, Z 50.56). The flip goes over the top, so plate 2
never passes through the chassis.
"""
import bpy, math, os, sys
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, "chassis-3deck-fascia.obj")
STATES = os.path.join(HERE, "plate1", "states")
OUT = os.path.join(HERE, "assembly-animation.mp4")
PREVIEW = "--preview" in sys.argv
PIVOT = Vector((-85.0, 0.0, 50.56))
LIFT = 60.0

# what stays on plate 1; everything else of ours rides on plate 2
STAY = ("P1_battery", "P1_driver", "P1_run01a", "P1_run04a", "P1_sm2p-female", "P1_drop-")
PLATE2_CAD = ("obj36_", "obj146_", "obj147_", "obj148_", "obj149_", "FASCIA_LOWER")
DECK3 = ("DECK3", "FASCIA_UPPER")

# when each part goes onto the upturned plate 2 (frame), in MEC-16's order
PARTS = [("P1_bus-", 30), ("P1_fuse-main", 44), ("P1_fuse-motor", 52), ("P1_fuse-ubec", 60),
         ("P1_ina226", 70), ("P1_split-sw1", 80), ("P1_ubec", 88), ("P1_splice-s1", 96),
         ("P1_splice-s2", 101), ("P1_splice-s4", 104), ("P1_splice-s3", 109), ("P1_splice-s5", 112),
         ("P1_splice-s6", 117), ("P1_splice-s7", 120), ("FASCIA_LOWER", 130), ("P1_sw1", 138),
         ("P1_sw2", 138)]
WIRES = (150, 255)          # every run grows in this window, in run order
FLIP = (285, 360)           # over the top, lifting LIFT mm
LOWER = (372, 410)
PLUGS = 420
DECK3_IN = (440, 490)
END = 600

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
            f = f - 5 if n.endswith("-tape") else f
            show(o, [(f, END + 1)])
            o.location = (0, 0, -40 if not n.startswith(("FASCIA", "P1_sw")) else -25)
            o.keyframe_insert("location", frame=f)
            o.location = (0, 0, 0)
            o.keyframe_insert("location", frame=f + 8)
            break

# ---- wires grow, run by run
runs = sorted((o for o in meshes if o.name.startswith("P1_run") and on_plate2(o)), key=lambda o: o.name)
step = (WIRES[1] - WIRES[0]) / max(1, len(runs))
for i, o in enumerate(runs):
    mod = o.modifiers.new("grow", 'BUILD')
    mod.frame_start = WIRES[0] + i * step
    mod.frame_duration = 14

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
import_state("raised", (LOWER[0], LOWER[0] + 2))     # a glimpse at the top of the lowering

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
KEYS = [(1, (-140, -430, 390), (-95, 5, 25)),
        (26, (-150, -250, 250), (-165, 0, 15)),
        (150, (-140, -210, 230), (-168, 5, 15)),
        (262, (-150, -250, 250), (-165, 0, 15)),
        (284, (-140, -430, 390), (-95, 5, 25)),
        (330, (-420, -330, 300), (-40, 0, 60)),
        (430, (-330, -300, 180), (0, 10, 50))]
for f, c, t in KEYS:
    cam.location, target.location = c, t
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
for i in range(0, 17):                      # orbit from the front-right round the rear
    f = 440 + i * 10
    a = math.radians(-130 + i * 11)
    cam.location = (360 * math.cos(a), 360 * math.sin(a), 210 - i * 2)
    target.location = (0, 10, 55)
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions, riding with the camera
white = bpy.data.materials.new("caption")
white.diffuse_color = (0.95, 0.95, 0.95, 1)
CAPTIONS = [((1, 28), "Plate 2 upside down beside the chassis - pack and driver already on plate 1"),
            ((28, 128), "1  Parts onto plate 2 with 3M foam tape: buses, fuses, INA226, split, UBEC, splices"),
            ((128, 150), "2  The lower rear panel with SW1 / SW2 held to plate 2"),
            ((150, 285), "3  Wire the whole harness on the bench"),
            ((285, 415), "4  Flip plate 2 and the panel over, lower onto the standoffs"),
            ((415, 440), "5  From the right side: driver VM plug, fuses in, SM-2P last"),
            ((440, END + 1), "6  Plate 3 and the upper panel close the stack (MEC-16)")]
for (a, b), text in CAPTIONS:
    cu = bpy.data.curves.new("cap", 'FONT')
    cu.body = text
    cu.size = 0.52
    t = bpy.data.objects.new("cap", cu)
    t.data.materials.append(white)
    sc.collection.objects.link(t)
    t.parent = cam
    t.location = (-10.6, -5.8, -20)       # 20 mm in front of the lens: nothing gets closer
    show(t, [(a, b)])

# ---- render
sc.frame_start, sc.frame_end = 1, END
sc.render.fps = 24
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.color_type, sh.light = 'MATERIAL', 'STUDIO'
sh.show_cavity = sh.show_object_outline = True
sh.background_type = 'VIEWPORT'
sh.background_color = (0.16, 0.17, 0.19)
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
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
