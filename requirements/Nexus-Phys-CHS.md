# Nexus-Phys-CHS - Chassis, decks and fascia

Physical, level 2. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The Hiwonder three-deck chassis, the printed trays and pads, the harness board under plate 2 and the two-panel rear fascia.
- **Interfaces.** Carries every other physical element; the fascia holds SW1, SW2, the DE-9 port and the board debug ports, which belong electrically to [Nexus-Phys-PWR](Nexus-Phys-PWR.md), [Nexus-Phys-CAN](Nexus-Phys-CAN.md), [Nexus-Phys-STM32](Nexus-Phys-STM32.md) and [Nexus-Phys-FRDM](Nexus-Phys-FRDM.md).
- **Allocated functions.** 102 F01 to F03; the panel half of 501 F02.
- **Modes.** None.

## Requirements

### Nexus-Phys-CHS-R001

**Statement.** Components shall sit on the three decks as allocated in MEC-12: battery, motor driver and motors on plate 1, STM32 carrier and 5 V converter on plate 2, FRDM on plate 3.

- Derived-from: Nexus-SubSys-102-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The vehicle matches the chassis layout drawing
- Realised-by: HW
- Decisions: MEC-01, MEC-12

### Nexus-Phys-CHS-R002

**Statement.** A two-panel printed rear fascia, clamped at four corners, shall carry both power switches, the DE-9 port and the board debug ports.

- Derived-from: Nexus-SubSys-102-R003
- Allocated-to: -
- Phase: 1
- Verification: Inspection The fascia is fitted and every item on it is reached from outside
- Realised-by: HW
- Decisions: MEC-02, MEC-03, MEC-05, MEC-07, MEC-13

### Nexus-Phys-CHS-R003

**Statement.** The switches shall be legended DRIVE for SW1 and LOGIC for SW2.

- Derived-from: Nexus-SubSys-501-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The legends read as stated
- Realised-by: HW
- Decisions: MEC-06
