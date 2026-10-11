# Nexus-STM32-App - STM32 application (software item)

Software item, level 2, handed over to the repository `Nexus-STM32-App`. Written to [../system/method.md](../system/method.md).

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

**Statement.** The application shall show on an LED that it receives the FRDM node's heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R003
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-STM32-App-R003

**Statement.** The application shall be linked for the application region and started by the bootloader.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-App-R004

**Statement.** The application shall show its own LED pattern while it runs, written in the repository.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-App-R005

**Statement.** The application shall report its version in its node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
