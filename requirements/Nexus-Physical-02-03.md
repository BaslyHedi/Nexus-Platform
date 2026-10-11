# Nexus-Physical-02-03 - Linux image

Software element, level 2, handed over: the repository in the [configuration table](Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The bootable image: BSP, kernel and device tree, root file system, and the released applications it carries.
- **Interfaces.** The FRDM board [02-01](Nexus-Physical-02-01.md); the applications [02-04](Nexus-Physical-02-04.md), [02-05](Nexus-Physical-02-05.md), [02-06](Nexus-Physical-02-06.md) by release tag.
- **Allocated functions.** 401 F1, 501 F1, 503 F3, 504 F1.
- **Modes.** Booting; running.

## Requirements

### Nexus-Physical-02-03-R001

**Statement.** The Linux image shall bring up the CAN interface at the bit rate of the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-02-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-Physical-02-03-R002

**Statement.** When the FRDM board powers up, the Linux image shall boot to a login prompt.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Physical-02-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-Physical-02-03-R003

**Statement.** The Linux image shall carry each released application at the release tag of the application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-Physical-02-03-R004

**Statement.** The Linux image shall include SocketCAN support for the FlexCAN controller.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Physical-02-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-Physical-02-03-R005

**Statement.** The Linux image shall include the candump tool.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Physical-02-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-Physical-02-03-R006

**Statement.** The Linux image shall include the flashing client of a tagged Nexus-CAN-Utils release.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
