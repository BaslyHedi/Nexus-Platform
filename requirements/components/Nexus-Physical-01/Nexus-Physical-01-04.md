# Nexus-Physical-01-04 - Bootloader

Software element, level 2, handed over: the repository in the [configuration table](../../system/Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** The resident flash bootloader: bare-metal and small by design ([phases.md](../../../system/phases.md)), unsigned and unencrypted in Phase 1.
- **Interfaces.** The bus through CAN1; the application [01-06](Nexus-Physical-01-06.md) and the FBL-Updater [01-05](Nexus-Physical-01-05.md) through the memory map; the CAN matrix by a pinned tag.
- **Allocated functions.** 503 F4, 504 F1 to F3.
- **Modes.** Idle; receiving.

## Requirements

### Nexus-Physical-01-04-R001

**Statement.** The bootloader shall operate CAN1 at the bit rate of the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-Physical-01-04-R002

**Statement.** When a software-update request arrives, the bootloader shall pull the image from the requesting host by Cyphal file transfer.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-Physical-01-04-R003

**Statement.** When the image is received, the bootloader shall erase and program the application region with the image.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-01-04-R004

**Statement.** When the application region is programmed, the bootloader shall compute the CRC of the programmed image.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Physical-01-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-01-04-R005

**Statement.** When the CRC of the programmed image matches, the bootloader shall jump to the application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-01-04-R006

**Statement.** If a download is interrupted, then the bootloader shall remain reachable over the bus.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Physical-01-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-01-04-R007

**Statement.** If the application region holds no valid image, then the bootloader shall remain reachable over the bus.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Physical-01-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-01-04-R008

**Statement.** The bootloader shall reside in the bootloader region of the memory map of the node.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R011
- Allocated-to: -
- Phase: 1
- Verification: Inspection The memory map
- Realised-by: SW

### Nexus-Physical-01-04-R009

**Statement.** The bootloader shall download and start the FBL-Updater as an application image.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-Physical-01-04-R010

**Statement.** While idle, the bootloader shall show the idle pattern on the four LEDs.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-Physical-01-04-R011

**Statement.** While receiving an image, the bootloader shall show the receiving pattern on the four LEDs.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-Physical-01-04-R012

**Statement.** When asked over the bus, the bootloader shall report the bootloader version in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R014
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
