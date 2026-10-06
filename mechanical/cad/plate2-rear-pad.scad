// NEXUS plate 2 rear pad - a plain plate spread over plate 2's rear, to drill for whatever comes next (MEC-19)
//
//   openscad -D 'PART="tray"' -o plate2-rear-pad.stl plate2-rear-pad.scad
//
// STATUS 2026-10-06: ORDERED with the carrier and compute trays (Craftcloud #516727254320, BOM 3.28), not printed or dry-fitted yet.
//
// FRAME. Plate 2's own: x from the front to the rear, y from the vehicle's RIGHT edge to its LEFT, mm (the layout frame of MEC-15 /
// MEC-17 / hardware/scripts/chassis-layout.py). Plates 1, 2 and 3 are identical, so plate3-data.scad is plate 2's data too. With z up the
// layout frame is a mirror image of the real world, so the output passes through real() once. The pad's underside is z 0, on plate 2's top face.
//
// WHERE. The rear of plate 2, behind the carrier tray: x 196-251, y 12-108 (55 x 96 mm), 4 mm like the other trays. It stays clear of
//   - the carrier tray: its rear corner pads end at x 191.6, 4.4 mm ahead;
//   - the chassis standoffs at (256.82, 22.17 and 98.36), 6 mm hexagons: 2.3 mm to the nearest corner;
//   - the cross-slot (x 260.3-265.7) and the fascia pads and clamp holes (x 262.9), which the J7 CAN lead and the fascia harness use;
//   - the Discovery, which overhangs the carrier tray to x 217.5 at z 95 and above: the pad is 4 mm tall, so nothing meets it.
// THE J7 CAN LEAD crosses the pad. It comes down plate 3's cross-slot at about y 74 and runs forward to board B (y 92 at x 190), a diagonal
// over the pad's top: it lies on it like any other wire. Keep its lane (about y 70-96) free of drilled parts, or tie the lead down.
// The harness to the fascia's ports (MEC-12) lies over the pad the same way. The pad's top is flat, with no windows, so the plate's three long
// slots here (x 203.5, 219.5, 235.5, y 26-94) are covered: nothing in the BOM passes through them.
// SIX FIXINGS, from below into a nut held in a pocket on top, each on an opening plate 2 already has: two places along the long slot at
// x 203.47-207.77 (a 4.29 mm slot: the screw may slide along it, a washer under the head, so the pad can be moved along y by hand before it is
// tightened), M2.5 into the plate holes at (227.88, 20.23 and 100.23), M3 into the holes at (245.88, 38.76 and 81.77). The harness taped under
// plate 2 stops at x 202 (BOM 3.8 / MEC-16), so the screw heads are free.
//
// TO MEASURE before ordering: the M3 and M2.5 nuts' real across-flats and thickness (assumed 5.5 / 2.4 and 5.0 / 2.4 mm, as MEC-17).

PART = "tray";             // "tray" | "plan" | "outline"

T            = 4.0;       // as the other trays
R_CORNER     = 3.0;
M3_POCKET    = 5.9;       // M3 nut across flats 5.5, a printing fit (MEC-17)
M3_DEPTH     = 2.6;
M25_POCKET   = 5.4;       // M2.5 nut across flats 5.0
M25_DEPTH    = 2.4;
FIX3_D       = 3.4;       // M3 through the pad, loose; the plate's slot or hole is the guide
FIX25_D      = 3.2;       // M2.5 through the pad, in a 2.71 plate hole
FIX_PAD_D    = 8.4;       // a round pad round each fixing, so no pocket breaks the edge

PAD = [196.0, 251.0, 12.0, 108.0];                              // x0 x1 y0 y1
// [x, y, plate opening d]: 4.3 = the long slot at x 203.47-207.77 (y 26.1-94.4), 3.18 = M3 hole, 2.71 = M2.5 hole
FIX = [[205.62, 40.0, 3.18], [205.62, 80.0, 3.18], [227.88, 20.23, 2.71], [227.88, 100.23, 2.71], [245.88, 38.76, 3.18], [245.88, 81.77, 3.18]];

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
module real() mirror([0, 1, 0]) children();
module outline2d() union() { rrect(PAD[0], PAD[1], PAD[2], PAD[3]); for (f = FIX) translate([f[0], f[1]]) circle(d = FIX_PAD_D, $fn = 48); }

module body() difference() {
    linear_extrude(T) difference() {
        outline2d();
        for (f = FIX) translate([f[0], f[1]]) circle(d = f[2] > 3 ? FIX3_D : FIX25_D, $fn = 32);
    }
    for (f = FIX) translate([f[0], f[1], T - (f[2] > 3 ? M3_DEPTH : M25_DEPTH)])
        cylinder(d = (f[2] > 3 ? M3_POCKET : M25_POCKET) / cos(30), h = (f[2] > 3 ? M3_DEPTH : M25_DEPTH) + 0.01, $fn = 6);
}

if (PART == "tray") real() body();
else if (PART == "plan") real() color("lightgrey") body();
else if (PART == "outline") outline2d();
