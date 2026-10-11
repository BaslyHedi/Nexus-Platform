# Nexus-Physical-01-03 - CAN transceiver module

Hardware element, level 2, bought: its requirements state what the node relies on, checked against the vendor documentation; the recursion stops here. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** The SN65HVD230 module (BOM 4.1), with its own 120 Ω termination.
- **Interfaces.** The carrier [01-02](Nexus-Physical-01-02.md) on the logic side; the bus [Nexus-Physical-04](../../level-1/Nexus-Physical-04.md) on the CAN side.
- **Allocated functions.** 401 F1.
- **Modes.** None.

## Requirements

### Nexus-Physical-01-03-R001

**Statement.** The transceiver module shall translate between the CAN bus and the 3.3 V logic of the STM32F407.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Analysis The SN65HVD230 datasheet
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-01-03-R002

**Statement.** The transceiver module shall terminate the bus with the 120 Ω resistor of the module.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R003
- Allocated-to: -
- Phase: 1
- Verification: Test Resistance across CAN_H and CAN_L at the module, disconnected, reads 120 Ω ± 5 Ω
- Realised-by: HW
- Decisions: HW-09, HW-19
