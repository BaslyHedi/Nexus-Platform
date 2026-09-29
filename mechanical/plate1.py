#!/usr/bin/env python3
"""Plate 1 stand-ins for an eye review - one STL per component and per wire run.

    python3 plate1.py          # writes plate1/*.stl
    python3 make-assembly.py   # adds them to chassis-3deck-fascia.obj, coloured

Every part is a box, a cylinder or a tube at the ASSUMED size recorded in MEC-16.
Nothing here is measured: it exists to see whether the parts and the harness fit
between the decks, not to build from. The positions are the ones in MEC-16 and on
the chassis layout drawing.

Coordinates are written in the LAYOUT frame, the one the chassis layout drawing and
the decisions use: x from the front of plate 1 to the rear, y from the vehicle's
right edge to its left, z up from plate 1's top face. They are mapped once, on
output, into the assembly's frame (the Hiwonder CAD's):

    X = y - 57.8     Y = x - 138.4     Z = z + 29.12

That swap of x and y is a mirror, so every triangle's winding is reversed on output
to keep the normals pointing out. The mapping was checked against the CAD: both
fascia clamp holes and both rear motors land where the drawing has them.

Heights that matter, from the CAD: plate 2's underside is z 50, the rear motors top
out at z 40.8 and the rear wheels at z 44.7. The motors leave 9 mm under plate 2, so
nothing hangs over them; the harness to the switches runs through the 7 mm slot
between the two encoders, on the centreline at y 57-63.
"""
import math, os, struct

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "plate1")

# ---------------------------------------------------------------- materials
# name -> (r, g, b, alpha). make-assembly.py writes these into the .mtl.
MATERIALS = {
    "battery":      (0.16, 0.33, 0.62, 1), "pad":          (0.25, 0.25, 0.25, 1),
    "pcb_driver":   (0.45, 0.20, 0.75, 1), "parts":        (0.35, 0.35, 0.38, 1),
    "connector":    (0.93, 0.93, 0.90, 1), "pcb_ina":      (0.05, 0.45, 0.55, 1),
    "terminal":     (0.10, 0.55, 0.25, 1), "wago":         (0.82, 0.82, 0.82, 1),
    "lever":        (0.95, 0.50, 0.10, 1), "mark_red":     (0.85, 0.10, 0.10, 1),
    "mark_black":   (0.05, 0.05, 0.05, 1), "holder":       (0.10, 0.10, 0.10, 1),
    "fuse_7_5":     (0.55, 0.30, 0.10, 1), "fuse_5":       (0.85, 0.70, 0.45, 1),
    "tie":          (0.97, 0.97, 0.97, 1), "tape": (0.55, 0.55, 0.60, 1), "ubec":         (0.95, 0.80, 0.10, 1),
    "switch":       (0.75, 0.75, 0.78, 1), "bezel_red":    (0.85, 0.10, 0.10, 1),
    "bezel_green":  (0.10, 0.70, 0.20, 1), "placeholder":  (0.85, 0.20, 0.25, 0.55),
    "pcb_carrier":  (0.10, 0.60, 0.30, 0.45), "tire": (0.08, 0.08, 0.09, 1),
    "wire_red":     (0.90, 0.08, 0.08, 1), "wire_orange":  (1.00, 0.55, 0.00, 1),
    "wire_black":   (0.03, 0.03, 0.03, 1), "wire_teal":    (0.00, 0.62, 0.58, 1),
}

AWG18, AWG16, AWG22 = 2.4, 2.9, 1.6          # silicone insulation OD, mm
Z2 = 50.0                                     # plate 2 underside
PLATE2_TOP = 52.0


# ---------------------------------------------------------------- primitives
def box(x0, x1, y0, y1, z0, z1):
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    q = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    t = []
    for a, b, c, d in q:
        t += [(v[a], v[b], v[c]), (v[a], v[c], v[d])]
    return t


def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def _mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _norm(a):
    l = math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)
    return (a[0] / l, a[1] / l, a[2] / l)


def cyl(p0, p1, r, n=16, caps=True):
    """Cylinder from p0 to p1."""
    ax = _norm(_sub(p1, p0))
    ref = (0, 0, 1) if abs(ax[2]) < 0.9 else (1, 0, 0)
    u = _norm(_cross(ax, ref)); w = _cross(ax, u)
    ring = lambda c: [_add(c, _add(_mul(u, r * math.cos(2 * math.pi * i / n)),
                                   _mul(w, r * math.sin(2 * math.pi * i / n)))) for i in range(n)]
    a, b = ring(p0), ring(p1)
    t = []
    for i in range(n):
        j = (i + 1) % n
        t += [(a[i], a[j], b[j]), (a[i], b[j], b[i])]
        if caps:
            t += [(p0, a[j], a[i]), (p1, b[i], b[j])]
    return t


def ball(c, r, n=8):
    t = []
    for i in range(n // 2):
        t0, t1 = math.pi * i / (n // 2), math.pi * (i + 1) / (n // 2)
        for j in range(n):
            p0, p1 = 2 * math.pi * j / n, 2 * math.pi * (j + 1) / n
            pt = lambda th, ph: (c[0] + r * math.sin(th) * math.cos(ph),
                                 c[1] + r * math.sin(th) * math.sin(ph), c[2] + r * math.cos(th))
            a, b, cc, d = pt(t0, p0), pt(t0, p1), pt(t1, p1), pt(t1, p0)
            t += [(a, cc, b), (a, d, cc)]
    return t


def wire(pts, d):
    """A round wire along a polyline, with a ball at every bend."""
    t = []
    for a, b in zip(pts, pts[1:]):
        t += cyl(a, b, d / 2, n=8, caps=False)
    for p in pts:
        t += ball(p, d / 2)
    return t


def revolve(profile, xc, zc, y0, n=72):
    """Solid of revolution about a lateral axis (layout y) through (xc, zc).

    profile: closed polygon of (w, r) - w across the width from y0, r the radius.
    """
    t = []
    ring = lambda w, r, a: (xc + r * math.cos(a), y0 + w, zc + r * math.sin(a))
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        for (w0, r0), (w1, r1) in zip(profile, profile[1:] + profile[:1]):
            p00, p01 = ring(w0, r0, a0), ring(w1, r1, a0)
            p10, p11 = ring(w0, r0, a1), ring(w1, r1, a1)
            t += [(p00, p01, p11), (p00, p11, p10)]
    return t


# ---------------------------------------------------------------- components
PARTS = []            # (name, material, triangles)


def part(name, mat, tris):
    PARTS.append((name, mat, tris))


def holder(name, rating, o, a, n):
    """ATC inline holder lying flat under plate 2, lid to one side.

    o: plan point where the wire axis enters (u = 0), a: unit along the wire axis,
    n: unit towards the lid. 50 long with boots, body 18 x 18, lid 12 more, so
    30 across in plan and 18 tall, hanging z 32-50. Nominal - scaled off a photo.
    """
    def P(u, v): return (o[0] + u * a[0] + v * n[0], o[1] + u * a[1] + v * n[1])

    def uvbox(u0, u1, v0, v1, z0, z1):
        (xa, ya), (xb, yb) = P(u0, v0), P(u1, v1)
        return box(min(xa, xb), max(xa, xb), min(ya, yb), max(ya, yb), z0, z1)

    zc = Z2 - 10                     # 1 mm of foam tape between holder and plate 2
    body = uvbox(7, 43, -9, 9, Z2 - 19, Z2 - 1) + uvbox(12, 38, 9, 21, Z2 - 19, Z2 - 1)
    for u0, u1 in ((0, 7), (43, 50)):
        (xa, ya), (xb, yb) = P(u0, 0), P(u1, 0)
        body += cyl((xa, ya, zc), (xb, yb, zc), 5)
    part(name, "holder", body)
    part(name + "-rating", rating, uvbox(16, 34, 21, 21.6, zc - 5, zc + 5))
    part(name + "-tape", "tape", uvbox(9, 41, -8, 8, Z2 - 1, Z2))       # 3M foam tape, 1 mm
    return P(0, 0), P(50, 0)        # wire exits, (x, y) at z = zc


def clip(name, x0, x1, y0, y1, z0, z1, ports_y, face_x, lever_z):
    """WAGO 221 or a DOMAXWILL clone: all ports on one face, levers on one side."""
    part(name, "wago", box(x0, x1, y0, y1, z0, z1))
    lv = []
    for y in ports_y:
        lx0, lx1 = (face_x - 10, face_x - 1) if face_x > x0 else (face_x + 1, face_x + 10)
        lv += box(lx0, lx1, y - 2, y + 2, lever_z[0], lever_z[1])
    if lv:
        part(name + "-levers", "lever", lv)


# Tires. Hiwonder's CAD has the rims only: 58.7 across the lips, 29.4 wide, a well down
# to r 25.2. The rubber is estimated from a photo of the kit, scaled on the 120.5 mm
# plate: about 68 mm outside diameter and 30 wide - measure before trusting it.
# Axles from the CAD, in layout coordinates: rear x 221.56, z 15.33; front x 50.02,
# z 12.69 (the front axle sits 2.6 mm lower). Wheel spans across, y: rear -38.11..-8.70
# and 129.27..158.67, front -38.95..-9.55 and 130.11..159.51.
TIRE_R, TIRE_W = 34.0, 30.0
WHEELS = [("tire-rear-right", 221.56, 15.33, -38.41), ("tire-rear-left", 221.56, 15.33, 128.97),
          ("tire-front-right", 50.02, 12.69, -39.25), ("tire-front-left", 50.02, 12.69, 129.81)]


def tires():
    R, W = TIRE_R, TIRE_W
    prof = [(0, 28.6), (0, 31.0), (1.0, 33.2), (3.0, R), (9.0, R), (9.6, R - 1.4), (10.8, R - 1.4),
            (11.4, R), (18.6, R), (19.2, R - 1.4), (20.4, R - 1.4), (21.0, R), (27.0, R),
            (W - 1.0, 33.2), (W, 31.0), (W, 28.6)]
    prof = prof[::-1]                      # wound so the faces point outwards once mirrored
    for name, xc, zc, y0 in WHEELS:
        part(name, "tire", revolve(prof, xc, zc, y0))


def build():
    tires()
    # battery as fixed on the vehicle 2026-09-28 (photos): lengthwise right behind the
    # tie rod, on a felt pad, held by two felt straps and zip ties. Leads leave the
    # FRONT face: SM-2P lead at the front-right corner, charge lead at the front-left.
    part("battery-pad", "tie", box(85, 162, 30, 93, 0, 3))
    part("battery", "battery", box(85, 162, 30, 93, 3, 24))
    straps = []
    for x0 in (92, 136):
        straps += box(x0, x0 + 20, 28, 95, 24, 26) + box(x0, x0 + 20, 28, 30, 3, 26) + box(x0, x0 + 20, 93, 95, 3, 26)
    part("battery-straps", "tie", straps)
    part("battery-charge-lead", "mark_black", wire([(85, 91, 12), (82, 95, 8), (100, 110, 4), (180, 112, 4)], 4.0))
    part("battery-charge-socket", "mark_black", cyl((180, 112, 4.5), (198, 112, 4.5), 4.5))

    # motor driver: PCB on its spacers, parts block, harness connectors on the right edge
    part("driver-pcb", "pcb_driver", box(168, 210, 22.6, 80.6, 6, 7.6))
    sp = []
    for x in (172.8, 205.2):
        for y in (27.4, 75.8):
            sp += cyl((x, y, 0), (x, y, 6), 3, n=6)
    part("driver-spacers", "switch", sp)
    part("driver-parts", "parts", box(171, 200, 26, 78, 7.6, 16))
    part("driver-connectors", "connector",
         box(176, 181, 19, 26, 7.6, 14) + box(182, 194, 19, 26, 7.6, 14) + box(195, 200, 19, 26, 7.6, 14))

    # ---- plate 2's lower face is the harness board (MEC-16): every part below is stuck
    # to it with 3M double-sided foam tape (1 mm), wired with plate 2 upside down on the
    # bench, then plate 2 is lowered onto its standoffs and the drops fold down.
    T1 = Z2 - 1                                        # underside of the tape

    def taped(name, mat, x0, x1, y0, y1, h, **kw):
        part(name + "-tape", "tape", box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, T1, Z2))
        part(name, mat, box(x0, x1, y0, y1, T1 - h, T1))

    def taped_clip(name, x0, x1, y0, y1, ports_y, face_x, h=8.5):
        part(name + "-tape", "tape", box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, T1, Z2))
        clip(name, x0, x1, y0, y1, T1 - h, T1, ports_y, face_x, (T1 - h - 1.5, T1 - h))

    # the two buses either side of plate 2's opening (x 110-133), levers down, entry
    # faces towards each other across the opening
    taped_clip("bus-plus", 88, 106.6, 40, 70, (43, 49, 55, 61, 67), 106.6)
    part("bus-plus-mark", "mark_red", box(88, 92, 40, 70, T1 - 9, T1 - 8.5))
    taped_clip("bus-minus", 134, 152.6, 40, 70, (43, 49, 55, 61, 67), 134)
    part("bus-minus-mark", "mark_black", box(148.6, 152.6, 40, 70, T1 - 9, T1 - 8.5))

    # fuse holders flat on plate 2, lids to the open sides
    main_in, main_out = holder("fuse-main", "fuse_7_5", (96, 23), (1, 0), (0, -1))
    mot_in, mot_out = holder("fuse-motor", "fuse_5", (202, 23), (-1, 0), (0, -1))
    ub_in, ub_out = holder("fuse-ubec", "fuse_5", (202, 97), (-1, 0), (0, 1))

    # INA226 upside down behind the opening, terminals facing it (y 78 edge)
    part("ina226-tape", "tape", box(109, 133, 79, 99, T1, Z2))
    part("ina226", "pcb_ina", box(108, 134, 78, 100, T1 - 1.6, T1))
    part("ina226-terminals", "terminal", box(110, 132, 78, 84, T1 - 11.6, T1 - 1.6))

    # SW1 split over the driver; UBEC over the pack's left edge
    taped_clip("split-sw1", 178, 196.6, 51, 69.4, (54, 60.2, 66.4), 196.6)
    taped("ubec", "ubec", 100, 135, 100, 112, 5)

    # 2-port splices (DOMAXWILL), 18.6 x 13 x 8.5, both wires on one face
    taped_clip("splice-s1-battery-plus", 83, 96, 21, 39.6, (), 83)        # ports on its x 83 face
    part("splice-s1-battery-plus-levers", "lever", box(84, 93, 25, 29, T1 - 10, T1 - 8.5) + box(84, 93, 31, 35, T1 - 10, T1 - 8.5))
    taped_clip("splice-s2-vm-plus", 157, 175.6, 35, 48, (38, 44), 157)
    clip("splice-s4-vm-minus", 157, 175.6, 35, 48, T1 - 18.5, T1 - 10, (38, 44), 157, (T1 - 20, T1 - 18.5))
    taped_clip("splice-s3-ubec-plus", 138.7, 157.3, 104, 117, (107, 113), 138.7)
    clip("splice-s5-ubec-minus", 138.7, 157.3, 104, 117, T1 - 18.5, T1 - 10, (110, 115), 138.7, (T1 - 20, T1 - 18.5))
    clip("splice-s6-bauer-plus", 87.7, 106.3, 41.5, 54.5, PLATE2_TOP, PLATE2_TOP + 8.5, (48, 52), 87.7, (60.5, 62))
    clip("splice-s7-bauer-minus", 87.7, 106.3, 63.5, 76.5, PLATE2_TOP, PLATE2_TOP + 8.5, (68, 74), 87.7, (60.5, 62))

    # SM-2P, the battery disconnect: the female half stays on the pack lead (plate 1),
    # the male half is on a drop from plate 2 and is plugged in last (DROPS)
    part("sm2p-female", "connector", box(85, 91, 21, 29, 33, 39))

    # switches: bezel on the fascia's outer face (x 273.3), body 20 behind it, tabs 5 more
    for nm, yc, bz in (("sw1-drive", 82.3, "bezel_red"), ("sw2-logic", 38.3, "bezel_green")):
        part(nm, "switch", cyl((253.3, yc, 25), (270.3, yc, 25), 10) + cyl((267.3, yc, 25), (270.3, yc, 25), 14.25, n=6))
        part(nm + "-bezel", bz, cyl((273.3, yc, 25), (275.3, yc, 25), 12.4))
        tabs = []
        for dy in (-2.5, 2.5):
            for dz in (-2.5, 2.5):
                tabs += box(248.3, 253.3, yc + dy - 2.4, yc + dy + 2.4, 25 + dz - 0.4, 25 + dz + 0.4)
        part(nm + "-tabs", "switch", tabs)

    # plate 2 context: Bauer placeholder, carrier boards A, B and board C (translucent)
    part("p2-bauer-placeholder", "placeholder", box(20, 84, 32, 89, PLATE2_TOP, PLATE2_TOP + 22))
    part("p2-carrier-board-a", "pcb_carrier", box(117, 187, 4.95, 34.95, 62, 63.6))
    part("p2-carrier-board-b", "pcb_carrier", box(117, 187, 60.99, 110.99, 62, 63.6))
    part("p2-board-c", "pcb_carrier", box(85.5, 115.5, 25.2, 95.2, 62, 63.6))
    part("p2-board-a-6v-in", "terminal", box(143, 153, 6, 13, 63.6, 71))

    zc = Z2 - 10                             # fuse wire axis
    F = 47.3                                 # wires lying flat on plate 2's lower face
    pz = T1 - 4.25                           # clip port height
    P = lambda y: (106.6, y, pz)             # (+) bus ports
    M = lambda y: (134, y, pz)               # (-) bus ports
    # --- drops: the only wires that cross between the decks, each with slack to fold
    W("run01a-pack-lead-plus", "wire_red", AWG22,
      [(85, 33, 12), (87.5, 21, 14), (88, 19, 26), (86, 18, 33), (86, 21, 36)])
    W("run04a-pack-lead-minus", "wire_black", AWG22,
      [(85, 35, 12), (89.5, 21, 14), (90, 19, 26), (90, 18, 33), (90, 21, 36)])
    # --- plate 2 harness
    W("run01b-sm2p-to-s1", "wire_red", AWG18, [(81, 37, 44), (81, 33, pz), (83, 33, pz)])
    W("run01c-s1-to-main-fuse", "wire_red", AWG16, [(83, 27, pz), (81, 26, 44), (84, 22, zc), main_in + (zc,)])
    W("run02-main-fuse-to-ina226", "wire_red", AWG16,
      [main_out + (zc,), (150, 26, F), (154, 34, F), (154, 76, F), (114, 76, F), (114, 77, pz), (114, 78, T1 - 7)])
    W("run03-ina226-to-plus-bus", "wire_red", AWG18,
      [(126, 78, T1 - 7), (126, 76, pz), (110, 74, F), (109, 43, F), (109, 43, pz), P(43)])
    W("run04b-battery-minus-to-bus", "wire_black", AWG18,
      [(95, 39, 44), (107, 39, F), (108, 66, F), (128, 67, F), (128, 67, pz), M(67)])
    W("run05-plus-bus-to-sw1", "wire_red", AWG18,
      [P(49), (109, 49, F), (109, 74, F), (200, 74, F), (203, 62, F), (240, 62, F), (244, 80, 30), (248.3, 79.8, 22.5)])
    W("run06-plus-bus-to-sw2", "wire_red", AWG18,
      [P(55), (109.5, 55, F - 2.4), (109.5, 75.5, F - 2.4), (200, 75.5, F - 2.4), (203, 60.5, F), (240, 60.5, F),
       (244, 37, 30), (248.3, 35.8, 22.5)])
    W("run07-sw1-no-to-split", "wire_orange", AWG18,
      [(248.3, 84.8, 22.5), (243, 84, 30), (240, 63.5, F - 2.4), (203, 63.5, F - 2.4), (198, 60.2, pz), (196.6, 60.2, pz)])
    W("run08a-split-to-motor-fuse", "wire_orange", AWG16,
      [(196.6, 54, pz), (203, 50, 45), (204, 25, 42), mot_in + (zc,)])
    W("run08b-motor-fuse-to-s2", "wire_orange", AWG16,
      [mot_out + (zc,), (150, 26, 44), (150, 38, pz), (157, 38, pz)])
    W("run08c-vm-plus-pigtail", "wire_orange", AWG18, [(155, 46, 44), (155, 44, pz), (157, 44, pz)])
    W("run09a-split-to-ubec-fuse", "wire_orange", AWG16,
      [(196.6, 66.4, pz), (203, 70, 45), (204, 95, 42), ub_in + (zc,)])
    W("run09b-ubec-fuse-to-s3", "wire_orange", AWG16,
      [ub_out + (zc,), (137, 100, pz), (137, 107, pz), (138.7, 107, pz)])
    W("run09c-ubec-plus-lead", "wire_orange", AWG18,
      [(135, 103, T1 - 2.5), (136, 112, pz), (138.7, 113, pz)])
    W("run10a-ubec-6v-plus-to-board-a", "wire_teal", AWG18,
      [(100, 103, T1 - 2.5), (97, 100, 46), (104, 78, 46), (112, 75, 44), (114, 72, 46), (114, 72, 58), (146, 20, 58),
       (146, 1, 62), (146, 1, 67), (146, 6, 67)])
    W("run10b-ubec-6v-minus-to-board-a", "wire_black", AWG18,
      [(100, 109, T1 - 2.5), (95, 105, 46), (102, 79, 46), (116, 77, 44), (117, 75, 46), (117, 75, 58), (150, 22, 58),
       (150, 1, 62), (150, 1, 67), (150, 6, 67)])
    W("run11a-ubec-minus-lead", "wire_black", AWG18,
      [(135, 109, T1 - 2.5), (136, 110, 36), (138.7, 110, T1 - 14.25)])
    W("run11b-s5-to-minus-bus", "wire_black", AWG18,
      [(138.7, 115, T1 - 14.25), (137, 116, 36), (137, 76, 40), (130, 76, 42), (128, 61, 44), M(61)])
    W("run12a-vm-minus-pigtail", "wire_black", AWG18, [(155, 46, 36), (155, 44, T1 - 14.25), (157, 44, T1 - 14.25)])
    part("driver-vm-socket", "connector", box(176, 182, 19, 23, 7.6, 14))

    # --- drops: the only wires that cross between the decks (see DROPS below).
    # The switches ride with plate 2: the lower fascia panel is held to plate 2 on the
    # bench and wired there, so their leads never cross. What crosses is two plugs, the
    # SM-2P and the driver's VM, and both are plugged from the right side once closed.
    D("drop-sm2p-plus", "wire_red", AWG18, (81, 37, 44), (86, 37, 36), (0, 0, -1), (0, 1, 0), 30,
      plug="sm2p", plugged=("closed",), tail=(-1, 0, 0))
    D("drop-sm2p-minus", "wire_black", AWG18, (95, 39, 44), (90, 37, 36), (0, 0, -1), (0, 1, 0), 30,
      plug=None, plugged=("closed",), tail=(-1, 0, 0))
    D("drop-vm-plus", "wire_orange", AWG18, (155, 46, 44), (178, 19, 11), (0, 0, -1), (0, -1, 0.3), 70,
      plug="vm", plugged=("closed",), tail=(1, 0, 0))
    D("drop-vm-minus", "wire_black", AWG18, (155, 48, 36), (180, 19, 11), (0, 0, -1), (0, -1, 0.3), 70,
      plug=None, plugged=("closed",), tail=(1, 0, 0))
    W("run12b-s4-to-minus-bus", "wire_black", AWG18,
      [(157, 38, T1 - 14.25), (155, 38, 37), (130, 38, 38), (128, 55, 44), M(55)])
    W("run13a-led-minus-jumper", "wire_black", AWG18, [(248.3, 84.8, 27.5), (247, 62, 29), (248.3, 40.8, 27.5)])
    W("run13b-led-minus-return", "wire_black", AWG18,
      [(247, 62, 29), (242, 61.5, 40), (240, 61.5, F - 2.4), (203, 61.5, F - 2.4), (200, 77, F), (155, 77, F),
       (153, 72, 46), (130, 72, 44), (130, 49, 44), M(49)])
    W("run14a-led-plus-sw1", "wire_orange", AWG18, [(248.3, 79.8, 27.5), (246.5, 82.3, 25), (248.3, 84.8, 22.5)])
    W("run14b-led-plus-sw2", "wire_orange", AWG18, [(248.3, 35.8, 27.5), (246.5, 38.3, 25), (248.3, 40.8, 22.5)])
    W("run15a-sw2-no-to-s6", "wire_orange", AWG18,
      [(248.3, 40.8, 22.5), (243, 42, 30), (240, 59, F - 2.4), (203, 59, F - 2.4), (200, 73, F), (126, 73, F),
       (126, 60, F), (126, 60, 56), (110, 44, 56), (86, 42, 56), (86, 48, 56.25), (87.7, 48, 56.25)])
    W("run15b-bauer-plus-lead", "wire_orange", AWG18, [(84, 55, 56), (86, 52, 56.25), (87.7, 52, 56.25)])
    W("run16a-bauer-minus-lead", "wire_black", AWG18, [(84, 62, 56), (86, 68, 56.25), (87.7, 68, 56.25)])
    W("run16b-s7-to-minus-bus", "wire_black", AWG18,
      [(87.7, 74, 56.25), (86, 74, 56), (86, 80, 56), (123, 66, 56), (123, 66, 46), (128, 44, 45),
       (128, 43, pz), M(43)])


RUNS = []             # (name, material, diameter, polyline) - lengths come from these


def W(name, mat, d, pts):
    RUNS.append((name, mat, d, pts))
    part(name, mat, wire(pts, d))


DROPS = []            # wires that cross between the decks, one curve per state
STATES = ("closed", "raised", "open")
LIFT = 60.0           # "raised": plate 2 on its way down, both plugs still hanging free


def plate2_move(p, state):
    """Where a point fixed to plate 2 goes in each state, in layout coordinates.

    raised: straight up LIFT mm. open: hinged 180 deg like a book about a line along
    the vehicle's right side (vehicle X -85, Z 50.56), so plate 2 lies beside the
    chassis with its lower face up - the renders use the same hinge.
    """
    x, y, z = p
    if state == "raised":
        return (x, y, z + LIFT)
    if state == "open":
        return (x, -54.4 - y, 42.88 - z)
    return p


def _bez(p0, p1, p2, p3, n=24):
    return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d
                  for a, b, c, d in zip(p0, p1, p2, p3)) for t in (i / n for i in range(n + 1))]


def _plen(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def drop_curve(b, a, db, da, L):
    """A wire of length L from b to a, leaving b along db and a along da: a cubic whose
    handles are stretched until the length fits - the slack is what the handles hold."""
    db, da = _norm(db), _norm(da)
    lo, hi = 0.0, 400.0
    for _ in range(40):
        s = (lo + hi) / 2
        pts = _bez(b, _add(b, _mul(db, s)), _add(a, _mul(da, s)), a)
        lo, hi = (s, hi) if _plen(pts) < L else (lo, s)
    return pts


def plug_box(c, kind):
    if kind == "sm2p":
        return box(c[0] - 3, c[0] + 7, c[1] - 8, c[1], c[2] - 3, c[2] + 3)
    return box(c[0] - 4, c[0] + 4, c[1] - 2, c[1] + 4, c[2] - 3, c[2] + 3)


def D(name, mat, d, b, a, db, da, L, plug, plugged, tail):
    DROPS.append(dict(name=name, mat=mat, d=d, b=b, a=a, db=db, da=da, L=L, plug=plug,
                      plugged=plugged, tail=tail))
    for n, m, tris in drop_parts(DROPS[-1], "closed"):
        part(n, m, tris)


def drop_parts(dp, state):
    """The drop's wire (and its plug) for one state, in layout coordinates."""
    b = plate2_move(dp["b"], state)
    if state in dp["plugged"]:
        db = dp["db"] if state != "open" else _mul(dp["db"], -1)
        pts = drop_curve(b, dp["a"], db, dp["da"], dp["L"])
        end = dp["a"]
    elif state == "open":                    # unplugged, lying on the upturned face
        t = dp["tail"]
        e = (dp["b"][0] + t[0] * dp["L"], dp["b"][1] + t[1] * dp["L"], dp["b"][2])
        pts = [plate2_move(dp["b"], state), plate2_move(e, state)]
        end = pts[-1]
    else:                                    # unplugged, hanging from plate 2
        pts = [b, (b[0], b[1], b[2] - dp["L"])]
        end = pts[-1]
    out = [(dp["name"], dp["mat"], wire(pts, dp["d"]))]
    if dp["plug"]:
        out.append((dp["name"] + "-plug", "connector", plug_box(end, dp["plug"])))
    return out


def run_lengths():
    """Modelled length of every run, mm, bend to bend - the cut list starts here."""
    out = []
    for name, mat, d, pts in RUNS:
        L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        out.append((name, mat, d, L))
    return out


# ---------------------------------------------------------------- output
def to_vehicle(p):
    x, y, z = p
    return (y - 57.8, x - 138.4, z + 29.12)


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"plate1 stand-in".ljust(80, b" ") + struct.pack("<I", len(tris)))
        for a, b, c in tris:
            a, c, b = to_vehicle(a), to_vehicle(b), to_vehicle(c)     # mirror: swap winding
            nx, ny, nz = _cross(_sub(b, a), _sub(c, a))
            l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack("<12fH", nx / l, ny / l, nz / l, *a, *b, *c, 0))


def main():
    build()
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith(".stl"):
            os.remove(os.path.join(OUT, old))
    for name, mat, tris in PARTS:
        write_stl(os.path.join(OUT, name + ".stl"), tris)
    print(f"plate1/: {len(PARTS)} parts, {sum(len(t) for _, _, t in PARTS)} triangles")
    for st in ("raised", "open"):
        d = os.path.join(OUT, "states", st)
        os.makedirs(d, exist_ok=True)
        for old in os.listdir(d):
            os.remove(os.path.join(d, old))
        for dp in DROPS:
            for n, m, tris in drop_parts(dp, st):
                write_stl(os.path.join(d, n + ".stl"), tris)
    for name, mat, d, L in run_lengths():
        print(f"  {name:36s} {mat:12s} {L:6.0f} mm")


if __name__ == "__main__":
    main()
