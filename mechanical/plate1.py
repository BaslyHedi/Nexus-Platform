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
    "tie":          (0.97, 0.97, 0.97, 1), "ubec":         (0.95, 0.80, 0.10, 1),
    "switch":       (0.75, 0.75, 0.78, 1), "bezel_red":    (0.85, 0.10, 0.10, 1),
    "bezel_green":  (0.10, 0.70, 0.20, 1), "placeholder":  (0.85, 0.20, 0.25, 0.55),
    "pcb_carrier":  (0.10, 0.60, 0.30, 0.45),
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

    zc = Z2 - 9
    body = uvbox(7, 43, -9, 9, Z2 - 18, Z2) + uvbox(12, 38, 9, 21, Z2 - 18, Z2)
    for u0, u1 in ((0, 7), (43, 50)):
        (xa, ya), (xb, yb) = P(u0, 0), P(u1, 0)
        body += cyl((xa, ya, zc), (xb, yb, zc), 5)
    part(name, "holder", body)
    part(name + "-rating", rating, uvbox(16, 34, 21, 21.6, zc - 5, zc + 5))
    ties = []
    for u in (13, 34.5):
        ties += uvbox(u, u + 2.5, -10, 10, Z2 - 19, PLATE2_TOP + 0.6)
    part(name + "-ties", "tie", ties)
    return P(0, 0), P(50, 0)        # wire exits, (x, y) at z = zc


def clip(name, x0, x1, y0, y1, z0, z1, ports_y, face_x, lever_z):
    """WAGO 221 or a DOMAXWILL clone: all ports on one face, levers on one side."""
    part(name, "wago", box(x0, x1, y0, y1, z0, z1))
    lv = []
    for y in ports_y:
        lx0, lx1 = (face_x - 10, face_x - 1) if face_x > x0 else (face_x + 1, face_x + 10)
        lv += box(lx0, lx1, y - 2, y + 2, lever_z[0], lever_z[1])
    part(name + "-levers", "lever", lv)


def build():
    # battery on its 2 mm pad, leads leaving the rear face at the right corner
    part("battery-pad", "pad", box(55, 132, 30, 93, 0, 2))
    part("battery", "battery", box(55, 132, 30, 93, 2, 22))
    part("battery-charge-socket", "mark_black", cyl((132, 91.5, 12), (138, 91.5, 12), 4))

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

    # INA226: pad, PCB, terminal block on its outboard (right) edge
    part("ina226-pad", "pad", box(135, 157, 2, 28, 0, 2))
    part("ina226", "pcb_ina", box(135, 157, 2, 28, 2, 3.6))
    part("ina226-terminals", "terminal", box(137, 155, 2, 8, 3.6, 13.6))

    # the two buses, 221-415, wires entering the rear face x 153.6
    clip("bus-plus", 135, 153.6, 31, 61, 0, 8.5, (34, 40, 46, 52, 58), 153.6, (8.5, 10))
    part("bus-plus-mark", "mark_red", box(136, 140, 31, 61, 8.5, 9))
    clip("bus-minus", 135, 153.6, 65, 95, 0, 8.5, (68, 74, 80, 86, 92), 153.6, (8.5, 10))
    part("bus-minus-mark", "mark_black", box(136, 140, 65, 95, 8.5, 9))

    # SM-2P, mated, lying on the lead at the pack's rear corner
    part("sm2p", "connector", box(134, 150, 29.5, 35, 24, 30))

    # fuse holders under plate 2 (MEC-16)
    main_in, main_out = holder("fuse-main", "fuse_7_5", (133, 2), (0, 1), (-1, 0))
    mot_in, mot_out = holder("fuse-motor", "fuse_5", (194, 23), (-1, 0), (0, -1))
    ub_in, ub_out = holder("fuse-ubec", "fuse_5", (194, 97), (-1, 0), (0, 1))

    # SW1 split: DOMAXWILL 3-port hung under plate 2 over the driver, levers down
    clip("split-sw1", 178, 196.6, 51, 69.4, Z2 - 8.5, Z2, (54, 60.2, 66.4), 196.6, (Z2 - 10, Z2 - 8.5))

    # 2-port splices (DOMAXWILL), 18.6 deep x 13 wide x 8.5, both wires on one face
    clip("splice-s1-battery-plus", 133.7, 152.3, 37.5, 50.5, 21.75, 30.25, (41, 47), 152.3, (30.25, 31.5))
    clip("splice-s2-vm-plus", 165.7, 184.3, 2.5, 15.5, 8.5, 17, (6, 12), 165.7, (17, 18.5))
    clip("splice-s4-vm-minus", 165.7, 184.3, 2.5, 15.5, 0, 8.5, (6, 12), 165.7, (-1.5, 0))
    clip("splice-s3-ubec-plus", 108.7, 127.3, 90.5, 103.5, Z2 - 8.5, Z2, (97, 103), 127.3, (Z2 - 10, Z2 - 8.5))
    clip("splice-s5-ubec-minus", 108.7, 127.3, 90.5, 103.5, 33, 41.5, (97, 103), 127.3, (31.5, 33))
    clip("splice-s6-bauer-plus", 87.7, 106.3, 41.5, 54.5, PLATE2_TOP, PLATE2_TOP + 8.5, (48, 52), 87.7, (60.5, 62))
    clip("splice-s7-bauer-minus", 87.7, 106.3, 63.5, 76.5, PLATE2_TOP, PLATE2_TOP + 8.5, (68, 74), 87.7, (60.5, 62))

    # UBEC, potted, lying along y under plate 2 above the pack's left half
    part("ubec", "ubec", box(90, 102, 62, 97, Z2 - 5, Z2))

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

    zc = Z2 - 9
    W = lambda name, mat, d, pts: part(name, mat, wire(pts, d))
    # --- the runs, numbered as in the chassis layout's run table
    W("run01a-pack-lead-plus", "wire_red", AWG22, [(132, 31.5, 12), (133, 31, 20), (134, 31, 27)])
    W("run01b-sm2p-to-s1", "wire_red", AWG18, [(150, 31, 27), (155, 31, 27), (155, 41, 26), (152.3, 41, 26)])
    W("run01c-s1-to-main-fuse", "wire_red", AWG16,
      [(152.3, 47, 26), (156, 47, 26), (156, 55, 30), (main_out[0], 55, zc), (main_out[0], main_out[1], zc)])
    W("run02-main-fuse-to-ina226", "wire_red", AWG16,
      [(main_in[0], main_in[1], zc), (main_in[0], -1, zc), (140, -1, 20), (140, 1, 10), (140, 2, 8)])
    W("run03-ina226-to-plus-bus", "wire_red", AWG18,
      [(150, 2, 8), (150, 0, 10), (158, 0, 10), (158, 34, 4.25), (153.6, 34, 4.25)])
    W("run04a-pack-lead-minus", "wire_black", AWG22, [(132, 33.5, 12), (133, 33.5, 20), (134, 33.5, 27)])
    W("run04b-battery-minus-to-bus", "wire_black", AWG18,
      [(150, 33.5, 27), (157, 34, 27), (159, 60, 20), (159, 92, 6), (158, 92, 4.25), (153.6, 92, 4.25)])
    W("run05-plus-bus-to-sw1", "wire_red", AWG18,
      [(153.6, 40, 4.25), (158, 40, 4.25), (162, 55, 20), (203, 59, 20), (240, 59, 20), (244, 78, 22.5), (248.3, 79.8, 22.5)])
    W("run06-plus-bus-to-sw2", "wire_red", AWG18,
      [(153.6, 46, 4.25), (158, 46, 4.25), (163, 57, 23), (203, 60, 23), (240, 60, 23), (244, 37, 22.5), (248.3, 35.8, 22.5)])
    W("run07-sw1-no-to-split", "wire_orange", AWG18,
      [(248.3, 84.8, 22.5), (244, 84, 26), (240, 61, 26), (203, 61, 26), (200, 60.2, 40), (196.6, 60.2, 45.75)])
    W("run08a-split-to-motor-fuse", "wire_orange", AWG16,
      [(196.6, 54, 45.75), (200, 52, 45), (200, mot_in[1], zc), (mot_in[0], mot_in[1], zc)])
    W("run08b-motor-fuse-to-s2", "wire_orange", AWG16,
      [(mot_out[0], mot_out[1], zc), (143.5, 23, 34), (144, 22, 28), (163, 21.5, 26), (163, 6, 12.75), (165.7, 6, 12.75)])
    W("run08c-vm-plus-pigtail", "wire_orange", AWG18,
      [(178, 22, 11), (178, 17, 11), (163, 16, 12.75), (163, 12, 12.75), (165.7, 12, 12.75)])
    W("run09a-split-to-ubec-fuse", "wire_orange", AWG16,
      [(196.6, 66.4, 45.75), (200, 68, 45), (200, ub_in[1], zc), (ub_in[0], ub_in[1], zc)])
    W("run09b-ubec-fuse-to-s3", "wire_orange", AWG16,
      [(ub_out[0], ub_out[1], zc), (131, 97, 45.75), (127.3, 97, 45.75)])
    W("run09c-ubec-plus-lead", "wire_orange", AWG18,
      [(93, 97.5, 47.5), (93, 108, 47), (131, 108, 46), (131, 103, 45.75), (127.3, 103, 45.75)])
    W("run10a-ubec-6v-plus-to-board-a", "wire_teal", AWG18,
      [(93, 62, 47.5), (93, 58, 48), (118, 56, 48), (118, 56, 58), (140, 4, 58), (146, 1, 62), (146, 1, 67), (146, 6, 67)])
    W("run10b-ubec-6v-minus-to-board-a", "wire_black", AWG18,
      [(99, 62, 47.5), (99, 59, 48), (121, 58, 48), (121, 58, 58), (144, 4, 58), (150, 1, 62), (150, 1, 67), (150, 6, 67)])
    W("run11a-ubec-minus-lead", "wire_black", AWG18,
      [(99, 97.5, 47.5), (99, 110, 40), (131, 110, 37.25), (131, 103, 37.25), (127.3, 103, 37.25)])
    W("run11b-s5-to-minus-bus", "wire_black", AWG18,
      [(127.3, 97, 37.25), (134, 96, 30), (158, 90, 10), (158, 86, 4.25), (153.6, 86, 4.25)])
    W("run12a-vm-minus-pigtail", "wire_black", AWG18,
      [(180, 22, 11), (180, 17, 5), (163, 15, 4.25), (163, 12, 4.25), (165.7, 12, 4.25)])
    W("run12b-s4-to-minus-bus", "wire_black", AWG18,
      [(165.7, 6, 4.25), (160, 6, 4.25), (160, 80, 4.25), (153.6, 80, 4.25)])
    W("run13a-led-minus-jumper", "wire_black", AWG18, [(248.3, 84.8, 27.5), (247, 62, 29), (248.3, 40.8, 27.5)])
    W("run13b-led-minus-return", "wire_black", AWG18,
      [(247, 62, 29), (242, 61, 29), (203, 61, 29), (170, 60, 32), (160, 74, 12), (158, 74, 4.25), (153.6, 74, 4.25)])
    W("run14a-led-plus-sw1", "wire_orange", AWG18, [(248.3, 79.8, 27.5), (246.5, 82.3, 25), (248.3, 84.8, 22.5)])
    W("run14b-led-plus-sw2", "wire_orange", AWG18, [(248.3, 35.8, 27.5), (246.5, 38.3, 25), (248.3, 40.8, 22.5)])
    W("run15a-sw2-no-to-s6", "wire_orange", AWG18,
      [(248.3, 40.8, 22.5), (244, 42, 32), (240, 60, 32), (203, 60, 32), (170, 60, 36), (126, 68, 45),
       (126, 68, 56), (110, 44, 56), (86, 42, 56), (86, 48, 56.25), (87.7, 48, 56.25)])
    W("run15b-bauer-plus-lead", "wire_orange", AWG18, [(84, 55, 56), (86, 52, 56.25), (87.7, 52, 56.25)])
    W("run16a-bauer-minus-lead", "wire_black", AWG18, [(84, 62, 56), (86, 68, 56.25), (87.7, 68, 56.25)])
    W("run16b-s7-to-minus-bus", "wire_black", AWG18,
      [(87.7, 74, 56.25), (86, 74, 56), (86, 80, 56), (129, 74, 56), (129, 72, 45), (150, 70, 30),
       (158, 68, 10), (158, 68, 4.25), (153.6, 68, 4.25)])


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


if __name__ == "__main__":
    main()
