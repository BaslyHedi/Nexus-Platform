# Nexus-Enabling - Enabling system: build, release and bench tools

Enabling system (ISO/IEC/IEEE 15288), level 0, beside the vehicle. Its requirements are not derived from the vehicle's: it serves the vehicle through its life cycle without being part of it. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The repositories and their CI, the release tags, the `kas` build of the Linux image, the CAN matrix as a released artifact, and the bench PC with the USB-CAN adapter and the ST-LINK.
- **Interfaces.** The vehicle, at its diagnostic port and its debug ports; the software items, which it builds and releases.
- **Allocated functions.** None of the vehicle's: it is outside the system boundary.
- **Modes.** None.

## Requirements

### Nexus-Enabling-R001

**Statement.** Every software item shall have its own repository, with a README, a CLAUDE.md and CI that builds it from a clean clone, citing decision IDs back to Nexus-Platform.

- Phase: 1
- Verification: Inspection The repositories and their CI runs (deliverable 1.7)
- Realised-by: SYS

### Nexus-Enabling-R002

**Statement.** Every software item shall be released under a tag vMAJOR.MINOR.PATCH with a release artifact built by its CI.

- Phase: 1
- Verification: Test T2.1
- Realised-by: SYS

### Nexus-Enabling-R003

**Statement.** The Linux image shall be built with kas from a clean clone, fetching each application at its release tag.

- Phase: 1
- Verification: Test T2.2
- Realised-by: SYS

### Nexus-Enabling-R004

**Statement.** Every consumer of the CAN matrix shall build against a pinned Nexus-CAN-Utils tag and its generated bindings, so that a mismatch is a build error.

- Phase: 1
- Verification: Inspection Each consumer's build pins a tag (deliverables 1.2, 1.7)
- Realised-by: SYS

### Nexus-Enabling-R005

**Statement.** A Linux PC with the USB-CAN adapter shall run the Nexus-CAN-Utils flashing client against the vehicle's diagnostic port.

- Phase: 1
- Verification: Test T1.1
- Realised-by: SYS
- Decisions: SW-01, HW-18

### Nexus-Enabling-R006

**Statement.** The USB-CAN adapter shall be used with its own termination off and a cable of 2 m or less.

- Phase: 1
- Verification: Inspection The adapter's termination switch is off
- Realised-by: SYS
- Decisions: HW-18

### Nexus-Enabling-R007

**Statement.** The ST-LINK shall install the first flash bootloader and remain its recovery path.

- Phase: 1
- Verification: Test T1.2
- Realised-by: SYS
