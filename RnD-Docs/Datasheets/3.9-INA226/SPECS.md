# 3.9 - INA226 current/voltage monitor

`INA226-TI-Datasheet.pdf` is the authoritative silicon datasheet (TI SBOS547).
The module in hand is silkscreened **MJKDZ · INA226** (red PCB, photographed 2026-09-21).

| Parameter | Value |
|---|---|
| Bus voltage range | 0–36 V - measures the 12.6 V pack directly, no divider |
| Current | bidirectional, ±20 A with a 2 mΩ shunt |
| Resolution | 16-bit |
| Interface | I²C, 16 programmable addresses |
| Logic supply | 2.7–5.5 V |
| Accuracy | ±1 % (module-level claim) |
| **ALERT pin** | hardware threshold interrupt - the low-voltage trip is an IRQ, not a poll |

⚠️ **Verify the shunt on arrival.** Some INA226 breakouts ship with a 0.1 Ω shunt, which
caps the range at roughly 0.8 A and would be useless here. The part needed is the
**2 mΩ / 20 A** variant. Measure the shunt or read the marking before wiring it in.

**Range is not the limitation** since HW-13 rescaled the main fuse to **7.5 A**. A 2 mΩ shunt
gives ±41 A, far above anything the pack's 22 AWG lead can pass. The module's 5.08 mm screw
terminals, typically 10–16 A, are the real ceiling.

**Placement:** on the STM32, in the battery main. The MCU owns safety and real-time,
reads it over I²C and publishes pack state on CAN. The FRDM's own 2 ADC channels stay
free as an independent cross-check.


## Mounting - decided 2026-09-21

**It is not screwed down.** Measured off the photograph of the module in hand:

| Hole | Diameter | Pitch |
|---|---|---|
| Two **corner holes**, bottom edge | ⌀ **~1.8-2.0** | 18.6 mm apart |
| **V-** and **V+** in the top terminal row | ⌀ **~2.2-2.4** | 15.7 mm apart |

Both are ±0.3 from a hand-held photo. M2.5 fits neither, which is what was found on the bench;
**M2 fits V- / V+ and is an interference fit in the corner holes.**

**Why no screws at all.** The module is 26 mm deep and the channel it lives in - between the
plate's front edge at y ≈ 2 and the (+) WAGO at y 28 - is 26 mm. It fits exactly, with nothing
spare. The only fixing feature in that band is the **48.3 × 5.3 slot at y 9.88-15.17**, and no
pair of the module's holes lands on it: the V-/V+ pair sits 3 mm from the terminal edge and the
corner pair 2 mm from the other, so whichever way round it goes the screws fall 6-10 mm clear of
the slot. Screwing it would mean pushing the module into the WAGO column and cascading the whole
harness for a 5 g part.

**How it is held instead:** an adhesive insulating pad under it, and the two 18 AWG runs into its
screw terminals. Those wires are stiff and they restrain it better than a fastener would. This is
the same treatment the WAGOs and the UBEC get.

### ⚠️ If it ever does get screwed, not through V+ / V-

They are live nets, not fixings, and so are the two **Current** holes beside them. With an
all-nylon screw, standoff and nut it is electrically safe, but it leaves a trap: **one steel
screw through V+ later puts pack positive onto the aluminium chassis.** Use the corner holes, and
label the module if anything metal ever goes near those four holes.

### The I²C header points the wrong way

The 4-pin `VCC SDA SCL GND` header is soldered with its pins protruding from the **back** of the
board, so laying it flat needs about 6 mm of standoff. **Re-solder that header so the pins point
up**, on the component side. The board then lies flat on a 1-2 mm pad and the Dupont leads come
off the top, which is where they are wanted anyway.

### Position on plate 1

**x 135-157, y 2-28**, terminal row on the **y 28 edge** facing the (+) WAGO bus directly behind
it. That puts it in the battery (+) chain with the shortest possible run: pack SM-2P at the
battery's x 132 / y 30 corner, out into the y 0-30 channel, through the 7.5 A main fuse, into
this module, out to the (+) bus.
