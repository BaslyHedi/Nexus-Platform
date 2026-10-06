// NEXUS compute tray - the preview scene (MEC-18): plate 3, the tray, both boards on their standoffs, and the screws.
//
//   openscad -D 'VIEW="top"' --camera=135,-60,0,0,0,0,420 --projection=o --autocenter --viewall --imgsize=4000,1800 -o ../renders/compute-tray-top.png compute-tray-preview.scad
//   VIEW: "top" | "iso" | "explode" | "side" (the camera is chosen on the command line)
//
// The FRDM's connector boxes are read off NXP's Quick Start Guide top view (figure 1) at 10 px / mm, +-1 mm; their heights are the
// parts' usual ones. They are for judging placement, not for building from. The Pi's blocks are indicative.
include <compute-tray.scad>
include <plate3-data.scad>
PART = "lib";
VIEW = "iso";
EX = (VIEW == "explode") ? 45 : 0;
PLATE_T = 2;
LABELS = (VIEW == "top");

module slotshape(s) { // x, y, w, h: a rounded rectangle, full round ends on the short side
    w = s[2]; h = s[3]; r = min(w, h) / 2;
    hull() { if (h >= w) { translate([s[0] + r, s[1] + r]) circle(r = r, $fn = 24); translate([s[0] + r, s[1] + h - r]) circle(r = r, $fn = 24); }
             else        { translate([s[0] + r, s[1] + r]) circle(r = r, $fn = 24); translate([s[0] + w - r, s[1] + r]) circle(r = r, $fn = 24); } } }
module plate3() color("slategray", 0.9) translate([0, 0, -PLATE_T - EX]) linear_extrude(PLATE_T) difference() {
    polygon(OUTLINE);
    for (h = HOLES) translate([h[0], h[1]]) circle(d = h[2], $fn = 20);
    for (s = SLOTS) slotshape(s);
}
module chassis_bits() {
    for (p = STANDOFFS) color("goldenrod") translate([p[0], p[1], -PLATE_T - EX]) cylinder(d = 6.93, h = PLATE_T + 1.2, $fn = 6);
    for (p = CLAMPS) color("mediumpurple") translate([p[0], p[1], 0.01 - EX]) cylinder(d = 7, h = 0.4, $fn = 24);
}
module screw_below(p, d, len, z0) color("gold") translate([p[0], p[1], z0]) { cylinder(d = d, h = len, $fn = 20); translate([0, 0, -2]) cylinder(d = d * 1.9, h = 2, $fn = 20); }
module lab(p, t, s = 2.6, c = "black") color(c) translate([p[0], p[1], T + 30]) linear_extrude(0.2) mirror([0, 1, 0]) text(t, size = s, halign = "center", valign = "center");

// a connector box in the FRDM's own frame: [u, v, du, dv, height, colour, label]
FRDM_PARTS = [
    [0.5, 7.0, 5.5, 52.0, 8.5, "navy", "40-pin"],         // header, left edge: toward the nose
    [60.5, 1.8, 13.0, 5.5, 8.5, "dimgray", "CAN J7"],          // 2x5 NXP header, top edge
    [27.0, 1.0, 20.0, 5.0, 2.0, "tan", "FPC"],                 // 30-pin FPC
    [74.0, 3.0, 14.0, 4.0, 3.5, "gray", ""],                   // USER / ONOFF / RESET
    [89.0, 10.3, 7.0, 8.5, 3.3, "silver", "J11 DBG"],          // USB-C debug, right edge (0.8 mm over the edge)
    [89.0, 27.0, 7.0, 9.0, 3.3, "silver", "USB-C"],            // USB-C, right edge
    [81.5, 43.0, 15.5, 13.5, 6.5, "silver", "USB-A"],          // USB-A, right edge
    [60.0, 44.0, 17.0, 23.0, 13.5, "silver", "ETH"],           // RJ45, bottom edge (2.5 mm over)
    [30.8, 56.8, 10.0, 9.5, 3.3, "silver", "J1 PWR"],          // power USB-C, bottom edge
    [16.0, 54.0, 7.0, 13.0, 6.0, "gray", "AUDIO"],             // audio jack, bottom edge
    [13.0, 6.0, 11.0, 14.5, 2.5, "darkgreen", "WIFI"],
    [17.0, 25.0, 17.0, 17.0, 1.6, "black", "SoC"],
];
module frdm() {
    z = T + FRDM_STANDOFF;
    for (p = FRDM_SCREWS) { color("silver") translate([p[0], p[1], T + EX * 0.25]) cylinder(d = 5, h = FRDM_STANDOFF, $fn = 24);
                            color("gold") translate([p[0], p[1], T - PI_CB_DEPTH + 0.2 + EX * 0.25]) { cylinder(d = 2.5, h = FRDM_STANDOFF + 3, $fn = 16); translate([0, 0, -2]) cylinder(d = 4.4, h = 2, $fn = 16); } }
    for (p = FRDM_FREE) color("silver") translate([p[0], p[1], T + EX * 0.25]) cylinder(d = 5, h = FRDM_STANDOFF, $fn = 24);
    translate([FRDM_X0, FRDM_Y0, EX * 0.6]) {
        color("royalblue") translate([0, 0, z]) cube([FRDM_L, FRDM_W, 1.6]);
        for (c = FRDM_PARTS) color(c[5]) translate([c[0], c[1], z + 1.6]) cube([c[2], c[3], c[4]]);
        color("silver") translate([29.4, -1.0, z - 2.0]) cube([15.3, 15.7, 2.0]);       // microSD socket on the underside, opening to the top edge
    }
}
module pi() {
    z = T + PI_STANDOFF;
    for (p = PI_HOLES) { color("silver") translate([p[0], p[1], T + EX * 0.25]) cylinder(d = 5, h = PI_STANDOFF, $fn = 24);
                         color("gold") translate([p[0], p[1], T - PI_CB_DEPTH + 0.2 + EX * 0.25]) { cylinder(d = 2.5, h = PI_STANDOFF + 6, $fn = 16); translate([0, 0, -2]) cylinder(d = 4.4, h = 2, $fn = 16); } }
    // the Pi in its own frame (a east 0-85, b south 0-56) put on the plate by x = PI_X0 + 56 - b, y = PI_Y0 + a
    translate([0, 0, EX * 1.2]) multmatrix([[0, -1, 0, PI_X0 + PI_W], [1, 0, 0, PI_Y0], [0, 0, 1, 0], [0, 0, 0, 1]]) {
        color("seagreen") translate([0, 0, z]) cube([85, 56, 1.6]);
        color("silver") { translate([64, 2, z + 1.6]) cube([21, 16, 13.5]); translate([68, 20, z + 1.6]) cube([17, 14, 16]); translate([68, 36, z + 1.6]) cube([17, 14, 16]); }
        color("dimgray") translate([7, 1, z + 1.6]) cube([51, 5, 8.5]);
        color("black") translate([30, 20, z + 1.6]) cube([14, 14, 2]);
    }
    for (f = PAD_FIX) { d = f[2] > 3 ? 3 : 2.5;
        color("gold") translate([f[0], f[1], -PLATE_T - 2 - EX]) { cylinder(d = d, h = 2 + PLATE_T + T - 1.2 + EX, $fn = 16); translate([0, 0, -2.4]) cylinder(d = d * 1.9, h = 2.4, $fn = 16); } }
}
module tray() color("lightgrey") translate([0, 0, EX * 0.25]) trayBody();

real() {
    plate3(); chassis_bits(); tray(); frdm(); pi();
    if (LABELS) {
        for (c = FRDM_PARTS) if (c[6] != "") lab([FRDM_X0 + c[0] + c[2] / 2, FRDM_Y0 + c[1] + c[3] / 2], c[6], 2.4, "white");
        lab([FRDM_X0 + 47, FRDM_Y0 + 32], "FRDM-IMX91S", 4, "white");
        lab([PI_X0 + 28, PI_Y0 + 42], "Pi 5 (later)", 4, "white");
        lab([40, 60], "SPARE", 5, "black"); lab([40, 53], "drill here", 3.2, "black");
        lab([4, 60], "NOSE", 3, "black");
    }
}
