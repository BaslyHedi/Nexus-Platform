// NEXUS compute tray - one plate on plate 3: spare pad in the nose, the FRDM-IMX91S in the middle, a Raspberry Pi 5 behind (MEC-18)
//
//   openscad -D 'PART="tray"' -o compute-tray.stl compute-tray.scad     // to print
//   compute-tray-preview.scad draws it with the boards, plate 3 and the screws (the renders)
//
// STATUS 2026-10-06: PROPOSED, not printed, not ordered. Read "TO MEASURE" before ordering.
//
// FRAME. Plate 3's own: x from the front of the vehicle to the rear, y from the vehicle's RIGHT edge to its LEFT, mm
// (the layout frame of MEC-11 / MEC-15 / hardware/scripts/chassis-layout.py). With z up it is a mirror image of the real
// world, so every output passes through real() once. The tray's underside is z 0 and sits on plate 3's top face.
//
// WHY THIS ARRANGEMENT (the connector positions are from NXP's FRDM-IMX91S Quick Start Guide, figures 1 and 2; see MEC-18)
//   The FRDM lies along the vehicle, its 40-pin header (left edge in the guide's top view) toward the NOSE, so a ribbon reaches a
//   Sense HAT up front. Its USB-C DBG (J11), USB-C and USB-A (right edge) face the REAR, where the fascia's USB-C extension is. Its
//   Ethernet, power J1 and audio jack (bottom edge) face the vehicle's LEFT; its 2x5 CAN header J7 and, on the underside, the
//   microSD slot (top edge) face the RIGHT. The board is turned no further than MEC-11 already had it.
//   NOSE PAD   x 8-75: plain 4 mm plate, four fixings, nothing else. Drill it for whatever comes next (a Sense HAT is 65 x 56).
//   FRDM PAD   its footprint, x 72-167. Its four screws go in from the tray's underside through counterbores into the 6 mm standoffs.
//   PLUG GAP   x 167-196: no tray except two narrow ribs at the plate's edges. A USB plug needs about 25 mm beyond the board's
//              rear edge, and plate 3's slot at x 187.5-191.8 is where the cables from the fascia come up to J11, J5 and the USB-A.
//   Pi PAD     behind the gap, turned across the vehicle, ports to the LEFT (next to the FRDM's Ethernet), GPIO to the rear.
//
// TO MEASURE before ordering (the defaults are guesses)
//   FRDM_L   - the board's length. The Quick Start Guide's photos give 95 mm (the repo's 105 is the non-S board's); measure it
//   its two rear mounting holes (about u 91.5) - not screwed, the standoffs just stand on the tray
//   the Pi standoffs' thread (female-female assumed) and the M2.5 screw head height, for the counterbore

PART = "tray";               // "tray" | "plan" | "lib" (the preview file includes this one)

T            = 4.0;          // tray thickness, as the carrier tray
R_CORNER     = 2.0;
FRDM_STANDOFF = 6.0;         // the metal standoffs the FRDM carries (Hedi, 2026-10-06)
PI_STANDOFF  = 8.0;          // 8 or 10 mm, Hedi's choice; only the preview uses it
PI_HOLE_D    = 3.4;          // M2.5 through the tray, loose
PI_CB_D      = 6.4;          // counterbore from below for an M2.5 head, as the carrier tray (MEC-17)
PI_CB_DEPTH  = 2.4;          // 1.6 mm of floor remains
M25_POCKET   = 5.4;  M25_DEPTH = 2.4;     // M2.5 nut across flats 5.0, as the carrier tray
M3_POCKET    = 5.9;  M3_DEPTH  = 2.6;     // M3 nut across flats 5.5, as the Bauer's nuts (MEC-17)
FIX3_D       = 3.4;          // M3 through the tray, in a 3.18 plate hole
FIX25_D      = 3.2;          // M2.5 through the tray, in a 2.71 plate hole
FIX_PAD_D    = 8.4;          // a round pad round each fixing and counterbore, so none breaks the tray's edge

// ---- the boards, plate 3 frame -----------------------------------------------------------------------
// FRDM board frame: u along the long edge, v along the short one, as in the Quick Start Guide's top view (40-pin header at u 0).
FRDM_X0 = 72.0;   FRDM_Y0 = 20.26;       // 23.7 mm ahead of MEC-11's place, to leave the plug gap; it no longer lands on plate 3's grid
FRDM_L  = 95.0;   FRDM_W  = 65.0;        // 95 is from the Quick Start Guide photo (+-1); the non-S board is 105
FRDM = [FRDM_X0, FRDM_X0 + FRDM_L, FRDM_Y0, FRDM_Y0 + FRDM_W];
FRDM_SCREWS = [for (u = [3.5, 52.5]) for (v = [3.5, 61.5]) [FRDM_X0 + u, FRDM_Y0 + v]];   // the four screwed from below, MEC-11's datum
FRDM_FREE = [for (v = [3.5, 61.5]) [FRDM_X0 + FRDM_L - 3.5, FRDM_Y0 + v]];                 // the two rear standoffs: they just stand on the tray

// Pi board frame: a along the 85 mm (ports at a = 85), b the 56 mm measured from the GPIO edge. Holes at a 3.5 / 61.5, b 3.5 / 52.5.
// Turned so the ports face the vehicle's left (+y) and the GPIO header the rear: x = PI_X0 + 56 - b, y = PI_Y0 + a.
PI_X0 = 196.0;  PI_Y0 = 17.75;
PI_L = 85;  PI_W = 56;
function pi_at(a, b) = [PI_X0 + PI_W - b, PI_Y0 + a];
PI_BBOX = [PI_X0, PI_X0 + PI_W, PI_Y0, PI_Y0 + PI_L];
PI_HOLES = [for (a = [3.5, 61.5]) for (b = [3.5, 52.5]) pi_at(a, b)];

// nose pad
NOSE = [8.0, 75.0, 32.25, 88.25];       // 5 mm inside the plate's outline at the front

// the tray's fixings to plate 3: [x, y, plate hole d]. All on plate 3's own holes, 17 mm or more from every standoff hole.
// FRDM pad: M3 (99.24 and 148.18, 38.76 and 81.77). Nose: M2.5 (49, 35.94 and 84.53), M3 (17.82, 53.24 and 67.24).
// Pi pad: M3 (245.88, 38.76 and 96.77), M2.5 (227.88, 20.23 and 100.23).
PAD_FIX = [[99.24, 38.76, 3.18], [99.24, 81.77, 3.18], [148.18, 38.76, 3.18], [148.18, 81.77, 3.18],
           [49.0, 35.94, 2.71], [49.0, 84.53, 2.71], [17.82, 53.24, 3.18], [17.82, 67.24, 3.18],
           [245.88, 38.76, 3.18], [245.88, 96.77, 3.18], [227.88, 20.23, 2.71], [227.88, 100.23, 2.71]];

// the one window: plate 3's wire opening, x 110.3-133.0, y 42.5-77.9 (a cable route under the FRDM, J1's lead), two end-circle centres and the radius
WINDOWS = [[[121.65, 53.85], [121.65, 66.55], 11.35]];

CB_HOLES = concat(PI_HOLES, FRDM_SCREWS);     // the counterbored holes: the Pi's four and the FRDM's four

module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
module stadium(s) hull() { translate(s[0]) circle(r = s[2], $fn = 48); translate(s[1]) circle(r = s[2], $fn = 48); }

module outline2d() union() {
    rrect(NOSE[0], NOSE[1], NOSE[2], NOSE[3]);
    rrect(FRDM[0], FRDM[1], FRDM[2], FRDM[3]);
    rrect(PI_BBOX[0], PI_BBOX[1], PI_BBOX[2], PI_BBOX[3]);
    for (p = CB_HOLES) translate(p) circle(d = FIX_PAD_D, $fn = 48);
    for (f = PAD_FIX) translate([f[0], f[1]]) circle(d = FIX_PAD_D, $fn = 48);
    translate([FRDM[1] - 4, FRDM[2]]) square([PI_X0 - FRDM[1] + 8, 6.8]);       // two ribs join the pads, along the plate's edges, clear of the cable slot
    translate([FRDM[1] - 4, 79.0]) square([PI_X0 - FRDM[1] + 8, FRDM[3] - 79.0]);
}

module holes2d() {
    for (f = PAD_FIX) translate([f[0], f[1]]) circle(d = f[2] > 3 ? FIX3_D : FIX25_D, $fn = 32);
    for (p = CB_HOLES) translate(p) circle(d = PI_HOLE_D, $fn = 32);
    for (w = WINDOWS) stadium(w);
}

module real() mirror([0, 1, 0]) children();

module trayBody() difference() {
    linear_extrude(T) difference() { outline2d(); holes2d(); }
    for (p = CB_HOLES) translate([p[0], p[1], -0.01]) cylinder(d = PI_CB_D, h = PI_CB_DEPTH, $fn = 32);
    for (f = PAD_FIX) translate([f[0], f[1], T - (f[2] > 3 ? M3_DEPTH : M25_DEPTH)])
        cylinder(d = (f[2] > 3 ? M3_POCKET : M25_POCKET) / cos(30), h = (f[2] > 3 ? M3_DEPTH : M25_DEPTH) + 0.01, $fn = 6);
}

if (PART == "tray") real() trayBody();
else if (PART == "plan") real() color("lightgrey") trayBody();
