// NEXUS compute tray - one plate on plate 3 that carries the FRDM-IMX91S and the Raspberry Pi 5 (MEC-18)
//
//   openscad -D 'PART="tray"' -o compute-tray.stl                    compute-tray.scad   // to print
//   openscad -D 'PART="plan"' -o ../renders/compute-tray-plan.png    compute-tray.scad   // the boards ghosted on the tray, on plate 3
//
// STATUS 2026-10-06: PROPOSED, not printed, not ordered. Every item under "TO MEASURE" is a guess.
//
// FRAME. Plate 3's own: x from the front of the vehicle to the rear, y from the vehicle's RIGHT edge to its LEFT, mm
// (the layout frame of MEC-11 / MEC-15 / hardware/scripts/chassis-layout.py). With z up it is a mirror image of the real
// world, so every output passes through real() once. The tray's underside is z 0 and sits on plate 3's top face.
//
// WHAT THE TRAY HAS
//   - FRDM pad: the board's 105 x 65 footprint at its MEC-11 place. The board keeps its four M2.5 screws from BELOW,
//     up through plate 3's M3 grid holes (heads under the plate), now through the tray as well, into the standoffs on the
//     board. Those four screws are also what clamps the FRDM end of the tray down. Two of the board's six holes are unused, as in MEC-11.
//   - Pi pad ahead of it: the board's 85 x 56 footprint, turned so its Ethernet / USB edge faces the nose (the rear edge
//     would end 4 mm from the FRDM). Four M2.5 standoffs (PI_STANDOFF, 8 or 10 mm) carry it on its 58 x 49 pattern: a screw from
//     below through a counterbore in the tray into each standoff (the tray sits flat on plate 3), the Pi screwed on top.
//   - four M3 fixings in the Pi pad on plate 3's M3 holes, each a nut pocket on top, screw from below. A 28 x 14 rectangle,
//     so the pad cannot rock.
//   - a bridge joining the two pads, and one window over plate 3's wire opening (a cable can still come up there).
//
// TO MEASURE before printing (the defaults are guesses)
//   the Pi standoffs' thread (female-female assumed) and the M2.5 screw head height, for the counterbore
//   SD_WINDOWS    - the FRDM's microSD socket and its J1 / J11 cable landing: no window is cut for them yet
//   Pi 5 microSD  - its socket is on the underside at the board's end that now faces the FRDM, and the card leaves toward it

PART = "plan";               // "tray" | "plan"

T            = 4.0;          // tray thickness, as the carrier tray
R_CORNER     = 2.0;
FIX_D        = 3.4;          // M2.5 through the tray at the FRDM's holes: loose, so the plate hole is the only guide
FRDM_STANDOFF = 6.0;         // the metal standoffs the FRDM carries (Hedi, 2026-10-06)
PI_STANDOFF  = 8.0;          // 8 or 10 mm, Hedi's choice; only the preview uses it
PI_HOLE_D    = 3.4;          // M2.5 through the tray, loose like the FRDM's
PI_CB_D      = 6.4;          // counterbore from below for an M2.5 head, as the carrier tray (MEC-17)
PI_CB_DEPTH  = 2.4;          // 1.6 mm of floor remains
M3_NUT_AF    = 5.5;  M3_POCKET  = 5.9;  M3_DEPTH  = 2.6;     // as the Bauer's nuts (MEC-17)
FIX3_D       = 3.4;          // M3 through the tray, in a 3.18 plate hole

// ---- the boards, plate 3 frame -----------------------------------------------------------------------
FRDM = [95.74, 200.74, 20.26, 85.26];                         // MEC-11: hole (3.5, 3.5) lands on (99.24, 23.76)
FRDM_FIX = [[99.24, 23.76], [99.24, 81.76], [148.18, 23.76], [148.18, 81.76]];   // the four used, on plate 3's M3 grid

PI_X0 = 6.0;  PI_Y0 = 32.25;                                  // Pi footprint x 6-91, y 32.25-88.25, centred on the plate (y 60.25)
PI_L = 85;  PI_W = 56;
// the Pi's holes are 3.5 from its left short edge and 58 apart, 3.5 and 52.5 from a long edge; turned 180 degrees so the ports face the nose
PI_HOLES = [for (a = [3.5, 61.5]) for (b = [3.5, 52.5]) [PI_X0 + PI_L - a, PI_Y0 + PI_W - b]];

// plate 3's M3 holes under the Pi pad (3.18), a 28 x 14 rectangle
PAD_FIX = [[17.82, 53.24], [17.82, 67.24], [45.82, 53.24], [45.82, 67.24]];

// plate 3's wire opening, x 110.3-133.0, y 42.5-77.9: a stadium of radius 11.35 (MEC-17, same plate)
WINDOWS = [[[121.65, 53.85], [121.65, 66.55], 11.35]];

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
module stadium(s) hull() { translate(s[0]) circle(r = s[2], $fn = 64); translate(s[1]) circle(r = s[2], $fn = 64); }

module outline2d() union() {
    rrect(FRDM[0], FRDM[1], FRDM[2], FRDM[3]);
    rrect(PI_X0, PI_X0 + PI_L, PI_Y0, PI_Y0 + PI_W);
    for (p = PI_HOLES) translate(p) circle(d = PI_CB_D + 2.2, $fn = 48);       // a pad round each counterbore, so it never breaks the edge
    translate([PI_X0 + PI_L - 4, 42]) square([FRDM[0] - PI_X0 - PI_L + 8, 36]);   // the bridge
}

module holes2d() {
    for (p = FRDM_FIX) translate(p) circle(d = FIX_D, $fn = 32);
    for (p = PAD_FIX) translate(p) circle(d = FIX3_D, $fn = 32);
    for (p = PI_HOLES) translate(p) circle(d = PI_HOLE_D, $fn = 32);
    for (w = WINDOWS) stadium(w);
}

module real() mirror([0, 1, 0]) children();

module trayBody() difference() {
    linear_extrude(T) difference() { outline2d(); holes2d(); }
    // counterbores from below for the Pi's screw heads, so the tray sits flat on plate 3
    for (p = PI_HOLES) translate([p[0], p[1], -0.01]) cylinder(d = PI_CB_D, h = PI_CB_DEPTH, $fn = 32);
    // the pad's M3 nuts: pocket open on top, flush with the tray, screw from below
    for (p = PAD_FIX) translate([p[0], p[1], T - M3_DEPTH]) cylinder(d = M3_POCKET / cos(30), h = M3_DEPTH + 0.01, $fn = 6);
}

// ---- previews ---------------------------------------------------------------------------------------------
module board_ghost(x0, x1, y0, y1, z, c) color(c, 0.55) translate([x0, y0, z]) cube([x1 - x0, y1 - y0, 1.6]);
if (PART == "tray") real() trayBody();
else if (PART == "plan") real() {
    color("lightgrey") trayBody();
    board_ghost(FRDM[0], FRDM[1], FRDM[2], FRDM[3], T + FRDM_STANDOFF, "royalblue");
    board_ghost(PI_X0, PI_X0 + PI_L, PI_Y0, PI_Y0 + PI_W, T + PI_STANDOFF, "seagreen");
    for (p = PI_HOLES) color("silver") translate([p[0], p[1], T]) cylinder(d = 5, h = PI_STANDOFF, $fn = 24);
}
