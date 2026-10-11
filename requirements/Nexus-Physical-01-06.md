# Nexus-Physical-01-06 - Application

Software element, level 2, handed over: the repository in the [configuration table](Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The minimal Zephyr application the bootloader loads: LED pattern, Cyphal heartbeat, shows what it hears.
- **Interfaces.** Started by the bootloader [01-04](Nexus-Physical-01-04.md); the bus through CAN1; the CAN matrix by a pinned tag.
- **Allocated functions.** 401 F1, 503 F4, 504 F1.
- **Modes.** Running.

## Requirements

### Nexus-Physical-01-06-R001

**Statement.** The application shall operate CAN1 at the bit rate of the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-Physical-01-06-R002

**Statement.** The application shall publish a Cyphal heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-Physical-01-06-R003

**Statement.** When the application receives a heartbeat from the FRDM node, the application shall indicate the reception on an LED.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-Physical-01-06-R004

**Statement.** The application shall be linked for the application region of the memory map of the node.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R008, Nexus-Physical-01-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-01-06-R005

**Statement.** While running, the application shall show the application pattern on the four LEDs.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-Physical-01-06-R006

**Statement.** When asked over the bus, the application shall report the application version in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R014
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
