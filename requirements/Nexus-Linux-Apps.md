# Nexus-Linux-Apps - Linux applications (software items)

Software items, level 2. **A class**: each application is its own repository, `Nexus-<AppName>`, named when it is made, and gets its own file here then. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** Phase 1 has the heartbeat program and two throwaway applications that print their name and version.
- **Interfaces.** Carried by [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md) at their release tags; the CAN matrix by a pinned tag.
- **Allocated functions.** From [Nexus-Physical-02](Nexus-Physical-02.md): 401 F1, 503 F4.
- **Modes.** Running.

## Requirements

### Nexus-Linux-Apps-R001

**Statement.** The heartbeat program shall publish a Cyphal heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R003
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-Linux-Apps-R002

**Statement.** When the heartbeat program receives a heartbeat from the STM32 node, the heartbeat program shall log the heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-Linux-Apps-R003

**Statement.** When started, each application shall print the name and the version of the application.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-02-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW
