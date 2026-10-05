// NEXUS carrier tray - one plate that carries boards A, B and C, bolted to plate 2 (MEC-17)
//
//   openscad -D 'PART="tray"'     -o carrier-tray.stl                  carrier-tray.scad   // to print
//   openscad -D 'PART="template"' -o ../renders/tray-template.svg      carrier-tray.scad   // 1:1, to cut a sheet by hand
//   openscad -D 'PART="step1"'    -o ../renders/tray-step1-boards.png  carrier-tray.scad   // 1: boards placed on the tray
//   openscad -D 'PART="step2"'    -o ../renders/tray-step2-plate2.png  carrier-tray.scad   // 2: the tray placed on plate 2
//
// STATUS 2026-10-05: PROPOSED, not built. Print it (PETG, 4 mm); a hand-cut sheet is the fallback.
//
// TWO STEPS, TWO FRAMES
//   STEP 1 - the tray frame (u, v). Origin at the tray's front-right corner, u toward the rear, v toward
//            the left, mm. The boards are placed on the tray HERE: BOARD_A / B / C, their corner holes,
//            the tray's own fixings. Nothing in step 1 knows where plate 2 is.
//   STEP 2 - the plate-2 frame (x, y), the LAYOUT frame of MEC-15 / MEC-16 / plate1.py: x from the front
//            to the rear, y from the vehicle's RIGHT edge to its LEFT. PLACE is the one translation that
//            puts the tray on plate 2. The plate's holes (PLATE_HOLES) are in this frame.
//   With z up the layout frame is a mirror image of the real world, so every output passes through
//   real() once, and the lettering is pre-mirrored to read correctly. The tray's underside is z 0.
//
// WHAT THE TRAY HAS
//   - every plate-2 hole that lies wholly under it, copied at the plate's own diameter, plus the plate's
//     large slot (PLATE_SLOT), so nothing that is open on the plate is blocked by the tray;
//   - four fixing holes that land on four of those plate holes (F1, F2, F5, F6), each with a hex pocket
//     on top that captures an M2.5 nut, so the tray comes off with one screw per corner from BELOW;
//   - twelve board holes, four per board (M2.5 clearance), with counterbores from below so the tray sits
//     flat; boards go on the nylon standoffs already fitted;
//   - the window over plate 2's wire opening, where the S6 / S7 and UBEC wires climb to the top face.
//   The S6 / S7 splices (plate1.py) sit on the tray under board C.
//
// HEIGHTS. A and B stand 10 mm above plate 2: 4 mm tray + 6 mm standoffs. C stands on 10 mm standoffs
// to clear the 8.5 mm splices, so it is 4 mm higher than it was, which its 13 mm capacitor and the
// 40 mm gap allow.
//
// TO MEASURE before printing (the defaults are guesses):
//   CORNER_INSET  - a board's corner hole centre from each edge
//   board C's holes once it is built

PART = "step2";              // "tray" | "template" | "step1" | "step2"

T            = 4.0;          // tray thickness
CORNER_INSET = 2.5;          // MEASURE: board corner hole centre from each edge
HOLE_D       = 2.8;          // M2.5 clearance
CB_D         = 5.6;          // counterbore for an M2.5 nylon screw head, from below
CB_DEPTH     = 2.0;
FIX_D        = 2.8;          // tray-to-plate-2 screws, M2.5 from below
NUT_AF       = 5.0;          // M2.5 nut across flats
NUT_POCKET   = 5.2;          // pocket across flats, a printing fit
NUT_DEPTH    = 2.4;          // M2.5 nut is 2.0 thick
R_CORNER     = 2.0;
WALL         = 1.5;          // least tray left between a copied plate hole and the tray's edge

// ---- STEP 1: the boards on the tray (tray frame, mm) ------------------------------------------------
// board = [u0, u1, v0, v1]. A and B as built 2026-10-03 (A one pitch ahead of B, 5.88 mm apart across
// the tray); C across the waist, 1.5 mm from A.
BOARD_A = [ 31.50, 101.50,   0.00,  50.00];
BOARD_B = [ 34.04, 104.04,  55.88, 105.88];
BOARD_C = [  0.00,  30.00,  20.09,  90.09];
BOARDS  = [BOARD_A, BOARD_B, BOARD_C];

// ---- STEP 2: the tray on plate 2 ------------------------------------------------------------------------
PLACE = [85.50, 5.11];       // plate-2 position of the tray frame's origin

// plate 2's holes under the tray, from the chassis layout (hardware/renders/chassis-layout.svg): [x, y, d].
// Left out because the tray cannot hold them: (72.41, 52.65/67.88) and (99.24, 23.76/96.76),
// (104.41, 19.59/100.94) are outside it; (86.94, 40.24/80.24) leave 0.1 mm to C's edge;
// (186.12, 9.71/110.82) sit 2.5 mm from A's and B's rear corner holes; the long side slots
// (x 109-158, y 10-15 and 105-111) run off the tray's front edge.
FIXINGS = [ // the four the tray is screwed down with, and the name MEC-15 gave them
    [148.18, 23.76, 3.18], // F1  M3 hole, M2.5 and a washer
    [148.18, 72.24, 2.71], // F2
    [ 99.24, 38.76, 3.18], // F5
    [ 99.24, 81.76, 3.18], // F6
];
PLATE_HOLES = [
    [ 96.71,  52.65, 2.71], [ 96.71,  67.88, 2.71], [102.18,  48.24, 2.71], [102.18,  72.24, 2.71],
    [120.06,  35.94, 2.71], [120.06,  84.53, 2.71], [143.47,  52.65, 2.71], [143.47,  67.88, 2.71],
    [148.18,  38.76, 3.18], [148.18,  48.24, 2.71], [148.18,  81.76, 3.18], [148.18,  96.76, 3.18],
    [162.06,  16.71, 2.47], [162.06, 103.82, 2.47],
    [169.88,  14.24, 2.71], [169.88,  20.24, 2.71], [169.88, 100.24, 2.71], [169.88, 106.24, 2.71],
    [ 92.65,  36.35, 4.30], [ 92.65,  84.25, 4.30],
];
// the plate's large slot, x 161.2-175.8, y 30.4-90.2, as the two end-circle centres and the radius
PLATE_SLOT = [[168.5, 37.7], [168.5, 82.9], 7.3];
// the plate's wire opening, x 110.3-133.0, y 42.5-77.9, a stadium of radius 11.35
PLATE_OPENING = [[121.65, 53.85], [121.65, 66.55], 11.35];
// the window: the opening up to x 115, clear of A's front-inboard corner counterbore
WINDOW_X1 = 115.0;

// the S6 / S7 splices, on the tray under C (plate1.py footprints, 18.6 x 13), plate-2 frame
SPLICES = [[87.7, 106.3, 41.5, 54.5], [87.7, 106.3, 63.5, 76.5]];

function tray(p) = [p[0] - PLACE[0], p[1] - PLACE[1]];          // plate-2 frame -> tray frame
function corners(b) = [[b[0] + CORNER_INSET, b[2] + CORNER_INSET], [b[1] - CORNER_INSET, b[2] + CORNER_INSET],
                       [b[0] + CORNER_INSET, b[3] - CORNER_INSET], [b[1] - CORNER_INSET, b[3] - CORNER_INSET]];

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);

module stadium(s) hull() { translate(tray(s[0])) circle(r = s[2], $fn = 64); translate(tray(s[1])) circle(r = s[2], $fn = 64); }

// the outline: each board's footprint, C joined to A / B across the 1.5 mm between them, and
// the 5.9 mm between A and B filled so the tray is one stiff piece
module outline2d()
    union() {
        for (b = BOARDS) rrect(b[0], b[1], b[2], b[3]);
        rrect(BOARD_C[1] - 3, BOARD_A[0] + 3, BOARD_C[2], BOARD_C[3]);
        translate([BOARD_B[0], BOARD_A[3] - 3]) square([BOARD_A[1] - BOARD_B[0], BOARD_B[2] - BOARD_A[3] + 6]);
    }

module window2d()
    intersection() {
        stadium(PLATE_OPENING);
        translate([-1000, -1000]) square([WINDOW_X1 - PLACE[0] + 1000, 2000]);
    }

// layout frame -> the real world (the layout's y runs right to left)
module real() mirror([0, 1, 0]) children();
module word(p, t, h) translate(p) mirror([0, 1, 0]) text(t, size = h, halign = "center", valign = "center");

module holes2d() {
    for (b = BOARDS) for (p = corners(b)) translate(p) circle(d = HOLE_D, $fn = 32);
    for (f = FIXINGS) translate(tray(f)) circle(d = FIX_D, $fn = 32);
    for (h = PLATE_HOLES) translate(tray(h)) circle(d = h[2], $fn = 32);
    stadium(PLATE_SLOT);
    window2d();
}

module labels2d(h = 6) {
    word([55, 12], "A", h);
    word([55, 94], "B", h);
    word([15, 55], "C", h);
    word([60, 52.9], "REAR >", 3.5);
}

// a drilling cross through each board hole and fixing, for the hand-cut sheet
module crosses2d()
    for (p = concat([for (b = BOARDS) for (c = corners(b)) c], [for (f = FIXINGS) tray(f)]))
        translate(p) { square([7, 0.35], center = true); square([0.35, 7], center = true); }

module trayBody() {
    difference() {
        linear_extrude(T) difference() { outline2d(); holes2d(); }
        // counterbores from below for the board screws, so the tray sits flat on plate 2
        for (b = BOARDS) for (p = corners(b)) translate([p[0], p[1], -0.01]) cylinder(d = CB_D, h = CB_DEPTH, $fn = 32);
        // a hex pocket on top at each fixing, holding the nut so the screw turns from below
        for (f = FIXINGS) translate([tray(f)[0], tray(f)[1], T - NUT_DEPTH])
            cylinder(d = NUT_POCKET / cos(30), h = NUT_DEPTH + 0.01, $fn = 6);
        // engraved board letters and the direction, 0.6 mm deep on top
        translate([0, 0, T - 0.6]) linear_extrude(1) labels2d();
        // where S6 / S7 go, a 0.4 mm outline on top
        for (s = SPLICES) translate([0, 0, T - 0.4]) linear_extrude(1)
            difference() { translate(-PLACE) rrect(s[0], s[1], s[2], s[3], 0.5); offset(delta = -0.6) translate(-PLACE) rrect(s[0], s[1], s[2], s[3], 0.5); }
    }
}

// ---- previews -----------------------------------------------------------------------------------------------
module board_ghost(b, z, solid) {
    // a solid ghost for the side section, an outline frame for the plan views, so the tray stays visible
    translate([b[0], b[2], z]) difference() {
        cube([b[1] - b[0], b[3] - b[2], 1.6]);
        if (!solid) translate([0.8, 0.8, -1]) cube([b[1] - b[0] - 1.6, b[3] - b[2] - 1.6, 4]);
    }
}
module ghost_boards(solid = false) {
    for (b = [BOARD_A, BOARD_B]) color("seagreen") board_ghost(b, T + 6, solid);
    color("seagreen") board_ghost(BOARD_C, T + 10, solid);
    for (b = BOARDS) for (p = corners(b)) color("gold") translate([p[0], p[1], T + 6.1 + (b == BOARD_C ? 4 : 0)]) cylinder(d = 3, h = 1, $fn = 20);
    for (s = SPLICES) color("orange", 0.8) translate([tray([s[0], s[2]])[0], tray([s[0], s[2]])[1], T]) cube([s[1] - s[0], s[3] - s[2], 8.5]);
    for (f = FIXINGS) color("silver") translate([tray(f)[0], tray(f)[1], T - NUT_DEPTH]) cylinder(d = NUT_AF / cos(30), h = 2, $fn = 6);
}

// plate 2 as a ghost slab 2 mm thick below z 0, drawn in the tray frame: its holes, slot and opening
module ghost_plate() {
    color("slategray", 0.75) translate([0, 0, -2]) linear_extrude(2) difference() {
        translate([-40, -20]) square([190, 160]);
        for (h = PLATE_HOLES) translate(tray(h)) circle(d = h[2], $fn = 24);
        for (f = FIXINGS) translate(tray(f)) circle(d = f[2], $fn = 24);
        for (p = [[72.41, 52.65, 2.71], [72.41, 67.88, 2.71], [99.24, 23.76, 3.18], [99.24, 96.76, 3.18], [104.41, 19.59, 3.18], [104.41, 100.94, 3.18],
                  [86.94, 40.24, 2.71], [86.94, 80.24, 2.71], [186.12, 9.71, 3.18], [186.12, 110.82, 3.18]]) translate(tray(p)) circle(d = p[2], $fn = 24);
        stadium(PLATE_SLOT);
        stadium(PLATE_OPENING);
    }
}

if (PART == "tray") real() trayBody();
else if (PART == "template") real() {
    difference() { outline2d(); holes2d(); crosses2d(); offset(delta = 0.4) labels2d(); }
    // print check: this bar must measure exactly 50 mm on paper (print at 100 %, no "fit to page")
    translate([BOARD_C[0], BOARD_A[2] - 9]) difference() {
        square([50, 4]);
        translate([25, 2]) mirror([0, 1, 0]) text("50 mm", size = 2.6, halign = "center", valign = "center");
    }
}
// step 1: the tray alone in its own frame, the boards on it
else if (PART == "step1") real() { color("lightgrey") trayBody(); ghost_boards(); }
// step 2: the same, set down on plate 2 over the plate's holes
else if (PART == "step2") real() { color("lightgrey") trayBody(); ghost_boards(); ghost_plate(); }
