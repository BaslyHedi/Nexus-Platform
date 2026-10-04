// NEXUS carrier tray - one plate that carries boards A, B and C, bolted to plate 2 (MEC-17)
//
//   openscad -D 'PART="tray"'     -o carrier-tray.stl          carrier-tray.scad   // to print
//   openscad -D 'PART="template"' -o carrier-tray-template.svg carrier-tray.scad   // 1:1, to cut a sheet by hand
//   openscad -D 'PART="preview"'  -o /tmp/tray-preview.png     carrier-tray.scad   // with the boards ghosted in
//
// STATUS 2026-10-03: PROPOSED, not built. Two ways to make it from this one file:
//   BEST    printed PETG, 4 mm, counterbores for the board screws so it sits flat (~15 EUR)
//   CHEAP   a 3 mm plastic sheet cut and drilled by hand over the 1:1 template; the board
//           screw heads then lift it ~1.8 mm, which is accepted
//
// COORDINATES are the LAYOUT frame of MEC-15 / MEC-16 / plate1.py: x from the front to the rear,
// y from the vehicle's RIGHT edge to its LEFT, mm. With z up that frame is a mirror image of the
// real world, so every output passes through real() once, and the lettering is pre-mirrored to
// read correctly. The tray's underside is z 0, on plate 2's top face.
//
// WHAT IT HOLDS
//   - Boards A, B and C on their own M2.5 corner holes, through the nylon standoffs already
//     fitted. Nothing is drilled into the boards. A and B sit where MEC-15 put them as built
//     (A one pitch ahead of B); C where MEC-15 put it, across the waist.
//   - The S6 / S7 splices (the Bauer's 5 V feed, plate1.py), which used to sit on plate 2
//     under board C. They now sit on the tray, under C, and their wires come up through
//     the window.
//
// HEIGHTS. Today the boards stand 10 mm above plate 2. Keep A and B there: 4 mm tray + 6 mm
// standoffs (printed); 3 mm sheet + 1.8 mm screw heads + 6 mm standoffs = 10.8 (by hand).
// C needs 10 mm standoffs on the tray to clear the 8.5 mm splices under it, so it stands
// 4 mm higher than before, which its 13 mm capacitor and the 40 mm gap allow.
//
// TO MEASURE before printing or drilling (the defaults are guesses):
//   CORNER_INSET - the corner holes' centres from both edges of a kit board
//   the plate-2 wire opening's y extent (WINDOW), taken here as centred on the carrier

PART = "preview";            // "tray" | "template" | "preview"

T            = 4.0;          // tray thickness, printed (the sheet option is whatever the sheet is)
CORNER_INSET = 2.5;          // MEASURE: board corner hole centre from each edge
HOLE_D       = 2.8;          // M2.5 clearance
CB_D         = 5.6;          // counterbore for an M2.5 nylon screw head, from below
CB_DEPTH     = 2.0;
FIX_D        = 2.8;          // tray-to-plate-2 screws, M2.5 from below, nut on top
NUT_AF       = 5.0;          // M2.5 nut across flats, for the keep-out around each fixing
R_CORNER     = 2.0;

// boards, as placed in MEC-15 (chassis x0, x1, y0, y1) - A and B as built 2026-10-03
BOARD_A = [117.00, 187.00,  5.11,  55.11];
BOARD_B = [119.54, 189.54, 60.99, 110.99];
BOARD_C = [ 85.50, 115.50, 25.20,  95.20];
BOARDS  = [BOARD_A, BOARD_B, BOARD_C];

// tray to plate 2: the four plate holes the carrier already used (MEC-15 F1, F2, F5, F6).
// MEC-16's open check on the screw heads under plate 2 still applies to these four.
FIX = [[148.18, 23.76], [148.20, 72.20], [99.24, 38.76], [99.24, 81.76]];

// over plate 2's wire opening (x 110-133): the slot between C and A/B, clear of A's
// front-inboard corner hole. Everything that climbs to the top face passes here.
WINDOW = [108.0, 116.2, 40.4, 75.8];

// the S6 / S7 splices, now on the tray under C (plate1.py footprints, 18.6 x 13)
SPLICES = [[87.7, 106.3, 41.5, 54.5], [87.7, 106.3, 63.5, 76.5]];

function corners(b) = [[b[0] + CORNER_INSET, b[2] + CORNER_INSET], [b[1] - CORNER_INSET, b[2] + CORNER_INSET],
                       [b[0] + CORNER_INSET, b[3] - CORNER_INSET], [b[1] - CORNER_INSET, b[3] - CORNER_INSET]];

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);

// the outline: each board's footprint, C joined to A / B across the 1.5 mm between them, and
// the 5.9 mm between A and B filled so the tray is one stiff piece
module outline2d()
    union() {
        for (b = BOARDS) rrect(b[0], b[1], b[2], b[3]);
        rrect(BOARD_C[1] - 3, BOARD_A[0] + 3, BOARD_C[2], BOARD_C[3]);
        translate([BOARD_B[0], BOARD_A[3] - 3]) square([BOARD_A[1] - BOARD_B[0], BOARD_B[2] - BOARD_A[3] + 6]);
    }

// layout frame -> the real world (the layout's y runs right to left)
module real() mirror([0, 1, 0]) children();
module word(p, t, h) translate(p) mirror([0, 1, 0]) text(t, size = h, halign = "center", valign = "center");

module holes2d() {
    for (b = BOARDS) for (p = corners(b)) translate(p) circle(d = HOLE_D, $fn = 32);
    for (p = FIX) translate(p) circle(d = FIX_D, $fn = 32);
    translate([WINDOW[0], WINDOW[2]]) square([WINDOW[1] - WINDOW[0], WINDOW[3] - WINDOW[2]]);
}

module labels2d(h = 6) {
    word([160, 30], "A", h);
    word([160, 86], "B", h);
    word([100.5, 60], "C", h);
    word([165, 58], "REAR >", 3.5);
}

// a drilling cross through each hole centre, for the hand-cut sheet
module crosses2d()
    for (p = concat([for (b = BOARDS) for (c = corners(b)) c], FIX))
        translate(p) { square([7, 0.35], center = true); square([0.35, 7], center = true); }

module tray() {
    difference() {
        linear_extrude(T) difference() { outline2d(); holes2d(); }
        // counterbores from below for the board screws, so the tray sits flat on plate 2
        for (b = BOARDS) for (p = corners(b)) translate([p[0], p[1], -0.01]) cylinder(d = CB_D, h = CB_DEPTH, $fn = 32);
        // engraved board letters and the direction, 0.6 mm deep on top
        translate([0, 0, T - 0.6]) linear_extrude(1) labels2d();
        // where S6 / S7 go, a 0.4 mm outline on top
        for (s = SPLICES) translate([0, 0, T - 0.4]) linear_extrude(1)
            difference() { rrect(s[0], s[1], s[2], s[3], 0.5); offset(delta = -0.6) rrect(s[0], s[1], s[2], s[3], 0.5); }
    }
}

module ghosts() {
    // board A / B / C at their heights, the splices, and the nuts on the tray's fixings
    for (b = [BOARD_A, BOARD_B]) color("green", 0.35) translate([b[0], b[2], T + 6]) cube([b[1] - b[0], b[3] - b[2], 1.6]);
    color("green", 0.35) translate([BOARD_C[0], BOARD_C[2], T + 10]) cube([BOARD_C[1] - BOARD_C[0], BOARD_C[3] - BOARD_C[2], 1.6]);
    for (s = SPLICES) color("orange", 0.8) translate([s[0], s[2], T]) cube([s[1] - s[0], s[3] - s[2], 8.5]);
    for (p = FIX) color("silver") translate([p[0], p[1], T]) cylinder(d = NUT_AF / cos(30), h = 2, $fn = 6);
}

if (PART == "tray") real() tray();
else if (PART == "template") real() {
    difference() { outline2d(); holes2d(); crosses2d(); offset(delta = 0.4) labels2d(); }
    // print check: this bar must measure exactly 50 mm on paper (print at 100 %, no "fit to page")
    translate([BOARD_C[0], BOARD_A[2] - 9]) difference() {
        square([50, 4]);
        translate([25, 2]) mirror([0, 1, 0]) text("50 mm", size = 2.6, halign = "center", valign = "center");
    }
}
else real() { color("lightgrey") tray(); ghosts(); }
