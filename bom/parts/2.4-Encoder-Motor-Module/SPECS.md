# 2.4 - Hiwonder Encoder Motor Module V1.4 · geometry and ports

Vendor page: [4-Channel Encoder Motor Driver with Onboard Voltage Regulation
Circuit](https://www.hiwonder.com/products/4-channel-encoder-motor-driver). This file owns the
**physical** numbers for the module; BOM 2.4 owns its status and the wiring decisions live in
`Architecture/Design-Decisions/HW-Electrical-Decisions.md` (HW-11).

## Where the numbers come from

**Measured 2026-09-21 from a photograph** of the board lying on 5 mm graph paper, no calipers.
Method, so the uncertainty is honest:

1. The paper grid gives a first scale, ~9.85 px/mm, but the board sits ~2 mm above the paper and
   the camera was ~150 mm away, so anything on the board top face is magnified ~1.5 % relative to
   the paper.
2. The scale actually used is taken **off the board itself**: the `SCL SDA GND 5V` pads are a
   2.54 mm header, measured at 25.37 px per pitch → **10.00 px/mm** on the board's top face. That
   cancels the parallax.
3. Outline edges found by sub-pixel threshold crossing on 60+ scan lines per edge; corner holes
   found by fitting circles to the plated annulus (radial-gradient search, all four agreeing on
   r = 30.5 ± 0.5 px).

Cross-check: the width that falls out, **42.06 mm**, lands on the vendor's "approximately
58 x 42 x 10 mm" without being told to. That is the confidence in the rest.

## Board

| | Value | Confidence |
|---|---|---|
| Outline | **42.0 x 58.0 mm**, 10 mm tall | vendor figure, confirmed by measurement |
| Corner radius | ~3.5 mm | measured |
| Corner holes | **four, round** - ⌀ **3.8 ±0.3 mm**, plated, annulus OD 6.1 mm | measured |
| Hole pattern | **32.4 x 48.4 mm ±0.4** | measured |
| Hole inset | **4.8 mm from each edge**, all four the same | measured |
| Tallest parts | the two 220 µF cans lie flat; C5 stands ~10 mm | photo |

**The holes are round, not slotted.** The earlier BOM entry said slotted; the circle fits are
clean and all four annuli are concentric rings.

⌀3.8 takes an **M3 with 0.4 mm of slop a side**. Too loose to call M3 clearance, too tight for
M4 - and M3 is now confirmed, because the board is bolted to the chassis through two of these
holes (see *As mounted*, below). The 32.4 x 48.4 pattern is confirmed the same way, off a second
set of photographs at a different scale.

[`hole-template-1to1.svg`](hole-template-1to1.svg) is still here and still worth printing if the
pattern ever has to go into a bracket or a printed tray: at exactly 100 %, check the 50 mm scale
bar with a ruler, then lay the board on it.

## Ports

All three power/host connectors are on **one 42 mm short edge**. The four motor ports are on the
two 58 mm long edges, two per side: **M1 and M3 share one edge, M2 and M4 the other** - which is
what decides the module's orientation on the deck.

| Port | Type | Pins | Note |
|---|---|---|---|
| M1 … M4 | PH2.0, 6-pin | `M+ VCC A B GND M-` | motor power and encoder in one lead. M1/M3 on one long edge, M2/M4 on the other. Centres ~15 mm and ~43 mm from the connector edge |
| **Power port** | 2-pin, 2.5 mm class (XH2.54 family), side-entry | `+ -` | main VM input. Body ~5.2 mm wide, pins ~2.6 mm apart measured |
| **3-pin power port** | servo lead, 2.54 mm, side-entry | `- + nc` | Hiwonder: "use a 3-pin wire (servo cable) to supply power to this module from another powered module". Same VM rail as the 2-pin - **confirm with a meter before relying on it** |
| **IIC port** | 4-pin, 2.54 mm, side-entry | `SCL SDA GND 5V` | body ~13.3 x 9.5 mm, **overhangs the board edge by ~3.5 mm**; allow ~15 mm beyond that edge for the mating lead |
| serial | 4-pin, 2.54 mm | `GND TX RX NC` | not used in NEXUS |

### ⚠ The IIC port's 5 V pin is an OUTPUT

Vendor spec: *power output VM, 5 V, 3.3 V · 5 V output current 1 A*, and Hiwonder support
confirms the 5 V sits on the IIC 4-pin header. So the STM32 link uses **SCL, SDA and GND only**.
Landing that pin on the carrier's 5 V rail would parallel this module's regulator with the
Bauer 50 W, which is two supplies fighting over one rail. Leave it unconnected and say so on the
harness label.

## As mounted on plate 1 - 2026-09-21

Fitted to the chassis and measured back off two photographs: a top view and an underside view,
scaled against the chassis slot pitch (the four rear slots are 16.00 mm apart in the CAD).

| | Value |
|---|---|
| Fore-aft | board **x 168 - 210**, holes at x **172.8** and **205.2** |
| Across | board **y 22.6 - 80.6**, holes at y **27.4** and **75.8** |
| Centre | x 189, y 51.6 - **8.6 mm off the centreline, toward the vehicle's right** |
| Long axis | **58 across the vehicle**, 42 fore-aft |
| Connector edge | faces the **vehicle's right** (y decreasing). Power at x 176-182, IIC at x 182-195, 3-pin at x 195-200 |
| Motor ports | M1 and M3 face **forward**; M2 and M4 face the motors and are unused |
| Fixing | **2 x M3 + spacers** through the 4.29 mm chassis slot at **x 203.5 - 207.8**. Front pair unfixed |

**The two photographs independently reproduce the hole pattern.** The screw pair measures
48.4 mm apart and the two hole rows 32.4 mm apart, off a completely different image at a
different scale from the graph-paper shot. That is the template check, passed in hardware.

**Why the ports face forward.** The board's rear edge is at x 210 and the motors begin at
x 203.3, so the rear edge sits **over the front of the cans**. There is no room for a connector
body and a lead on that edge, and moving the board forward to the x 187.5 slot would still leave
only 8.8 mm. Facing M1/M3 forward costs a loop of ribbon over the board and is the right trade.

**Why it sits off centre.** The forward of the two screws is within about a millimetre of the
front end of its slot (slot starts at y 26.12, screw at y 27.4, M3 needs 27.6). The board is at
the end stop. There is about **17 mm of slot left in the other direction**, so it can be slid
toward the vehicle's left at any time and nothing else has to move.

**Clearance is vertical and it is the spacer height that buys it.** At x 210 the underside of
the ⌀33 can sits 10.7 mm above the plate. Board 1.6 plus a rear-edge connector body of about 7
leaves roughly 2 mm for the spacer before something touches. ⚠️ **Measure the spacers that are
fitted** and record it here; the height is now a constraint, not a free choice.

## Electrical

| | Value |
|---|---|
| VM input | **5 - 15 V** (3S pack 9.0 - 12.6 V sits inside it) |
| Per channel | **2 A rated, 2.5 A peak** |
| Protection | input reverse-connection protection on board |
| Controller | MM32F103CBT6, I²C slave · driver chip SA8870C |

**This is the number that sizes the drive branch.** The JGB37-520s stall at 2.3 A each: above the
2 A rating, inside the 2.5 A peak. Two of them stalled together is 4.6 A through a 2-pin
2.5 mm connector whose contacts are good for about 3 A. The 5 A inline fuse on that branch
protects the 18 AWG wire, not the module and not its connector.
