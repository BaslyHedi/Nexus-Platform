# Nexus-Enabling - Enabling system: build, release and bench tools

Enabling system (ISO/IEC/IEEE 15288), level 0, beside the vehicle. Its requirements are not derived from the vehicle's: it serves the vehicle through its life cycle without being part of it. Written to [../system/method.md](../../system/method.md) and [rules.md](../rules.md).

- **Purpose and boundary.** The repositories and their CI, the release tags, the `kas` build of the Linux image, the CAN matrix as a released artifact, the configuration table below, and the bench PC with the USB-CAN adapter and the ST-LINK.
- **Interfaces.** The vehicle, at its diagnostic port and its debug ports; the software elements, which it builds and releases.
- **Allocated functions.** None of the vehicle's: it is outside the system boundary.
- **Modes.** None.


## Configuration table

Which repository implements each software element, and as which build target. This is configuration management, not
architecture: requirements are allocated to the elements, never to the repositories. Each repository cites the requirement
IDs of the elements it implements.

| Software element | Repository | Build target |
|---|---|---|
| [Nexus-Physical-01-04](../components/Nexus-Physical-01/Nexus-Physical-01-04.md) Bootloader | `Nexus-STM32-FBL` | the bootloader |
| [Nexus-Physical-01-05](../components/Nexus-Physical-01/Nexus-Physical-01-05.md) FBL-Updater | `Nexus-STM32-FBL` | the FBL-Updater |
| [Nexus-Physical-01-06](../components/Nexus-Physical-01/Nexus-Physical-01-06.md) Application | `Nexus-STM32-App` | the application |
| [Nexus-Physical-02-03](../components/Nexus-Physical-02/Nexus-Physical-02-03.md) Linux image | `Nexus-IMX91-Yocto` | the image |
| [Nexus-Physical-02-04](../components/Nexus-Physical-02/Nexus-Physical-02-04.md) Heartbeat program | its own repository, named when created | the program |
| [Nexus-Physical-02-05](../components/Nexus-Physical-02/Nexus-Physical-02-05.md) Flashing client | `Nexus-CAN-Utils` | the flashing client |
| [Nexus-Physical-02-06](../components/Nexus-Physical-02/Nexus-Physical-02-06.md) Test applications | one repository each, named when created | one program each |
| The CAN matrix, an interface definition and not an element | `Nexus-CAN-Utils` | the matrix release and its generated bindings |

## Requirements

### Nexus-Enabling-R001

**Statement.** Each repository shall have a README and a CLAUDE.md.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The repositories
- Realised-by: SYS

### Nexus-Enabling-R002

**Statement.** Each software element shall be implemented in the repository that the configuration table assigns to the software element.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The configuration table against the repositories
- Realised-by: SYS

### Nexus-Enabling-R003

**Statement.** Each repository shall cite the requirement IDs of each software element that the repository implements.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The software requirements of each repository
- Realised-by: SYS

### Nexus-Enabling-R004

**Statement.** Each repository shall cite the Nexus-Platform decision IDs that the repository implements.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The README of each repository
- Realised-by: SYS

### Nexus-Enabling-R005

**Statement.** The CI of each repository shall build each software element of the repository from a clean clone.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Inspection The CI runs
- Realised-by: SYS

### Nexus-Enabling-R006

**Statement.** Each repository shall release under a tag in the form vMAJOR.MINOR.PATCH.

- Need: T2.1
- Phase: 1
- Verification: Test T2.1
- Realised-by: SYS

### Nexus-Enabling-R007

**Statement.** The CI of each repository shall publish a release artifact for each tag.

- Need: T2.1
- Phase: 1
- Verification: Test T2.1
- Realised-by: SYS

### Nexus-Enabling-R008

**Statement.** The Linux image build shall run with kas from a clean clone.

- Need: T2.2
- Phase: 1
- Verification: Test T2.2
- Realised-by: SYS

### Nexus-Enabling-R009

**Statement.** The Linux image build shall fetch each application at the release tag of the application.

- Need: T2.2
- Phase: 1
- Verification: Test T2.2
- Realised-by: SYS

### Nexus-Enabling-R010

**Statement.** Each consumer of the CAN matrix shall build against a pinned Nexus-CAN-Utils tag.

- Need: Deliverable 1.2
- Phase: 1
- Verification: Inspection The build of each consumer
- Realised-by: SYS

### Nexus-Enabling-R011

**Statement.** The build of each consumer of the CAN matrix shall fail on a mismatch with the pinned tag.

- Need: Deliverable 1.7
- Phase: 1
- Verification: Demo A consumer built against a changed matrix fails
- Realised-by: SYS

### Nexus-Enabling-R012

**Statement.** The bench PC shall run the flashing client through the USB-CAN adapter.

- Need: T1.1
- Phase: 1
- Verification: Test T1.1
- Realised-by: SYS
- Decisions: SW-01, HW-18

### Nexus-Enabling-R013

**Statement.** The USB-CAN adapter shall have the termination of the adapter switched off.

- Need: T2.3
- Phase: 1
- Verification: Inspection The termination switch of the adapter
- Realised-by: SYS
- Decisions: HW-18

### Nexus-Enabling-R014

**Statement.** The cable from the USB-CAN adapter to the diagnostic port shall be 2 m long at most.

- Need: T2.3
- Phase: 1
- Verification: Inspection The cable length
- Realised-by: SYS
- Decisions: HW-18

### Nexus-Enabling-R015

**Statement.** The ST-LINK shall install the first bootloader.

- Need: T1.2
- Phase: 1
- Verification: Test T1.2
- Realised-by: SYS

### Nexus-Enabling-R016

**Statement.** The ST-LINK shall remain the recovery path of the bootloader.

- Need: T1.2
- Phase: 1
- Verification: Test T1.2
- Realised-by: SYS
