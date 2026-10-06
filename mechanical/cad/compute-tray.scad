// NEXUS compute tray - one wide plate on plate 3: a large spare pad in the nose, a Raspberry Pi 5, a plug gap, the FRDM-IMX91S (MEC-18)
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
// BOTH BOARDS ARE TURNED ACROSS THE VEHICLE (long edges along y), as Hedi asked. From the nose:
//   SPARE PAD  x 14-93: plate 3's own outline moved in 5 mm, plain 4 mm, six fixings, two windows over plate 3's slots. Drill it.
//   Pi PAD     x 94-150: the Pi 5, ports to the vehicle's LEFT. Plate 3 is 84.5 mm wide at x 70-88, so the Pi (85) cannot go further forward.
//   PLUG GAP   x 150-184: two 15 mm ribs at the plate's edges and nothing between them. The FRDM's Ethernet, power J1 and audio jack face
//              the nose and their plugs need about 35 mm; plate 3's big slot (x 161-176, y 30-90) is right under them for the cables.
//   FRDM PAD   x 184-249: the board across the vehicle (95 long along y), its 40-pin header to the RIGHT, USB-C DBG (J11), USB-C and
//              USB-A to the LEFT (the plugs hang over the plate's left edge), its CAN header J7 and microSD slot to the REAR, where
//              plate 3's cross-slot at x 260 is. The FRDM is last because the rear is the only place its CAN / microSD edge is free.
//   The connector positions are from NXP's FRDM-IMX91S Quick Start Guide, figures 1 and 2 (MEC-18). The cables that reach the FRDM are the BOM's
//   (J1 power 5.1, J11 console 5.9, J7 CAN 4.4); MEC-18 traces each. No 40-pin ribbon: nothing in the BOM uses it.
//
// TO MEASURE before ordering (the defaults are guesses)
//   FRDM_L / FRDM_W - the bare PCB, 95 x 65 from the Quick Start Guide. Hedi's 96 x 67 includes the connectors that overhang; check the PCB alone
//   the Pi standoffs' thread (female-female assumed) and the M2.5 screw head height, for the counterbore

PART = "tray";               // "tray" | "plan" | "outline" | "lib" (the preview file includes this one)

T            = 4.0;          // tray thickness, as the carrier tray
R_CORNER     = 2.0;
FRDM_STANDOFF = 6.0;         // the metal standoffs the FRDM carries (Hedi, 2026-10-06)
PI_STANDOFF  = 8.0;          // 8 or 10 mm, Hedi's choice; only the preview uses it
PI_HOLE_D    = 3.4;          // M2.5 through the tray, loose
PI_CB_D      = 6.4;          // counterbore from below for an M2.5 head, as the carrier tray (MEC-17)
FRDM_HOLE_D  = 4.2;          // the FRDM's holes are read off a photo (+-1 mm): a loose hole and a wide counterbore take that, the board locates by its own screws
FRDM_CB_D    = 7.2;
PI_CB_DEPTH  = 2.4;          // 1.6 mm of floor remains
M25_POCKET   = 5.4;  M25_DEPTH = 2.4;     // M2.5 nut across flats 5.0, as the carrier tray
M3_POCKET    = 5.9;  M3_DEPTH  = 2.6;     // M3 nut across flats 5.5, as the Bauer's nuts (MEC-17)
FIX3_D       = 3.4;          // M3 through the tray, in a 3.18 plate hole
FIX25_D      = 3.2;          // M2.5 through the tray, in a 2.71 plate hole
FIX_PAD_D    = 8.4;          // a round pad round each fixing and counterbore, so none breaks the tray's edge
STANDOFF_CLEAR_D = 9.0;      // plate 3's chassis standoffs (6 mm hex) stand up through the tray's footprint: a notch round each

include <plate3-data.scad>   // OUTLINE, HOLES, SLOTS, STANDOFFS, CLAMPS: generated from the layout drawing

// ---- the boards, plate 3 frame -----------------------------------------------------------------------
// FRDM board frame: u along the long edge, v along the short one, as in the Quick Start Guide's top view (40-pin header at u 0, the
// CAN header and microSD at v 0). Turned so u runs toward the vehicle's LEFT and v toward the NOSE: x = X0 + 65 - v, y = Y0 + u.
FRDM_X0 = 184.0;  FRDM_Y0 = 6.75;      // 6 mm toward the 40-pin side (the right), so the USB plugs on the left have 16 mm of plate beside them
FRDM_L  = 95.0;   FRDM_W  = 65.0;        // the bare PCB, from the Quick Start Guide photo (+-1). Hedi measured 96 x 67 over the connectors, which overhang the
                                          // edges by 1.8 mm (USB-A) and 2.5 mm (RJ45); the non-S board is 105 x 65
function frdm_at(u, v) = [FRDM_X0 + FRDM_W - v, FRDM_Y0 + u];
FRDM = [FRDM_X0, FRDM_X0 + FRDM_W, FRDM_Y0, FRDM_Y0 + FRDM_L];
FRDM_SCREWS = [for (u = [3.5, 52.5]) for (v = [3.5, 61.5]) frdm_at(u, v)];     // the four screwed from below
FRDM_FREE   = [for (v = [3.5, 61.5]) frdm_at(FRDM_L - 4.0, v)];                // the two on the far edge: they just stand on the tray

// Pi board frame: a along the 85 mm (ports at a = 85), b the 56 mm measured from the GPIO edge. Holes at a 3.5 / 61.5, b 3.5 / 52.5.
// Turned so the ports face the vehicle's left and the GPIO header the rear: x = PI_X0 + 56 - b, y = PI_Y0 + a.
PI_X0 = 94.0;  PI_Y0 = 17.75;
PI_L = 85;  PI_W = 56;
function pi_at(a, b) = [PI_X0 + PI_W - b, PI_Y0 + a];
PI_BBOX = [PI_X0, PI_X0 + PI_W, PI_Y0, PI_Y0 + PI_L];
PI_HOLES = [for (a = [3.5, 61.5]) for (b = [3.5, 52.5]) pi_at(a, b)];

// the tray's fixings to plate 3: [x, y, plate hole d]. All on plate 3's own holes, 10 mm or more from every standoff hole.
// spare pad: M3 (17.82, 53.24 and 67.24), M2.5 (49, 35.94 and 84.53), M2.5 (86.94, 40.23 and 80.23).  Pi pad: M2.5 (120.06, 35.94 and 84.53),
// (143.47, 52.65 and 67.88).  FRDM pad: M3 (196.88 and 245.88, 38.76 and 81.77).
PAD_FIX = [[17.82, 53.24, 3.18], [17.82, 67.24, 3.18], [49.0, 35.94, 2.71], [49.0, 84.53, 2.71], [86.94, 40.23, 2.71], [86.94, 80.23, 2.71],
           [120.06, 35.94, 2.71], [120.06, 84.53, 2.71], [143.47, 52.65, 2.71], [143.47, 67.88, 2.71],
           [196.88, 38.76, 3.18], [196.88, 81.77, 3.18], [245.88, 38.76, 3.18], [245.88, 81.77, 3.18]];

// windows over plate 3's two slots in the spare pad (x 56.2-80.1, y 26.9-37.2 and 83.2-93.5), each as two end-circle centres and the radius
WINDOWS = [[[61.33, 32.09], [74.93, 32.09], 5.15], [[61.33, 88.33], [74.93, 88.33], 5.15]];


module rrect(x0, x1, y0, y1, r = R_CORNER)
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
module stadium(s) hull() { translate(s[0]) circle(r = s[2], $fn = 48); translate(s[1]) circle(r = s[2], $fn = 48); }

// the spare pad: plate 3's own outline moved in 5 mm, from x 8 to the Pi pad, with its thin spikes (the plate's side tabs) rounded off
module spare2d() intersection() {
    offset(r = 4) offset(delta = -4) offset(delta = -5) polygon(OUTLINE);
    translate([14, 0]) square([PI_X0 + 4 - 14, 200]);
}

module outline2d() union() {
    spare2d();
    rrect(PI_BBOX[0], PI_BBOX[1], PI_BBOX[2], PI_BBOX[3]);
    rrect(FRDM[0], FRDM[1], FRDM[2], FRDM[3]);
    for (p = PI_HOLES) translate(p) circle(d = FIX_PAD_D, $fn = 48);
    for (p = FRDM_SCREWS) translate(p) circle(d = FRDM_CB_D + 2.2, $fn = 48);
    for (f = PAD_FIX) translate([f[0], f[1]]) circle(d = FIX_PAD_D, $fn = 48);
    // two ribs join the Pi pad to the FRDM pad along the plate's edges, clear of the big slot between them (y 30.4-90.2)
    translate([PI_BBOX[1] - 4, 17.75]) square([FRDM[0] - PI_BBOX[1] + 8, 10.5]);
    translate([PI_BBOX[1] - 4, 93.0]) square([FRDM[0] - PI_BBOX[1] + 8, 8.75]);
}

module holes2d() {
    for (f = PAD_FIX) translate([f[0], f[1]]) circle(d = f[2] > 3 ? FIX3_D : FIX25_D, $fn = 32);
    for (p = PI_HOLES) translate(p) circle(d = PI_HOLE_D, $fn = 32);
    for (p = FRDM_SCREWS) translate(p) circle(d = FRDM_HOLE_D, $fn = 32);
    for (w = WINDOWS) stadium(w);
    for (s = STANDOFFS) translate(s) circle(d = STANDOFF_CLEAR_D, $fn = 48);
}

module real() mirror([0, 1, 0]) children();

module trayBody() difference() {
    linear_extrude(T) difference() { outline2d(); holes2d(); }
    for (p = PI_HOLES) translate([p[0], p[1], -0.01]) cylinder(d = PI_CB_D, h = PI_CB_DEPTH, $fn = 32);
    for (p = FRDM_SCREWS) translate([p[0], p[1], -0.01]) cylinder(d = FRDM_CB_D, h = PI_CB_DEPTH, $fn = 32);
    for (f = PAD_FIX) translate([f[0], f[1], T - (f[2] > 3 ? M3_DEPTH : M25_DEPTH)])
        cylinder(d = (f[2] > 3 ? M3_POCKET : M25_POCKET) / cos(30), h = (f[2] > 3 ? M3_DEPTH : M25_DEPTH) + 0.01, $fn = 6);
}

if (PART == "tray") real() trayBody();
else if (PART == "plan") real() color("lightgrey") trayBody();
else if (PART == "outline") outline2d();           // the outline alone, in the layout frame, for the layout drawing
