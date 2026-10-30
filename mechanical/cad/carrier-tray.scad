// NEXUS carrier tray - one plate that carries boards A, B and C, bolted to plate 2 (MEC-17)
//
//   openscad -D 'PART="tray"'     -o carrier-tray.stl                  carrier-tray.scad   // to print
//   openscad -D 'PART="template"' -o ../renders/tray-template.svg      carrier-tray.scad   // 1:1, to cut a sheet by hand
//   openscad -D 'PART="step1"'    -o ../renders/tray-step1-boards.png  carrier-tray.scad   // 1: boards placed on the tray
//   openscad -D 'PART="step2"'    -o ../renders/tray-step2-plate2.png  carrier-tray.scad   // 2: the tray placed on plate 2
//
// STATUS 2026-10-06: fit-reviewed for one print (MEC-17, "Fit review before ordering"). Print it (PETG, 4 mm); a hand-cut sheet is the fallback.  ORDERED 2026-10-06 (Craftcloud, BOM 3.28), not printed yet.
// 2026-10-26: board B is now a 3x7 (MEC-15), at tray v 76.04-106.04. This file stays as ordered: B's outboard pair of holes takes the 3x7's
// outboard corners, B's inboard pair stays empty, and one hole is drilled by hand at tray (178.54, 78.54) = plate 2 (187.04, 83.65) for B's
// rear inboard corner. It is 2.5 mm from the tray's edge, where there is no corner pad, so no counterbore: a 2.1 mm hole and an 8 mm
// male-female standoff screwed into it, its stud cut to 3.5 mm. B's front inboard corner takes no screw (MEC-17).
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
//   - six fixing holes that land on six of those plate holes (T1-T6), each with a hex pocket
//     on top that captures an M2.5 nut, so the tray comes off with a screw per fixing from BELOW; plus two M3 pockets
//     under the Bauer's two mounting holes;
//   - twelve board holes, four per board (M2.5 clearance), with counterbores from below so the tray sits
//     flat; boards go on the nylon standoffs already fitted;
//   - the window over plate 2's wire opening, where the UBEC's 6 V pair climbs to the top face; the S6 / S7 wires come up
//     the plate's two tie slots beside the Bauer.
//   The S6 / S7 splices sit on the tray in a lane either side of the Bauer.
//
// HEIGHTS. All three boards keep the 8 mm standoffs already fitted (Hedi, 2026-10-05; not measured with a gauge), so they
// stand 12 mm above plate 2: 4 mm tray + 8 mm. The 8.5 mm S6 / S7 splices do not fit under C at that height, so they sit beside the Bauer. Check the Discovery's top against the FRDM's screw heads under plate 3.
//
// TO MEASURE before printing (the defaults are guesses):
//   CORNER_INSET  - a board's corner hole centre from each edge (estimated 2.5 mm; the loose holes and the corner pads cover +-0.5)
//   board C's holes once it is built

PART = "step2";              // "tray" | "template" | "step1" | "step2" | "outline"

T            = 4.0;          // tray thickness
CORNER_INSET = 2.5;          // ESTIMATED, not measured (+-0.5): board corner hole centre from each edge; see MEC-17
HOLE_D       = 4.0;          // M2.5 screw in a deliberately loose hole: +-0.75 mm, less ~0.1 mm a printed hole loses. Absorbs the inset
                             // estimate above (+-0.5) and the hand-widened board holes; the standoff base (5 across flats) still bears on the tray
CB_D         = 6.4;          // counterbore for an M2.5 nylon screw head, from below; a head 0.5 mm off centre still sits inside it
BOSS_R       = 4.6;          // a round pad round each board corner, so the counterbore never breaks the tray's edge
CB_DEPTH     = 2.4;          // a head up to 2.2 mm tall leaves the tray flat on plate 2; 1.6 mm of floor remains
FIX_D        = 3.4;          // tray-to-plate-2 screws, M2.5 from below; loose, so the NUT locates the screw and the plate hole is the only guide
NUT_AF       = 5.0;          // M2.5 nut across flats
NUT_POCKET   = 5.4;          // pocket across flats: 0.4 mm over the nut, a printing fit (a printed hex comes out ~0.1-0.2 small)
NUT_DEPTH    = 2.4;          // M2.5 nut is 2.0 thick
R_CORNER     = 2.0;
WALL         = 1.5;          // least tray left between a copied plate hole and the tray's edge

// ---- STEP 1: the boards on the tray (tray frame, mm) ------------------------------------------------
// board = [u0, u1, v0, v1]. A and B as built 2026-10-03 (A one pitch ahead of B, 5.88 mm apart across
// the tray); C across the waist, 1.5 mm from A.
BOARD_A = [108.50, 178.50,   0.00,  50.00];
BOARD_B = [111.04, 181.04,  55.88, 105.88];
BOARD_C = [ 77.00, 107.00,  20.09,  90.09];
BOARDS  = [BOARD_A, BOARD_B, BOARD_C];

// ---- STEP 2: the tray on plate 2 ------------------------------------------------------------------------
PLACE = [ 8.50, 5.11];       // plate-2 position of the tray frame's origin: the front edge of the Bauer's end

// plate 2's holes under the tray, from the chassis layout (hardware/renders/chassis-layout.svg): [x, y, d].
// Left out because the tray cannot hold them: (99.24, 23.76/96.76), (104.41, 19.59/100.94) and
// everything ahead of x 17.5 are outside it; (16.94, 32.24/88.24) and (17.82, 53.24/67.24) are on its front edge;
// (186.12, 9.71/110.82) sit 2.5 mm from A's and B's rear corner holes; the long side slots
// (x 109-158, y 10-15 and 105-111) run off the tray's front edge.
// The six plate holes the tray is screwed down with, T1-T6 (MEC-15's F1-F6 were the direct-fixing scheme this replaces). Chosen
// because their screw heads, with a washer in the M3 holes, are at least 0.8 mm clear of every part taped under plate 2 (MEC-17);
// the holes the old scheme used (148.18, 23.76), (148.18, 72.24) and (99.24, 38.76) are 2.2, 2.2 and 1.2 mm from a fuse holder or a bus.
FIXINGS = [
    [ 24.82, 60.24, 3.18], // T1  under the Bauer, on the plate's M3 line along y 60.24; M3 hole, M2.5 screw and a washer
    [ 52.82, 60.24, 3.18], // T2  under the Bauer
    [ 99.24, 81.76, 3.18], // T3  under board C (MEC-15's F6)
    [120.06, 35.94, 2.71, 1.0], // T4  under board A; M2.5 hole, no washer. The plate hole is only 2.71 (+-0.1 slack), so the nut pocket and the
                                //     hole are slotted 1.0 mm along the tray's length: the nut can sit 0.5 mm either way (a print scaling error acts along u)
    [148.18, 81.76, 3.18], // T5  under board B
    [148.18, 96.76, 3.18], // T6  under board B, near its rear-left corner
];
PLATE_HOLES = [
    [ 96.71,  52.65, 2.71], [ 96.71,  67.88, 2.71], [102.18,  48.24, 2.71], [102.18,  72.24, 2.71],
    [120.06,  84.53, 2.71], [143.47,  52.65, 2.71], [143.47,  67.88, 2.71],
    [148.18,  23.76, 3.18], [148.18,  38.76, 3.18], [148.18,  48.24, 2.71], [148.18,  72.24, 2.71], [ 99.24,  38.76, 3.18],
    [162.06,  16.71, 2.47], [162.06, 103.82, 2.47],
    [169.88,  14.24, 2.71], [169.88,  20.24, 2.71], [169.88, 100.24, 2.71], [169.88, 106.24, 2.71],
    [ 92.65,  36.35, 4.30], [ 92.65,  84.25, 4.30],
    // under the Bauer (x 8.5-87): the plate's M3 line along y 60.24 and its diamond, the M2.5 pairs, the 4.2 and 4.3 mm holes.
    // Not copied: the two 9 mm holes (x 17.9 and 45.85, y 60.3), (10.82, 60.24), (17.82, 53.24 and 67.24) and (72.41, 67.88):
    // they run into a nut pocket or the tray's front edge.
    [ 38.82,  60.24, 3.18], [ 45.82,  53.24, 3.18], [ 45.82,  67.24, 3.18], 
    [ 16.94,  32.24, 2.71], [ 16.94,  88.24, 2.71], [ 25.65,  52.65, 2.71], [ 25.65,  67.88, 2.71],
    [ 49.00,  35.94, 2.71], [ 49.00,  84.53, 2.71], [ 72.41,  52.65, 2.71],
    [ 86.94,  40.24, 2.71], [ 86.94,  80.24, 2.71],
    [ 12.65,  36.35, 4.29], [ 12.65,  84.25, 4.29], 
    [ 43.50,  36.33, 4.29], [ 43.50,  84.21, 4.29], [ 45.86,  44.27, 4.29], [ 45.86,  76.27, 4.29],
    [ 36.09,  35.91, 4.18], [ 36.09,  84.56, 4.18],
];
// the plate's slots, as the two end-circle centres and the radius: the large one at x 161.2-175.8, y 30.4-90.2,
// and the pair beside the Bauer, x 56.2-80.1, y 26.9-37.2 and 83.2-93.5, where the plate takes cable ties
PLATE_SLOTS = [ [[168.5, 37.7], [168.5, 82.9], 7.3], [[61.35, 32.09], [74.89, 32.09], 5.15], [[61.35, 88.33], [74.89, 88.33], 5.15] ];
// The four chassis standoffs stand on plate 2's top face (6.0 mm across flats, 40 mm up to plate 3), so the tray must stay clear of the two
// under its Bauer end. Found 2026-10-06: the tray was solid over both (22.8 mm2 of overlap each, either hex orientation) and would have rested
// on the two hexes instead of the plate. STANDOFF_CLEAR_D is the hex's corner-to-corner 6.93 plus 2.1 mm for the print and the survey (it also swallows the lane corner at (24, 100.9) cleanly: 8.4 left a zero-area sliver). The 4.29 mm
// copies of the plate's holes at those two places are dropped from PLATE_HOLES: the notch replaces them.
CHASSIS_STANDOFFS = [[27.35, 22.17], [27.35, 98.36]];       // from the chassis layout: x, y in the plate-2 frame
STANDOFF_CLEAR_D  = 9.0;
// the Bauer 50 W converter: base 64 x 57 x 22 mm (BOM 3.4a), the body about 64 x 64.5 with its side walls; plate1.py still parks it at x 20-84, y 32-89 (BAUER below says where it goes now).
// Its drawing (the seller's, 2026-10-05; the drawing calls them ears): two 6.8 mm holes INSIDE the outline, 5 mm in from each end, 54 mm apart,
// 26 mm from one long edge of the base (30 from the wall). The photo (2026-10-05) shows that is the edge the four leads leave from, through the middle of the
// plateau. That edge is put on the vehicle's LEFT (wall at y 93), facing board C's 5 V terminals, with a 3 mm lane to the S6 splice.
// They take M3 screws from above into nuts held in the tray: one pocket under each hole.
BAUER = [11.0, 75.0, 28.5, 93.0];     // 9 mm ahead of where plate1.py parks it: 10.5 mm between its rear end and board C, for the leads and the 5 V cable. From Hedi's photo on 5 mm paper (2026-10-06): the side walls stand 3.5-4 mm outside the 57 mm base, so ~64.5 wide, leads wall at y 93, not 89.
                                      // Its fin tips reach ~5 mm further than the tabs at the FRONT end (x ~6). Holes unchanged: measured 54 mm apart, ~5 mm from each tab end.
                                      BAUER_HOLES = [[16.0, 63.0, 3.2], [70.0, 63.0, 3.2]];   // x, y, hole: 54 apart, 5 from each tab end; 30 from the leads wall (the drawing's 26 is to the base)
BAUER_NUT_AF = 5.9; BAUER_NUT_DEPTH = 2.6;            // M3 nut, 5.5 across flats and 2.4 thick, as a printing fit
// the plate's wire opening, x 110.3-133.0, y 42.5-77.9, a stadium of radius 11.35
PLATE_OPENING = [[121.65, 53.85], [121.65, 66.55], 11.35];
// the window: the opening up to x 115, clear of A's front-inboard corner counterbore
WINDOW_X1 = 115.0;

// the S6 / S7 splices (Bauer + and -), 18.6 x 13 x 8.5, plate-2 frame. They do not fit under C on 8 mm standoffs, so they sit
// in two lanes either side of the Bauer, beside the plate's two tie slots, which bring up the wires from SW2 and the bus.
// The Bauer's leads leave on the left (y 89): + goes to S6 there, - runs round the Bauer's rear to S7. Plate 2 is symmetric
// about y 60.25, so the right lane is the left one mirrored.
SPLICES = [[42.0, 60.6, 96.0, 109.0], [42.0, 60.6, 11.5, 24.5]];
LANE_L = [[24, 100.9], [34, 107.0], [39.5, 110.0], [60.6, 110.0], [64, 106.0], [70, 100.5], [80, 100.5], [80, 89], [24, 89]];   // 1.5 mm inside the plate edge
LANE_R = [for (p = LANE_L) [p[0], 120.5 - p[1]]];

// the Bauer's end: from 2.5 mm ahead of the converter to 1.5 mm into board C's footprint, as wide as C
EXT = [0.0, BOARD_C[0] + 1.5, BOARD_C[2], BOARD_C[3]];     // its front is narrowed in outline2d(): plate 2 narrows there
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
        for (b = BOARDS) for (p = corners(b)) translate(p) circle(r = BOSS_R, $fn = 48);       // corner pads
        rrect(BOARD_C[1] - 3, BOARD_A[0] + 3, BOARD_C[2], BOARD_C[3]);
        for (L = [LANE_L, LANE_R]) polygon([for (p = L) tray(p)]);       // the two splice lanes beside the Bauer
        hull() {                                               // the Bauer's end of the tray, narrower at the front where plate 2 is
            rrect(EXT[0], EXT[0] + 4, EXT[2] + 3.8, EXT[3] - 3.7, 1.0);
            rrect(EXT[0] + 15.5, EXT[1], EXT[2], EXT[3]);
        }
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

// a fixing's hole: round, or a slot f[3] mm long along the tray's length (u) when the entry has a fourth value
module fixslot2d(f, d) {
    sl = len(f) > 3 ? f[3] : 0;
    hull() for (k = [-1, 1]) translate([k * sl / 2, 0]) circle(d = d, $fn = 32);
}

module holes2d() {
    for (b = BOARDS) for (p = corners(b)) translate(p) circle(d = HOLE_D, $fn = 32);
    for (f = FIXINGS) translate(tray(f)) fixslot2d(f, FIX_D);
    for (s = CHASSIS_STANDOFFS) translate(tray(s)) circle(d = STANDOFF_CLEAR_D, $fn = 48);
    for (e = BAUER_HOLES) translate(tray(e)) circle(d = e[2], $fn = 32);
    for (h = PLATE_HOLES) translate(tray(h)) circle(d = h[2], $fn = 32);
    for (sl = PLATE_SLOTS) stadium(sl);
    window2d();
}

module labels2d(h = 6) {
    word([132, 12], "A", h);
    word([132, 94], "B", h);
    word([92, 55], "C", h);
    word([137, 52.9], "REAR >", 3.5);
    word([45, 12], "BAUER", 4);
}

// a drilling cross through each board hole and fixing, for the hand-cut sheet
module crosses2d()
    for (p = concat([for (b = BOARDS) for (c = corners(b)) c], [for (f = FIXINGS) tray(f)], [for (e = BAUER_HOLES) tray(e)]))
        translate(p) { square([7, 0.35], center = true); square([0.35, 7], center = true); }

module trayBody() {
    union() {
    difference() {
        linear_extrude(T) difference() { outline2d(); holes2d(); }
        // counterbores from below for the board screws, so the tray sits flat on plate 2
        for (b = BOARDS) for (p = corners(b)) translate([p[0], p[1], -0.01]) cylinder(d = CB_D, h = CB_DEPTH, $fn = 32);
        // a hex pocket on top at each fixing, holding the nut so the screw turns from below
        for (f = FIXINGS) translate([tray(f)[0], tray(f)[1], T - NUT_DEPTH]) linear_extrude(NUT_DEPTH + 0.01)
            hull() for (k = [-1, 1]) translate([k * (len(f) > 3 ? f[3] : 0) / 2, 0]) circle(d = NUT_POCKET / cos(30), $fn = 6);
        // and a larger one under each of the Bauer's two holes, for an M3 nut
        for (e = BAUER_HOLES) translate([tray(e)[0], tray(e)[1], T - BAUER_NUT_DEPTH])
            cylinder(d = BAUER_NUT_AF / cos(30), h = BAUER_NUT_DEPTH + 0.01, $fn = 6);
        // engraved board letters and the direction, 0.6 mm deep on top
        translate([0, 0, T - 0.6]) linear_extrude(1) labels2d();
        // where S6 / S7 go, a 0.4 mm outline on top
        for (s = SPLICES) translate([0, 0, T - 0.4]) linear_extrude(1)
            difference() { translate(-PLACE) rrect(s[0], s[1], s[2], s[3], 0.5); offset(delta = -0.6) translate(-PLACE) rrect(s[0], s[1], s[2], s[3], 0.5); }
    }
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
    for (b = [BOARD_A, BOARD_B]) color("seagreen") board_ghost(b, T + 8, solid);
    color("seagreen") board_ghost(BOARD_C, T + 10, solid);
    for (b = BOARDS) for (p = corners(b)) color("gold") translate([p[0], p[1], T + 8.1]) cylinder(d = 3, h = 1, $fn = 20);
    for (s = SPLICES) color("orange", 0.8) translate([tray([s[0], s[2]])[0], tray([s[0], s[2]])[1], T]) cube([s[1] - s[0], s[3] - s[2], 8.5]);
    for (f = FIXINGS) color("silver") translate([tray(f)[0], tray(f)[1], T - NUT_DEPTH]) cylinder(d = NUT_AF / cos(30), h = 2, $fn = 6);
    for (e = BAUER_HOLES) color("gold") translate([tray(e)[0], tray(e)[1], T - 2.4]) cylinder(d = 5.5 / cos(30), h = 2.4, $fn = 6);
    color("steelblue", 0.7) translate([tray([BAUER[0], BAUER[2]])[0], tray([BAUER[0], BAUER[2]])[1], T]) cube([BAUER[1] - BAUER[0], BAUER[3] - BAUER[2], 22]);
}

// plate 2 as a ghost slab 2 mm thick below z 0, drawn in the tray frame: its holes, slot and opening
module ghost_plate() {
    color("slategray", 0.75) translate([0, 0, -2]) linear_extrude(2) difference() {
        translate([-20, -20]) square([240, 160]);
        for (h = PLATE_HOLES) translate(tray(h)) circle(d = h[2], $fn = 24);
        for (f = FIXINGS) translate(tray(f)) circle(d = f[2], $fn = 24);
        for (p = [[72.41, 52.65, 2.71], [72.41, 67.88, 2.71], [99.24, 23.76, 3.18], [99.24, 96.76, 3.18], [104.41, 19.59, 3.18], [104.41, 100.94, 3.18],
                  [86.94, 40.24, 2.71], [86.94, 80.24, 2.71], [186.12, 9.71, 3.18], [186.12, 110.82, 3.18]]) translate(tray(p)) circle(d = p[2], $fn = 24);
        for (sl = PLATE_SLOTS) stadium(sl);
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
// the tray's outline alone, in the layout frame (plate 2's x, y after adding PLACE), for the layout drawing
else if (PART == "outline") outline2d();
else if (PART == "step1") real() { color("lightgrey") trayBody(); ghost_boards(); }
// step 2: the same, set down on plate 2 over the plate's holes
else if (PART == "step2") real() { color("lightgrey") trayBody(); ghost_boards(); ghost_plate(); }
