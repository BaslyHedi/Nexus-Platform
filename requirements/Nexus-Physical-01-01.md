# Nexus-Physical-01-01 - Discovery board

Hardware element, level 2, bought: its requirements state what the node relies on, checked against the vendor documentation; the recursion stops here. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The STM32F4DISCOVERY, board revision MB997B (BOM 1.2): the STM32F407, the on-board ST-LINK V2 and four user LEDs.
- **Interfaces.** The carrier [01-02](Nexus-Physical-01-02.md) through headers P1 and P2; the bench PC through the ST-LINK USB port.
- **Allocated functions.** 401 F1, 503 F4, 504 F1 and the prepared pins of 201 F1 and 202 F1.
- **Modes.** None of its own.

## Requirements

### Nexus-Physical-01-01-R001

**Statement.** The Discovery board shall run from 5 V applied to pins 3 and 4 of header P2.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Physical-01-R001
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM1472 Table 5 and the P2 schematic
- Realised-by: HW
- Decisions: HW-19

### Nexus-Physical-01-01-R002

**Statement.** The Discovery board shall leave PD0 and PD1 free for CAN1.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM1472 pin assignment
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-01-01-R003

**Statement.** The flash of the STM32F407 shall allow the bootloader sectors to be erased apart from the application sectors.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R011, Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Analysis The sector layout in the reference manual against the memory map
- Realised-by: HW

### Nexus-Physical-01-01-R004

**Statement.** The Discovery board shall provide four user LEDs driven by the STM32F407.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Inspection The four user LEDs
- Realised-by: HW

### Nexus-Physical-01-01-R005

**Statement.** The Discovery board shall provide SWD to the STM32F407 through the on-board ST-LINK V2 over USB.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R015
- Allocated-to: -
- Phase: 1
- Verification: Test A debug session opens through the ST-LINK
- Realised-by: HW

### Nexus-Physical-01-01-R006

**Statement.** The Discovery board shall leave PB10 and PB11 free for I2C2.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Physical-01-R016
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM1472 pin assignment
- Realised-by: HW
- Decisions: HW-10

### Nexus-Physical-01-01-R007

**Statement.** The Discovery board shall leave PE9 free for channel 1 of TIM1.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Physical-01-R017
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM1472 pin assignment
- Realised-by: HW
- Decisions: HW-21
