# Nexus-Linux-Apps - Linux applications (software items)

Software items, level 2. **A class**: each application is its own repository, `Nexus-<AppName>`, named when it is made, and gets its own file here then. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** Phase 1 has the heartbeat program and two throwaway applications that print their name and version.
- **Interfaces.** Carried by [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md) at their release tags; the CAN matrix by a pinned tag.
- **Allocated functions.** From [Nexus-Physical-02](Nexus-Physical-02.md): 401 F1, 503 F4.
- **Modes.** Running.

## Requirements

### Nexus-Linux-Apps-R001

**Statement.** The heartbeat program shall publish a Cyphal heartbeat at the rate set in the CAN matrix and log each heartbeat it receives from the STM32 node.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-Linux-Apps-R002

**Statement.** Each application shall print its own name and version.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-02-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW
