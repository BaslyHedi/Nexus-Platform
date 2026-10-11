# HW · Electrical design decisions

Power, protection, grounding, wiring and on-vehicle networking. Each entry is settled - revisit one only if something concrete contradicts it.

Numbering is `HW-nn`, unique across the project and never reused. Format, and how to add one: [README](README.md). Parts, prices and status: [`../bom/BOM.md`](../bom/BOM.md).

Drawings: [wiring schematic](../hardware/renders/wiring-schematic.svg) · [STM32 carrier](../hardware/renders/stm32-carrier.svg).

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
| **HW-19** | The 5 V split, its bulk capacitor and the USB-C Rp move onto a board; CAN termination is a jumper. *Rp dropped 2026-10-07* |
| **HW-20** | Three fuses - the logic branch runs on the main fuse |
| **HW-21** | Servo PWM on PE9 (TIM1_CH1); the servo lead is black / red / white |

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

**Revised 2026-10-07: no Rp, no CC.** The KUOQIY socket carries its own **5.1 kΩ Rd on CC1 and CC2**
(4.98 kΩ measured on an unwired spare), so it is a sink and could never be the source this entry
calls for. The FRDM was then run from the socket on **VBUS and GND only, CC unconnected, and booted**.
So J1 needs no CC at all: the source Rp, the 10 kΩ pull-ups and the CC wires are dropped, and the
text below that asks for them is history. Full-load current is still untested.

**Decision.** Bauer 50 W → 5 V → J1 through a USB-C pigtail on **VBUS and GND only**. *(Original: a
USB-C **source** pigtail carrying 10 kΩ Rp.)*

**Why.** Verified on the bench 2026-09-13: the board boots and runs from a dumb 5 V / 1 A
supply. No negotiation, no 12–20 V.

**This contradicts UM12262**, which states the FRDM-IMX91's supply is "VBUS_IN (12 V - 20 V)
through USB Type-C PD connector (P1)" with PTN5110 PD PHYs and an MP8759GD pre-buck.
**That manual describes the non-S board.** The -S evidently feeds its 5 V rail directly.
Treat UM12262's entire power chapter as not applicable to this board.

**Consequence.** A 12 V→USB-C PD source module was specified and then cancelled - €20 saved.
*Original, superseded 2026-10-07:* the pigtail must be **source** role: 10 kΩ Rp pull-**ups** on
CC1/CC2 advertise 5 V @ 3 A, and the 5.1 kΩ pull-**downs** on most DIY USB-C leads are the sink role.
The bench showed the board does not look at CC, so neither is needed.

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

**Updated by HW-19:** the STM32 end's 120 Ω is on the carrier behind a jumper, and the module's own resistor comes off.

*Formerly HD-10.*

**Decision.** SN65HVD230 (3.3 V) on the STM32; the FRDM-IMX91S has its own transceiver and
presents CAN_H/CAN_L on its 2×5 connector. **CAN1 on PD0 (RX) / PD1 (TX), AF9.**

**Why.** 3.3 V transceiver matches F407 I/O directly - MCP2551 and TJA1050 modules are 5 V
parts. Pin choice verified against UM1472: PA11/PA12 are taken by USB OTG on this board and
PB9 is `Audio_SDA` for the CS43L22 codec. PD0/PD1 are free and both broken out on header P2.

**Consequence.** 120 Ω at **both** ends and nowhere else. **Resolved 2026-10-11 (Hedi, from the FRDM schematic page):** the STM32 end is terminated by **the CAN transceiver module's own 120 Ω**, and the carrier's removable R3 (HW-19) is **built but not used** (its jumper stays open); the FRDM end is terminated by its own split termination, **R139 + R144, 60.4 Ω each, joined through jumper JP1** (120.8 Ω across CAN_H/CAN_L, 47 pF from the midpoint to GND), so **JP1 fitted = terminated**. R140 and R143 are not fitted. The board has no SW4 on this page; JP1 is the control. Run H, L **and GND**; twist the pair. The DE-9 debug port (HW-18) hangs
off this bus as an **unterminated stub** - it does not change these two ends.

---

## HW-10 · I²C on PB10/PB11

*Formerly HD-11.*

**Decision.** INA226 on I²C2 - PB10 SCL, PB11 SDA.

**Why.** PB6/PB9 carry the audio codec's I²C on this board (`Audio_SDA` confirmed in the
UM1472 schematic pages). PB10/PB11 are on header P1.

**Corrected 2026-10-03: PB10 is not unallocated.** It also drives the clock input of the
Discovery's MEMS microphone, the MP45DT02: CLK_IN on PB10, PDM_OUT on PC3 (UM1472). PB11 has no
on-board load that could be found. **The decision stands.** The microphone's CLK_IN is an input,
so it adds a few pF to SCL and nothing else. While SCL toggles, the microphone clocks out data onto
PC3, which nothing reads. I²C2 on PB10/PB11 is a common working setup on this board.
**Consequence for firmware:** the on-board microphone cannot be used, and nothing may enable I2S2 or
any other function on PB10. The I²C pull-ups must be strong enough for the extra capacitance;
4.7 kΩ is fine at 100 and 400 kHz.

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

**Updated by HW-20:** the logic fuse is removed - three fuses, not four.

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

**Updated by MEC-16:** the (−) bus is **one** 221-415, five ports; since 2026-10-06 the two switch LED returns join the UBEC return in a 5-port clip (S5), so it uses four ports and one is spare. The (+) bus uses two (the INA226 and S8, the switch feed). The 221-500 carriers were already dropped; both buses are taped to plate 2's lower face with 3M foam tape.

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

**Updated by HW-19:** the split is board C, not a WAGO 3-port.

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

**Updated by MEC-13:** the DE-9 now has the upper panel's top row to itself, back on the centreline at x +2.48, z 107.12 in vehicle coordinates.

**Decision.** A **male DE-9** panel connector sits in the upper gap of the rear fascia
(z 101.12, x 0 - moved off the panel centreline by MEC-05 to make room for the two USB debug
ports), wired to the existing CAN bus per **CiA 303-1**: pin 2 = CAN_L,
pin 3 = CAN_GND, pin 7 = CAN_H. Pin 9 (CAN_V+) stays **unconnected** - the robot does not
feed the PC adapter. A USB-CAN adapter joins the bus through a straight-through 9-pin
**female-to-female** cable. *Revised 2026-10-07: the adapter bought (BOM 4.7) has a screw terminal
rather than a DE-9, so the PC end is a hand-made twisted pair from a female DE-9 to that terminal.*

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

- **The USB-CAN adapter's own 120 Ω stays OFF.** It has switches for it and needs none: both ends of the bus are already terminated (HW-09). Checked 2026-10-11.
  Three terminators pull the bus to 40 Ω and it stops working - this is the single most likely
  cause of a dead bus after this port is added, so check it first.
- **Keep the adapter cable short**, ≤ 2 m. Fine at 500 kbit/s; revisit if the bus ever goes to
  1 Mbit/s, where the stub guidance tightens to ~0.3 m.
- **CAN_GND must be in the cable.** The PC and the robot are on separate supplies; without pin 3
  the two transceivers have no shared reference and common-mode drifts.
- **The adapter is chosen (2026-10-11): the Jhoinrch RH-02 PLUS, BOM 4.7.** It is Canable 2.0 based, so Linux sees it as SocketCAN (`gs_usb`, or `slcand`), which is what the Cyphal tools (`yakut`, `pycyphal`) use for the bootloader's file server (SW-01) and for the third-node trace. It is ordered and in hand (arrived, 2026-10-11).
- **Galvanic isolation was considered and waived (2026-10-07).** The PC's USB ground meets the
  robot's battery ground at this connector, and an isolated adapter would keep a wiring fault on the
  robot away from the laptop. But CAN and ST-LINK debugging happen together on one laptop, and the
  ST-LINK already ties the same grounds with no isolation, so isolating CAN alone buys little: it
  covers only a wiring fault on the CAN pins. No isolated adapter and no USB isolator is used.
  The residual risk is a hand-wiring mistake, so before the laptop is connected: robot off, buzz
  pin 2, 7 and 3 against each other and against 5 V and the battery rails, and read CANH-CANL
  (about 60 Ω with both ends terminated and the adapter's R120 off).
- Fascia geometry: the flange (30.8 × 12.55) clears the deck-2 tab (z 81.12…85.12, x ±38…56) by
  ~15 mm vertically and sits inside the 88.5 mm flat rear face. It no longer has that face to
  itself - see MEC-05 for how it shares it with the USB ports.

---

---

## HW-19 · The 5 V split, its bulk capacitor and the USB-C Rp move onto a board; CAN termination is a jumper

**Revised 2026-09-29: the USB-C socket itself sits on board C.** The FRDM PWR and FRDM CC
terminals are gone. The KUOQIY socket (BOM 5.1) is zip-tied flat at C's row-1 end, opening out, and
its pigtail is soldered straight into the board. See "Revision 2026-09-29" at the end.

**Decision (2026-09-28).** No passive part is left hanging in a lever connector or on its own legs.

- **Board C, the 5 V split.** A 3×7 cm kit board takes the Bauer's 5 V and splits it in two, one
  output to the STM32 carrier and one to the USB-C pigtail that feeds the FRDM's J1. It carries **C1,
  470 µF**, and **R1/R2, 10 kΩ from CC1 and CC2 to 5 V**, the source Rp that HW-02 then called for
  (*dropped 2026-10-07: HW-02 no longer needs it, see the revision at the end*). Four
  2-pin screw terminals: IN 5V, TO STM32, FRDM PWR (VBUS/GND), FRDM CC. *Since 2026-09-29:
  two terminals, and the USB-C socket soldered in place of the FRDM pair (see the revision below).*
- **C2, the second 470 µF, sits on carrier board A across the servo header,** where the stall current
  is drawn.
- **The carrier carries a removable termination (R3), which is not used.** *Revised 2026-10-11: the SN65HVD230 module already has its own 120 Ω and that is the STM32 end's terminator, so the jumper stays open and the module's resistor is not removed. R3 stays as the fallback if the module is ever changed.* As built: R3, 120 Ω, in series with a 2-pin
  header across CAN_H/CAN_L on board B. Jumper on means terminated. *As built 2026-10-03: the kit
  has no 120 Ω, so R3 is **R3a 100 Ω + R3b 20 Ω in series**, exactly 120 Ω. R3a sits where R3 was
  (B·F8-B8), R3b along the front row (B·A8-A4), and R3a's own lead is bent from B·B8 to B·A8 to
  join them. Each 1/4 W part carries under 30 mW.*
- **R4, 1 kΩ, in series with the servo PWM** between PE9 and the servo header.

**Why.**

- **A capacitor in a WAGO port is a lead seal waiting to fail.** BOM 3.14 already had to say "tie or
  glue the body". A radial can soldered to a board and sitting beside its terminals does not need
  that.
- **Board C rather than the STM32 carrier.** The carrier had no room left once the module and its
  terminals were placed (MEC-15). A separate board also keeps the FRDM's 1-2 A off the STM32
  carrier's wiring, and it sits where the old WAGO split did, so the topology of HW-17 is unchanged.
- **Selectable termination is how the bus actually gets debugged.** Which end is terminated has been
  an open question since HW-09 (the module's resistor, the FRDM's SW4). A jumper makes it a setting.
  It would only work if the module's own 120 Ω were removed; since 2026-10-11 it is not, and R3 is the spare.
- **R4 is the cheapest insurance on the board.** A servo plug fitted one pin off puts 6 V on PE9; 1 kΩ
  limits that to about 3 mA into the clamp diode. At 50 Hz it costs nothing.

**The header pinout was wrong on the old carrier drawing, and this corrects it.** UM1472 Table 5 and
the P1/P2 schematic give **P2-3/4 = 5V, P2-5/6 = 3V, P2-7 = PH0**. The old sheet fed 5 V into
P2-5 (the 3 V pin), took 3.3 V from P2-7 (the oscillator input) and treated P2-3 (5 V) as ground.
Built as drawn, it would have shorted the 5 V rail. It also said odd pins are outboard on both
headers; Fig. 10 puts P2's odd pins **inboard**.

**Consequences.**

- The WAGO 3-port for the 5 V split is no longer used, and BOM 3.14's "legs into a WAGO port" and
  5.1's "resistor leg into a WAGO port" are superseded.
- **The carrier's single ground lead is its 5V IN pair**, back through board C to the (−) WAGO
  (HW-06). The I²C and 6 V grounds also reach the bus through the INA226, the motor module and the
  UBEC. They carry signal or return current only, and the loop is accepted.
- A third board needs a home on plate 2, next to the Bauer.

**To confirm.** *Closed 2026-10-11 (Hedi):* the CAN termination check is done; the STM32 end is terminated by the module's own resistor, and the carrier's R3 jumper is left open so there is no second terminator.

**Revision 2026-09-29 · the USB-C socket lives on board C.** Hole names as printed on the kit board (MEC-15).
*Renamed 2026-10-05: C's print runs the other way round from A and B (numbers 1-24 along the long side from the USB-C end, letters A-J up the short side from the bottom, components up and the socket on the left). Every C name below was swapped to match; the old names were letter = row, number = 11 - column.*

- **Where.** At C's row-1 end, lying on its side with the flange flush at the board edge and the
  opening facing the vehicle's right. That end is the only free one: C's long sides have 1.5 mm to
  the Bauer and the carrier (MEC-15), and the row-24 end keeps IN 5V and TO STM32.
- **Held by two zip ties** through 3 mm holes drilled at C·I2 / B2 and C·I6 / B6: one over the body,
  one over the pigtail as strain relief. Both clear the F5 standoff (C·F4) underneath by about 0.9 mm.
- **Superseded by MEC-17 (2026-10-05): F5 and F6 no longer exist.** The board stands on four corner holes and nylon standoffs on the carrier tray, and the drawing, the routing check and the animation follow. What follows is the 2026-09-29 reasoning.
- **The F5 screw is under the body.** The flange is 10.3 mm tall and the body 5.3 mm, centred, so
  the body rides 2.5 mm off the board and clears a pan-head M2.5. Fit that screw first.
- **The pigtail is soldered, cut to about 20 mm:** red V into C·J7 and black G into H7, each the
  end of an 18 AWG chain from IN 5V through C1 (J24 → J12 → J7 and H24 → H12 → H7, MEC-15's
  2026-09-30 routing). Green CC1 goes into D7 and yellow CC2 into B7 *(superseded 2026-10-07: both are cut short, see the revision at the end)*. **R1 and R2 sit at D8-D12 and
  B8-B12**, their lower leads bent over to D7 / B7, and their tops fed from TO STM32 + (D24 → D12 →
  B12). White D− and blue D+ are cut short and insulated one by one, never twisted together.
- **Why solder rather than terminals.** The pigtail is 24 AWG, which a 5.08 screw clamp holds
  poorly without ferrules, and two terminals and a loose socket become one tied-down part. It costs
  unplugging: to free the socket, cut the ties and desolder four wires.
- **Checked 2026-10-07:** the socket has its own 5.1 kΩ Rd on CC1 and CC2 (4.98 kΩ on a spare), so
  it cannot be the source. See the revision 2026-10-07 below.
- **To confirm on the vehicle.** The socket's face is at C's edge, and plate 2 is only about 80 mm
  wide at the waist, so the C-to-C plug stands about 20 mm past the plate edge at plate-2 height.
  Check nothing outboard is in its way, and that the 20 cm cable reaches J1 on plate 3.
  J1 is on the FRDM's v-max edge, u 31-41 (MEC-18, from the Quick Start Guide); the 20 cm cable fits (MEC-18 traces it).

**Revision 2026-10-07 · no Rp: R1, R2 and the CC wires are gone.** The socket's own 5.1 kΩ Rd made it a
sink, and the FRDM booted with VBUS and GND only, so CC is not used (HW-02). Board C is now IN 5V,
TO STM32, C1 and the socket on its red and black wires, and nothing else.

- **R1 and R2 are not fitted.** If already soldered, leave them unconnected or remove them. The two
  22 AWG wires that fed their tops (TO STM32 + to R1 top to R2 top) are not run, and C·D8 / B8 and
  C·D12 / B12 stay empty.
- **The green (CC1) and yellow (CC2) pigtail wires are cut short and insulated one by one**, like the
  white and blue D- and D+: never twisted together, never soldered. Only red (C·J7) and black (C·H7)
  go into the board; C·D7 and C·B7 stay empty.
- **Why leave the socket's Rd alone.** It sits inside the moulded body and cannot be reworked. With CC
  unconnected it is harmless, and the bench test above ran exactly this way.
- **Not tested: full load.** The FRDM booted; its loaded current draw is still unmeasured, and Hedi
  has deferred that test until the vehicle can run it.
- **The drawing, the routing check (`tools/check-carrier-routing.py`), the wiring schematic and the
  animation script were updated, and the carrier animation was re-rendered locally (the videos are not
  tracked in git).**

---

## HW-20 · Three fuses - the logic branch runs on the main fuse

**Decision (2026-09-28).** The 5 A logic fuse is removed. The (+) bus feeds SW2 directly on 18 AWG,
and SW2 feeds the Bauer 50 W. The vehicle has **three** fuses: main 7.5 A, motors 5 A, UBEC 5 A.

```
battery + ─ 7.5 A ─ shunt ─ (+) bus ─┬─ SW1 ─┬─ 5 A ─ Encoder Motor Module
                                     │       └─ 5 A ─ UBEC 6.0 V ─ servo (via carrier board A)
                                     └─ SW2 ─ Bauer 50 W ─ board C ─ FRDM, STM32
```

**Why.**

- **A fuse protects the thinnest conductor it feeds.** Every conductor on the logic branch is
  18 AWG, the Bauer's own leads included (HW-05), good for about 10 A. The 7.5 A main already
  protects all of it. The two fuses that stay each feed something thinner: the motor module's VM
  connector is good for about 3 A, and the UBEC's input leads are lighter than 18 AWG.
- **Keeping the drive branch alive after a logic fault is worth nothing.** A logic fault leaves the
  FRDM and the STM32 dead either way. The STM32 is the safety controller, and HW-17 already names
  the drive running on without it as the risk. The main blowing, which cuts the wheels as well, is
  the safer outcome.
- **The holders are large** (about 50 mm long, 28 across and 18 deep: a base with a narrower strap-on cap, 12-13 cm of 16 AWG each
  side) and plate 1 could not take four of them (MEC-16). The logic holder was also the one that
  had to follow the longest run, from the (+) bus back to SW2 at the fascia.

**Consequences.**

- **Three holders in use, two spare.** HW-15's four fuses become three.
- **A logic-branch short now blows the main.** Accepted, for the reason above.
- **The (+) bus uses 3 of its 5 ports**: INA226 out, SW1, SW2.
- The BOM fuse table and the wiring schematic drop the logic fuse.

**Settled 2026-10-11.** The UBEC is already mounted and stays as it is, so its fuse stays on the list. The input lead gauge was not measured.

---

## HW-21 · Servo PWM on PE9 (TIM1_CH1); the servo lead is black / red / white

**Decision (2026-10-03).** The steering servo's signal comes from **PE9, P1-27**, as
**TIM1_CH1** (alternate function AF1), through R4 (1 kΩ, HW-19) to the SERVO header on carrier
board A. The LD-1501MG's lead, checked on the part in hand, is **black = GND, red = +6 V,
white = signal**. It lands white on **A·K16**, red on **A·L16** and black on **A·M16**,
**white toward the front**. Header rows count from the CN1 end, so K16, the signal pin, is the
frontmost of the three. The drawing's plug table said "signal at the rear" until 2026-10-03, which
was wrong; the pins themselves were always right.

**Why PE9.**

- **It is a hardware timer channel.** PE9 carries TIM1_CH1 as alternate function AF1, so the
  pulse comes from the timer, with no CPU jitter. The NuttX board support for this Discovery uses the
  same pin as a TIM1 PWM output.
- **Nothing on the Discovery uses it**, as far as UM1472 and the NuttX board support show. It is
  on header P1, and NuttX drives it as a free TIM1 output. Check it against UM1472 Table 5
  before the first power-up, as for every pin on the carrier.
- **The servo takes 500-2500 µs pulses** (2.3 SPECS), at the usual 50 Hz frame. TIM1 runs off APB2 at 168 MHz. Prescaler
  167 gives a 1 µs tick, ARR 19999 a 20 ms period, and CCR1 500-2500 sets the pulse directly in µs.
- **TIM1 is an advanced-control timer**: its outputs stay off until MOE in TIM1_BDTR is set. This
  is the usual reason a first TIM1 PWM shows nothing on the pin.

**Why the lead order matters, and what R4 covers.** The header is three plain pins with no key,
so the plug can go on reversed or one pin off.

- **Reversed** (black on K16, white on M16). Red stays on the centre pin, so +6 V still reaches
  the servo's + lead. The servo's ground then returns only through R4 into PE9's clamp diode, about
  (6 - 3.3 - 0.6) V / 1 kΩ, roughly 2 mA. That is within the pin's injection limit, and the servo
  simply does not move.
- **One pin off toward the front** (white hanging, red on K16, black on L16) puts the servo across
  +6 V backwards, with R4 in series: again about 2 mA into PE9's clamp. This is the case HW-19's R4
  was added for.
- **One pin off toward the rear** (white on L16, red on M16, black hanging) leaves the servo
  unpowered with 6 V on its signal input. PE9 is not involved.
- None of the three damages the STM32.
- **So mark the header:** a white paint dot on the board beside A·K16, the signal pin, and the
  plug's white wire goes to the dot.

**To confirm on the bench.**

- **3.3 V drive.** The LD-1501MG runs at 6-8.4 V but takes a logic-level pulse. A 3.3 V high is
  normally enough for this class of servo, but it is not in the listing. If the servo jitters or
  ignores the pulse, the fix is a single-transistor or 74AHCT buffer to 5 V, not a different pin.
- **R4 against the servo's input.** 1 kΩ in series with a servo input of tens of kΩ costs
  nothing at 50 Hz. Check the edge on a scope once, at the header.

