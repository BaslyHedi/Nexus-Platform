# Hardware

Build drawings for NEXUS. Each is an `.svg` - the editable source and the only copy.

**No PDFs.** They are generated once, when the design is frozen. Until then the SVG is the
truth and a stale PDF beside it is just a second thing to get wrong. To read one, open the
SVG in a browser; to render, point headless Chrome at it.

| Drawing | Owns |
|---|---|
| [chassis-layout.svg](chassis-layout.svg) | Where components sit on the **three** decks, to scale at 1.7 px/mm, plus the side elevation of the deck stack |
| [wiring-schematic.svg](wiring-schematic.svg) | What connects to what - fuses, switches, wire gauges, 5 V rails, CAN, I²C, motor control |
| [stm32-carrier.svg](stm32-carrier.svg) | Soldering and wiring for the three kit boards: A and B, which the Discovery drops onto, and C, the 5 V split. Component side and solder side, hole by hole, with netlist and pre-solder checks (MEC-08, MEC-15, HW-19) |
| [`../decisions/README.md`](../decisions/README.md) | **Why** the drawings look the way they do - HW, MEC, SYS and SW entries, each with its reasoning and consequences. Not in this folder any more |

Part numbers, prices and status live in [`../bom/BOM.md`](../bom/BOM.md);
datasheets in [`../bom/`](../bom/).

## Still open

### Plate 1, the motor driver - fitted 2026-09-21

Footprint and position are both settled and the drawing matches the hardware. Geometry, the
as-mounted coordinates and the method behind them are in
[`../bom/parts/2.4-Encoder-Motor-Module/SPECS.md`](../bom/parts/2.4-Encoder-Motor-Module/SPECS.md).
In short: **42 x 58 at x 168-210, y 22.6-80.6**, long axis across the vehicle, connector edge to
the vehicle's right, **2 x M3 and spacers through the chassis slot at x 203.5**.

No chassis hole pattern matches the board's 32.4 x 48.4 - all 96 plate-1 features were searched,
nothing within 1.5 mm in either orientation - so that one slot is the whole fixing, and it takes
both rear holes anywhere along its length. What is still open:

- **The front pair is not fixed.** Two screws on one line let the board pivot. The front-left hole
  (y 75.8) sits **directly over the 14.6 x 59.8 cutout**, so a cable tie there is a straight pull
  with no diagonal; the front-right (y 27.4) lands on solid plate 3 mm past the cutout's end and
  can tie diagonally to the ⌀2.71 hole at x 169.9, y 20.2. Two ties, no new parts.
- **Spacer height is now a clearance, not a preference.** The board's rear 7 mm sits over the
  front of the motor cans, and at x 210 the ⌀33 can is only 10.7 mm above the plate. Measure what
  is fitted before ordering more.
- **M3 spacers are still not in the BOM** even though they are on the vehicle.
- **VM cannot be fed the way every other load is.** Input is a 2-pin 2.5 mm connector, about 3 A
  and 22 AWG, while the drive branch is 18 AWG behind a 5 A fuse and can see 4.6 A with both
  motors stalled. The adapter, and whether to double up through the 3-pin port, is open.
- **The board sits 8.6 mm off the centreline** because the forward screw is at the end of its
  slot. Fine as it is; the UBEC it displaced no longer sits on the floor at all (MEC-16).

### Plate 1, the clips and the fuses - proposed 2026-09-28

The floor now carries only the INA226 and two 221-415 buses, in the bay between the pack and the
driver. The main fuse, the SW1 split, the motor and UBEC fuses, the UBEC and seven 2-port splices
hang under plate 2 (MEC-16), and the logic fuse is gone (HW-20). The drawing lists all 16 runs
with cut lengths. What it still rests on:

- **Clip outlines**: 221-415, DOMAXWILL 3-port and 2-port, and which face the wires enter.
- **Fuse holder body**, with calipers - 50 x 18 x 30 is scaled off a photo.
- **Battery height, driver top height, rear wheel tops** - they set the clear air under plate 2
  and whether the two lids over the motors can be reached from the side.
- **SW1 / SW2 tab layout** and the lengths of the SM-2P mating lead and the Bauer's own leads.

### Elsewhere

- **The carrier and board C are placed but not fitted** (MEC-15). The carrier's header row 1 is at
  x 181.20, fixed at four existing plate-2 holes. Board C sits across the waist at x 85.5-115.5, on
  the M3 pair at x 99.24. Two of the carrier's holes are drilled off grid, marked from the plate.
  Still to check: six 10 mm M2.5 standoffs in stock, and the Bauer not moving rearward into C.
- **The Bauer 50 W is still parked** on plate 2 with a `?` on it, because its 54 mm ear pitch
  matches no chassis rectangle.
- **Battery straps are not bought and the kit ships none** (BOM 3.24). Two 20 mm hook-and-loop
  straps and a non-slip pad; the pack is soft shrink wrap, so nothing narrow goes on it. Routes
  are drawn: front through the 23.9 x 10.3 slots at x 56-80, rear through the 48.3 x 5.3 slots
  at y 12.5 and 108.
- **The pack's real capacity is unknown.** 63 x 77 x 20 with the leads on a 63 face is three
  21700s in a single row, so 3S1P and **4300-5000 mAh, not the 6000 on the label**. Measure it on
  the first full discharge through the INA226 - it is the denominator for coulomb counting.
- **The CAN matrix is still to draw** - message IDs, rates, payloads.
- Switch depth and mounting-nut OD, once SW1/SW2 arrive (MEC-07).
- USB-C and Mini-B aperture sizes on the parts ordered 20 Sep (MEC-05).

## Related 3D files

The rear fascia and the chassis CAD live in
[`../mechanical/`](../mechanical/). Its
[README](../mechanical/README.md) owns the file-by-file description, the build
commands and the `PART="clash"` check that must pass before any print. The decisions behind the
panels are MEC-02, HW-18 to MEC-07 and MEC-09 in
[`../decisions/README.md`](../decisions/README.md).
