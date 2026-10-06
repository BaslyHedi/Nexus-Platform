// NEXUS plate 2 rear pad - a small plain plate on plate 2's rear, to drill for whatever comes next (MEC-19)
//
//   openscad -D 'PART="tray"' -o plate2-rear-pad.stl plate2-rear-pad.scad
//
// STATUS 2026-10-06: PROPOSED with Hedi, to go in the same print order as the carrier and compute trays (one order costs less than two).
//
// FRAME. Plate 2's own: x from the front to the rear, y from the vehicle's RIGHT edge to its LEFT, mm (the layout frame of MEC-15 /
// MEC-17 / hardware/scripts/chassis-layout.py). Plates 1, 2 and 3 are identical, so plate3-data.scad is plate 2's data too. With z up the
// layout frame is a mirror image of the real world, so the output passes through real() once. The pad's underside is z 0, on plate 2's top face.
//
// WHERE, AND WHY THERE. MEC-12 keeps the rear of plate 2 (x 224-266) empty for the harness to the fascia's three ports. The pad takes the part of
// it that nothing needs: x 222-252, y 28-70. It stays clear of
//   - the cross-slot (x 260.3-265.7) and the fascia pads and clamp holes (x 262.9), which the J7 CAN lead and the fascia harness use;
//   - the chassis standoffs at (256.82, 22.17 and 98.36), 6 mm hexagons: 3.4 mm to the nearest;
//   - the lane of the J7 CAN lead, which comes down the cross-slot at about y 74 and runs forward to board B (y 92 at x 190): the pad ends at y 70;
//   - the Discovery, which overhangs the carrier tray to x 217.5 at z 95 and above: the pad is 4 mm tall, so nothing meets it.
// THREE FIXINGS, all M3 from below into a nut held in a pocket on top, each on plate 2's own opening: one plate hole (245.88, 38.76) and two
// places along the long slot at x 235.47-239.77 (a 4.29 mm slot: the screw may slide along it, a washer under the head, so the pad can move
// along y by hand before it is tightened). Three points make a plane; the pad does not rock. The harness taped under plate 2 stops at x 202 (BOM 3.8 / MEC-16), so the screw heads are free.
//
// TO MEASURE before ordering: the M3 nut's real across-flats and thickness (assumed 5.5 and 2.4 mm, as the Bauer's pockets in MEC-17).

PART = "tray";             // "tray" | "plan" | "outline"

T            = 4.0;       // as the other trays
R_CORNER     = 3.0;
M3_POCKET    = 5.9;       // M3 nut across flats 5.5, a printing fit (MEC-17)
M3_DEPTH     = 2.6;
FIX_D        = 3.4;       // M3 through the pad, loose; the plate's slot or hole is the guide
FIX_PAD_D    = 8.4;       // a round pad round each fixing, so no pocket breaks the edge

PAD = [222.0, 252.0, 28.0, 70.0];                              // x0 x1 y0 y1
FIX = [[245.88, 38.76], [237.62, 31.0], [237.62, 60.0]];       // plate hole, then two places along the slot (y 26.1-94.4)

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
module real() mirror([0, 1, 0]) children();

module body() difference() {
    linear_extrude(T) difference() {
        union() { rrect(PAD[0], PAD[1], PAD[2], PAD[3]); for (f = FIX) translate(f) circle(d = FIX_PAD_D, $fn = 48); }
        for (f = FIX) translate(f) circle(d = FIX_D, $fn = 32);
    }
    for (f = FIX) translate([f[0], f[1], T - M3_DEPTH]) cylinder(d = M3_POCKET / cos(30), h = M3_DEPTH + 0.01, $fn = 6);
}

if (PART == "tray") real() body();
else if (PART == "plan") real() color("lightgrey") body();
else if (PART == "outline") union() { rrect(PAD[0], PAD[1], PAD[2], PAD[3]); for (f = FIX) translate(f) circle(d = FIX_PAD_D, $fn = 48); }
