# Nexus-Physical-05 - Power supply and distribution

System element, level 1. Realised in hardware; the recursion stops here. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** Pack, fuses, buses, SW1 and SW2, the 5 V converter with board C, the steering UBEC, the shunt and INA226.
- **Interfaces.** Supplies [Nexus-Physical-01](Nexus-Physical-01.md), [Nexus-Physical-02](Nexus-Physical-02.md), [Nexus-Physical-07](Nexus-Physical-07.md) and the servo of [Nexus-Physical-08](Nexus-Physical-08.md); the charger and the operator outside.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 101 F1 to F5, 501 F2.
- **Modes.** Pack disconnected; pack connected, switches off; logic on; drive on.

## Requirements

### Nexus-Physical-05-R001

**Statement.** The element shall supply 5 V to the STM32 node and the FRDM node from one converter, split on board C.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Vehicle-R001
- Allocated-to: -
- Phase: 1
- Verification: Test 5 V measured at the FRDM J1 and the STM32 5V pin with the logic switch on
- Realised-by: HW
- Decisions: HW-17, HW-19

### Nexus-Physical-05-R002

**Statement.** The element shall supply the motor driver at pack voltage through SW1 and a 5 A fuse.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection Harness checks (hardware/README.md)
- Realised-by: HW
- Decisions: HW-08, HW-20

### Nexus-Physical-05-R003

**Statement.** The element shall supply the steering servo at 6 V from a UBEC fed through SW1, and from no 5 V rail.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection The servo lead takes the UBEC output through the carrier header
- Realised-by: HW
- Decisions: HW-11, HW-14

### Nexus-Physical-05-R004

**Statement.** SW1 shall switch the drive branch (motor driver and UBEC) and SW2 the logic branch (the 5 V converter), each independently of the other.

- Function: Nexus-Logical-101-F03, Nexus-Logical-501-F02
- Derived-from: Nexus-Vehicle-R002
- Allocated-to: -
- Phase: 1
- Verification: Demo SW1 off with SW2 on, then the reverse
- Realised-by: HW
- Decisions: HW-08

### Nexus-Physical-05-R005

**Statement.** No switch shall sit in the pack's main current path; the pack connector is the disconnect.

- Function: Nexus-Logical-101-F02
- Derived-from: Nexus-Vehicle-R003
- Allocated-to: -
- Phase: 1
- Verification: Inspection Harness checks (hardware/README.md)
- Realised-by: HW
- Decisions: HW-08

### Nexus-Physical-05-R006

**Statement.** The pack feed shall be fused at 7.5 A within 15 cm of the battery terminal, and the motor-driver and UBEC branches at 5 A each.

- Function: Nexus-Logical-101-F02
- Derived-from: Nexus-Vehicle-R003
- Allocated-to: -
- Phase: 1
- Verification: Inspection Three fuses fitted, values and position as stated
- Realised-by: HW
- Decisions: HW-13, HW-20
