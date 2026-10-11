# Nexus-Enabling - Enabling system: build, release and bench tools

Enabling system (ISO/IEC/IEEE 15288), level 0, beside the vehicle. Its requirements are not derived from the vehicle's: it serves the vehicle through its life cycle without being part of it. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The repositories and their CI, the release tags, the `kas` build of the Linux image, the CAN matrix as a released artifact, and the bench PC with the USB-CAN adapter and the ST-LINK.
- **Interfaces.** The vehicle, at its diagnostic port and its debug ports; the software items, which it builds and releases.
- **Allocated functions.** None of the vehicle's: it is outside the system boundary.
- **Modes.** None.

## Requirements

### Nexus-Enabling-R001

**Statement.** Each software item shall have a repository of the software item's own, with a README and a CLAUDE.md.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The repositories
- Realised-by: SYS

### Nexus-Enabling-R002

**Statement.** The CI of each repository shall build the software item from a clean clone.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The CI runs
- Realised-by: SYS

### Nexus-Enabling-R003

**Statement.** Each repository shall cite the Nexus-Platform decision IDs that the software item implements.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The README of each repository
- Realised-by: SYS

### Nexus-Enabling-R004

**Statement.** Each software item shall be released under a tag in the form vMAJOR.MINOR.PATCH.

- Need: T2.1
- Phase: 1
- Verification: Test T2.1
- Realised-by: SYS

### Nexus-Enabling-R005

**Statement.** The CI of each repository shall publish a release artifact for each tag.

- Need: T2.1
- Phase: 1
- Verification: Test T2.1
- Realised-by: SYS

### Nexus-Enabling-R006

**Statement.** The Linux image build shall run with kas from a clean clone.

- Need: T2.2
- Phase: 1
- Verification: Test T2.2
- Realised-by: SYS

### Nexus-Enabling-R007

**Statement.** The Linux image build shall fetch each application at the application's release tag.

- Need: T2.2
- Phase: 1
- Verification: Test T2.2
- Realised-by: SYS

### Nexus-Enabling-R008

**Statement.** Each consumer of the CAN matrix shall build against a pinned Nexus-CAN-Utils tag.

- Need: Deliverable 1.2
- Phase: 1
- Verification: Inspection The build of each consumer
- Realised-by: SYS

### Nexus-Enabling-R009

**Statement.** The build of each consumer of the CAN matrix shall fail on a mismatch with the pinned tag.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Demo A consumer built against a changed matrix fails
- Realised-by: SYS

### Nexus-Enabling-R010

**Statement.** The bench PC shall run the Nexus-CAN-Utils flashing client through the USB-CAN adapter.

- Need: T1.1
- Phase: 1
- Verification: Test T1.1
- Realised-by: SYS
- Decisions: SW-01, HW-18

### Nexus-Enabling-R011

**Statement.** The USB-CAN adapter shall have the adapter's own termination switched off.

- Need: T2.3
- Phase: 1
- Verification: Inspection The termination switch of the adapter
- Realised-by: SYS
- Decisions: HW-18

### Nexus-Enabling-R012

**Statement.** The cable from the USB-CAN adapter to the diagnostic port shall be 2 m long at most.

- Need: T2.3
- Phase: 1
- Verification: Inspection The cable length
- Realised-by: SYS
- Decisions: HW-18

### Nexus-Enabling-R013

**Statement.** The ST-LINK shall install the first flash bootloader.

- Need: T1.2
- Phase: 1
- Verification: Test T1.2
- Realised-by: SYS

### Nexus-Enabling-R014

**Statement.** The ST-LINK shall remain the recovery path of the flash bootloader.

- Need: T1.2
- Phase: 1
- Verification: Test T1.2
- Realised-by: SYS
