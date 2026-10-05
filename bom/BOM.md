# NEXUS Platform - Bill of Materials

Status as of **2026-09-19**. Covers Phase 1 only (battery → 5 V → i.MX 91 → CAN → STM32 →
motors/steering). Sensors and Raspberry Pi integration are listed under *Later phases* for
visibility but are not Phase-1 items.

Legend: 📦 **delivered, in hand** · ✅ ordered, in transit · 🔴 blocking, to order
· 🟡 to check · 🔵 later phase

**Purchase record.** Amazon #303-3892799-2621160, 17 Sep, **€128.37** (16 items; 13 delivered
18 Sep) · Amazon #303-1096511-4948360, 17 Sep, **€8.74** (capacitors) · eBay 13-15161-69285,
14 Sep, **€25.59** (both switches, SpeedPAK 17 Sep, due 29 Sep – 13 Oct) · Amazon
#302-7140340-3101964, **20 Sep, €40.00** (the three fascia connectors + prototype PCB kit,
arriving 21 Sep). **Total €202.70.**

---

## 1. Compute and control

| # | Item | Qty | Status | Role | Notes |
|---|---|---|---|---|---|
| 1.1 | **NXP FRDM-IMX91S** | 1 | ✅ Purchased | Main Embedded Linux compute | **105 × 65 mm**, 10-layer. Cortex-A55, 512 MB LPDDR4, 256 MB QSPI NAND (NAND boot), microSD 3.0 **on the underside**, IW610 Wi-Fi 6 + BLE 5.4 + 802.15.4 on board, 1 GbE, 40-pin expansion (5 V on pins 2/4), 2×5 NXP custom connector carrying **CAN + 2× ADC + I2C/I3C**. Powered from **J1, USB-C** - no barrel jack, no screw terminal. Kit ships a 32 GB SD with the BSP |
| 1.2 | **STM32F4DISCOVERY, board rev MB997B** | 1 | ✅ Owned | Real-time MCU | Confirmed from silkscreen 2026-09-13. ST-LINK/V2, **SWD only - no Virtual COM Port**, so UART console needs a separate USB-TTL adapter. Mini-USB for ST-LINK (CN1), micro-USB OTG (CN5). UM1472 in the library is the correct manual for this revision |

## 2. Chassis and drive

Chassis plate is **270 × 120.5 × 2 mm** anodised aluminium, 126 g. The advanced kit is the
**double-layer** version: two plates on standoffs, **bottom deck intended for the battery**.

| # | Item | Qty | Status | Role | Notes |
|---|---|---|---|---|---|
| 2.1 | **Hiwonder advanced bundle (double-layer)** | 1 | ✅ Ordered | Mechanical platform | 4-wheel chassis, **2 driven rear wheels + front Ackermann steering**, rear pair on an electronic differential |
| 2.2 | Encoder gear motors | **2 (rear axle)** | ✅ Included | Propulsion | Corrected 2026-09-13: **rear-wheel drive, 2 motors**, not 4. **12 V**, ~8.3 W each → **~1.4 A total rated**, ~7–11 A at stall. 1:90, 110 rpm no-load, 15 kg·cm stall, AB encoder, PH2.0-6PIN. The "electronic differential" is firmware across these two |
| 2.3 | **LD-1501MG steering servo** | 1 (front) | ✅ Included | Ackermann steering | **6–8.4 V** working voltage - *not* a 5 V part. 17 kg·cm @ 7.4 V, PWM 500–2500 µs. Must be fed from its own 6–7.4 V supply or the Hiwonder driver's BEC, never off a logic rail |
| 2.4 | **Encoder Motor Module V1.4** (motor driver) | incl. | ✅ Included | Motor power stage | **42 x 58 x 10 mm**, four **round** ⌀3.8 corner holes on a **32.4 x 48.4** pattern, 4.8 mm in from each edge - measured 2026-09-21 off a photo on 5 mm graph paper, geometry and method in [`parts/2.4-Encoder-Motor-Module/SPECS.md`](parts/2.4-Encoder-Motor-Module/SPECS.md). The earlier "59 x 42, slotted" was wrong on both counts. VM **5-15 V**, **2 A rated / 2.5 A peak per channel** - the JGB37-520's 2.3 A stall is above the rating and inside the peak. **Fitted to plate 1 on 2026-09-21** - x 168-210, y 22.6-80.6, 2 × M3 + spacers through the chassis slot at x 203.5; the fit confirms the measured 32.4 × 48.4 pattern in hardware. **No servo output** (HW-11). ⚠️ The IIC port's 5 V pin is an **output**, 1 A: wire SCL/SDA/GND only, never that pin to the carrier's 5 V rail. ⚠️ VM comes in on a 2-pin 2.5 mm-class connector good for ~3 A against a 4.6 A both-stalled case - see the adapter question in [`../hardware/README.md`](../hardware/README.md) |

## 3. Power

Two independent 5 V rails, both fed from the 3S pack through a fused distribution block.
Decided 2026-09-12: separate converters per compute board, standardised on Bauer Electronics.

| # | Item | Qty | Status | Role | Notes |
|---|---|---|---|---|---|
| 3.1 | **Hiwonder 3S LiPo, 11.1 V / 6000 mAh** | 1 | ✅ Included with 2.1 | Main energy source | **63 × 77 mm** footprint (measured 2026-09-20), **height TBC and probably not the 20 mm on the drawing** - 63×77×20 is 686 Wh/L at pack level, above what the cells alone manage. ⚠️ **Shrink-wrapped cell pack, NOT hard-cased** (photographed 2026-09-21) - no cable ties on the wrap, wide flat straps and a pad only. Both leads leave **one face at opposite corners**: SM-2P discharge and a **live female DC barrel socket** for charging, which must be tied down and insulated. **No balance connector** - 2-pin discharge lead + DC barrel jack for charging. Charging over 2 wires implies an **internal protection PCB**; confirm. 12.6 V full → 9.0 V empty. Detail in [`parts/3.1-Battery-3S-LiPo/SPECS.md`](parts/3.1-Battery-3S-LiPo/SPECS.md) |
| 3.2 | **LiPo charger** | 1 | ✅ Included with 2.1 | Battery charging | Part of the Hiwonder order |
| 3.3 | 5 V regulators (misc.) | - | ✅ Purchased | Spares / bench use | Superseded for the vehicle by 3.4a/3.4b |
| 3.4a | **Bauer Electronics 8–36 V → 5 V, 10 A / 50 W (Wire)** | 1 | 📦 **Delivered 18 Sep** €19.99 | **Compute rail** - FRDM-IMX91S | Confirmed 2026-09-13: the board boots from a dumb 5 V supply, no PD. 10 A is generous for a board drawing <1 A at idle, and leaves the Pi 5 room to join this rail later. **Dimensions confirmed from the Bauer drawing:** body **64 x 57 x 22 mm**, two **⌀6.8 mm** mounting ears at **54 mm** centres. **Mounting (revised 2026-10-05, MEC-17):** the seller's drawing and the real part show the two ⌀6.8 holes sit *inside* the 64 x 57 outline, 5 mm from each end and 26 mm from the edge the four leads leave by. It is screwed to the carrier tray through them with two M3 x 8 into captive nuts, at x 11-75 so the leads have a lane; the 54 mm pitch no longer has to match a chassis rectangle |
| ~~3.4c~~ | ~~12 V → USB-C PD source~~ | - | ❌ **Cancelled 2026-09-13** | - | Not needed. The -S takes plain 5 V; UM12262's 12–20 V PD requirement is for the non-S board only. €20 saved |
| 3.4b | ~~Bauer Electronics 8–32 V → 5 V, 3 A / 15 W~~ | - | ❌ **Dropped 2026-09-17 (HW-17)** | - | The 50 W rail carries both boards (~1.2–1.8 A of 10 A). €11.99 released for CAN transceivers (4.1) |
| 3.5a | **SW1 - 22 mm latching push button, RED LED, 20 A / 12–24 V** | 1 | ✅ Ordered (eBay) **€8.36** | **POWER TRAIN** branch | "LED hoher Strom Druckknopf Schalter", seller GooBetter/sz_bahua. Spade tabs **plus** a socket harness. Delivery ca. **29 Sep – 13 Oct** |
| 3.5c | **SW2 - 22 mm latching push button, GREEN LED, 20 A / 12–24 V** | 1 | ✅ Ordered (eBay) **€8.36** | **LOGIC** branch | Same part, green. Order 13-15161-69285 confirms both: item 358569266510, *Selbstsperrende* (latching), 12–24 V, 22 mm, one **Red+wire** one **Green+wire**. €16.72 + €5.79 shipping + €4.08 VAT − €1.00 voucher = **€25.59 the pair**. Shipped SpeedPAK 17 Sep |
| 3.5b | **Main battery disconnect** | 1 | 🟡 **Decided: keep SM-2P for now** | True battery main disconnect | No master switch (HW-08); the pack's **SM-2P** connector is the disconnect. Typically rated ~3 A against a ~7 A worst case - **monitor its temperature under load**, move to **XT30 (15 A)** if it runs warm (HW-13) |
| 3.5d | Automotive relay, 12 V 30/40 A + socket | 1 | 🔵 **Deferred** ~€6 | STM32-commanded drive cutoff | Not needed for manual switching (HW-12). Returns when SYS-01 step 2 is implemented |
| 3.7 | **RUNCCI-YUN standard blade fuse kit - 120 fuses + 5 × inline 16 AWG holders** | 1 set | 📦 **Delivered 18 Sep** €9.99 | Circuit protection - every fuse is now inline (HW-15) | Fuses 5 / 7.5 / 10 / 15 / 20 / 25 / 30 A + puller; holders 16 AWG, ATC/ATO, waterproof lid. Replaces the KOLACEN 3-holder kit. **No 3 A fuses.** Holder allocation: see the fuse plan |
| 3.8 | **WAGO 221-415 lever connectors (5-port, 0.2–4 mm², 32 A) × 5** | 5 | ✅ Dispatched 18 Sep €6.15 | **Power distribution** - (+) bus: 1 × 221-415; (−) bus: 1 × 221-415, five returns with the switch LED returns joined (MEC-16) | Genuine WAGO on the buses, where every amp flows. **3 spare.** Both are taped to plate 2's lower face either side of its opening, entry faces towards each other (MEC-16). Takes 18 AWG and the 16 AWG fuse-holder leads directly - no ring terminals, no crimper, no washers. Strip 11 mm. Mark the (+) connector red and the (−) black. **221-500 carriers dropped** - mounted with cable ties through the chassis holes; tie around the body, never across the levers |

**Rejected:** XH-M609 low-voltage disconnect. Its operating range starts at **12 V** - a 3S pack
sits below that for most of its discharge curve - and it burns <1.5 W continuously (~135 mA at
11.1 V) as parasitic drain. Wrong part for this pack.

### Fuse plan and wire gauges

**Revised 2026-09-15 - bus bars and inline fuses (HW-15).** The pack leaves through **22 AWG** and an
**SM-2P** connector, which caps the main fuse at 7.5 A (HW-13). Two WAGO 221-415 buses - (+) and (−) -
replace the fuse block, and every fuse is inline (HW-16).

| Circuit | Fuse | Wire | Wire ampacity | Notes |
|---|---|---|---|---|
| Battery lead (pack's own) | pack PCM | 22 AWG + SM-2P | ~5–7 A wire · SM-2P typically ~3 A | **The system ceiling.** Kept for now - monitor connector temperature; XT30 if it runs warm |
| Battery + → shunt → (+) WAGO bus | **7.5 A inline (main)** | **18 AWG** | ~10 A | **Within ~15 cm of the battery + terminal**, ahead of the shunt. Also protects the short (+) bus → SW1 → split run |
| (+) bus → SW1 → split | - (main covers it) | **18 AWG** | ~10 A | Motors stalled 4.6 A + servo stalled ~1.5 A ≈ 6.1 A; servo bursts ~7.6 A for milliseconds |
| ↳ SW1 → Encoder Motor Module | **5 A inline** | **18 AWG** | ~10 A | Both motors stalled: 2 × 2.3 A = 4.6 A |
| ↳ SW1 → servo UBEC (3.18) | **5 A inline** | **18 AWG** | ~10 A | UBEC input ≈ 1.5 A at servo stall, ≈ 3 A at a 5 A / 6 V burst |
| (+) bus → SW2 → Bauer 50 W | - (main covers it, HW-20) | **18 AWG** | ~10 A | Feeds both boards through one converter (HW-17). ~0.7 A today, ~1.1 A on a flat pack. The run and the Bauer's leads are 18 AWG, which the 7.5 A main protects |
| 3.4a output 5 V → FRDM | - | **18 AWG** | - | 19 mV drop at 3 A over 0.3 m |
| 50 W output 5 V → STM32 | - | **18 AWG** | - | Split from the FRDM feed on **board C** (HW-19), which replaced the WAGO 3-port |
| INA226 I²C + supply | - | Dupont jumpers | - | signal only |

**Holders.** 3 of the 5 RUNCCI-YUN holders in use - main, motors, UBEC (HW-20). **2 spare.** Each is about 50 × 18 mm, 30 mm tall with the lid, with 12-13 cm of 16 AWG each side - all three taped flat to plate 2's lower face, lids to the sides (MEC-16).

**Discrimination.** Main 7.5 A against the 5 A load fuses = **1.5×**. A fault on the short (+) bus →
SW1 → split run is covered only by the main. Accepted: the lead cannot carry more (HW-13).

**Current budget from the battery** (11.1 V, converters ~90 % efficient):

| Load | Normal driving | Worst case |
|---|---|---|
| 2 × drive motors | 0.5–2 A | 4.6 A, both stalled |
| Steering servo | ~0.2 A | 1.5 A stalled, ~3 A bursts |
| FRDM (5 V) | ~0.5 A | ~0.75 A |
| STM32 (5 V) | ~0.15 A | ~0.15 A |
| **Total** | **~1.5–3 A** | **~7 A**, ~8.5 A in a servo burst |

**Corrections, for the record.** (1) The first fuse plan paired 15 A with 16 AWG (~13 A). (2) Drive
stall was estimated at 7–11 A for both motors; the JGB37-520 figure is 2.3 A each, so the estimate
was about double - which is what pushed the earlier fuses and the 14 AWG so high.

### Wire length estimate

Every run is short. Measured off the layout drawing, with routing slack:

| Gauge | Runs | Total per colour |
|---|---|---|
| 18 AWG | plate 1 runs as listed on the [chassis layout](../hardware/renders/chassis-layout.svg) (MEC-16): 16 runs, the fuse leads doing the fused ones | **~1.5 m red + ~1.1 m black** of 2.5 + 2.5 m bought, measured off the 3D model |

The inline fuse holders bring their own 30 cm of 16 AWG, which shortens the main run.
Measure before cutting and keep offcuts.

### 3c. Wiring and termination

| # | Item | Status | Notes |
|---|---|---|---|
| 3.11 | **Silicone stranded wire, pure copper** - Gruiqrd 18 AWG 5 m (2.5 red + 2.5 black) €5.79 | 📦 **Delivered 18 Sep** | Copper, not CCA. **18 AWG only** - the 14 AWG was dropped with the HW-13 rescale |
| 3.12 | **Acual ferrule + crimp kit, 1300 pc, 0.25–10 mm², HSC8 6-4A ratcheting pliers** | 📦 **Delivered 18 Sep** €11.99 | **Ferrules only** - for screw-clamp terminals that take bare wire (INA226 module, converter or switch clamps) | The HSC8 6-4A has a square jaw for ferrules and **cannot crimp insulated ring terminals** properly. That no longer matters: the ring terminals died with the LAOYE bus bars (3.19/3.20 cancelled, HW-16) and the WAGO buses need neither rings nor ferrules. Confirm on unboxing that no ring terminals are included |
| 3.13 | **DOMAXWILL 60-piece lever connector kit** (10 × 5-port, 30 × 3-port, 20 × 2-port, 4 mm²) | 1 set | 📦 **Delivered 18 Sep** €13.96 | Inline joints: **1 × 3-port** as the SW1 split and **7 × 2-port** splices (MEC-16) | WAGO-221 clone: stranded range 0.5–2.5 mm² covers 18 AWG and the 16 AWG fuse leads; current rating not published. Used everywhere **except the two buses**, which are genuine WAGO (3.8). Every one is taped to plate 2's lower face beside its run (MEC-16). **Outlines to measure** |
| 3.14 | **elpohl 470 µF / 35 V low-ESR radial electrolytic, 105 °C, 10 × 13 mm - pack of 5** (B0FK3QYPKM) | 2 used, 3 spare | ✅ Dispatched 18 Sep €5.99 (+€2.75 del.) | **Smoothing** - C1 on the 5 V split board C, C2 across the servo header on carrier board A (HW-19) | 35 V on a 5 V rail is harmless over-rating. **Soldered to boards since HW-19**, lead spacing 5.0 = two holes. *Superseded:* the legs are ~0.6–0.8 mm (0.28–0.5 mm²), inside the WAGO 221's 0.2–4 mm² solid range, so they go straight into a spare port - + leg into the 5 V WAGO, − leg (striped side) into the (−) WAGO. Leave ~15 mm of leg, and **tie or glue the body to the chassis** - an electrolytic fails at the lead seal if a heavy can vibrates on thin legs. **Check polarity before closing the lever;** reversed, it vents |
| 3.15 | Heat-shrink assortment, cable ties, spiral wrap | 📦 **Delivered 18 Sep** | Insulating the switch terminals; zip ties for the pack's felt straps. The harness parts are taped, not tied (3.25, MEC-16) | Tie around connector bodies, never across the levers |
| 3.16 | ~~22 mm step drill or hole saw~~ | ❌ **Not needed** | - | The switches now mount in the printed rear fascia, whose holes are printed in (MEC-02) |
| 3.17 | **4.8 mm insulated female receptacles, flag (right-angle) type** | 🟡 Check the crimp kit | 18 AWG onto SW1/SW2 tabs | The vendor drawing gives **4.8 mm** tabs, not 6.3 (MEC-14). Flag type keeps the depth to 2-3 mm past the tabs. Needed if the supplied socket harness is too deep for the motors or too thin for the DRIVE current |
| 3.18 | **ZHITING switching UBEC, 5 V / 6 V, 3 A continuous / 5 A max**, 2–6S input - B089SH9YWV | 1 | 📦 **Delivered 18 Sep** €6.68 | Steering servo supply, fed from **SW1 via a 5 A inline fuse** (power train, HW-14) | Separate converter required (HW-11): the servo is a 6–7.4 V part, the vehicle has only 5 V rails and the ~11 V pack, and its stall current must stay off the logic rails. Sizing: stall 2.5 A @ 6 V (LD-1501MG datasheet) → 3 A continuous has thin but adequate margin; > 3 A bursts are inside the 5 A max. Reverse-polarity protected, metal-shielded, output filter, status LED. **35 x 12 x 5 mm confirmed from the supplier drawing; potted, with no mounting holes - cable tie or adhesive pad.** Taped to plate 2's lower face, its 6 V pair climbing to carrier board A through plate 2's opening (MEC-16). **Set the jumper to 6 V before first power-up.** Wire servo +/− to the UBEC, signal to the STM32 PWM pin, UBEC ground to the star ground. A sustained stall trips its over-temperature cut-out - steering goes limp |
| 3.21 | **Elegoo metal film resistor kit, 525 pc, 1/4 W, 0 Ω – 10 kΩ** | 📦 **Delivered 18 Sep** €11.99 | **Closes two open items at once:** the CAN bus **120 Ω** terminators (4.3) and the **10 kΩ** Rp fallback for the USB-C feed (5.1). Bought 17 Sep but never recorded - added 19 Sep. **Fitted on boards since HW-19:** R3 120 Ω behind the TERM jumper on carrier board B, R1/R2 10 kΩ on board C, R4 1 kΩ in the servo PWM. 1/4 W is ample: a 120 Ω terminator across a 2 V CAN differential dissipates ~33 mW. **No 120 Ω in the kit (checked 2026-10-03)**: R3 is built as **100 Ω + 20 Ω in series**, exactly 120 Ω (HW-19). |
| 3.19 | ~~Insulated ring terminal kit with ratchet crimper~~ | ❌ **Not needed** | - | Only required for the LAOYE M4 screw terminals, dropped in HW-16 |
| 3.20 | ~~Spring (split) lock washers, M4 / M6~~ | ❌ **Not needed** | - | Only required for the LAOYE screw terminals, dropped in HW-16 |
| 3.22 | **M3 fascia fixings** - 4 × M3×8, 2 × M3×12, 6 × M3 nyloc nuts, 6 × M3 washers | 🔴 To order | Clamps both fascia panels to decks 1, 2 and 3 (MEC-07). Nuts are **captive in printed pockets** in the panels, so nothing is held inside the chassis; plate 2's M3×12 comes down from the open upper gap through the upper panel's pad and into the nut in the lower panel's top pad, clamping both. Washer under every head, on the plastic |
| 3.23 | **M3 spacers and screws for the motor driver** - 2 × M3 screws, 2 × nuts, 4 × spacers | 🟡 **On the vehicle, not sourced here** | Stands the Encoder Motor Module off plate 1 (2.4) | Fitted 2026-09-21 from what was to hand. ⚠️ **Measure the spacer height and record it** in [`parts/2.4-Encoder-Motor-Module/SPECS.md`](parts/2.4-Encoder-Motor-Module/SPECS.md): the board's rear edge overhangs the motor cans and the ⌀33 can is only 10.7 mm above the plate there, so the height is a clearance. Two more ties or screws are wanted for the unfixed front pair |
| 3.24 | **Battery straps and pad** | ✅ **Fitted 2026-09-28 from stock** | Holds the pack (3.1) to plate 1 | The pack is on a **felt pad**, held by **two felt strips and zip ties** through the side slots, lengthwise **right behind the tie rod at x 85-162** (MEC-16) - the drawn x 55-132 went through the steering linkage. The hook-and-loop straps first listed here were not needed. ⚠️ The pack is soft shrink wrap: keep the felt under every tie |
| 3.25 | **3M double-sided foam tape**, ~1 mm, 12-19 mm wide | 🔴 **To buy** ~€6 | Sticks every harness part to **plate 2's lower face** (MEC-16) | The two 221-415 buses, the three fuse holders, the INA226, the UBEC, the 3-port split and the 2-port splices. Clean the plate with isopropyl alcohol first. A foam tape, not a thin film one - it takes up the anodised plate's texture and the clips' uneven backs |

Not included: the battery-side connector, which waits on identifying the Hiwonder discharge
lead (see 3.5b).

## 3b. Battery monitoring and BMS sensing

Decided 2026-09-12: build the monitoring in software from the start rather than buying a
canned protection module. The buzzer covers the human-in-the-loop phase; once the STM32
service works, monitoring becomes standalone.

| # | Item | Qty | Status | Role | Notes |
|---|---|---|---|---|---|
| 3.9 | **INA226 module, R002 shunt** - GERUI, €10.99 | 1 | 📦 **Delivered 18 Sep** €10.99 | Pack voltage **and** current, one part | I2C, 16-bit, bidirectional. **Shunt confirmed R002 = 2 mΩ** from the product photo → ±41 A electrical range at 1.25 mA resolution. Bus input takes the 12.6 V pack directly, no divider. Logic 2.7–5.5 V. Screw terminals + address-select jumper. **Module confirmed 22 x 26 x 14 mm** (2026-09-21 - the 26 is the depth, not the width) with **two** ⌀1.8-2.0 corner holes, 18.6 mm apart. M2.5 fits nothing on it; **it is not screwed down** - taped upside down to plate 2's lower face with 3M foam tape, beside the (+) bus (MEC-16), like the WAGOs and the UBEC. ⚠️ **Re-solder the 4-pin I²C header onto the component side**; as shipped the pins protrude from the back, which is the face that goes flat on the tape. Mounting reasoning in [`parts/3.9-INA226/SPECS.md`](parts/3.9-INA226/SPECS.md). **The four large holes in the top row - V-, Current-, Current+, V+ - are NOT fixing holes** - they are the high-current terminals, plated pads for soldering heavy wire straight in as an alternative to the screw terminals. At 7.5 A the screw terminals are ample, so leave them unused. ⚠️ The 5.08 mm terminal blocks are the real ceiling (typically 10–16 A), not the shunt - check them for heating on the first loaded runs |
| 3.10 | ~~ARCELI 1S–8S LiPo alarm~~ | - | ❌ **Cancelled** | - | (was 3.6) Independent of all software. Keep it fitted permanently |

**Range is not the limitation.** R002 = 2 mΩ gives **±41 A**, far above the 7.5 A main fuse
(HW-13) - nothing on this vehicle can clip the reading. The real ceiling is the module's
**5.08 mm screw terminals**, typically 10–16 A, which is still well above the 7.5 A the lead
can pass. Watch them for heating on the first loaded runs.

**No per-cell visibility is possible on this pack.** The Hiwonder battery has no balance
connector, so the buzzer alarm (3.10) cannot be fitted and cell imbalance cannot be observed
without opening the case - which is not worth doing. Pack-level V and I from the INA226 is
the whole of the available signal, and the pack's own internal protection PCB is the safety
backstop the buzzer would have been.

Capacity is known - **6000 mAh** - which gives coulomb counting its denominator from day one.

**Where it belongs:** on the STM32, not the i.MX 91. The MCU owns safety and real-time, reads
the INA226 over I2C, and publishes pack state over CAN. Linux consumes it and decides when to
shut down cleanly. That is the platform's compute/control split doing real work, and it is a
better first CAN payload than a synthetic test message. The FRDM's own 2× ADC channels on the
custom connector stay free as a cross-check.

## 4. Communication (CAN)

| # | Item | Qty | Status | Role | Notes |
|---|---|---|---|---|---|
| 4.1 | **SN65HVD230 CAN transceiver module** - GERUI, €5.99 | 1 | 📦 **Delivered 18 Sep** €5.99 | Physical layer for the **STM32 side only** (the FRDM has its own, 4.2) | **26.98 × 10.24 mm**, straight header in the board's plane, so it **lies flat on carrier board B** with its pins bent 90° (or a right-angle header): upright it would hit plate 3. Dimensions: [`parts/4.1-SN65HVD230-Module/SPECS.md`](parts/4.1-SN65HVD230-Module/SPECS.md). 3.3 V part, matches F407 I/O. Pins: 3.3V · GND · CAN RX · CAN TX; screw terminal CANH / CANL. **As fitted (2026-10-03) it lies face down:** its CAN H / L reach the carrier through its own 2-pin CANH / CANL header, and the screw terminal is unused (MEC-15). **Wire straight, not crossed:** module CAN TX → STM32 **PD1 (CAN1_TX)**, module CAN RX → **PD0 (CAN1_RX)** - the module's labels are from the MCU's point of view, unlike a UART. The **103** resistor on board is 10 kΩ on RS = **slope-control mode**: fine to ~500 kbit/s, which is the intended bus rate; only an issue if you later want 1 Mbit/s |
| 4.1b | **CAN1 pin assignment** | - | ✅ Decided | - | **PD0 = CAN1_RX, PD1 = CAN1_TX (AF9).** PA11/PA12 are taken by USB OTG and PB9 by OTG_FS_SDA on this board; PD0/PD1 are free and both broken out on header P2 |
| 4.2 | **CAN on the FRDM-IMX91S** | - | ✅ Resolved | Physical layer for 1.1 - **on board, none to buy** | UM12262 §2.12 (FRDM-IMX91): one FlexCAN controller is wired to an on-board **TJA1051T/3**, which drives **P12 pin 8 = CAN_H, pin 10 = CAN_L**; Zephyr lists a board-level transceiver. The -S QSG describes the same 2×5 connector carrying one CAN port - strong but **inferred for the -S**, since no -S schematic is public. ⚠️ The non-S has **SW3 (enables/disables the CAN signals)** and **SW4 (CAN split termination)** - check for equivalents on the -S before debugging a dead bus, and SW4 may remove the need for an external 120 Ω at that end |
| 4.3 | CAN bus wiring + termination | 1 set | 🟡 **Measure, then fit from stock** | Bus between STM32 and FRDM, with the DE-9 port (4.5) as a stub | Run **H, L and GND**, twisted, ~30 cm. Termination must be **120 Ω at each end and nowhere else** - a third terminator drags the bus to 40 Ω and breaks it. **The two ends are the SN65HVD230 and the FRDM.** The DE-9 debug port is a **stub in the middle and gets no resistor**, and the USB-CAN adapter's own termination must be **switched off** (4.7). **Check the module:** measure CANH–CANL unpowered - ~120 Ω means it is already fitted, open means add one. **Check the FRDM:** the non-S has **SW4** for split termination (4.2); if the -S has it, that end needs nothing either. **No purchase needed** - 120 Ω comes from the resistor kit (3.21). **The STM32 end is now a jumper (HW-19):** R3 on carrier board B, TERM on = terminated; remove the module's own resistor so the jumper alone decides |
| 4.4 | 2×5 mating connector / cable for the custom header | 1 | 🔴 To order | Breaks CAN + ADC out of 1.1 | Pitch and part number to be read off the board UM |
| 4.5 | **GTIWUNG DE-9 male solder connector, 10-pack with hoods** | 1 pack | ✅ **Ordered 20 Sep** €8.88 | CAN debug port on the rear fascia - lets a PC join the bus as a third node | **Male on the robot** per CiA 303-1, so the live pins are never on a loose cable end. Wire **pin 2 = CAN_L, pin 3 = CAN_GND, pin 7 = CAN_H**; leave **pin 9 (CAN_V+) unconnected**. Mounts from behind the fascia upper panel, alone in its top row at x 2.48, z 107.12 in vehicle coords (MEC-13). ✅ Vendor drawing checked 2026-09-19: flange 30.84 ±0.38, screws 24.99 ±0.13, shell 16.92 × 8.38, own holes ⌀3.05 - `DE9_*` in `mechanical/cad/fascia.scad` now matches (aperture 17.9 × 9.2). ⚠️ **Mount the bare connector - do not fit the supplied plastic hood.** That hood is a cable backshell; it prevents the flange sitting flush on the fascia. The bare flange is DIN 41652 standard (30.8 mm, 24.99 mm pitch) so it matches `DE9_*` whatever the vendor. 10 pieces gives spares for the cable end and for practice - 3 wires each (pins 2, 3, 7) |
| 4.6 | **DE-9 female-to-female cable, straight-through** | 1 | 🔴 To order | Robot ↔ USB-CAN adapter | ⚠️ **Straight-through, not null-modem.** Old serial stock is very often crossed (2↔3), which would swap CAN_L into CAN_GND. Buzz pin-to-pin before first use. ≤ 2 m |
| 4.7 | **USB-CAN adapter** (PC side) | 1 | 🔴 To order - spec below | Third node for tracing, injecting and logging frames from the PC | Wanted: **switchable/removable 120 Ω termination** (it must be **OFF** - see 4.3), **galvanic isolation**, male DE-9, and Linux support via **SocketCAN** (`can0` through `slcand` or a native driver). Candidates worth comparing: CANable/CANtact-style open hardware (cheap, SocketCAN native), PEAK PCAN-USB (well supported, more costly) |

## 5. Development accessories

| # | Item | Qty | Status | Role | Notes |
|---|---|---|---|---|---|
| 5.1 | **KUOQIY 6-wire USB-C female panel socket, 150 mm 24 AWG pigtail, 3 A (6-pack)** + C-to-C cable (**Bkduice 20 cm, 3-pack, 60 W**) | 1 + 1 | 📦 **Delivered 18 Sep** €8.68 + €5.00 | Feeds 5 V from 3.4a into the FRDM's J1 | Converter → **board C** (HW-19) → socket pigtail → C-to-C **data** cable → J1. Preferred over the DAOKAI breakout board: **pre-wired (no soldering to pads), rated 3 A instead of 1.5 A, and it should carry no Rd resistors to remove**. 24 AWG = 0.2 mm², inside the WAGO 221 range, and ~38 mV drop at 1.5 A over 150 mm. **Check on arrival:** CC1→GND and CC2→GND should read **open**. If they read 5.1 kΩ the socket is a sink and the moulded body can't be reworked - use the breakout board instead. **Test:** VBUS + GND only, CC unconnected. Boots → done. **Since HW-19 the 10 kΩ Rp pair is soldered on 5 V split board C.** *Since 2026-09-29 the socket itself is zip-tied to board C and its pigtail soldered in:* red V C·J7, black G C·H7, green CC1 C·D7, yellow CC2 C·B7. White D− and blue D+ are cut short and insulated separately (HW-19 revision). The other 5 sockets in the pack are spares. *Superseded:* 10 kΩ from CC1→VBUS and CC2→VBUS, which needs no soldering: resistor leg and CC wire into one WAGO port, other leg into the VBUS WAGO. Fallback: DAOKAI 6-pin breakout 10-pack ~€11 (carries 2 × 5.1 kΩ marked 512, at opposite ends for easy removal). **The 10 kΩ for the Rp fallback is already in hand** - see 3.21. Note the cable bought is the Bkduice 20 cm 3-pack, not the ADILIFT 30 cm originally listed |
| 5.2 | USB-C to USB-A cable (debug) | 1 | ✅ Included in kit | UART console on J11 | Ships with the FRDM kit. With 5.9 fitted this plugs into the **fascia**, not the board |
| 5.3 | microSD cards | 2+ | 🟡 To check | Boot media | 32 GB with BSP ships in the kit. A second card is worth it - one known-good, one under test. **Slot is on the board underside**, so plan the standoffs |
| 5.4 | Ethernet cable | 1 | 🟡 To check | 1 GbE / image transfer | Wi-Fi 6 is on board, so this is convenience not necessity |
| 5.7 | **Elegoo 120 pc Dupont jumper kit** (M-M / M-F / F-F, 20 cm) | 1 | 📦 **Delivered 18 Sep** €6.99 | **Signals only** - I²C to the INA226, STM32↔transceiver, bench work | ⚠️ **Copper-coated aluminium**, ~24–26 AWG, ≤1 A. Never for any power branch. CCA work-hardens and its oxide is insulating, so crimps degrade under vibration - add strain relief on anything that stays on the vehicle |
| 5.11 | **RUNCCI-YUN 82 pc double-sided prototype PCB kit** | 1 | ✅ **Ordered 20 Sep** €11.98 | **Carrier board for the STM32** (MEC-08, MEC-15) | **Contents (listing, 2026-09-29):** 19 boards - 6 × 2×8, 6 × 3×7, 3 × 4×6, 3 × 5×7, 1 × 7×9 cm - plus 8 × 2p and 6 × 3p 5.08 mm screw terminals, 25 jumper caps, and 8 each of 40-pin male, right-angle male and female headers. **Built as three kit boards (MEC-15, HW-19):** A 5×7 under P1, B 5×7 under P2, 5.9 mm apart, on 1×25 sockets cut from the female headers; C 3×7 as the 5 V split, now with 2 terminals and the USB-C socket (5.1) tied to it - drawing [`../hardware/renders/stm32-carrier.svg`](../hardware/renders/stm32-carrier.svg). No kit board spans the Discovery and leaves room outboard (the one 7×9 is covered by it), so the "~70 × 66 minimum" below is history. The Discovery plugs into a hand-built carrier via its **male P1/P2 headers** - UM1472 §4.9 states this is what they are for. The carrier bolts to the chassis, breaks out 5 V, CAN (PD0/PD1), I²C2 (PB10/PB11) and the servo PWM, and hosts the SN65HVD230 so the CAN stubs stay short. Needs a board of ~70 × 66 mm minimum. ⚠️ **Dry-fit before soldering** - confirm the P1–P2 row spacing sits on the 2.54 mm grid, and which way the pins protrude |
| 5.6 | USB inline power meter | 1 | 🟡 Optional ~€10–15 | Measures real draw under load | No longer needed to settle the voltage question. Still the easiest way to get the FRDM's loaded current for fuse sizing - or wait and read it off the INA226 |
| 5.5 | Headers, jumper wires, ferrules | 1 set | ✅ Covered by 3.12 / 5.7 | Prototyping and terminating the converters' flying leads | 3.4a/3.4b ship as bare tinned wire |
| 5.8 | **USB-A to Mini-B cable, 1 m** (Digitus) | 1 | ✅ Ordered €1.33 | ST-LINK on the Discovery | MB997B uses **mini**-USB at CN1, not micro - confirmed in UM1472 §"type A to mini-B". With 5.10 fitted this plugs into the **fascia**, not CN1 |
| 5.9 | **chenyang USB-C male→female extension, panel screw holes, 0.2 m** | 1 | ✅ **Ordered 20 Sep** €8.99 | Brings the FRDM's **J11 UART console** out to the upper fascia panel | Panel end female, cable end male into J11. **Not J1** - that is the power input (HW-02). Vendor drawing: flange **23 mm**, screw centres **15 mm**, body 40 mm, 7.5 mm thick. ✅ **In hand, measured 2026-09-24:** flange 23 × ~8.3, 6 deep, **threaded M2.5 holes** 15 apart, M2.5 × 5 screws supplied, metal rim ~0.9 proud, body ~14 wide. **Mounts from behind** the upper panel, in the bottom row at x −16.52, in a pocket, with its own screws from the front, as in the vendor bracket. ⚠️ The heads leave ~11 mm for the plug grip: use a **slim-grip cable** (the 10 mm bench cable fits) - a chunky one will not seat (MEC-13). The body (~14 wide, from a photo) is 9 mm clear of the left standoff, so its exact width no longer matters. ⚠️ A USB-C *extension* is not spec-compliant; if it does not pass CC through, a C-to-C lead will not enumerate - **test with both C-to-C and A-to-C on arrival** |
| 5.10 | **JSER Mini USB 5-pin male→female extension, 50 cm, with screws** | 1 | ✅ **Ordered 20 Sep** €10.15 | Brings the Discovery's **CN1 ST-LINK** out to the upper fascia panel | Panel end female, cable end male into CN1. ✅ **In hand, measured 2026-09-24:** flange **36 × 10, 8 deep** (the 28 read off the vendor photo was wrong), **threaded M2.5 holes** ~28.5 apart, body ~20 × 10 × 13. **Mounts from behind** the upper panel, horizontal, in the bottom row at x +21.48 beside the USB-C, with its own screws from outside. The outboard hole is a slot taking any pitch 27–30 (MEC-13). 50 cm is ample for the ~100 mm run from the lower gap |

## 6. Later phases

| # | Item | Qty | Status | Role |
|---|---|---|---|---|
| 6.1 | **Raspberry Pi 5** | 1 | ✅ Owned | Future compute node - ROS 2, vision/AI |
| 6.2 | CAN hardware for the Pi 5 | 1 | 🔵 Later | Pi integration onto the bus |
| 6.3 | Sensors (camera, IMU, LiDAR, encoders) | - | 🔵 Later | Autonomous driving |

---

## Where the build stands - 19 Sep

**The power stage is bought and in hand.** Converter, fuses, wire, WAGOs, lever kit, ferrule
kit, heat-shrink, UBEC, INA226, CAN transceiver, resistor kit and the USB-C feed all arrived
18 Sep. Nothing in the power chain is waiting on a purchase.

### Bench work - now unblocked by delivery, and all of it free

| # | Check | Why it matters |
|---|---|---|
| 1 | **CC1→GND / CC2→GND on the KUOQIY socket must read OPEN** (5.1) | If they read 5.1 kΩ the socket is a sink and the moulded body cannot be reworked - the whole FRDM feed changes to the breakout board |
| 2 | **CANH–CANL on the SN65HVD230, unpowered** (4.3) | ~120 Ω = termination already fitted. Decides whether any resistor is fitted at all |
| 3 | **Does the resistor kit contain 120 Ω?** (3.21) | Assumed, not verified. E24 has it, E12 has it; a coarser kit might not |
| 4 | **Set the UBEC jumper to 6 V before first power-up** (3.18) | It ships on 5 V. Powering the servo at 5 V is out of its 6–8.4 V range |
| 5 | **FRDM boots from the Bauer 50 W through the KUOQIY socket** | Confirms the whole compute rail end to end |
| 6 | **FRDM current under load** | The logic branch has no fuse of its own since HW-20; the number still sizes the Bauer's margin |

### Still to buy - none of it blocks the power stage

| # | Item | Note |
|---|---|---|
| 4.4 | 2×5 mating connector for the FRDM CAN header | **Still unidentified.** The one genuine blocker for CAN, and free to resolve - the board is on the desk |
| 4.6 | DE-9 F-F straight-through cable | ~€10. The panel connector (4.5) is in hand |
| 4.7 | USB-CAN adapter | Must have **switchable** 120 Ω and isolation |

### Waiting on delivery

3.8 WAGO 221-415 and 5.8 Mini-B cable (dispatched 18 Sep) · 3.14 capacitors (dispatched 18 Sep)
· **3.5a/3.5c switches, due 29 Sep – 13 Oct** - no longer blocks the fascia: the vendor
drawing settles the hole, bezel and nut (MEC-14). Only the harness depth waits for them.

Resolved: board variant · DC-DC choice · servo rail · over-discharge approach · FRDM power
input (plain 5 V) · CAN transceiver count · bus distribution · fascia geometry.

## Open selections

| Question | Blocks | Why it is open |
|---|---|---|
| ~~Are the 2×5 CAN pins transceived on board?~~ | - | **Resolved:** the FRDM-IMX91S has its own transceiver; only the STM32 side needs one |
| ~~Deck gap~~ | - | **Measured 2026-09-20 (MEC-09):** lower gap **50 mm**, upper **40 mm** - two standoff lengths. Panels are 52 and 42 mm tall |
| ~~Hiwonder driver servo supply~~ | - | **Resolved:** the driver has no servo output - see 3.18 and HW-11 |
| ~~Bus bar pair dimensions~~ | - | **Closed:** the LAOYE bars were dropped for WAGO 221-415s on 221-500 carriers (HW-16) |
| ~~Battery discharge connector~~ | - | **Identified:** SM-2P on a 22 AWG lead. Kept for now, temperature monitored (HW-13) |
| Battery **height** | layout | Footprint measured 63 × 77 mm (2026-09-20); height decides lower-gap clearance |

## Over-discharge protection - the layered plan

A hard cutoff on the compute rail is worse than no cutoff: yanking 5 V from a running Linux
board mid-write corrupts the filesystem. So protection is layered rather than bought as one part:

1. ~~**Now - buzzer alarm.**~~ **Not available.** The pack has no balance connector, so the
   1S–8S alarm cannot be fitted (3.10 cancelled). **Step 1 of this plan does not exist** - the
   pack's own internal protection PCB is the only backstop until step 3 is built. That raises the
   priority of the INA226 low-voltage path, which is now the first real protection layer.
2. **Later - drive rail cutoff.** The motors can be hard-cut safely; a relay or MOSFET on the
   drive branch, commanded by the STM32, is the right place for an abrupt disconnect.
3. **Later - graceful shutdown.** Pack voltage through a divider into an STM32 ADC, reported
   over CAN, with a Linux service that shuts down cleanly on the low-voltage warning. This is
   the correct answer and it is also a genuinely useful piece of the software stack to build.

**Fuse block alternative considered and rejected (2026-09-12):** FULARR 6-way, B07GXCR732,
115 × 53 × 42 mm. Narrower than the Geloo, which would have helped on the 120.5 mm deck -
but only 8 % less area overall, no negative bus (so a separate ground bar would be needed,
eating the saving back), no blown-fuse LEDs, 6.3 mm spade terminals instead of screws, and
12 mm taller, which is worse on the deck gap - the dimension that is actually tight and
still unmeasured.

Documents for every confirmed part live in [`parts/`](parts/), one folder per
BOM item number - and [`README.md`](README.md) grades each one. The vendor documents
themselves are not in the repository; see the root [README](../README.md).

Prices are as invoiced: Amazon.de 17 Sep and eBay 14 Sep, VAT included.
