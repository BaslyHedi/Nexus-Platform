# Nexus-Linux-App - Linux applications (one repository each)

Component, level 3. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** **A class, not one repository.** Each Linux application has its own repository, CI, versioning and releases, named `Nexus-<AppName>` when it is made. Phase 1 has two throwaway name-printing apps and the heartbeat program. Each real repository gets its own entry here when it is created.
- **Interfaces.** Released to [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md) by tag; the heartbeat program consumes a [Nexus-CAN-Utils](Nexus-CAN-Utils.md) release.
- **Allocated functions.** From the FRDM node: the heartbeat program, the name-printing apps, their CI.
- **Modes.** Running.

## Requirements

### Nexus-Linux-App-R001

**Statement.** The heartbeat program shall publish a Cyphal heartbeat at the matrix rate and report each heartbeat it receives from the STM32.

- Derived-from: Nexus-Phys-FRDM-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-Linux-App-R002

**Statement.** Each application shall print its own name and version.

- Derived-from: Nexus-Phys-FRDM-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW

### Nexus-Linux-App-R003

**Statement.** Each application repository shall have CI that cross-builds it for the i.MX 91 on every push and publishes a release artifact on a tag.

- Derived-from: Nexus-Phys-FRDM-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW
