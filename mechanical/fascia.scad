// NEXUS rear fascia - two panels, one per inter-deck gap (different heights)
// STATUS: gaps measured 2026-09-20 - LOWER 50, UPPER 40. The two panels are now
//         DIFFERENT parts (MEC-09); MEC-03's single blank is dead. Fixing: two
//         screwed pads per panel (MEC-07).
//         Ports: DE-9 confirmed from its drawing; USB-C and Mini-B apertures
//         are still nominal - see the port block below.
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

BTN_D = 22.2;  BTN_C = 44.0;

// ---- upper-panel ports. Checked against vendor drawings 2026-09-19:
//   DE-9    flange 30.84, screws 24.99, shell 16.92 x 8.38 - ALL CONFIRMED
//   USB-C   flange 23, screws 15, body 40 x 7.5 - CONFIRMED; APERTURE still nominal
//   Mini-B  28.0 across the flange - CONFIRMED; SCREW PITCH inferred, aperture nominal
// So the two apertures and the Mini-B pitch are what to measure on arrival.
//
// Widths across the flat face, all centred at z 25:
//   USB-C flange 23.0 | DE-9 flange 30.8 | Mini-B flange 28.0  = 81.8 mm
// MEC-05 laid these out on an 88.47 mm face (x -41.76 .. 46.71). Since MEC-07 the
// wall sits outside the plate edge and the face is 94.24 mm (x -44.64 .. 49.60),
// so every bay gained ~3 mm; the positions were deliberately left unchanged.
// The DE-9 sits at x 0, NOT at XC (2.48): that 2.5 mm shift is what buys the
// Mini-B its bay (MEC-05).
DE9_W  = 17.9;    // shell aperture width   - drawing: shell 16.92 +/-0.13, so 0.5 a side
DE9_H  =  9.2;    // shell aperture height  - drawing: shell  8.38 +/-0.13, so 0.4 a side
DE9_S  = 24.99;   // mounting screw centres - CONFIRMED on the drawing, +/-0.13
DE9_SD =  3.4;    // panel clearance; the connector's own holes are 3.05 (M3 is a squeeze there)
DE9_X  =  0.0;    // shifted off XC to make both debug bays fit

// USB-C panel-mount extension, CY type, 20 cm -> FRDM J11 (USB-C UART console).
// Drawing CONFIRMS flange 23 wide, screw centres 15, body 40 long, 7.5 thick.
UC_W   = 12.0;    // aperture width  - still NOMINAL, sized for the moulded boss
UC_H   =  7.0;    // aperture height - still NOMINAL
UC_S   = 15.0;    // screw centres - CONFIRMED on the drawing
UC_SD  =  3.0;    // screw clearance - thread size still NOT given; the flange hides the hole
UC_X   = -28.58;  // centre of the 26.36 mm left bay

// Mini-B panel-mount extension, JSER type, 50 cm -> Discovery CN1 (ST-LINK).
// Photo CONFIRMS 28.0 across the flange, ear to ear. Screw pitch still not stated.
MB_W   = 11.0;    // aperture width  - still NOMINAL
MB_H   =  8.0;    // aperture height - still NOMINAL
MB_S   = 21.0;    // screw centres - INFERRED from 28 overall less the two ~3.5 mm ears
MB_SD  =  3.0;    // screw clearance - thread size still NOT given; the flange hides the hole
MB_SLOT = 2.5;    // outboard hole only: the screw centre travels +/-1.25 along x, so any
                  // pitch 18.5..23.5 bolts up - the plausible range from 28.0 overall is
                  // 20..22, so this cannot be missed. Slot ends up 5.5 x 3.0, hidden under
                  // a 28 mm flange. The USB-C keeps two ROUND holes: its 15.0 is on the
                  // drawing, and every hole left round is one the part cannot creep along.
MB_X   = 31.06;   // centre of the 31.31 mm right bay

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
// and their nuts (~10..40). Upper panel: 0..5 and 35..40, clear of its vents
// (7.5..10.5, 29.5..32.5) and every port flange (13.7..26.3).
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
module de9_cut()   panel_port(DE9_X, DE9_W, DE9_H, DE9_S, DE9_SD, 0,       FZ_U);
module usbc_cut()  panel_port(UC_X,  UC_W,  UC_H,  UC_S,  UC_SD,  0,       FZ_U);
module minib_cut() panel_port(MB_X,  MB_W,  MB_H,  MB_S,  MB_SD,  MB_SLOT, FZ_U);

// ---------- port labels, upper panel only ------------------------------------
// Debossed 0.6 mm into the rear face, in the 8 mm band between the flange tops
// (z 32) and the upper vent row (z 40). Debossed, not raised: raised letters on
// a vertical wall are fragile and print mushy, and a recess takes a paint pen -
// wipe it across, wipe the face clean, the letters stay filled.
// 0.6 mm into a 3 mm wall removes nothing structural.
LBL_H = 4.5;     // cap height
LBL_D = 0.6;     // depth into the wall
LBL_Z = 34.5;    // upper panel: between the 31 vent row and the 40 wrap line
LBL_F = "Liberation Sans:style=Bold";

// Lower panel sits higher. A 22.2 mm button leaves only 3.9 mm above it, too
// little for 4.5 mm text - but the upper vent row leaves 27.2 mm gaps BETWEEN
// its slots (x -32.69..-5.52 and 10.48..37.65), clear from the button tops to
// the panel top, and each gap sits almost exactly over its own button.
// z 43 clears even a 26 mm switch bezel by 2.75 mm.
LBL_ZL = 43.0;

// mirror(): the rear face looks down +y, so an observer outside sees world +x
// running to their LEFT. Without the flip every label reads backwards.
module label(x, txt, z = LBL_Z)
  translate([x, YR + 0.05, z]) rotate([90,0,0]) mirror([1,0,0])
    linear_extrude(LBL_D + 0.05)
      text(txt, size=LBL_H, halign="center", valign="center", font=LBL_F);

module labels_upper() {
  label(UC_X,  "IMX91");
  label(DE9_X, "CAN");
  label(MB_X,  "STM32");
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
VENT_DZU = 11.0;             // upper panel: rows at 20 +/- 11 = 9 and 31. The 40 mm gap
                             // leaves two clear bands only - 5..13.7 and 26.3..35, between
                             // the pads and the DE-9 flange - and these sit centred in them.

// [x offset from XC, slot length]. The button holes span XC-33.1..XC-10.9 and
// XC+10.9..XC+33.1, so these three columns land in the clear gaps: outside the
// left button, between the two, and outside the right button. Nothing is cut
// above or below a switch.
VENT    = [[-38.67, 7], [0, 16], [38.67, 7]];

module vent_slot(L)
  hull() for (s=[-1,1])
    translate([s*(L/2 - VENT_H/2), 0, 0]) cylinder(d=VENT_H, h=40);

module vents(fz, dz_)
  for (dz=[-dz_, dz_]) for (v=VENT)
    translate([XC+v[0], YR+8, fz+dz]) rotate([90,0,0]) vent_slot(v[1]);

module fascia_lower() difference() {
  blank(GAP_L);
  buttons_cut(FZ_L); vents(FZ_L, VENT_DZ); labels_lower();
}
module fascia_upper() difference() {
  blank(GAP_U);
  de9_cut(); usbc_cut(); minib_cut();
  vents(FZ_U, VENT_DZU); labels_upper();
}

// ---------- output -----------------------------------------------------------
if      (PART == "lower") fascia_lower();
else if (PART == "upper") fascia_upper();
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
