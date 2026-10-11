# Nexus-STM32-App - STM32 application (software item)

Software item, level 2, handed over to the repository `Nexus-STM32-App`. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The minimal Zephyr application the bootloader loads.
- **Interfaces.** Loaded by [Nexus-STM32-FBL](Nexus-STM32-FBL.md); the CAN matrix by a pinned tag.
- **Allocated functions.** From [Nexus-Physical-01](Nexus-Physical-01.md): 401 F1, 503 F4, 504 F1.
- **Modes.** Running.

## Requirements

### Nexus-STM32-App-R001

**Statement.** The application shall publish a Cyphal heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-STM32-App-R002

**Statement.** When the application receives a heartbeat from the FRDM node, the application shall indicate the reception on an LED.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R003
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-STM32-App-R003

**Statement.** The application shall be linked for the application region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-App-R004

**Statement.** While running, the application shall show the application pattern that the repository defines.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-App-R005

**Statement.** When asked over the bus, the application shall report the application version in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
