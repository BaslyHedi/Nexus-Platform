# HW · Electrical design decisions

Power, protection, grounding, wiring and on-vehicle networking. Each entry is settled - revisit one only if something concrete contradicts it.

Numbering is `HW-nn`, unique across the project and never reused. Format, and how to add one: [README](README.md). Parts, prices and status: [`../../RnD-Docs/BOM.md`](../bom/BOM.md).

Drawings: [wiring schematic](../hardware/wiring-schematic.svg) · [STM32 carrier](../hardware/stm32-carrier.svg).

| # | Decision |
|---|---|
| **HW-01** | Two independent 5 V rails, one per compute board |
| **HW-02** | The FRDM-IMX91S is fed plain 5 V, not USB-C PD |
| **HW-03** | Two-level fuse hierarchy, main fuse first in the chain |
| **HW-04** | Fuse discrimination - 2× ratio between main and largest branch |
| **HW-05** | Two wire gauges only, pure copper, silicone insulated |
| **HW-06** | Single star ground at the fuse block negative bus |
| **HW-07** | High-side current sensing, INA226 with a 2 mΩ shunt |
| **HW-08** | Neither switch carries full pack current |
| **HW-09** | CAN - transceiver on the STM32 side only |
| **HW-10** | I²C on PB10/PB11 |
| **HW-11** | The steering servo never touches a 5 V rail |
| **HW-12** | Direct switching now; the relay is deferred, not rejected |
| **HW-13** | The 22 AWG battery lead sets the current ceiling - fuse plan rescaled |
| **HW-14** | The steering servo is power train - its UBEC hangs off SW1 |
| **HW-15** | Bus bars and inline fuses replace the fuse block |
| **HW-16** | WAGO 221-415 lever connectors as the power buses |
| **HW-17** | One 5 V converter, not two |
| **HW-18** | CAN debug port - DE-9 on the fascia, PC as an unterminated third node |

---

## HW-01 · Two independent 5 V rails, one per compute board

*Formerly HD-01.*

**Superseded 2026-09-17 by HW-17.** The noise-isolation reason no longer applies: the servo and motors moved off the 5 V rail entirely, so one converter now feeds both boards.

**Decision.** The FRDM-IMX91S and the STM32F407 each get their own DC-DC converter
(Bauer 50 W and Bauer 15 W), not a shared rail.

**Why.** The Linux board runs a filesystem off SD. A voltage dip mid-write corrupts it; an
STM32 reset costs nothing. Separating the rails contains brownouts to the cheap side. It also
lets either board be powered alone during bring-up, and a converter failure takes down half
the vehicle rather than all of it.

**Consequence.** Two converters, two branch fuses. Note this is *not* electrical isolation -
both are non-isolated bucks sharing battery negative. See HW-06.

---

## HW-02 · The FRDM-IMX91S is fed plain 5 V, not USB-C PD

*Formerly HD-02.*

**Decision.** Bauer 50 W → 5 V → J1 through a USB-C **source** pigtail carrying 10 kΩ Rp.

**Why.** Verified on the bench 2026-09-13: the board boots and runs from a dumb 5 V / 1 A
supply. No negotiation, no 12–20 V.

**This contradicts UM12262**, which states the FRDM-IMX91's supply is "VBUS_IN (12 V - 20 V)
through USB Type-C PD connector (P1)" with PTN5110 PD PHYs and an MP8759GD pre-buck.
**That manual describes the non-S board.** The -S evidently feeds its 5 V rail directly.
Treat UM12262's entire power chapter as not applicable to this board.

**Consequence.** A 12 V→USB-C PD source module was specified and then cancelled - €20 saved.
The pigtail must be **source** role: 10 kΩ Rp pull-**ups** on CC1/CC2 advertise 5 V @ 3 A.
The 5.1 kΩ pull-**downs** on most DIY USB-C leads are the sink role and are wrong here.

---

## HW-03 · Two-level fuse hierarchy, main fuse first in the chain

*Formerly HD-03.*

**Updated by HW-15:** the fuse block is gone - the main fuse now feeds the (+) bus bar. Fuse-before-shunt ordering still stands.

**Decision.** Battery (+) → **inline main fuse - 7.5 A since HW-13, within ~15 cm of the terminal** → INA226
shunt → fuse block → branch fuses.

**Why.** A branch fuse only protects what is downstream of it. The battery-to-block cable sits
upstream of every branch fuse and so cannot be protected by any of them - a chafe-through
there would draw hundreds of amps from the pack with no fuse in the path. Every conductor is
protected at its source.

The main fuse **cannot** live inside the fuse block: the block's input bus feeds all six ways
in parallel, so any fuse in a way is downstream of the bus and cannot protect it.

**Ordering matters.** The fuse goes *ahead* of the shunt, not after. An unprotected 2 mΩ shunt
in a short would see fault current directly - 80 W at 200 A. Fusing first protects the shunt
as well as the cable.

---

## HW-04 · Fuse discrimination - 2× ratio between main and largest branch

*Formerly HD-04.*

**Superseded 2026-09-15 by HW-13.** Kept for the reasoning; the numbers below no longer apply.

**Decision.** 20 A main, 10 A largest branch (drive).

**Why.** With the original 15 A drive fuse the ratio was only 1.33×, so a dead short on the
drive branch could blow the main as well - a jammed wheel would take down Linux, defeating the
point of separate branches. The drivetrain is **2 rear motors** (1.4 A rated, 7–11 A stall),
so 10 A is ample and restores a 2× ratio.

**Fallback.** If autonomy testing produces nuisance blows, 15 A. But a stall lasting more than
a few seconds is a fault worth interrupting.

---

## HW-05 · Two wire gauges only, pure copper, silicone insulated

*Formerly HD-05.*

**Superseded 2026-09-15 by HW-13.** Kept for the reasoning; the numbers below no longer apply.

**Decision.** **14 AWG** for the battery main and drive branch; **18 AWG** for everything else.
Copper - explicitly not copper-coated aluminium. Silicone insulation.

**Why.** Matching every branch to its own gauge is textbook but optimises for copper cost,
which is meaningless on a 270 mm vehicle. Going thicker than required is never unsafe. Two
gauges is four line items instead of ten, and 18 AWG matches the Bauer converters' own leads.

CCA has ~60 % of copper's conductivity, work-hardens under vibration, and its oxide is an
insulator - so CCA crimps drift high-resistance over time. Silicone's high strand count
survives vibration where PVC-insulated automotive wire fatigues.

**Corrected along the way.** An earlier version of the fuse plan paired a 15 A fuse with
16 AWG (~13 A). A fuse protects the wire, so the wire must always be the stronger of the pair.

---

## HW-06 · Single star ground at the fuse block negative bus

*Formerly HD-06.*

**Updated by HW-16:** the star point is now the (−) WAGO bus - two 221-415s bridged.

**Updated by HW-15:** the star point is now the black (−) bus bar.

**Decision.** Every return lands on the Geloo block's negative bus. No daisy-chaining.

**Why.** Both converters are non-isolated, so grounds are common whether we plan it or not.
The choice is whether returns share a controlled star point or route through each other. A
daisy-chained ground puts the MCU's return current into the MPU's ground reference. The common
ground is also what CAN needs for common-mode reference.

**This is why the Geloo block was chosen over the FULARR** (which is 8 % smaller in area but
has no negative bus, no blown-fuse LEDs, spade rather than screw terminals, and is 12 mm
taller - worse on the deck gap, the tighter constraint).

---

## HW-07 · High-side current sensing, INA226 with a 2 mΩ shunt

*Formerly HD-07.*

**Decision.** INA226 module with the `R002` shunt, sensing the positive main, read by the
STM32 over I²C.

**Why.** Against the INA226's ±81.92 mV input range, 2 mΩ gives **±41 A at 1.25 mA
resolution** - the chip's range is set entirely by the shunt. High-side keeps the shunt out of
the ground path, and the 0–36 V common-mode range covers a 12.6 V pack comfortably.

It belongs on the **STM32, not the i.MX 91**: the MCU owns safety and real-time, and publishes
pack state on CAN. That is the compute/control split doing real work, and a better first CAN
payload than a synthetic test frame.

**Known limit.** The module's 5.08 mm screw terminals are rated ~10–16 A, below the shunt's
capability - they, not the shunt, are the ceiling. Acceptable here; check them for heating on
the first loaded runs, and move to an external bolt-down shunt if they warm.

**Alert.** The INA226 has a single Alert Limit Register and only **one** alert function can be
enabled at a time. Use Bus Voltage Under-Limit on the pin; poll current in the control loop.

---

## HW-08 · Neither switch carries full pack current

*Formerly HD-09.*

**Updated 2026-09-15 (HW-14):** SW1 now switches the steering servo's supply as well as the motors - peak ≈ 7.6 A against its 20 A rating.

**Decision.** **SW1 (POWER TRAIN)** switches the motor branch; **SW2 (LOGIC)** switches the
converter branch. Naming fixed 2026-09-14 - this ordering is used everywhere.
No master rocker in the battery main - the pack connector is the true disconnect.

**Why.** Automotive rocker current ratings are optimistic, and a €2.50 switch in the main path
of a pack that can deliver hundreds of amps is the wrong part in the wrong place. Splitting
also gives the thing you actually want on the bench: kill the wheels while Linux and the
debugger stay up.

**No master switch is fitted, and none is needed.** SW1 and SW2 between them cover every load,
so with both off the vehicle draws essentially nothing - the INA226's own supply comes from the
STM32 rail and is off with it.

**What stays live while the pack is plugged in:** battery → main fuse → shunt → fuse block
positive bus → both switch inputs. That segment is energised at all times and is protected by
the 20 A main fuse, which is precisely its job (HW-03).

**Consequences.**

- The **battery connector is the disconnect** for storage, transport and anything alarming.
  Mount it where it can be reached without dismantling the vehicle.
- **SW1 is the practical emergency stop** - it kills the wheels, which is the part that can hurt.
- **Do not fit an always-on "bus live" indicator.** A 5 mA LED costs ~120 mAh/day, about 2 % of
  the pack per day. The discipline is to unplug the pack instead.

---

## HW-09 · CAN - transceiver on the STM32 side only

*Formerly HD-10.*

**Decision.** SN65HVD230 (3.3 V) on the STM32; the FRDM-IMX91S has its own transceiver and
presents CAN_H/CAN_L on its 2×5 connector. **CAN1 on PD0 (RX) / PD1 (TX), AF9.**

**Why.** 3.3 V transceiver matches F407 I/O directly - MCP2551 and TJA1050 modules are 5 V
parts. Pin choice verified against UM1472: PA11/PA12 are taken by USB OTG on this board and
PB9 is `Audio_SDA` for the CS43L22 codec. PD0/PD1 are free and both broken out on header P2.

**Consequence.** 120 Ω at **both** ends and nowhere else. Measure before fitting anything:
the SN65HVD230 module may already carry its 120 Ω, and the FRDM's SW4 (CAN split termination)
may cover that end. Run H, L **and GND**; twist the pair. The DE-9 debug port (HW-18) hangs
off this bus as an **unterminated stub** - it does not change these two ends.

---

## HW-10 · I²C on PB10/PB11

*Formerly HD-11.*

**Decision.** INA226 on I²C2 - PB10 SCL, PB11 SDA.

**Why.** PB6/PB9 carry the audio codec's I²C on this board (`Audio_SDA` confirmed in the
UM1472 schematic pages). PB10/PB11 are unallocated and on header P1.

---

## HW-11 · The steering servo never touches a 5 V rail

*Formerly HD-13.*

**Supply routing revised by HW-14:** the UBEC is fed from SW1 (power train), not F3.

**Decision.** The LD-1501MG is fed by the Hiwonder driver's BEC, or by its own 6–7.4 V supply.

**Why.** It is a **6–8.4 V** part, not a 5 V one - 17 kg·cm stall at 7.4 V. This is what makes
both 5 V rails purely logic rails, and it removes the worst transient source from them.

**Resolved 2026-09-14, and the answer is no.** The chassis arrived. The driver is a
**Hiwonder Encoder Motor Module V1.4** with an **MM32F103CBT6** on board - an intelligent I²C
slave, not a dumb H-bridge. Its ports are four 6-pin motor connectors (`M+ VCC A B GND M−`),
a power input, and host headers `SCL SDA GND 5V` and `GND TX RX NC`. **There is no servo
output.**

Hiwonder's own assembly doc confirms the split: "Dupont wires for connecting the PWM servo to
the Raspberry Pi, and three female-to-female DuPont wires for IIC communication between the
motor driver and Raspberry Pi." In NEXUS the STM32 takes the Pi's place in both roles.

**Consequences.**

1. **A third branch is needed** - F3 on the fuse block, feeding a 6–7.4 V regulator for the
   servo. Part chosen 2026-09-15: ZHITING switching UBEC set to 6.0 V, 3 A continuous / 5 A max (BOM 3.18).
2. **The STM32 drives the servo directly** with PWM, 500–2500 µs.
3. **HW-09's motor interface was wrong.** The STM32 does not generate PWM/DIR or read encoder
   channels; it sends I²C commands and the module does commutation and counting itself. The
   module's I²C may share the INA226 bus (different addresses) or get its own - decide when
   the firmware is written.

---

## HW-12 · Direct switching now; the relay is deferred, not rejected

*Formerly HD-14.*

**Decision (2026-09-14).** Both branches are switched directly by their push buttons. No relay.

**Parts, and why each sits where it does** - each switch is placed so that its weakness does
not bite:

| | Part | Branch | The weakness, neutralised |
|---|---|---|---|
| **SW1** | Gebildet 19 mm, blue LED, 20 A | POWER TRAIN | Solder tags need a 60 W+ iron - but they take **14 AWG directly**, which is exactly what the drive branch wants |
| **SW2** | GUUZI 16 mm, red LED, 15 A | LOGIC | Plug harness of unknown gauge - **irrelevant at ~1.3 A**. Amazon's Rufus could not tell us the gauge and now it does not matter |

This is what removed the need for a relay. The relay was proposed to keep motor current out of
an unknown-gauge harness; putting the solder-tag button on the drive branch solves the same
problem with no extra part, no coil drain and no added failure point.

**Rejected along the way: a 2-channel relay module for both branches.** Two reasons.

1. **Bootstrap deadlock.** The common modules have 5 V coils, and the only 5 V rails are
   downstream of the converters the module would be switching. It could never turn itself on.
2. **Wrong fail-safe direction for the compute rail.** A relay is normally-open, so a coil
   dropout - vibration, a cracked joint, a brownout - hard-kills Linux mid-write. That is
   precisely what SYS-01 exists to prevent. On the drive branch the same behaviour is correct.

A relay also costs ~150 mA of coil current continuously, which is noise beside 1.4 A of motors
but over 10 % overhead on a 1.3 A logic branch.

**When the relay comes back.** When SYS-01 step 2 is implemented and the STM32 needs to cut the
drive branch itself. Use a **12 V automotive relay in a socket**, not an Arduino module:
30–40 A contacts, no opto/active-low ambiguity, and the button and the MCU can pull the same
coil pin in parallel. Fuse way F1 already feeds that branch, so nothing upstream changes.

**Switches, final (2026-09-14).** Both are the **same 22 mm latching metal push button**,
20 A / 12–24 V, ordered from eBay: **red on SW1 (power train), green on SW2 (logic)**. This
restores the convention - red is the one you hit when something is moving that should not be.

**Consequence of using one part in two colours: the tactile difference is gone.** The earlier
pairing had 19 mm against 16 mm, distinguishable by feel. Now colour and position are the only
discriminators, so:

- **Fix a position convention and never change it** - power train always on the same side.
- **Label the deck** beside each button. The Geloo fuse block ships with name stickers.

**Two things to check on arrival.** The supplied socket harness gauge is unknown, same
question as before - but these have **spade tabs as well as a harness**, so if the blades are
6.3 mm you can crimp your own 14 AWG spades for SW1 and ignore the harness. Also confirm the
body depth clears the deck gap; 22 mm buttons are deeper than 16 mm ones.

---

## HW-13 · The 22 AWG battery lead sets the current ceiling - fuse plan rescaled

*Formerly HD-16.*

**Fuse layout revised by HW-15:** every fuse is inline and F1 is removed.

**F1 and F3 revised by HW-14:** F1 is now 7.5 A with two 5 A inline fuses after SW1; F3 is spare.

**Decision (2026-09-15).** Size the whole harness to the pack's own output lead - **22 AWG with
an SM-2P connector**.

| | Was | Now |
|---|---|---|
| Main fuse | 20 A | **7.5 A** |
| F1 drive | 10 A | **5 A** |
| F2 logic | 5 A | **5 A** |
| F3 servo | 5 A | **5 A** |
| Harness wire | 14 + 18 AWG | **18 AWG only** |
| Battery connector | - | **SM-2P kept**, temperature monitored |

The full fuse table and current budget live in the BOM, section *Fuse plan and wire gauges*.

**Why.**

- **A fuse protects the thinnest conductor it feeds.** The pack's 22 AWG lead (~5–7 A) sits
  upstream of every fuse we fit; a 20 A main could never protect it.
- **Real loads are smaller than first estimated.** The JGB37-520 motor stalls at 2.3 A each; the
  earlier 7–11 A for both motors was about double. Normal driving draws ~1.5–3 A for the whole
  vehicle; the realistic worst case - both wheels stalled while the servo strains - is ~7 A.
- **Hiwonder's own listing** says usable current is limited by the protection circuit, wiring and
  connector, not by the 10C cell rating.

**Consequences.**

- **Discrimination drops to 1.5×**, superseding HW-04. A dead short on a branch may blow the main
  too. Accepted - the lead cannot carry more.
- **One wire gauge**, superseding HW-05. The 14 AWG was removed from the order.
- **F2 and F3 would ideally be 3 A**; the fuse kit has none, and 5 A still protects 18 AWG.
- **The SM-2P connector is typically rated ~3 A**, below the ~7 A worst case. Kept for now: feel
  it after a stalled-wheel test and after a long drive, and move to **XT30 (15 A)** if it runs warm.

**To confirm.** Motor stall current on the INA226 with a wheel held; the pack PCM's overcurrent
cut-off, which isn't published and may trip before our fuses do.

---

## HW-14 · The steering servo is power train - its UBEC hangs off SW1

*Formerly HD-17.*

**Updated by HW-15:** the separate 7.5 A F1 is removed - the main fuse covers the (+) bus → SW1 run.

**Decision (2026-09-15).** The servo supply is switched with the drive motors by **SW1**, not fed
from an always-live fuse. F1 feeds SW1; after SW1 the branch splits through two inline fuses:

```
F1 7.5 A ─ SW1 ─┬─ inline 5 A ─ Hiwonder driver ─ 2 × rear motors
                └─ inline 5 A ─ ZHITING UBEC 6.0 V ─ steering servo
F3 → spare
```

**Why.**

- **Steering is actuation, not logic.** The red power-train button now stops every moving part -
  wheels and steering - which is what the button you hit under stress should do.
- **No standby drain.** Fed from F3, the UBEC and servo would stay live whenever the pack is plugged
  in, contradicting HW-08's "draws essentially nothing" with both switches off.

**Consequences.**

- **F1 rises from 5 A to 7.5 A**, equal to the main fuse. It carries both motors stalled (4.6 A) plus
  the servo stalled (~1.5 A at the UBEC input) ≈ 6.1 A, with millisecond servo bursts to ~7.6 A.
- **Per-load protection moves to two 5 A inline fuses** after SW1, using the two spare KOLACEN
  holders. A motor or servo fault clears at its own fuse, 1.5× below F1; a fault on the short
  F1 → SW1 → split run may take the main as well.
- **SW1 peaks at ≈ 7.6 A**, well inside its 20 A rating.
- **With SW1 off and SW2 on**, the STM32 runs but the servo is unpowered - steering can't be
  exercised without enabling the power train.
- **F3 is a spare again**, and no inline holders are left over.

---

## HW-15 · Bus bars and inline fuses replace the fuse block

*Formerly HD-18.*

**Hardware superseded by HW-16:** WAGO 221-415 connectors replace the LAOYE bus bars. The inline-fuse layout below still stands.

**Decision (2026-09-15).** Replace the Geloo 6-way fuse block with a **LAOYE bus bar pair** - red (+)
and black (−) - and put **every fuse inline**, using 4 of the 5 RUNCCI-YUN holders.

```
battery + ─ 7.5 A ─ shunt ─ (+) bar ─┬─ SW1 ─┬─ 5 A ─ Encoder Motor Module ─ 2 × rear motors
                                     │       └─ 5 A ─ UBEC 6.0 V ─ steering servo
                                     └─ 5 A ─ SW2 ─┬─ Bauer 50 W ─ FRDM-IMX91S
                                                   └─ Bauer 15 W ─ STM32
every return ─ (−) bar ─ battery −
```

**Why.**

- **The fuse block wasn't earning its place.** Two of its six ways were used, the servo and drive
  fuses already sat inline after SW1, and it was the bulkiest item on the bottom deck.
- **A separate F1 added nothing.** At 7.5 A it sat in series with the 7.5 A main; equal-rated fuses
  in series never discriminate, and the main already protects that short 18 AWG run (~10 A).
- **The black bar is a proper star point**, with a screw terminal for every return.

**Consequences.**

- **Four fuses:** main 7.5 A, motors 5 A, UBEC 5 A, logic 5 A. **One holder spare.**
- **Blown-fuse LEDs are gone** - a dead branch now means checking the holders by hand.
- **Every bus bar connection is a ring terminal** on M4 or M6 - **red, 0.5–1.5 mm²** for 18 AWG (BOM
  3.19). The yellow rings supplied with the bars are for 4–6 mm² and won't hold 18 AWG.
- **A fault on the (+) bar → SW1 → split run blows the main**, exactly as it would have with F1 at 7.5 A.
- **Bus bar dimensions aren't published** - measure on arrival before fixing the bottom-deck layout.

---

## HW-16 · WAGO 221-415 lever connectors as the power buses

*Formerly HD-19.*

**Decision (2026-09-16).** Replace the LAOYE bus bars with **WAGO 221-415** lever connectors on
**221-500** mounting carriers.

| Bus | Parts | Ports used / available |
|---|---|---|
| (+) | 1 × 221-415 | 3 / 5 - shunt in, SW1 feed, logic fuse feed |
| (−) | 2 × 221-415, bridged with an 18 AWG jumper | 5 / 8 - battery return, motor module, UBEC, Bauer 50 W, Bauer 15 W |

**Why.**

- **No ring terminals, no second crimper, no washers.** The LAOYE route needed a ring-terminal kit
  with a ratchet crimper (~€15–20) and spring washers (~€5) on top of its €12.99. The 221-415 takes
  18 AWG and the 16 AWG fuse-holder leads directly.
- **The spring clamp holds under vibration** without re-torquing; the 221 series is listed against
  IEC 60068-2-6.
- **Rated 32 A, 0.2–4 mm²** - far above the 7.5 A main fuse.
- **Same family as the 221-413s** already used to join the converter leads.

**Consequences.**

- **Battery return and motor-module return go on the same (−) connector**, so the largest return
  current never flows through the jumper.
- **WAGO bodies aren't colour-coded** - mark the (+) carrier red and the (−) carriers black.
- **Strip 11 mm** and seat each conductor fully, so no bare copper shows at the entry.
- **BOM 3.19 (ring terminals) and 3.20 (spring washers) are cancelled.** The WAGO connections need no ferrules.
- **(−) has 3 spare ports and (+) has 2**, so future returns or branches don't need new hardware.

---

## HW-17 · One 5 V converter, not two

*Formerly HD-20.*

**Decision (2026-09-17).** Drop the Bauer 15 W. The **Bauer 50 W** feeds both boards, split at a
**WAGO 3-port** on its output. The released €11.99 goes to a second CAN transceiver (BOM 4.1).

```
(+) bus ─ 5 A ─ SW2 ─ Bauer 50 W ─ 5 V ─┬─ FRDM-IMX91S (J1 USB-C)
                                        └─ STM32F4DISCOVERY (5 V pin, P2)
```

**Why the original reason expired.** HW-01 split the rails so that transient loads could not dip the
Linux board's supply and corrupt an SD write. Since then the **servo moved to its own UBEC** (HW-11,
HW-14) and the **motors run at 12 V off the Encoder Motor Module** - neither touches the 5 V rail.
What is left is two steady loads totalling **~1.2–1.8 A against the converter's 10 A**.

**What is given up.**

- ⚠️ **A converter failure now takes out both boards at once.** The STM32 is the safety controller,
  and the motor module holds its last I²C command - so if the 5 V rail dies mid-drive, nothing is
  left to stop the wheels.
- Bring-up independence: powering one board without the other now means unplugging a wire.

**Mitigation - test this early.** With the vehicle on blocks and driving, cut the STM32's 5 V and
watch the wheels. If the motor module keeps turning, it has no command timeout and the drive branch
needs an independent cutoff before autonomous running - the relay deferred in HW-12, driven by a
watchdog. If the wheels stop, the module times out and this decision costs nothing.

---

## HW-18 · CAN debug port - DE-9 on the fascia, PC as an unterminated third node

*Formerly HD-21.*

**Decision.** A **male DE-9** panel connector sits in the upper gap of the rear fascia
(z 101.12, x 0 - moved off the panel centreline by MEC-05 to make room for the two USB debug
ports), wired to the existing CAN bus per **CiA 303-1**: pin 2 = CAN_L,
pin 3 = CAN_GND, pin 7 = CAN_H. Pin 9 (CAN_V+) stays **unconnected** - the robot does not
feed the PC adapter. A USB-CAN adapter joins the bus through a straight-through 9-pin
**female-to-female** cable.

| | |
|---|---|
| Robot side | **male** DE-9 (pins) - CiA convention: every node is male |
| Adapter side | **male** DE-9 on essentially every USB-CAN adapter |
| Cable | **female-to-female, straight-through** |

**Why male on the robot.** CANopen/CiA 303-1 makes the node male and the cable female, so a
node's live pins are never exposed on a dangling cable end. It also means one standard cable
type works for every node added later.

**Why an unterminated stub.** Termination belongs at the two electrical ends of the bus, which
are the STM32 transceiver and the FRDM (HW-09). Making the DE-9 an *end* instead would leave the
bus half-terminated whenever the PC is unplugged - which is most of the time, and the robot has
to run standalone. As a stub it changes nothing: at 500 kbit/s a bit is 2 µs and a 2 m stub costs
about 10 ns, four orders of magnitude below anything that matters.

**Consequences.**

- **The USB-CAN adapter's own 120 Ω must be switched OFF.** Most ship with it on or jumpered on.
  Three terminators pull the bus to 40 Ω and it stops working - this is the single most likely
  cause of a dead bus after this port is added, so check it first.
- **Keep the adapter cable short**, ≤ 2 m. Fine at 500 kbit/s; revisit if the bus ever goes to
  1 Mbit/s, where the stub guidance tightens to ~0.3 m.
- **CAN_GND must be in the cable.** The PC and the robot are on separate supplies; without pin 3
  the two transceivers have no shared reference and common-mode drifts.
- **Galvanic isolation is worth paying for** in the adapter. The PC's USB ground meets the robot's
  battery ground at this connector; an isolated adapter keeps a wiring fault on the robot away
  from the laptop.
- Fascia geometry: the flange (30.8 × 12.55) clears the deck-2 tab (z 81.12…85.12, x ±38…56) by
  ~15 mm vertically and sits inside the 88.5 mm flat rear face. It no longer has that face to
  itself - see MEC-05 for how it shares it with the USB ports.

---
