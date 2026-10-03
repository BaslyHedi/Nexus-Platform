"""Assembly animation of the harness-board sandwich (MEC-16), rendered by Blender.

    python3 plate1.py && python3 make-assembly.py      # the model it animates
    blender -b -P animate-assembly.py                   # -> assembly-animation.mp4, 36 s
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
STAY = ("P1_battery", "P1_driver", "P1_tire", "P1_run01a", "P1_run04a", "P1_sm2p-female", "P1_drop-")
PLATE2_CAD = ("obj36_", "obj146_", "obj147_", "obj148_", "obj149_", "FASCIA_LOWER")
DECK3 = ("DECK3", "FASCIA_UPPER")

FPS = 24
SPEED = 2                    # the timeline is written in seconds and plays SPEED times faster
S = lambda sec: int(round(sec * FPS / SPEED)) + 1

# when each part goes onto the upturned plate 2 (seconds), in MEC-16's order
PARTS = [("P1_bus-", 3.0), ("P1_fuse-main", 4.4), ("P1_fuse-motor", 5.6), ("P1_fuse-ubec", 6.8),
         ("P1_ina226", 8.2), ("P1_split-sw1", 9.6), ("P1_ubec", 11.0), ("P1_splice-s1", 12.4),
         ("P1_splice-s2", 13.4), ("P1_splice-s4", 14.2), ("P1_splice-s3", 15.2), ("P1_splice-s5", 16.0),
         ("FASCIA_LOWER", 20.5), ("P1_sw1", 21.6), ("P1_sw2", 21.6)]
# S6 and S7 are on plate 2's TOP face, beside the Bauer, which faces the floor while
# plate 2 lies open: a drop-in would push them through the plate. Like the Bauer and
# the carrier, they are simply there from the start.
DROP_IN = S(0.8) - 1         # how long a part takes to settle onto the face
WIRES = (S(24), S(42))       # every run grows in this window, in run order
GROW = S(1.2) - 1
FLIP = (S(45), S(51))        # over the top, lifting LIFT mm
LOWER = (S(52.5), S(56))     # held a moment at the top, then down onto the standoffs
PLUGS = S(57)
DECK3_IN = (S(60), S(63))
END = S(72)

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

# ---- wires grow, run by run
runs = sorted((o for o in meshes if o.name.startswith("P1_run") and on_plate2(o)), key=lambda o: o.name)
step = (WIRES[1] - WIRES[0]) / max(1, len(runs))
for i, o in enumerate(runs):
    mod = o.modifiers.new("grow", 'BUILD')
    mod.frame_start = WIRES[0] + i * step
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
KEYS = [(0, (-140, -430, 390), (-95, 5, 25)),
        (2.0, (-150, -250, 250), (-165, 0, 15)),
        (23.0, (-140, -210, 230), (-168, 5, 15)),
        (42.5, (-150, -250, 250), (-165, 0, 15)),
        (44.5, (-140, -430, 390), (-95, 5, 25)),
        (49.0, (-420, -330, 300), (-40, 0, 60)),
        (57.5, (-330, -300, 180), (0, 10, 50))]
for sec, c, t in KEYS:
    f = S(sec)
    cam.location, target.location = c, t
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)
for i in range(0, 17):                      # orbit from the front-right round the rear
    f = S(60) + i * S(0.75)
    a = math.radians(-130 + i * 11)
    cam.location = (360 * math.cos(a), 360 * math.sin(a), 210 - i * 2)
    target.location = (0, 10, 55)
    cam.keyframe_insert("location", frame=f)
    target.keyframe_insert("location", frame=f)

# ---- captions, riding with the camera
white = bpy.data.materials.new("caption")
white.diffuse_color = (0.95, 0.95, 0.95, 1)
CAPTIONS = [((0, 3), "Plate 2 upside down beside the chassis - pack and driver already on plate 1"),
            ((3, 20.5), "1  Parts onto plate 2 with 3M foam tape: buses, fuses, INA226, split, UBEC, splices"),
            ((20.5, 23.5), "2  The lower rear panel with SW1 / SW2 held to plate 2"),
            ((23.5, 44.5), "3  Wire the whole harness on the bench"),
            ((44.5, 56.8), "4  Flip plate 2 and the panel over, lower onto the standoffs"),
            ((56.8, 60), "5  From the right side: driver VM plug, fuses in, SM-2P last"),
            ((60, 73), "6  Plate 3 and the upper panel close the stack (MEC-16)")]
band_mat = bpy.data.materials.new("caption-band")
band_mat.diffuse_color = (0.02, 0.02, 0.03, 0.72)
bpy.ops.mesh.primitive_plane_add(size=1)
band = bpy.context.active_object
band.name = "caption-band"
band.data.materials.append(band_mat)
band.parent = cam
band.location = (0, -5.62, -20.05)          # just behind the text, across the frame
band.scale = (24, 1.25, 1)
for (a, b), text in CAPTIONS:
    a, b = S(a), min(S(b), END + 1)
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
sc.render.fps = FPS
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
