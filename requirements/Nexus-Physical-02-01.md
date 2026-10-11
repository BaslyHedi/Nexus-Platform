# Nexus-Physical-02-01 - FRDM board

Hardware element, level 2, bought: its requirements state what the node relies on, checked against the vendor documentation; the recursion stops here. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The FRDM-IMX91S (BOM 1.1), with its on-board CAN transceiver, its split termination behind JP1, its SD slot and its debug USB-C port.
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md) at header J7; 5 V at USB-C J1; the bench PC at USB-C J11.
- **Allocated functions.** 101 F5, 401 F1, 501 F1, 503 F4.
- **Modes.** Off; booting; running.

## Requirements

### Nexus-Physical-02-01-R001

**Statement.** The FRDM board shall run from 5 V on USB-C port J1 without USB power delivery.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Physical-02-R001
- Allocated-to: -
- Phase: 1
- Verification: Test The board boots from the 5 V rail
- Realised-by: HW
- Decisions: HW-02

### Nexus-Physical-02-01-R002

**Statement.** The FRDM board shall present CAN_H and CAN_L of the on-board transceiver on pins 8 and 10 of header J7.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-02-01-R003

**Statement.** The FRDM board shall terminate the bus with jumper JP1 fitted.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R003
- Allocated-to: -
- Phase: 1
- Verification: Inspection JP1
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-02-01-R004

**Statement.** When powered up, the FRDM board shall boot from the SD card.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Physical-02-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: HW

### Nexus-Physical-02-01-R005

**Statement.** The FRDM board shall provide the UART console on USB-C port J11.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-02-R012
- Allocated-to: -
- Phase: 1
- Verification: Test A console session opens
- Realised-by: HW
- Decisions: MEC-05

### Nexus-Physical-02-01-R006

**Statement.** The boot switch SW1 of the FRDM board shall be set to 0011, which selects the SD card.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Physical-02-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection SW1[4:1] against the boot mode table of schematic SCH-95020 rev B
- Realised-by: HW
