# Nexus-Physical-01-07 - LED stick

Hardware element, level 2, bought: its requirements state what the node relies on, checked against the vendor documentation; the recursion stops here. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** The WS2812B 8-LED stick (BOM 1.3) on plate 3: eight RGB LEDs, each with its own driver, chained on one data line.
- **Interfaces.** The carrier [01-02](Nexus-Physical-01-02.md) through the LED header at the rear of board A: data from PC12, 5 V and GND from the 5 V input of the carrier.
- **Allocated functions.** 503 F4.
- **Modes.** None of its own. The LEDs keep the last frame they received until the next one or a loss of power.

## Requirements

### Nexus-Physical-01-07-R001

**Statement.** The LED stick shall show on each LED of the LED stick the colour sent to that LED on the data input of the LED stick.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: HW
- Decisions: HW-22

### Nexus-Physical-01-07-R002

**Statement.** The LED stick shall draw the supply of the LED stick from the 5 V input of the carrier.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Inspection The LED stick lead at the LED header of board A
- Realised-by: HW
- Decisions: HW-22, MEC-15
