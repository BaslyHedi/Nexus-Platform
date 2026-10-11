# Nexus-Physical-06 - Chassis and enclosure

System element, level 1. Realised in hardware; the recursion stops here. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The three-deck chassis, the trays and pads, the harness board and the rear fascia.
- **Interfaces.** Carries every other element; the fascia holds the switches of [Nexus-Physical-05](Nexus-Physical-05.md) and the ports of [Nexus-Physical-01](Nexus-Physical-01.md), [Nexus-Physical-02](Nexus-Physical-02.md) and [Nexus-Physical-04](Nexus-Physical-04.md).
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 102 F1 to F3.
- **Modes.** None.

## Requirements

### Nexus-Physical-06-R001

**Statement.** The element shall carry the components on its three decks as allocated in MEC-12: battery, motor driver and motors on plate 1, STM32 carrier and 5 V converter on plate 2, FRDM on plate 3.

- Function: Nexus-Logical-102-F01
- Derived-from: Nexus-Vehicle-R005
- Allocated-to: -
- Phase: 1
- Verification: Inspection The vehicle matches the chassis layout drawing
- Realised-by: HW
- Decisions: MEC-01, MEC-12

### Nexus-Physical-06-R002

**Statement.** A two-panel printed rear fascia, clamped at four corners, shall carry SW1, SW2, the DE-9 port, the ST-LINK USB port and the FRDM console port.

- Function: Nexus-Logical-102-F03
- Derived-from: Nexus-Vehicle-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection Every item is reached from outside the closed vehicle
- Realised-by: HW
- Decisions: MEC-02, MEC-03, MEC-05, MEC-07, MEC-13

### Nexus-Physical-06-R003

**Statement.** The switches shall be legended DRIVE for SW1 and LOGIC for SW2.

- Function: Nexus-Logical-102-F03, Nexus-Logical-501-F02
- Derived-from: Nexus-Vehicle-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection The legends read as stated
- Realised-by: HW
- Decisions: MEC-06
