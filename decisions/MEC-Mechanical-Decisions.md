# MEC · Mechanical design decisions

Packaging, the deck stack, printed parts and how things are fixed to the vehicle. Each entry is settled - revisit one only if something concrete contradicts it.

Numbering is `MEC-nn`, unique across the project and never reused. Format, and how to add one: [README](README.md). Parts, prices and status: [`../bom/BOM.md`](../bom/BOM.md).

Drawings: [chassis layout](../hardware/chassis-layout.svg). Geometry and build commands: [`../mechanical/README.md`](../mechanical/README.md).

| # | Decision |
|---|---|
| **MEC-01** | Power domain low, compute domain high |
| **MEC-02** | Rear fascia - 3D printed, covers the inter-deck gaps |
| **MEC-03** | The fascia is two interchangeable panels |
| **MEC-04** | Vents - six obround slots per panel, in the bands the features do not use |
| **MEC-05** | Board debug ports on the fascia - and the DE-9 moves off centre to fit |
| **MEC-06** | Switch legends - DRIVE and LOGIC, not POWER |
| **MEC-07** | The fascia is clamped at four corners - six M3 for the whole thing |
| **MEC-08** | The STM32 rides on a perfboard carrier, not on the chassis directly |
| **MEC-09** | The two deck gaps are 50 and 40 mm - the panels are different parts |
| **MEC-10** | The chassis holes are three sizes - and half of them are M2.5, not M3 |
| **MEC-11** | The FRDM's mounting holes land on the Hiwonder grid - 0.06 mm out |
| **MEC-12** | Component allocation across the three plates |
| **MEC-13** | The debug ports mount from behind, in two horizontal rows |
| **MEC-14** | The switch drawing closes the lower panel - and its holes open to 22.4 |

---

## MEC-01 · Power domain low, compute domain high

*Formerly HD-12.*

**Updated by HW-15:** the fuse block is replaced by a bus bar pair, so its placement on standoffs above the battery no longer applies.

**Decision.** Bottom deck: battery, Hiwonder driver, shunt, switches, fuse block on standoffs
above the battery. Top deck: both compute boards, both converters, CAN transceiver.

**Why.** Three reasons in order of weight: the fuse block is ~20 % of a deck and competes with
the boards; the battery is already on the bottom deck by the chassis's own design, so the
highest-current runs stay short; and motor switching currents end up on a different deck from
the CAN bus with an aluminium plate between them - free noise separation from a mounting choice.

**Converters go on the top deck deliberately.** Long wires then carry 12 V at low current and
short wires carry 5 V board-adjacent, which is where droop actually hurts.

---

## MEC-02 · Rear fascia - 3D printed, covers the inter-deck gaps

*Formerly HD-15.*

**Updated by MEC-14:** the switch holes are ⌀22.4, not 22.2.

**Updated by MEC-13:** the upper panel's ports are in two rows, not one, and mount from behind.

**Superseded in part by MEC-09 (2026-09-20).** The gaps were measured on the built kit: **lower 50,
upper 40** - the kit ships two standoff lengths. Everything below that assumes 52 mm pitch, a
104 mm span and identical gaps is wrong; the panels are 52 and 42 mm tall and the upper deck's top
face is z 123.12, not 133.12.

**Status.** Unfrozen 2026-09-17 - the CAN connector is chosen (HW-18) and the reserved
upper-gap cut-out is now defined. Source of truth:
[`../mechanical/fascia.scad`](../mechanical/fascia.scad); visual check:
`chassis-3deck-fascia.obj` in the same folder.

**Decision.** Printed panels close the rear of the vehicle between deck 1 and deck 3
(z 29.12 → 133.12, 104 mm). They follow the real rear taper of the plate - 88.5 mm at the rear
face - rather than a rectangle, and fix to plate holes that already exist
(x −41.34 / +46.30, y 124.54, on every deck). **Split into two interchangeable panels by
MEC-03** - that record owns the split, the fixing count and the absence of vents.

| Zone | z | Carries |
|---|---|---|
| Lower gap | 29.12 → 79.12 | **SW1 / SW2** ⌀22.2 at 44 mm centres, z 54.12 · labelled **DRIVE / LOGIC** (MEC-06) |
| Upper gap | 81.12 → 131.12 | **Three ports in one row at z 101.12** (MEC-09; was 106.12) - USB-C (x −28.58), **DE-9 CAN** (x 0, HW-18), Mini-B (x +31.06). Layout and apertures owned by **MEC-05** |

**Why.**

- **Advanced kit has three decks at 52 mm pitch** (confirmed on the real kit), not the two in
  the Hiwonder "Single Layer" CAD - the model was extended by duplicating the plate and its four
  standoffs.
- **The rear tapers** from 118.7 mm at y 114 to 88.5 mm at the edge; a flat panel overhangs it.
- **Nothing below deck 1** - the running gear stays open and there is no ground-clearance question.
- **Printed nylon/PETG, not acrylic** - acrylic is notch-sensitive and would crack from its holes
  under vibration.
- Tabs are clipped to the wall interior and notched around the bronze standoffs, so they cannot
  break through the taper or foul the pillars.

**Consequences.**

- **Button bodies protrude ~25 mm into the rear of the lower gap**, which is also where the FRDM
  and STM32 are meant to sit - board placement must stay forward of y ≈ 109.
- **The deck-2 tab sits on the floor of the upper gap** (x ±38…50). This was once read as "keep the
  CAN connector central"; that is **retired by MEC-05** - the tab is at local z 0…4 and every port
  flange is at z 18…32, so they never interact and the DE-9 is free to move in x.

**Open before printing.** Measure all three port apertures against the parts in hand (MEC-05); ~~screw retention~~ (closed by MEC-07); optional chamfer on the square wrap ends at y 118.

---

## MEC-03 · The fascia is two interchangeable panels

*Formerly HD-22.*

**Updated by MEC-07:** 8 M3 becomes 6 - the tabs are now pads with captive nuts, and deck 2's shared hole takes one M3×10 through both panels, the option this record already foresaw.

**Decision.** The rear fascia is **two panels from one blank**, one per inter-deck gap, differing
only in their cut-out: buttons in one, the DE-9 in the other. Vents are common to both and are
owned by **MEC-04**.

**Why the split is free.** The one-piece part spanned z 29.12 → 133.12 = **104 mm = exactly two
deck pitches of 52**, both gaps measure **50.00 mm**, and the rear profile is a constant
cross-section. So the halves are the *same* blank rather than two parts that merely resemble each
other, and both cut-outs already fell at local z 25.0 of their own half. Splitting at deck 2's top
face cost no geometry change.

**Why interchangeable is worth having.** Either panel bolts into either gap, so the ports can swap
decks later without a reprint. One blank means one print profile to tune and one spare to keep. A
damaged panel - the buttons are the part that gets handled - is replaced on its own instead of
reprinting 104 mm of shell.

**Consequences.**

- **8 M3 instead of 6.** Each panel is caught at both ends (tabs at local z 0 and 46), where the
  one-piece part relied on three tab levels. More fixings, and no unsupported free edge.
- **Deck 2's hole is now shared** by the lower panel's top tab (underneath) and the upper panel's
  bottom tab (on top). Use one M3×16 through tab + deck + tab with a nyloc nut, or two M3×8 from
  opposite faces. Either way the tabs are clamped, so no heat-set inserts are needed there.
- **Each panel wraps the deck above it** (52 mm, not 50), so the rear face stays continuous and no
  deck edge is exposed. The only shut line is at z 81.12.
- **Verified disjoint:** the two panels rendered together give 3 CGAL volumes - two separate solids
  plus outer space - so nothing interferes at the shut line.
- Print both from `fascia.scad` with `-D 'PART="lower"'` and `-D 'PART="upper"'`; `PART="blank"`
  gives the uncut body if a third panel is ever wanted.

---

## MEC-04 · Vents - six obround slots per panel, in the bands the features do not use

**Updated by MEC-13:** on the upper panel the two port rows fill the middle, so its vents are four slots at the ends and top corners. The lower panel is unchanged.

*Formerly HD-23.*

**Decision.** Each panel carries **six obround slots**, two rows of three, symmetric about the
panel centreline and about the cut-out centre. They are cut into the **shared blank**, so both
panels get exactly the same pattern and interchangeability is unaffected.

| | |
|---|---|
| Rows | local z **8.5** and **41.5** - 16.5 mm either side of the centre at 25 |
| Slots | outer pair **7.0 × 3.0 mm**, centre pair **16.0 × 3.0 mm**, radiused ends (⌀3.0) |
| Columns | centres at XC ±38.67 and XC - the three gaps beside and between the button holes |
| Material above/below each switch | **9.9 mm**, solid - no slot is cut over or under a button hole |
| Thinnest in-plane margin | 2.9 mm (centre slot to button hole) · 2.1 mm (outer slot to the face fold) |

**Why this pattern and not the first one.** The original vents failed for two reasons, and both
are fixed here rather than worked around:

- **They were square-cornered `cube()` cuts.** A sharp internal corner is a stress riser and is
  where a crack starts in a printed part under vibration. These are obround - two radiused ends
  hulled together - so there is no corner to initiate from.
- **They ran directly over and under the button holes.** That is the load path around a ⌀22.2
  hole in a panel that vibrates, and a slot 3.9 mm from the hole edge pinches it to a ligament.
  Moving the rows down in height would only have taken that to 4.4 mm. Instead the slots were
  moved *sideways*, into the three x-gaps the buttons leave free, so the material above and below
  each switch is now solid for the full 9.9 mm - a 2.5× gain in the section that actually carries
  load. The rows remain clear of the DE-9 flange (18.7–31.3) and both tab bands (0–4, 46–50).

**Why vent at all**, given the chassis is open on three sides: cross-flow past warm boards is
cheap once the slots cost nothing structurally, and the lower gap is where the FRDM and STM32 sit.

**Consequences.**

- **Verified identical on both panels:** the vent vertex delta is **the same on each**, so the
  pattern is provably common to both and the blank stays shared. Both compile as a single solid.
- **Open airway is ~42 % of the first pattern** (180 mm² per panel vs 432 mm²). Accepted
  deliberately: the chassis is open on three sides, so the rear panel is not the airflow path,
  and strength around the switches was the binding constraint. The outer slots are short (7 mm);
  if they are not earning their keep they can be dropped without touching anything else.
- The slots are **through-cuts in a 3 mm wall**; no bridging, so they print without support in the
  panel's natural flat-on-the-bed orientation.
- **They consume no connector space.** The bays beside the DE-9 are bounded by the flange and the
  flat face, not by the vents, so the vent rows do not reduce room for debug ports (MEC-05).

---

## MEC-05 · Board debug ports on the fascia - and the DE-9 moves off centre to fit

*Formerly HD-24.*

**Updated by MEC-13:** both extensions mount from behind in pockets, the Mini-B flange is 36 mm, and the ports are in two rows, centred: DE-9 on top at x +2.48, USB-C (x −16.52) and Mini-B (x +21.48) below. The single row, positions, apertures and Mini-B figures below are historical.

**Updated by MEC-07:** the flat face widened from 88.47 to 94.24 mm. Port positions are unchanged, so every bay gained ~3 mm of margin.

**Vendor drawings checked 2026-09-19.** The DE-9 is fully confirmed - flange **30.84 ±0.38**, screw centres **24.99 ±0.13**, shell **16.92 ±0.13 × 8.38 ±0.13**, its own flange holes ⌀3.05. The USB-C drawing confirms flange 23, screw centres 15, body 40 × 7.5. The Mini-B photo confirms 28.0 across the flange. Apertures were opened to suit: DE-9 **17.9 × 9.2** (0.5 and 0.4 mm a side on the measured shell, was 17.6 × 9.0 against an assumed 16.9 × 8.4), and all three screw clearances to 3.0–3.4 mm, since every flange covers its holes. **Still unmeasured:** the USB-C and Mini-B apertures (both sized for a moulded boss nobody has published) and the Mini-B screw pitch - which is now designed around rather than measured.

**The Mini-B's outboard hole is a 5.5 × 3.0 slot** (2026-09-19). Its screw centre can sit anywhere across ±1.25 mm, so any pitch from **18.5 to 23.5 mm** bolts up, against a plausible range of 20–22. Only that one hole is slotted: the inboard hole stays round and locates the connector, so the part can only pivot slightly about it rather than slide bodily - two slots would be the loose, needs-glue failure. The 28 mm flange covers the slot, and a washer under the screw head spans it. The USB-C keeps two round holes, its 15 mm pitch being on the drawing.

**Decision.** Both compute boards get their debug connector brought out to the **upper panel**,
in one row with the DE-9, all three centred at local z 25:

| x | Port | Goes to | Flange |
|---|---|---|---|
| **−28.58** | USB-C panel-mount extension (CY type, 20 cm) | FRDM **J11** - USB-C UART console, 115200 8N1 | 23.0 wide, screws 15 mm |
| **0** | DE-9 male, CAN (HW-18) | CAN bus stub | 30.8 wide, screws 24.99 mm |
| **+31.06** | Mini-B panel-mount extension (JSER type, 50 cm) | Discovery **CN1** - ST-LINK/V2 | 28.0 wide overall |

**Labels.** Each port is named on the panel - **IMX91 · CAN · STM32** - debossed **0.6 mm**,
4.5 mm cap height, centred on its port at z 36. They name the *board*, not the connector: the
connector is obvious by shape, which board it reaches is not. The band at z 32…40 between the
flange tops and the upper vent row holds them with 1.75 mm clear either side, and 0.6 mm into a
3 mm wall removes nothing structural.

- **Debossed, not raised.** Raised letters on a vertical wall are fragile and print mushy; a
  recess takes a paint pen - wipe across, wipe the face clean, the letters stay filled. That is
  what makes them readable without a second filament.
- **The text is mirrored in the model on purpose.** The rear face looks down **+y**, so an
  observer standing behind the vehicle sees world **+x running to their left**. Without the flip
  in `label()` every name would print backwards. This is why STM32 (x +31.06) appears on the left
  in a face-on render and IMX91 (x −28.58) on the right - that is the correct real-world reading.

**The DE-9 moves from x 2.48 to x 0.** The three flanges total 81.8 mm across an 88.47 mm flat
face, leaving 6.67 mm. Left where it was, the bays came out 28.86 and 28.81 mm - the 23 mm USB-C
fits one comfortably, but the **28 mm Mini-B would have had 0.4 mm a side and does not fit**. A
2.5 mm shift rebalances the bays to 26.36 and 31.31, giving **~1.67 mm each side of every part**.

**Why that shift is allowed.** MEC-02 recorded "keep the CAN connector central" because the deck-2
tab occupies x ±38…50 on the floor of the upper gap. That tab is at local **z 0…4**; every port
flange here is at **z 18…32**. They never interact, so the constraint was stale rather than real.
On an 88 mm face a 2.5 mm move is invisible, and x 0 is a cleaner datum than 2.48.

**Why J11 and not J1.** J1 is the *power* input, fed dumb 5 V (HW-02). J11 is the separate USB-C
UART console. Bringing J1 out here would be actively wrong.

**Consequences.**

- ⚠️ **Every aperture is NOMINAL - measure all three parts before printing.** The DE-9's 24.99 mm
  screw pitch is the only genuinely fixed number. The USB-C flange (23) and screw pitch (15) are
  read off a vendor drawing; the Mini-B's **screw pitch is inferred** from its 28 mm overall, and
  both aperture sizes are guesses at the moulded boss. All are named constants in `fascia.scad`.
- **~1.67 mm margins are tight.** If a measured part comes in larger, the cheapest fix is a
  narrower CAN connector or accepting a smaller vent column - not squeezing the margins further.
- **Verified:** the upper panel went 1904 → 2496 vertices, **+592 = exactly 2 × 296**, the same
  delta the DE-9 alone produced. Both ports cut cleanly and the panel is still a single solid.
  Adjacent screws clear each other by 8.6 mm (USB-C↔DE-9) and 8.1 mm (DE-9↔Mini-B).
- **The lower panel is untouched** and still carries only the two buttons, so the blank stays
  common and the panels stay interchangeable (MEC-03).
- **A USB-C extension is not a USB-spec-compliant thing to build.** Fine for a 115200 baud UART,
  but if the cable does not pass CC through, a C-to-C lead from the PC will not enumerate - test
  with both C-to-C and A-to-C on arrival.
- **Cable runs are upward**: both boards live in the *lower* gap (MEC-02), so each port's tail has
  to reach the upper panel. 20 cm (USB-C) and 50 cm (Mini-B) both cover ~100 mm comfortably.

---

## MEC-06 · Switch legends - DRIVE and LOGIC, not POWER

*Formerly HD-25.*

**Decision.** The lower panel names both switches, debossed 0.6 mm at 4.5 mm cap height, z 43:

| x | Legend | Switch | LED |
|---|---|---|---|
| **+24.48** | **DRIVE** | SW1 - power train | red |
| **−19.52** | **LOGIC** | SW2 - compute | green |

**Why not "POWER".** SW1 switches the power *train*. **Neither switch is a master cut-off** - that
is the battery connector (HW-08: neither switch carries full pack current). A panel reading POWER
invites someone reaching for an emergency stop to believe they have found one. DRIVE says what it
actually does and carries no such promise.

**Why z 43, when there is only 3.9 mm above a button.** A ⌀22.2 hole spans z 13.9…36.1, leaving
bands far too thin for 4.5 mm text above or below it. The upper vent row solves it: its slots sit
at x −39.69…−32.69, −5.52…10.48 and 37.65…44.65, so the **27.2 mm spans between them** are clear
from the button tops to the panel top - and each span sits almost exactly over its own button.
z 43 also clears a 26 mm switch bezel by 2.75 mm, which the hole diameter alone does not.

**Which button is which - a choice, not a record.** Nothing in the project fixed the left/right
assignment. Taken from the SW1/SW2 numbering: **SW1 leftmost as faced**. Faced from behind the
vehicle world +x runs to the observer's **left**, so SW1 is x +24.48. The opposite convention -
logic on the left, switched on first, reading left to right - is equally defensible; swapping is
one line in `labels_lower()`.

**Consequences.**

- Lower panel 1896 → 3296 vertices, still a single solid. Upper unchanged at 5058.
- **Labels are per-panel, not in the blank**, like the ports. The blank stays common and the
  panels stay interchangeable (MEC-03).
- Same debossed-and-paint-filled treatment as the upper panel (MEC-05), and the same `mirror()` -
  without it every legend prints backwards.
- **The legends assume the red switch is fitted at x +24.48.** Colour and legend must agree on
  assembly; if the switches go in the other way round the panel lies, which is worse than no
  legend at all.

---

## MEC-07 · The fascia is clamped at four corners - six M3 for the whole thing

**Updated by MEC-14:** the switch drawing gives the nut (25 A/F, 28.5 across corners) and the bare depth (25 mm), closing the check below for the switch itself. The harness depth is still open.

**Confirmed by MEC-10 (2026-09-20):** both fixing positions land exactly on real CAD holes,
and both are ⌀3.18 - the only M3-capable class on the plate.

*Formerly HD-26.*

**Decision (2026-09-18).** Each panel is clamped to the plate below *and* the plate above by a
**pad at each corner**, screwed through the plate holes that already exist at
**x −41.34 / +46.30, y 124.54** on every deck. Pads are 5 mm thick, at local z 0…5 and 45…50.
**Every nut is captive in a pad** - nothing has to be held inside the chassis.

| Joint | Screw | Driven from | Nut |
|---|---|---|---|
| Plate 1 | M3×8 | under the vehicle | captive in the lower panel's bottom pads |
| Plate 2 | M3×12 | above, in the open upper gap, downward | captive in the lower panel's **top** pads - **one screw clamps both panels**, the shared hole MEC-03 identified |
| Plate 3 | M3×8 | on top of the vehicle, downward | captive in the upper panel's top pads |

Washer under every head. Each pocket opens *away* from its own plate, so every nut is pulled onto
the closed end of its pocket as the screw tightens, and every screw is driven from whichever side
is open at that point in the build.

**Plate 2 is driven from above, not below.** The nut goes in the *lower* panel's top pad, pushed up
into its pocket from the open gap below; the screw then comes down through the upper panel's bottom
pad. The other way round - nut in the upper panel, screw upward from the lower gap - works
mechanically but asks for a blind upward drive in the gap where the FRDM and STM32 live. The upper
panel's own bottom pocket is then unused, and the washer under that head spans it.

**How this was arrived at.** The first cut of MEC-07 hung the panels on ring hangers round the
rear standoffs - screwless, dropped on during stacking. It was dropped before printing:

- **Rings locate, they do not clamp.** Bore 7.4 over a 6.0 A/F hex leaves 0.24 mm of play towards
  a corner and 0.7 mm towards a flat, ±0.36° of rotation (±0.37 mm at the panel ends) and 0.4 mm
  vertically. A panel carrying two latching switches and three connectors would have buzzed, and
  a switch press would have felt spongy.
- **Rings *and* screws is two features doing one job.** Once screws are there, they locate as well.
- **Bottom-only screws leave one direction open.** Pushing the panel in is stopped by the wrap
  hitting the plate edge after 0.4 mm, but *pulling* it - tugging a CAN or USB lead - is resisted
  only by the wall bending: about 0.3…0.5 mm of spring at 30 N, and a hard yank puts the load
  into the pad root. Clamping the top band removes it.
- **Top pads cost two screws, not four**, because plate 2's screw serves both panels.

**Why not the old 8 × M3 of MEC-03.** Same clamping for six screws instead of eight, and the
shared plate-2 hole is now used deliberately rather than worked around.

**Fixed along the way - the old wall collided with the decks.** The MEC-02 wall followed the plate
edge *on* the plate: its inner face was 0.3 mm inside the rear flat and up to ~3 mm inside along
the taper. Since each panel wraps the deck above (z 50…52), both printed panels would have hit a
deck across their whole width. The wall is now the plate outline offset by **0.4 mm clearance +
3 mm wall**, so it passes outside the deck edge. The rear face moves from y 134.24 to **134.94**,
which also widens the flat from 88.47 to **94.24 mm** - every port bay gained ~3 mm (MEC-05).

**Consequences.**

- **Assembled during stacking**, because each panel wraps the deck above it: lower panel in,
  plate 2 on, upper panel in, plate 3 on, then the six screws. Removal reverses that - this is a
  build-once fascia, which is what it is for.
- **Locked in all six directions** once the screws are tight. The only remaining motion is elastic.
- **Verified with a clash render.** `PART="clash"` intersects both panels with a stand-in of the
  three rear plates (holes and cross-slot cut) and the four rear standoffs: **zero volume** - the
  944 triangles it returns are the pad faces lying on the plates, which is the clamp itself. As
  controls, the same check on the pre-MEC-07 STLs returns solid overlap through the full panel
  height, and forcing `CLR=-0.3` returns 159 mm³. Both panels are single solids (CGAL: 2 volumes).
- **Parts:** 124.2 × 18.9 × 52 mm, 20.5 / 21.7 cm³ - about 26 and 28 g in PETG (was 19.0 / 20.2
  cm³ with the MEC-03 tabs). Re-quote before ordering.
- **Pads clear the standoffs** by 8.35 mm centre to centre, nicked to leave 0.5 mm, and sit in the
  z bands nothing else uses: vents 7…10 and 40…43, buttons and their nuts ~10…40, port flanges
  18…32.
- **Print orientation unchanged** - flat on the rear face, pads and nut pockets facing up and
  down, no support.

**Check before printing.** Switch depth with the spade terminals fitted, and the mounting nut's
outside diameter (switches arrive 29 Sep – 13 Oct): the body must clear the motors at y 101.7 -
a 25 mm body now ends at y ≈ 109.9, about 8 mm clear - and a nut over ~30 mm across would reach
the pad bands.

---

## MEC-08 · The STM32 rides on a perfboard carrier, not on the chassis directly

**Resolved 2026-09-20:** the Discovery's P1/P2 pins protrude **downward**, so the carrier sits
**below** the board and the Discovery drops onto female headers. The open question about pin
direction is closed, and the arrangement in the carrier schematic is the correct one.

*Formerly HD-27.*

**Decision (2026-09-20).** The Discovery plugs into a hand-built **prototype-PCB carrier** (5.11).
The carrier is what bolts to the chassis; the Discovery is a module that lifts out. Everything the
board needs crosses one board-to-board interface instead of a loom of flying leads.

**UM1472 says this is the intended use.** §4.9: *"The male headers P1 and P2 can connect the
STM32F4DISCOVERY to a standard prototyping/wrapping board."* The headers ship populated and the
100 mil pitch matches the perfboard grid, so no adapter is invented.

| Carries | From | Note |
|---|---|---|
| **5 V in + GND** | Bauer 50 W via SW2 (HW-17) | §4.3: the 5 V pin is a valid **input**, and **D1/D2 protect it from external supplies** - the rail and the ST-LINK USB cannot fight |
| **CAN PD0 (RX) / PD1 (TX), AF9** | P2 | Put the **SN65HVD230 on the carrier** - it keeps the TX/RX stubs to a few cm and gives H/L/GND one clean twisted exit |
| **I²C2 PB10 SCL / PB11 SDA** | P2 | INA226, and possibly the motor module on the same bus at a different address (HW-10) |
| **Servo PWM** | STM32 → 3.18 UBEC'd servo | Signal only; the servo's power never touches this board |
| **3.3 V for the transceiver** | Discovery 3 V pin | ⚠️ §4.3: 5 V and 3 V as **outputs are limited to 100 mA**. The SN65HVD230 is ~10 mA, fine - but **nothing else may hang off them**, in particular not the motor module |

**Why a carrier rather than mounting the Discovery directly and running flying leads.**

- **Vibration.** Dupont jumpers are the project's known weak point (5.7: copper-clad aluminium,
  crimps that degrade under vibration). A carrier turns dozens of vibrating individual crimps into
  one seated header pair plus soldered joints.
- **The Discovery becomes replaceable.** Unplug and swap without unpicking the loom - worth a lot
  on a board carrying the only ST-LINK.
- **One ground reference.** The carrier gives a single point to bring back to the (−) WAGO bus,
  which is what HW-06's star ground asks for.

**Consequences.**

- ⚠️ **Check which way P1/P2's pins protrude on the board in hand.** The plan assumes the
  Discovery drops *onto* female headers. If the pins stand proud of the top face only, the carrier
  sits above the board instead of beneath it, or the headers need re-soldering. **This is the one
  thing that decides the mechanical arrangement, and the board is on the desk.**
- **Board size:** P1/P2 run the long edges, 25 pins = 63.5 mm, and the Discovery is ~97 × 66 mm.
  The carrier must span ~70 × 66 mm minimum - a 70 × 90 mm perfboard from the kit is enough; it
  does not have to match the Discovery's footprint.
- **Dry-fit before soldering anything.** The P1–P2 row spacing must land on the 2.54 mm grid.
  UM1472's wording implies it does, but a dry fit costs nothing and a misjudged row spacing wastes
  the board.
- **Two PC ground paths now exist** - the fascia Mini-B ST-LINK (5.10) and the CAN debug port
  (HW-18) both tie PC ground to battery ground. This makes the **isolated** USB-CAN adapter in 4.7
  a requirement rather than a preference.
- **Height:** carrier + female header + Discovery is ~28 mm in a 50 mm gap. It fits, but board
  placement must still stay forward of **y ≈ 109** where the switch bodies intrude (MEC-02).

---

## MEC-09 · The two deck gaps are 50 and 40 mm - the panels are different parts

*Formerly HD-28.*

**Decision (2026-09-20).** Measured on the built kit: the **lower gap is 50.00 mm and the upper is
40.00 mm**. The kit ships two standoff lengths. The fascia is therefore two different panels -
**52 mm** and **42 mm** tall - and MEC-03's "one blank, two panels" is dead.

**Where the wrong number came from.** Hiwonder's `.3dm` is the **single-plate** version: one 50 mm
standoff. Our 3-deck model was built by duplicating that plate *and its standoffs*, which silently
asserted a second 50 mm gap. MEC-02 then recorded "three decks at 52 mm pitch (confirmed on the real
kit)" - a confirmation that never actually happened. Tape measurements off the build photos put the
upper gap at ~45, close enough to 40 to prove the equal-gap assumption wrong but not to replace it;
the standoffs themselves settled it.

**The corrected stack.**

| | z |
|---|---|
| plate 1 | 27.12 … 29.12 |
| **lower gap 50** | 29.12 … 79.12 |
| plate 2 | 79.12 … 81.12 |
| **upper gap 40** | 81.12 … 121.12 |
| plate 3 | 121.12 … 123.12 |

**What changed in the model.** `fascia.scad` is now parameterised per gap: `SO_L`/`SO_U` drive
`GAP_L`/`GAP_U`, panel heights, and each panel's cut-out centre (`FZ_L` 25, `FZ_U` 20).

- **Lower panel: unchanged.** 52 mm tall, buttons at local z 25, vents at 8.5 and 41.5. The STL is
  identical to the pre-MEC-09 one.
- **Upper panel: 42 mm tall**, ports at local z 20 (world 101.12), pads at 0…5 and 35…40.
- **Its vents moved** to rows at 9 and 31 (`VENT_DZU` 11). A 40 mm gap leaves only two clear bands -
  5…13.7 and 26.3…35, between the pads and the DE-9 flange - and the rows sit centred in them,
  keeping the ~3 mm margins MEC-04 asked for. Slot pattern and columns are untouched.
- **Its labels moved** to z 34.5, between the upper vent row and the wrap line.
- **Volumes:** lower 20.5 cm³ (26 g PETG), upper 17.5 cm³ (22 g) - the upper panel got cheaper.

**Consequences.**

- **No interchangeability.** A panel fits one gap only. Mark them on the inside face before fitting.
- **Six M3 unchanged** - the pads sit at each panel's own top and bottom, so MEC-07 is unaffected.
- **Verified:** `PART="clash"` is still zero volume against the corrected stack (plate 3 at 121.12),
  both panels single solids, and `CLR=-0.3` still returns 159 mm³ as the control.
- **`chassis-3deck-fascia.obj` is corrected too** - `make-assembly.py` drops our duplicated deck 3
  by 10 mm and shortens its four standoffs to 40 mm about their bases. The right fix is in the
  source CAD; this keeps the mock-up honest until then.
- **The chassis layout drawing** now states both gaps and draws the elevation to scale.

**Still assumed:** that both panels' gaps are uniform across the vehicle - i.e. that all four lower
standoffs are 50 and all four upper ones 40. Worth a glance when the panels go in.

---

## MEC-10 · The chassis holes are three sizes - and half of them are M2.5, not M3

**Decision (2026-09-20).** Fixings follow the hole that is already there, not a single preferred
thread. Surveyed from Hiwonder's CAD via the chassis layout: **64 holes per plate, in three
classes**.

| ⌀ | Count | Takes | Used for |
|---|---|---|---|
| **3.18** | 32 | **M3**, close fit (0.09 mm a side - not a clearance fit) | fascia clamps, STM32 carrier |
| **2.71** | 28 | **M2.5** clearance | compute boards on their own standoffs |
| **2.47** | 4 | M2.5 tight / M2 | - |

**MEC-07's fixing holes are verified.** Both clamp positions sit on real holes at **distance
0.00**, both ⌀3.18, spaced **87.65 mm** against `FIX`'s 87.64. `fascia.scad`'s "existing 3.2 mm
plate holes" is right to 0.02 mm.

**The M3 grid.** The ⌀3.18 holes form a regular block over the rear two-thirds - x stations
**99.24 · 148.18 · 196.88 · 245.88** (pitch ≈ 48.9) against y **23.76 · 38.76 · 81.76 · 96.76**
(pairs 15 apart, pair centres 58 apart). Usable rectangles are therefore **48.9 / 97.7 / 146.7**
wide by **43 / 58 / 73** deep. Plus pairs at x 104.41, 186.12, 50.00 and the clamps at 262.94.

**The M2.5 grid** is sparser but has one large rectangle: **58.00 × 92.00** at x 169.88/227.88,
y 14.24/106.24 (with 86 and 80 variants using the inner y holes), and **71.10 × 48.60** at
x 49.00/120.06.

**Why this matters.** The intent was "M3 everywhere". **Half the plate cannot take M3**, and the
M2.5 assortment already bought is the right kit for those. Forcing M3 would mean drilling out
28 holes in an anodised plate - for no gain, since the boards' own standoffs are M2.5 anyway.

**Consequences.**

- **Boards mount M2.5 into ⌀2.71**, on their own standoffs, the way the FRDM already is.
- **The STM32 carrier is ours to design, so its holes go onto the M3 grid** - MEC-08's carrier
  should be re-cut so its four holes land on a chassis rectangle rather than wherever is convenient.
- **M3 in ⌀3.18 is a close fit.** With the fascia's two screws 87.65 mm apart and 0.09 mm a side,
  the panel pads carry the tolerance. If a panel fights going in, ease the *panel*, not the plate.
- The survey lives in the chassis layout drawing, which draws all 64 holes per plate to scale.

**Resolved by MEC-11.** The FRDM's pattern came out of NXP's drill file, not a measurement, and
the transverse hypothesis above was wrong - it mounts fore-aft on the M3 grid.

---

## MEC-11 · The FRDM's mounting holes land on the Hiwonder grid - 0.06 mm out

**Decision (2026-09-20).** The FRDM-IMX91 bolts **fore-aft to plate holes that already exist**, on
four of its six mounting holes, with **M2.5 screws and washers up through the chassis** into the
female standoffs the board already carries.

**Where the pattern came from.** NXP's design files (`FRDM-IMX91_DESIGNFILES-Rev A1`), drill file
`LAY-94610_A1-1-10.drl`, tool **T11 = 106 mil = 2.692 mm, non-plated, quantity 6** - M2.5
clearance, and six of them, matching the standoffs on the board. Neither UM12262 nor the QSG
publishes this; the drill file is the authority.

| FRDM hole (board datum, mm) | |
|---|---|
| (3.5, 3.5) · (3.5, 61.5) | 3.5 mm inset all round - confirms the 105 × 65 outline |
| (52.5, 3.5) · (52.5, 61.5) | |
| (101.5, **23.0**) · (101.5, 61.5) | the sixth is pulled inboard, so the six are **not** a grid |

**The match.** FRDM spacings are **49.00 mm in x, 58.00 mm in y**. The chassis M3 grid (MEC-10)
is **48.94 in x, 58.00 in y**. That is **0.06 mm out in x and exact in y** - the board was never
designed for this chassis, and it fits anyway.

| FRDM hole | Chassis hole |
|---|---|
| (3.5, 3.5) | **(99.24, 23.76)** |
| (3.5, 61.5) | **(99.24, 81.76)** |
| (52.5, 3.5) | **(148.18, 23.76)** |
| (52.5, 61.5) | **(148.18, 81.76)** |

Board then spans **x 95.74 … 200.74**, y 20.26 … 85.26 - 7.5 mm off the centreline, which is
free to swap to the y 38.76/96.76 pair if the other side suits the wiring better.

**Why M2.5 into a ⌀3.18 hole is right.** The chassis holes on that grid are ⌀3.18, so an M2.5
screw has 0.34 mm a side of slop. **A washer spans it** - and the kit already bought has 60 of
them. The slop is a feature here: it absorbs the 0.06 mm pitch error without a fight.

**Consequences.**

- **Only four of the six holes are used.** The fifth (101.5, 23.0) has no chassis hole near it and
  the sixth is 0.36 mm out. Four M2.5 on a 105 × 65 board is ample.
- **Both boards cannot share plate 2.** The FRDM occupies x 95.7–200.7, which swallows the 196.88
  x-station. The STM32 carrier needs its own deck - see the layout note below.
- **The carrier is ours, so its holes are designed onto the grid**, not measured off it: four at
  **49.00 × 58.00**, which is an exact chassis rectangle (x 196.88/245.88 against y 23.76/81.76).
  That supersedes MEC-08's arbitrary 80 × 120 outline.
- **Recommended split:** carrier on **plate 2** (its I/O - servo PWM, I²C, motor module - all runs
  down to plate 1), FRDM on **plate 3** (Ethernet and Wi-Fi 6 want clear air, not a metal plate
  10 mm above them). Both plates are identical, so both use the same grid coordinates.

**To confirm.** Standoff height under the FRDM: the microSD is on the **underside** and a card is
fitted, so the standoff sets card access, not just clearance.

---

## MEC-12 · Component allocation across the three plates

**Decision (2026-09-21).** Parts sit where their function puts them, not where a rule puts them.

| Plate | Carries |
|---|---|
| **1** (z 29.12) | front to rear: steering servo and axle, **battery** (x 55-132), **INA226** and **UBEC** above a **3 x WAGO 221-415** column (x 135-153.6), **motor driver** (x 158-200), motors from x 203.2 |
| **2** (z 81.12) | **STM32 carrier** (x 93.2-223.2) and the **Bauer 50 W converter** (x 20-85). Rear region x 224-266 left clear for the harness |
| **3** (z 123.12) | **FRDM-IMX91S** |

**Order along the vehicle (revised 2026-09-21).** The first cut put the motor driver at x 54-96,
so both motor looms ran the length of the chassis to reach the motors at x 203. The driver now
sits at **x 158-200, 3.2 mm clear of the motors**, and the battery moved forward into the waist
to make room. The heavy, electrically noisy motor wiring is now the shortest run on the plate
instead of the longest, and it no longer crosses the sensing and distribution area.

**Why this split and not "power low, compute high".** That rule was the starting point, but two parts
argue harder than the rule:

- **The INA226 cannot leave plate 1.** Its shunt is in the battery path, so moving it up would drag
  the full pack current onto the compute deck. The same logic keeps the WAGO buses low: they are
  where the high current is distributed, and the switches they feed sit in the lower gap.
- **The UBEC belongs near the servo**, which is at the front of plate 1. Putting it on plate 2 would
  run 6 V down a deck and back forward for no gain.

**Why the converter goes up.** The Bauer feeds only 5 V loads, both of which are above it: the
carrier on plate 2 and the FRDM on plate 3. Plate 1 also has no contiguous space left once the
battery (99.9-176.9) and motors (from 203) are placed; the free gaps there are 52 mm at the waist
and 26 mm behind the battery.

**Consequences.**

- **12 V climbs one deck and comes back down.** Battery on plate 1, converter on plate 2, motor
  driver back on plate 1. Accepted: the alternative was no home for the converter at all.
- **The rear of plate 2 (x 224-266) is deliberately empty.** That is where the harness to the three
  fascia debug ports fans out, and filling it would make the one part of the loom that gets
  unplugged regularly the hardest to reach.
- **Plate 1 packing is now high.** Region A (x 52-98) holds the motor driver, region B (x 177-203)
  the WAGO column, and the band above the battery the INA226 and UBEC.

**To confirm.** **Two footprints on the drawing are placeholders**, and both are on the critical
path: the **Bauer 50 W** (drawn 65 x 55) and the **Hiwonder motor driver** (drawn 40 x 60). Neither
is measured, and the Bauer is the larger risk since plate 2's front region is only 80 mm wide at
the waist.

---

## MEC-13 · The debug ports mount from behind, in two horizontal rows

**Decision (2026-09-24, layout revised 2026-09-25).** Both panel-mount extensions sit in
**pockets on the inside face** of the upper panel, not on its outside. All three ports are
**horizontal**, in **two rows**: the DE-9 alone on top, the two USB debug ports side by side
below. The layout is **centred on what shows on the face** (the flanges are hidden inside): the
DE-9 on the chassis centreline XC, the two USB sockets 19 mm either side of it, and the group
centred on the 42 mm face height. Every connector body clears the rear standoffs:

| Row | x | Port | Mounting | Held by |
|---|---|---|---|---|
| top, z 26 | **+2.48** (XC) | DE-9 (4.5), unchanged in itself | from behind, as before | its own screws, as before |
| bottom, z 9 | **−16.52** (XC − 19) | USB-C (5.9), flange 23 × ~8.3 × 6 deep | pocket 23.6 × 9.0, **1.2 mm skin**, rim slot 9.6 × 3.8 | its own **2 × M2.5 × 5** from outside, through the skin into the flange's metal inserts |
| bottom, z 9 | **+21.48** (XC + 19) | Mini-B (5.10), flange **36 × 10 × 8 deep** | pocket 36.4 × 10.4, **1.5 mm skin**, grip aperture 14 × 9.5 | its own M2.5 screws from outside, inboard hole round, outboard a slot |

Local z is measured from the top of deck 2; world z is 81.12 higher (top row 107.12, bottom row
90.12).

**What the parts showed (measured 2026-09-24).** Both extensions have **threaded M2.5 holes** in
the flange face, so the screws come from the front and the flange has to sit behind the wall.
Neither body can pass through the panel. And the Mini-B flange is **36 mm**, not the 28 read off
the vendor photo in MEC-05.

**Why.**

- **The bodies run forward into the vehicle, past the rear standoffs.** The USB-C body is ~14 wide
  and ~40 long; at MEC-05's x −28.58 it overlapped the left standoff (flat at x −32.61) by ~3 mm.
  Only the flanges had ever been modelled, never the bodies. At **x −16.52** it clears by **9.1 mm**.
  The Mini-B body (~20 wide) at x 11.5…31.5 clears the right standoff (flat at x +37.57) by 6.1 mm.
- **Three flanges side by side no longer fit.** 23 + 30.84 + 36 = 89.8 mm on a 94.24 mm face, and
  the two standoffs pin the outer bodies inward. Two rows take the width problem away: the bottom
  row carries 23 + 36 = 59 mm with 8.5 mm between the flanges, and the DE-9 has its row to itself,
  so it goes back on the chassis centreline.
- **Centred on what is visible.** The flanges sit behind the wall, so centring them would leave the
  sockets off-balance. The sockets, screws and labels are what the eye reads, so the USB sockets
  are placed symmetric about the DE-9 (±19) and the visible group, apertures at z 4.25 up to the
  CAN label at 37.75, is centred on the face height.
- **The rows fit the 40 mm gap with room left.** Bottom-row flanges span z 4…14, the DE-9 flange
  z 19.7…32.3, which leaves 5.7 mm between the rows and 7.7 mm to the wrap line at z 40. Nothing
  in either row reaches the fixing pads (z 0…5 and 35…40, x beyond ±36.7).
- **The USB-C uses its own screws, the way the vendor's bracket does.** The part ships with a
  ~1 mm steel bracket and two M2.5 × 5 screws driven from the front into the flange's metal
  inserts. The heads are **~4 across, 15 apart**, which leaves **~11 mm** clear between them. The
  bench cable's round grip is **10 mm** (tape-measured), and a photo of it seated in the vendor
  bracket confirms it clears the heads. Metal threads survive any number of refits.
- **The Mini-B uses its own screws too.** They are ~28.5 apart, so the heads sit ~11.7 mm from
  centre, far outside any Mini-B grip.
- **Skins, not full walls, in front of the sockets.** The USB-C metal rim stands ~0.9 proud of its
  flange, so a 1.2 skin leaves the socket face ~0.3 below the outside and the plug seats with the
  grip clear of the panel. The Mini-B surround is flush with its ears, so its grip enters a 1.5 mm
  skin through a generous aperture.
- **Rejected: the Mini-B standing upright** in a single row (USB-C −25.0 · DE-9 +3.25 · Mini-B
  +25.0, 2026-09-24). It fitted, but left one port turned 90° to the others and pushed the STM32
  label onto its side. Two horizontal rows read as one panel and give every part more margin.
- **Rejected: two rows packed to the left** (USB-C −25.0, Mini-B +12.0, rows at z 11 and 28). The
  first two-row draft kept the USB-C where the single row had it, which left the group visibly
  off-centre and the USB-C body 0.61 mm from its standoff.
- **Rejected: turning the DE-9 around**, mounting it from the front so its flange sits outside the
  others. In the single-row layout it would have put the DE-9 flange on the outer face exactly
  where the Mini-B's screw heads went.
- **Rejected: a printed clip behind the USB-C flange.** It was designed first, for the worst case:
  the USB-C spec allows a plug grip up to **12.35 wide**, which would land on the heads and stop the
  plug ~1.8 mm short of seating. The clip pressed the flange's side shoulders and was screwed to two
  printed bosses. It worked with any cable, but it added a part and put the thread in printed PETG
  instead of the flange's metal inserts. Dropped once the real cable proved narrow enough. Thinning
  the wall or countersinking the heads does not fix a fat grip: a countersunk M2.5 head is ~1.5
  tall, and only ~0.9 mm lies between the flange face and where the grip ends up.

**Consequences.**

- **The USB-C debug lead must have a slim grip, under ~11 mm.** The 10 mm bench cable fits. Most
  chunky USB-C cables (11.5-12.5 mm) will stop on the screw heads and not seat. Keep one slim
  cable as the robot's debug lead.
- **Each label sits directly above its port.** IMX91 and STM32 at z 14.75…19.25, between the
  screw heads and the DE-9 aperture; CAN at z 33.25…37.75, above the DE-9.
- **The upper vents are laid out after the ports, in the space they leave (updates MEC-04 for
  this panel).** Symmetric about XC like the ports, and deliberately not matched to the lower
  panel: one upright slot at each end (XC ± 40.5, z 8…32) and two flat slots in each top corner
  beside the DE-9 (XC ± 28.25, z 23 and 30, 17.5 long). That is 118 mm of slot against 60 before.
  The right upright slot keeps 1.8 mm of web to the Mini-B pocket. The lower panel's vents are
  unchanged.
- **The upper panel is now 16.3 cm³** (~21 g PETG).
- **`PART="portclash"` is a second gate**, beside `clash`. It checks rough stand-ins of the three
  connectors, including the screw heads, against the upper panel, the rear chassis and each
  other. It renders **zero volume**; the faces it returns are the flange-on-pocket contacts.
- **No thin margins left.** The closest are 6.1 mm from the Mini-B body to the right standoff and
  1.8 mm of web between the right vent and the Mini-B pocket.

**To confirm.**

- **USB-C body width** behind the flange: 14.0 is read off a photo. It is no longer critical:
  anything up to ~31 mm clears the standoff.
- **The grip limit** rests on a tape measure: collar 10, heads 4, so ~0.5 mm a side. The photo of
  the cable seated in the vendor bracket is the stronger evidence.
- **Mini-B screw pitch** (~28.5, photo). The outboard slot takes 27…30.
- **Mini-B body**, ~20 × 10 × 13 (photo). It has 6.1 mm to the standoff, so it would have to be
  over 32 mm wide to touch.
- **The DE-9 rear insulator** is assumed 19 × 10.5 × 8 in the stand-in, not measured.

---

## MEC-14 · The switch drawing closes the lower panel - and its holes open to 22.4

**Decision (2026-09-24).** The lower panel's two switch holes are **⌀22.4**, up from 22.2. The
vendor drawing for the 22 mm switches (3.5a/3.5c) settles everything else the printed part
depended on, so the lower panel is ready to print.

| From the drawing (22 mm version) | What it settles |
|---|---|
| Thread **M22 × 1**, mounting hole 22 | the hole |
| Bezel **⌀24.8 × 2.0** | sits on the outer face. The DRIVE / LOGIC labels at z 43 clear it by 3.35 mm |
| Nut **25.0 A/F, 28.5 across corners** | under MEC-07's ~30 mm limit before a nut reaches the pad bands. The two nuts, 44 apart, are 15.5 mm apart |
| Thread length 14.2 | 3 mm wall plus nut uses ~6 of it |
| Body **20** behind the bezel, tabs **5** more | 25 mm: exactly the depth MEC-07 assumed, ending at y ≈ 109.9, 8 mm clear of the motors |
| Tabs **4.8 mm** wide | not 6.3 as BOM 3.17 assumed |

**Why 22.4.** 22.2 left 0.2 mm over a 22.0 thread. FDM holes from a print service commonly come out
0.1-0.2 mm small, which would leave the thread binding or no clearance at all. The bezel and nut
cover a 22.4 hole with 1.2 mm to spare a side.

**Consequences.**

- **MEC-07's "check before printing" is closed** for the switch itself: nut size and bare depth
  are on the drawing.
- **The wiring on the tabs is still open.** The red plug-on socket harness runs straight back;
  if the bezel-to-wire-exit depth is over ~33 mm it reaches the motors. The seller has been asked.
  The fallback is 4.8 mm flag (right-angle) receptacles, which add only 2-3 mm past the tabs.
- **BOM 3.17 is 4.8 mm receptacles, not 6.3.**

---
