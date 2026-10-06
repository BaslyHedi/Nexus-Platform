// NEXUS compute tray - one plate on plate 3 that carries the FRDM-IMX91S and the Raspberry Pi 5 (MEC-18)
//
//   openscad -D 'ORIENT="along"'  -D 'PART="tray"' -o compute-tray.stl         compute-tray.scad   // boards along the vehicle, Pi in the nose
//   openscad -D 'ORIENT="across"' -D 'PART="tray"' -o compute-tray-across.stl  compute-tray.scad   // boards turned 90 degrees, nose free
//
// STATUS 2026-10-06: PROPOSED, not printed, not ordered. Two orientations are modelled so they can be compared; Hedi picks one.
// Every item under "TO MEASURE" is a guess.
//
// FRAME. Plate 3's own: x from the front of the vehicle to the rear, y from the vehicle's RIGHT edge to its LEFT, mm
// (the layout frame of MEC-11 / MEC-15 / hardware/scripts/chassis-layout.py). With z up it is a mirror image of the real
// world, so every output passes through real() once. The tray's underside is z 0 and sits on plate 3's top face.
//
// ORIENT = "along"  (the default, MEC-18 as first proposed)
//   - FRDM pad at its MEC-11 place (x 95.7-200.7). The board keeps its four M2.5 screws from BELOW, up through plate 3's M3
//     grid holes and the tray, into its 6 mm standoffs; those four screws also clamp this end of the tray.
//   - Pi pad ahead of it (x 6-91), turned so its Ethernet / USB edge faces the nose. The nose is taken.
// ORIENT = "across"  (both boards turned 90 degrees, long edges across the vehicle)
//   - Pi x 98-154, FRDM x 158-223, both centred on the plate. The whole nose (x 0-98) is free (the LED front), and the rear is
//     left for the cables that climb from the fascia panel. The Pi's ports face the vehicle's RIGHT, its GPIO header the nose.
//     The FRDM's orientation of its ports is unknown; it is turned the same way (its u axis toward the right side).
//   - The FRDM no longer lands on plate 3's grid, so all SIX of its standoffs are screwed to the tray from below through
//     counterbores, like the Pi's. The tray is held to plate 3 by four fixings (two M3 nuts, two M2.5 nuts).
//
// BOTH: the Pi stands on four M2.5 standoffs (PI_STANDOFF, 8 or 10 mm), a screw from below through a counterbore in the tray
// (the tray sits flat), the Pi screwed on top. Assemble the screws and standoffs at the bench BEFORE the tray goes onto plate 3.
// One window over plate 3's wire opening keeps a cable route in the "along" layout.
//
// TO MEASURE before printing (the defaults are guesses)
//   the Pi standoffs' thread (female-female assumed) and the M2.5 screw head height, for the counterbore
//   where the FRDM's microSD socket and J1 / J11 plugs are (no window is cut for them); and the FRDM's ports, to choose its turn

ORIENT = "along";            // "along" | "across"
PART   = "plan";             // "tray" | "plan" | "lib" (a preview file includes this one)

T            = 4.0;          // tray thickness, as the carrier tray
R_CORNER     = 2.0;
FIX_D        = 3.4;          // M2.5 through the tray at the FRDM's grid holes ("along"): loose, the plate hole is the only guide
FRDM_STANDOFF = 6.0;         // the metal standoffs the FRDM carries (Hedi, 2026-10-06)
PI_STANDOFF  = 8.0;          // 8 or 10 mm, Hedi's choice; only the preview uses it
PI_HOLE_D    = 3.4;          // M2.5 through the tray, loose
PI_CB_D      = 6.4;          // counterbore from below for an M2.5 head, as the carrier tray (MEC-17)
PI_CB_DEPTH  = 2.4;          // 1.6 mm of floor remains
M25_POCKET   = 5.4;  M25_DEPTH = 2.4;     // M2.5 nut across flats 5.0, as the carrier tray
M3_POCKET    = 5.9;  M3_DEPTH  = 2.6;     // M3 nut across flats 5.5, as the Bauer's nuts (MEC-17)
FIX3_D       = 3.4;          // M3 through the tray, in a 3.18 plate hole
FIX25_D      = 3.2;          // M2.5 through the tray, in a 2.71 plate hole

ACROSS = (ORIENT == "across");

// ---- the boards, plate 3 frame -----------------------------------------------------------------------
// FRDM board frame (u along the 105 mm, v along the 65 mm; MEC-11's datum: (3.5, 3.5) lands on (99.24, 23.76) when "along")
FRDM_X0 = ACROSS ? 158.0 : 95.74;   FRDM_Y0 = ACROSS ? 7.75 : 20.26;
function frdm_at(u, v) = ACROSS ? [FRDM_X0 + v, FRDM_Y0 + 105 - u] : [FRDM_X0 + u, FRDM_Y0 + v];
FRDM = ACROSS ? [FRDM_X0, FRDM_X0 + 65, FRDM_Y0, FRDM_Y0 + 105] : [FRDM_X0, FRDM_X0 + 105, FRDM_Y0, FRDM_Y0 + 65];
FRDM_HOLES6 = [for (h = [[3.5, 3.5], [3.5, 61.5], [52.5, 3.5], [52.5, 61.5], [101.5, 23.0], [101.5, 61.5]]) frdm_at(h[0], h[1])];
FRDM_FIX = [[99.24, 23.76], [99.24, 81.76], [148.18, 23.76], [148.18, 81.76]];   // "along": the four used, on plate 3's M3 grid

// Pi board frame (a along the 85 mm, b along the 56 mm, b measured from the GPIO edge; its holes are 3.5 and 61.5 along a, 3.5 and 52.5 along b)
PI_X0 = ACROSS ? 98.0 : 6.0;   PI_Y0 = ACROSS ? 17.75 : 32.25;
PI_L = 85;  PI_W = 56;
function pi_at(a, b) = ACROSS ? [PI_X0 + b, PI_Y0 + PI_L - a] : [PI_X0 + PI_L - a, PI_Y0 + PI_W - b];
PI_BBOX = ACROSS ? [PI_X0, PI_X0 + PI_W, PI_Y0, PI_Y0 + PI_L] : [PI_X0, PI_X0 + PI_L, PI_Y0, PI_Y0 + PI_W];
PI_HOLES = [for (a = [3.5, 61.5]) for (b = [3.5, 52.5]) pi_at(a, b)];

// the tray's fixings to plate 3: [x, y, plate hole d]. "along": plate 3's M3 holes under the Pi pad, a 28 x 14 rectangle.
// "across": two M3 (196.88, 38.76 and 81.77) and two M2.5 (169.88, 20.23 and 100.23) under the FRDM pad, and two M3 under the Pi pad
// (99.24 and 148.18, 81.77 and 23.76 are 3.4 mm from the Pi's holes, so the Pi pad takes the grid's 23.76 / 81.77 rows, 17.6 mm clear).
PAD_FIX = ACROSS ? [[99.24, 23.76, 3.18], [99.24, 81.77, 3.18], [148.18, 23.76, 3.18], [148.18, 81.77, 3.18],
                    [196.88, 38.76, 3.18], [196.88, 81.77, 3.18], [169.88, 20.23, 2.71], [169.88, 100.23, 2.71]]
                  : [[17.82, 53.24, 3.18], [17.82, 67.24, 3.18], [45.82, 53.24, 3.18], [45.82, 67.24, 3.18]];

// plate 3's wire opening, x 110.3-133.0, y 42.5-77.9: a stadium of radius 11.35 (MEC-17, same plate); kept as a cable window
WINDOWS = [[[121.65, 53.85], [121.65, 66.55], 11.35]];

// the counterbored holes: every Pi hole, and in "across" all six FRDM holes
CB_HOLES = ACROSS ? concat(PI_HOLES, FRDM_HOLES6) : PI_HOLES;

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
module stadium(s) hull() { translate(s[0]) circle(r = s[2], $fn = 64); translate(s[1]) circle(r = s[2], $fn = 64); }

module outline2d() union() {
    rrect(FRDM[0], FRDM[1], FRDM[2], FRDM[3]);
    rrect(PI_BBOX[0], PI_BBOX[1], PI_BBOX[2], PI_BBOX[3]);
    for (p = CB_HOLES) translate(p) circle(d = PI_CB_D + 2.2, $fn = 48);       // a pad round each counterbore, so it never breaks the edge
    translate([PI_BBOX[1] - 4, 42]) square([FRDM[0] - PI_BBOX[1] + 8, 36]);          // the bridge
}

module holes2d() {
    if (!ACROSS) for (p = FRDM_FIX) translate(p) circle(d = FIX_D, $fn = 32);
    for (f = PAD_FIX) translate([f[0], f[1]]) circle(d = f[2] > 3 ? FIX3_D : FIX25_D, $fn = 32);
    for (p = CB_HOLES) translate(p) circle(d = PI_HOLE_D, $fn = 32);
    for (w = WINDOWS) stadium(w);
}

module real() mirror([0, 1, 0]) children();

module trayBody() difference() {
    linear_extrude(T) difference() { outline2d(); holes2d(); }
    // counterbores from below for the standoff screws, so the tray sits flat on plate 3
    for (p = CB_HOLES) translate([p[0], p[1], -0.01]) cylinder(d = PI_CB_D, h = PI_CB_DEPTH, $fn = 32);
    // the fixings' nuts: pocket open on top, flush with the tray, screw from below
    for (f = PAD_FIX) translate([f[0], f[1], T - (f[2] > 3 ? M3_DEPTH : M25_DEPTH)])
        cylinder(d = (f[2] > 3 ? M3_POCKET : M25_POCKET) / cos(30), h = (f[2] > 3 ? M3_DEPTH : M25_DEPTH) + 0.01, $fn = 6);
}

// ---- previews -----------------------------------------------------------------------------------------------
module board_ghost(x0, x1, y0, y1, z, c) color(c, 0.55) translate([x0, y0, z]) cube([x1 - x0, y1 - y0, 1.6]);
if (PART == "tray") real() trayBody();
else if (PART == "plan") real() {
    color("lightgrey") trayBody();
    board_ghost(FRDM[0], FRDM[1], FRDM[2], FRDM[3], T + FRDM_STANDOFF, "royalblue");
    board_ghost(PI_BBOX[0], PI_BBOX[1], PI_BBOX[2], PI_BBOX[3], T + PI_STANDOFF, "seagreen");
    for (p = PI_HOLES) color("silver") translate([p[0], p[1], T]) cylinder(d = 5, h = PI_STANDOFF, $fn = 24);
}
