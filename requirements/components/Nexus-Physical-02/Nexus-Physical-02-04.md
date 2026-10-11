# Nexus-Physical-02-04 - Heartbeat program

Software element, level 2, handed over: the repository in the [configuration table](../../system/Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** The Linux program that publishes the FRDM node's heartbeat and logs the STM32 node's.
- **Interfaces.** The bus through SocketCAN; the CAN matrix by a pinned tag.
- **Allocated functions.** 401 F1, 503 F4.
- **Modes.** Running.

## Requirements

### Nexus-Physical-02-04-R001

**Statement.** The heartbeat program shall publish a Cyphal heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-Physical-02-04-R002

**Statement.** When the heartbeat program receives a heartbeat from the STM32 node, the heartbeat program shall log the heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-Physical-02-04-R003

**Statement.** When asked on the console, the heartbeat program shall print the name and the version of the heartbeat program.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-02-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW
