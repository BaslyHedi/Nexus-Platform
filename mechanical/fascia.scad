// NEXUS rear fascia - two panels, one per inter-deck gap (different heights)
// STATUS: gaps measured 2026-09-20 - LOWER 50, UPPER 40. The two panels are now
//         DIFFERENT parts (MEC-09); MEC-03's single blank is dead. Fixing: two
//         screwed pads per panel (MEC-07).
//         Ports (MEC-13): all three measured or drawn, in two rows - DE-9 on
//         top, USB-C and Mini-B below. See the port block.
//
// TWO PANELS, TWO HEIGHTS. Measured on the built kit 2026-09-20: the lower gap
// is 50.00 mm and the upper is 40.00 mm - the kit ships two standoff lengths,
// not one. So the panels are 52 and 42 mm tall and are NOT interchangeable.
// Everything else is shared: the same wall section, the same pads, the same
// vent and label treatment, each re-centred on its own gap.
//
// MOUNTING (MEC-07): each panel is dropped into its gap while the chassis is
// stacked and CLAMPED at four corners - a pad on the deck below and one under the
// deck above - through plate holes that already exist at x -41.34 / +46.30,
// y 124.54. Six M3 for the fascia, every nut captive in a pad. See the fixing
// block below. Removing the lower panel means lifting deck 2, the upper deck 3.
//
// CHASSIS GEOMETRY below is measured from Hiwonder's own CAD (the .3dm in this
// folder, via chassis-3deck-fascia.obj), not from photos: rear standoffs are
// 6.0 mm A/F hex at x -35.61 / +40.57, y 118.46; plate rear edge at y 131.54.
//
//   lower panel  z  29.12 ..  81.12 (52 tall) : SW1 / SW2 buttons
//   upper panel  z  81.12 .. 123.12 (42 tall) : DE-9 CAN + USB-C and Mini-B debug
//
// Each panel wraps the deck above it, so the rear face stays continuous and no
// deck edge is left exposed; the only shut line is at z 81.12.
//
// VENTS (MEC-04): six obround slots per panel, two rows of three, symmetric about
// the cut-out centre AND about the panel centreline. Crucially they sit in the
// x-gaps BESIDE and BETWEEN the button holes - never above or below one - so the
// material carrying load around a switch is a full 9.9 mm, not a 3.9 mm ligament
// pinched between a slot and the hole. Ends are radiused: a square internal
// corner is where a crack starts under vibration. Identical on both panels, so
// the blank stays common and the panels stay interchangeable.
//
// LABELS (MEC-05): the upper panel names each port - IMX91 / CAN / STM32 -
// debossed 0.6 mm at z 36. They name the BOARD, not the connector: the connector
// is obvious by shape, which board it reaches is not. Upper panel only, so the
// blank stays common.
//
// Render:  openscad -D 'PART="lower"'    -o fascia-lower.stl fascia.scad
//          openscad -D 'PART="upper"'    -o fascia-upper.stl fascia.scad
//          openscad -D 'PART="both"'     ...  // preview: assembled, panels butt
//          openscad -D 'PART="exploded"' ...  // preview: separated, split visible
//          openscad -D 'PART="blank"'    ...  // the uncut common body
//          openscad -D 'PART="fit"'      ...  // both panels + rear decks and standoffs
//          openscad -D 'PART="clash"'    ...  // panels ∩ chassis - must render EMPTY
//          openscad -D 'PART="portclash"' ... // connectors ∩ panel, chassis, each other - EMPTY
// The two panels are ALWAYS separate parts. "both" only places them at their
// installed heights, where they meet flush and read as one continuous face.
PART = "both";

$fn = 72;

WALL = 3.0;
PLATE_T_ = 2.0;   // deck plate thickness (PLATE_T below is the same number)
// Deck stack. The two standoff lengths were measured on the built kit; the
// Hiwonder CAD only ever had the 50 and we wrongly repeated it for both gaps.
SO_L = 50.0;   // lower standoff, plate 1 -> plate 2
SO_U = 40.0;   // upper standoff, plate 2 -> plate 3
D1T = 29.12;
D2B = D1T + SO_L;        //  79.12
D2T = D2B + PLATE_T_;    //  81.12
D3B = D2T + SO_U;        // 121.12
D3T = D3B + PLATE_T_;    // 123.12

GAP_L   = SO_L;              // 50 - lower clear opening
GAP_U   = SO_U;              // 40 - upper clear opening
PITCH_L = GAP_L + PLATE_T_;  // 52 - panel height: the gap plus the deck it wraps
PITCH_U = GAP_U + PLATE_T_;  // 42
FZ_L    = GAP_L / 2;         // 25.0 - cut-outs sit dead centre of their own gap
FZ_U    = GAP_U / 2;         // 20.0

BTN_D = 22.4;  BTN_C = 44.0;   // M22x1 switches (vendor drawing). 0.4 over the thread: FDM holes print
                               // 0.1-0.2 small, and the 24.8 bezel and 25 A/F nut cover the rest (MEC-14)

// ---- upper-panel ports (MEC-13). Measured on the parts 2026-09-24:
//   DE-9    flange 30.84, screws 24.99, shell 16.92 x 8.38 - vendor drawing
//   USB-C   flange 23 x ~8.3 face, 6 deep, M2.5 THREADED holes 15 apart, body ~14 x 7.5
//   Mini-B  flange 36 x 10, 8 deep, M2.5 THREADED holes ~28.5 apart, body ~20 x 10
// Both extensions have threaded flange holes, so both mount from BEHIND the wall,
// in a pocket on its inside face. Neither body passes through the panel.
//
// Layout on the 94.24 mm flat face (x -44.64 .. 49.60), all three HORIZONTAL, in
// two rows (MEC-13). Side by side they would total 23 + 30.84 + 36 = 89.8 mm, and
// each body runs ~13-40 mm forward into the vehicle past the rear standoffs, whose
// flats are at x -32.61 and +37.57 (6.0 A/F hex at -35.61 / +40.57). Two rows take
// the width problem away:
//   top row,    z 28:  DE-9   flange -12.94 .. 17.90, z 21.73 .. 34.27, on XC
//   bottom row, z 11:  USB-C  flange -36.50 .. -13.50, body -32.00 .. -18.00
//                                    (0.61 to the left standoff)
//                      Mini-B flange  -6.00 ..  30.00, body   2.00 ..  22.00
//                                    (15.57 to the right standoff), 7.5 from the USB-C
YI = 131.942;     // inside face of the wall on the flat: PLATE_YR + CLR (set below)

DE9_W  = 17.9;    // shell aperture width   - drawing: shell 16.92 +/-0.13, so 0.5 a side
DE9_H  =  9.2;    // shell aperture height  - drawing: shell  8.38 +/-0.13, so 0.4 a side
DE9_S  = 24.99;   // mounting screw centres - CONFIRMED on the drawing, +/-0.13
DE9_SD =  3.4;    // panel clearance; the connector's own holes are 3.05 (M3 is a squeeze there)
DE9_X  =  2.48;   // = XC (set below), the chassis centreline: alone in its row (MEC-13)
ROW_T  = 28.0;    // top row: DE-9. Flange top 34.27, 5.7 clear of the 40 wrap line
ROW_B  = 11.0;    // bottom row: USB-C and Mini-B. Flanges z 6..16, 5.7 clear of the DE-9

// USB-C panel-mount extension, CY type, 20 cm -> FRDM J11 (USB-C UART console).
// Mounted from behind, the way the vendor's own bracket does it: its two M2.5 x 5
// screws go through the 1.2 mm skin from outside into the metal inserts in the
// flange face. The heads (~4 across, 15 apart) leave ~11 mm clear between them, so
// the plug grip has to be narrower than that - the bench cable's is 10. A full-width
// grip (up to 12.35 by the spec) would land on the heads and not seat (MEC-13).
UC_X    = -25.0;  // body clears the left standoff by 0.61 (MEC-13)
UC_Z    = ROW_B;
UC_FW   = 23.0;   // flange width - drawing
UC_FH   =  8.3;   // flange face height - PHOTO; measured "6" is probably the depth. Pocket fits both
UC_K    =  6.0;   // flange depth along the cable - PHOTO
UC_BW   = 14.0;   // body width behind the flange - PHOTO, MEASURE: it sets the standoff margin
UC_BH   =  7.5;   // body thickness - drawing
UC_BL   = 40.0;   // body length - drawing, taken as all behind the flange (conservative)
UC_SKIN =  1.2;   // wall left in front of the flange. The metal rim stands ~0.9 proud, so
                  // the socket face ends ~0.3 below the outside and any plug seats fully
UC_PW   = 23.6;   // pocket width
UC_PH   =  9.0;   // pocket height - fits a 6 or an 8.3 face; the screws, not the pocket, hold it
UC_SW   =  9.6;   // slot for the metal rim (~9 x 3 in the photo; 8.94 x 3.2 by the spec)
UC_SH   =  3.8;
UC_S    = 15.0;   // screw centres - drawing, and the face-on photo agrees
UC_SD   =  2.9;   // M2.5 clearance. 1.25 mm of skin is left between each hole and the slot
UC_HD   =  4.0;   // screw head diameter - tape-measured; sets the 11 mm grip limit

// Mini-B panel-mount extension, JSER type, 50 cm -> Discovery CN1 (ST-LINK).
// Horizontal, like the others. Its screws are ~28.5 apart, so the heads sit
// ~11.7 from centre, far outside any plug grip - it keeps its own screws, driven
// from outside through a 1.5 mm skin into the threaded ears (~3.5 mm of thread).
MB_X    = 12.0;
MB_Z    = ROW_B;
MB_FL   = 36.0;   // flange length (x) - measured
MB_FW   = 10.0;   // flange height (z) - measured
MB_K    =  8.0;   // flange depth - measured
MB_BW   = 20.0;   // body, along x - PHOTO
MB_BT   = 10.0;   // body, along z - PHOTO
MB_BL   = 13.0;   // body length behind the flange - PHOTO, then a ~5.6 mm cable sleeve
MB_S    = 28.5;   // screw centres - PHOTO, not measured; see MB_SLOT
MB_SLOT =  3.0;   // outboard (+x) hole only is a slot, +/-1.5: any pitch 27..30 bolts up. One hole
                  // stays round so the part can only pivot about it, never slide bodily
MB_SD   =  2.9;   // M2.5 clearance
MB_SKIN =  1.5;
MB_PL   = 36.4;   // pocket, x
MB_PW   = 10.4;   // pocket, z
MB_AL   = 14.0;   // aperture for the plug grip, x - ears start 10.5 from centre, so they bear in full
MB_AW   =  9.5;   // aperture, z - the flange bears on its ears, not here

XC = 2.48;

// ---------- chassis, from Hiwonder's CAD ---------------------------------------
// Rear outline of a deck plate, traced from the plate mesh. Only y >= 113 is
// real: the sides are closed straight down to y 100 because nothing forward of
// the taper matters here. Same outline on all three decks (the kit plates are
// identical, and the 3-deck model duplicates the one plate).
PLATE = [[-56.882,100], [-56.882,113.110], [-56.859,113.521], [-56.778,113.929], [-56.642,114.322], [-56.455,114.688],
         [-47.212,130.086], [-46.999,130.395], [-46.743,130.681], [-46.447,130.936], [-46.117,131.153], [-45.762,131.324], [-45.391,131.446], [-45.014,131.519], [-44.640,131.542],
         [49.604,131.542], [49.978,131.519], [50.356,131.446], [50.727,131.324], [51.082,131.153], [51.412,130.936], [51.707,130.681], [51.964,130.395], [52.176,130.086],
         [61.419,114.688], [61.606,114.322], [61.743,113.929], [61.823,113.521], [61.847,113.110], [61.847,100]];
PLATE_T = 2.0;
PLATE_YR = 131.542;        // rear flat edge

SO    = [[-35.61,118.46], [40.57,118.46]];   // rear standoff centres, 76.18 apart, centred on XC
SO_AF = 6.0;               // hex across flats - CHECK ON ONE REAL STANDOFF, the bore depends on it
SLOT_W = 5.38;             // rear cross-slot in every plate, y 121.94 .. 127.32
SLOT_END = [[-31.53,124.63], [36.50,124.63]];

// ---------- panel ------------------------------------------------------------
CLR  = 0.4;                // wall to plate edge, all round - the wall now passes OUTSIDE the deck
Y0   = 116.0;              // wall starts here along the taper
YR   = PLATE_YR + CLR + WALL;   // 134.94 - rear face

// ---- fixing: a screwed pad at each corner, top and bottom, into the plate
// holes that are already there. Six M3 for the whole fascia (MEC-07), and EVERY
// NUT IS CAPTIVE in a pad - nothing has to be held inside the chassis:
//
//   plate 1  M3x8   from UNDER the vehicle, up into the lower panel's bottom pads
//   plate 2  M3x12  from ABOVE, down through the upper panel's BOTTOM pad + plate 2
//                   + into the lower panel's TOP pad - one screw clamps both panels,
//                   as MEC-03 foresaw for this shared hole
//   plate 3  M3x8   from on top of the vehicle, down into the upper panel's TOP pads
//
// Every screw is driven from the side that is open at that point in the build, and
// every nut is pulled onto the CLOSED end of its pocket as it tightens. The upper
// panel's bottom pocket is the one that goes unused - plate 2's screw passes
// through it - so a washer under that head spans it. Washer under every head.
FIX    = [[-41.34,124.54], [46.30,124.54]];  // existing 3.2 mm plate holes, on every deck
PAD_H  = 5.0;              // pad thickness: 2.4 of material + 2.6 nut pocket
PAD_R  = 4.6;              // rounding round the screw hole - 1.37 of wall round the pocket
SCR_D  = 3.4;              // M3 clearance
NUT_AF = 5.6;              // M3 nut across flats + 0.1: a push fit, so it stays put
NUT_H  = 2.6;              // nut 2.4 + 0.2
SO_CLR = 0.5;              // pad to standoff

module wall2d()
  intersection() {
    difference() { offset(r=CLR+WALL) polygon(PLATE); offset(r=CLR) polygon(PLATE); }
    translate([-100, Y0]) square([200, 40]);
  }

// Pad outline: a disc round the screw hole, hulled back into the wall and
// clipped at the wall's mid-thickness so nothing reaches the rear face. The
// standoff is 8.35 mm away centre to centre, so it only needs nicking clear.
module pad2d(f)
  difference() {
    intersection() {
      hull() { translate(f) circle(r=PAD_R); translate([f[0]-PAD_R, f[1]]) square([2*PAD_R, 20]); }
      offset(r=CLR+WALL/2) polygon(PLATE);
    }
    for (p=SO) translate(p) circle(r=SO_AF/sqrt(3) + SO_CLR);
  }

// One band on the deck below (0..5) and one under the deck above (gap-5..gap).
// Lower panel: 0..5 and 45..50, clear of its vents (7..10, 40..43), the buttons
// and their nuts (~10..40). Upper panel: 0..5 and 35..40, clear of both port rows
// (flanges z 6..16 and 21.7..34.3) and, in x, of every vent (MEC-13).
module pads(gap)
  difference() {
    for (z=[0, gap-PAD_H]) translate([0,0,z]) linear_extrude(PAD_H) for (f=FIX) pad2d(f);
    for (f=FIX) {
      translate([f[0], f[1], -1]) cylinder(d=SCR_D, h=gap+2);
      // pockets: bottom band opens upward, top band opens downward
      translate([f[0], f[1], PAD_H-NUT_H])   cylinder(r=NUT_AF/sqrt(3), h=NUT_H+0.01, $fn=6);
      translate([f[0], f[1], gap-PAD_H-0.01]) cylinder(r=NUT_AF/sqrt(3), h=NUT_H+0.01, $fn=6);
    }
  }

// ---------- the blank, per gap -----------------------------------------------
module blank(gap) union() {
  linear_extrude(gap + PLATE_T_) wall2d();
  pads(gap);
}

// ---------- chassis stand-in for fit and clash checks ------------------------
module chassis_rear() {
  for (zb=[D1T-PLATE_T, D2B, D3B]) translate([0,0,zb]) linear_extrude(PLATE_T) difference() {
    polygon(PLATE);
    for (p=SO) translate(p) circle(d=4.3);
    hull() for (p=SLOT_END) translate(p) circle(d=SLOT_W);
  }
  for (p=SO) for (zr=[[D1T,D2B], [D2T,D3B]])
    translate([p[0], p[1], zr[0]]) rotate([0,0,30]) cylinder(r=SO_AF/sqrt(3), h=zr[1]-zr[0], $fn=6);
}

// ---------- cut-outs, both centred at FZ -------------------------------------
module buttons_cut(fz)
  for (dx=[-BTN_C/2, BTN_C/2])
    translate([XC+dx, YR+8, fz]) rotate([90,0,0]) cylinder(d=BTN_D, h=40);

// One rectangular aperture plus two flange screws, centred at z 25. Rectangular
// rather than shaped: the flange screws set the orientation, and a rectangle
// prints cleanly without support.
// `slot` lengthens the OUTBOARD hole only, along x, by that much in total. One
// round hole still locates the connector; the slot just absorbs an unknown screw
// pitch. Never slot both - two slots let the part slide bodily, which is the
// loose, needs-glue failure. With one, the part can only pivot about the round
// hole, and the boss in its aperture limits even that.
module panel_port(x, w, h, sp, sd, slot = 0, fz = 20)
  translate([x, YR+8, fz]) rotate([90,0,0]) {
    translate([-w/2, -h/2, 0]) cube([w, h, 40]);
    translate([-sp/2, 0, 0]) cylinder(d=sd, h=40);
    hull() for (k=[-1,1]) translate([sp/2 + k*slot/2, 0, 0]) cylinder(d=sd, h=40);
  }

// DE-9, CiA 303-1 pinout (2 = CAN_L, 3 = CAN_GND, 7 = CAN_H).
module de9_cut()   panel_port(DE9_X, DE9_W, DE9_H, DE9_S, DE9_SD, 0, ROW_T);

// A rounded rectangle in the x-z plane, w along x and h along z, from y0 to y1.
module xz_block(x, z, w, h, y0, y1, r = 0.5)
  translate([x, y1, z]) rotate([90,0,0])
    linear_extrude(y1 - y0) offset(r=r) square([w - 2*r, h - 2*r], center=true);

// USB-C (MEC-13): pocket from the inside, rim slot and two screw holes through the
// skin. The screws, driven from outside, pull the flange onto the skin.
module usbc_cut() {
  xz_block(UC_X, UC_Z, UC_PW, UC_PH, YI - 1, YR - UC_SKIN);
  xz_block(UC_X, UC_Z, UC_SW, UC_SH, YI - 1, YR + 1, r = UC_SH/2 - 0.01);
  for (s=[-1,1]) translate([UC_X + s*UC_S/2, YR + 1, UC_Z]) rotate([90,0,0]) cylinder(d=UC_SD, h=WALL + 2);
}

UC_YB = YR - UC_SKIN - UC_K;   // flange back face, 127.742

// Mini-B (MEC-13): pocket from the inside, a grip aperture through the skin, one
// round screw hole (inboard, -x) and one slot (outboard, +x) through the skin.
module minib_cut() {
  xz_block(MB_X, MB_Z, MB_PL, MB_PW, YI - 1, YR - MB_SKIN);
  xz_block(MB_X, MB_Z, MB_AL, MB_AW, YI - 1, YR + 1, r = 1.5);
  translate([MB_X - MB_S/2, YR + 1, MB_Z]) rotate([90,0,0]) cylinder(d=MB_SD, h=WALL + 2);
  hull() for (k=[-1,1]) translate([MB_X + MB_S/2 + k*MB_SLOT/2, YR + 1, MB_Z]) rotate([90,0,0]) cylinder(d=MB_SD, h=WALL + 2);
}

// ---------- port stand-ins, for PART="portclash" only ------------------------
// Rough solids of the three connectors as installed, from the measurements above.
// A DE-9 rear insulator of 19 x 10.5 x 8 is assumed, not measured.
module usbc_standin() {
  xz_block(UC_X, UC_Z, UC_FW, UC_FH, UC_YB, YR - UC_SKIN);                          // flange
  xz_block(UC_X, UC_Z, 8.94, 3.2, YR - UC_SKIN - 0.01, YR - UC_SKIN + 0.9, r = 1.5); // metal rim
  xz_block(UC_X, UC_Z, UC_BW, UC_BH, UC_YB - UC_BL, UC_YB + 0.01);                 // body
  for (s=[-1,1]) translate([UC_X + s*UC_S/2, YR, UC_Z]) rotate([-90,0,0]) cylinder(d=UC_HD, h=1.8); // screw heads
}
module minib_standin() {
  xz_block(MB_X, MB_Z, MB_FL, MB_FW, YR - MB_SKIN - MB_K, YR - MB_SKIN);
  xz_block(MB_X, MB_Z, MB_BW, MB_BT, YR - MB_SKIN - MB_K - MB_BL, YR - MB_SKIN - MB_K + 0.01);
  for (s=[-1,1]) translate([MB_X + s*MB_S/2, YR, MB_Z]) rotate([-90,0,0]) cylinder(d=4.0, h=1.8); // screw heads
}
module de9_standin() {
  xz_block(DE9_X, ROW_T, 30.84, 12.55, YI - 1.0, YI, r = 1);                        // flange
  xz_block(DE9_X, ROW_T, 16.92, 8.38, YI - 0.01, YI + 6, r = 1);                     // shell
  xz_block(DE9_X, ROW_T, 19.0, 10.5, YI - 9.0, YI - 0.99, r = 1);                   // insulator
}

// ---------- port labels, upper panel only ------------------------------------
// Debossed 0.6 mm into the rear face, each directly above its own port. Debossed,
// not raised: raised letters on
// a vertical wall are fragile and print mushy, and a recess takes a paint pen -
// wipe it across, wipe the face clean, the letters stay filled.
// 0.6 mm into a 3 mm wall removes nothing structural.
LBL_H = 4.5;     // cap height
LBL_D = 0.6;     // depth into the wall
LBL_ZB = 19.0;   // upper, bottom row: z 16.75..21.25, between the flange tops (16) and the DE-9 aperture (23.4)
LBL_ZT = 37.5;   // upper, top row: z 35.25..39.75, above the DE-9 aperture (32.6), below the 42 top edge
LBL_F = "Liberation Sans:style=Bold";

// Lower panel sits higher. A 22.4 mm button leaves only 3.8 mm above it, too
// little for 4.5 mm text - but the upper vent row leaves 27.2 mm gaps BETWEEN
// its slots (x -32.69..-5.52 and 10.48..37.65), clear from the button tops to
// the panel top, and each gap sits almost exactly over its own button.
// z 43 clears the real 24.8 mm bezel (MEC-14) by 3.35 mm.
LBL_ZL = 43.0;

// mirror(): the rear face looks down +y, so an observer outside sees world +x
// running to their LEFT. Without the flip every label reads backwards.
// `rot` 90 runs the text upward; after the mirror the letter tops face the
// observer's left, the normal way to read a bottom-to-top label.
module label(x, txt, z, rot = 0)
  translate([x, YR + 0.05, z]) rotate([90,0,0]) mirror([1,0,0])
    linear_extrude(LBL_D + 0.05) rotate(rot)
      text(txt, size=LBL_H, halign="center", valign="center", font=LBL_F);

// Each name sits over its own port. The bottom-row labels clear the USB-C and
// Mini-B screw heads (top z 13) and the DE-9 aperture (bottom z 23.4).
module labels_upper() {
  label(UC_X,  "IMX91", LBL_ZB);
  label(MB_X,  "STM32", LBL_ZB);
  label(DE9_X, "CAN",   LBL_ZT);
}

// DRIVE, not POWER: SW1 switches the power TRAIN, and neither switch is a master
// cut-off - that is the battery connector. A panel reading POWER invites someone
// to treat it as one. Faced from behind the vehicle world +x runs to the LEFT,
// so SW1 (x +24.48) is the left-hand button and SW2 (x -19.52) the right-hand.
module labels_lower() {
  label(XC + BTN_C/2, "DRIVE", LBL_ZL);   // SW1, red   - left as faced
  label(XC - BTN_C/2, "LOGIC", LBL_ZL);   // SW2, green - right as faced
}

// ---------- vents, identical on both panels ----------------------------------
// Obround, not rectangular: radiused ends leave no sharp internal corner.
VENT_H   = 3.0;              // slot height
VENT_DZ  = 16.5;             // lower panel: rows at 25 +/- 16.5 = 8.5 and 41.5

// [x offset from XC, slot length]. The button holes span XC-33.2..XC-10.8 and
// XC+10.8..XC+33.2, so these three columns land in the clear gaps: outside the
// left button, between the two, and outside the right button. Nothing is cut
// above or below a switch.
VENT    = [[-38.67, 7], [0, 16], [38.67, 7]];

module vent_slot(L)
  hull() for (s=[-1,1])
    translate([s*(L/2 - VENT_H/2), 0, 0]) cylinder(d=VENT_H, h=40);

module vents(fz, dz_)
  for (dz=[-dz_, dz_]) for (v=VENT)
    translate([XC+v[0], YR+8, fz+dz]) rotate([90,0,0]) vent_slot(v[1]);

// Upper panel (MEC-13): the two port rows fill the middle, so the vents move to
// where nothing else is - one upright slot at each end of the face, clear of the
// pad bands (z 0..5, 35..40), and one flat slot in each top corner beside the
// DE-9. 82 mm of slot, against 60 before. [x, z, length, upright?]
VENT_U  = [[-40.5, 20, 24, true], [40.5, 20, 24, true],
           [-25.0, 35.5, 18, false], [29.0, 35.5, 16, false]];
module vents_upper()
  for (v=VENT_U)
    translate([v[0], YR+8, v[1]]) rotate([90,0,0]) rotate([0,0, v[3] ? 90 : 0]) vent_slot(v[2]);

module fascia_lower() difference() {
  blank(GAP_L);
  buttons_cut(FZ_L); vents(FZ_L, VENT_DZ); labels_lower();
}
module fascia_upper() difference() {
  blank(GAP_U);
  de9_cut(); usbc_cut(); minib_cut();
  vents_upper(); labels_upper();
}

// ---------- output -----------------------------------------------------------
assert(abs(YI - (PLATE_YR + CLR)) < 1e-3, "YI must equal PLATE_YR + CLR");

if      (PART == "lower") fascia_lower();
else if (PART == "upper") fascia_upper();
else if (PART == "portclash") translate([0,0,D2T]) {   // must render EMPTY, like "clash"
  // every connector against the upper panel, the rear chassis and each other
  for (p=[0:2]) intersection() {
    if (p==0) usbc_standin(); else if (p==1) minib_standin(); else de9_standin();
    union() { fascia_upper(); translate([0,0,-D2T]) chassis_rear(); }
  }
  intersection() { usbc_standin();  de9_standin(); }
  intersection() { minib_standin(); de9_standin(); }
  intersection() { usbc_standin();  minib_standin(); }
}
else if (PART == "blank") blank(GAP_L);
else if (PART == "fit") {                // panels in situ, with the rear chassis in grey
  translate([0,0,D1T]) fascia_lower();
  translate([0,0,D2T]) fascia_upper();
  %chassis_rear();
}
else if (PART == "clash") intersection() {   // anything rendered here is an interference
  union() { translate([0,0,D1T]) fascia_lower(); translate([0,0,D2T]) fascia_upper(); }
  chassis_rear();
}
else if (PART == "exploded") {           // separated, so the split is visible
  translate([0,0,D1T])      fascia_lower();
  translate([0,0,D2T+25])   fascia_upper();
}
else {                                   // "both" - in situ; they BUTT, they are
  translate([0,0,D1T]) fascia_lower();   // still two parts (see PART="exploded")
  translate([0,0,D2T]) fascia_upper();
}
