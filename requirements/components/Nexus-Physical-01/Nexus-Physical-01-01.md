# Nexus-Physical-01-01 - MCU board

Hardware element, level 2, bought: its requirements state what the node relies on, checked against the vendor documentation; the recursion stops here. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** The NUCLEO-H533RE, board MB1814 (BOM 1.2, HW-22): the STM32H533, the on-board STLINK-V3EC and the user LED LD2. It replaced the STM32F4DISCOVERY on 2026-10-25.
- **Interfaces.** The carrier [01-02](Nexus-Physical-01-02.md) through the ST morpho headers CN10 and CN7; the bench PC through the ST-LINK's USB-C port CN1.
- **Allocated functions.** 401 F1, 503 F4, 504 F1 and the prepared pins of 201 F1 and 202 F1.
- **Modes.** None of its own.

## Requirements

### Nexus-Physical-01-01-R001

**Statement.** The MCU board shall run from 5 V applied to E5V, CN7 pin 6, with JP5 on [5-6].

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Physical-01-R001
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM3121 Table 8
- Realised-by: HW
- Decisions: HW-19, HW-22

### Nexus-Physical-01-01-R002

**Statement.** The MCU board shall leave PB12 and PB13 free for FDCAN2.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM3121 Table 17 and the MB1814 schematic
- Realised-by: HW
- Decisions: HW-09, HW-22

### Nexus-Physical-01-01-R003

**Statement.** The flash of the STM32H533 shall allow the bootloader sectors to be erased apart from the application sectors.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R011, Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Analysis The sector layout in the reference manual against the memory map
- Realised-by: HW

### Nexus-Physical-01-01-R004

**Statement.** The MCU board shall provide a user LED driven by the STM32H533.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Inspection LD2, on PA5
- Realised-by: HW

### Nexus-Physical-01-01-R005

**Statement.** The MCU board shall provide SWD to the STM32H533 through the on-board STLINK-V3EC over USB.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R015
- Allocated-to: -
- Phase: 1
- Verification: Test A debug session opens through the ST-LINK
- Realised-by: HW

### Nexus-Physical-01-01-R006

**Statement.** The MCU board shall leave PB6 and PB7 free for I2C1.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Physical-01-R016
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM3121 Table 17 and the MB1814 schematic
- Realised-by: HW
- Decisions: HW-10, HW-22

### Nexus-Physical-01-01-R007

**Statement.** The MCU board shall leave PC2 free for channel 4 of TIM4.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Physical-01-R017
- Allocated-to: -
- Phase: 1
- Verification: Analysis UM3121 Table 17 and the MB1814 schematic
- Realised-by: HW
- Decisions: HW-21, HW-22
