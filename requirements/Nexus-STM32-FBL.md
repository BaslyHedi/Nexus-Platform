# Nexus-STM32-FBL - STM32 flash bootloader (software item)

Software item, level 2, handed over to the repository `Nexus-STM32-FBL`, which derives its own software requirements from these. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The resident bootloader, bare-metal and small by design ([phases.md](../system/phases.md)), and its FBL-Updater target. Unsigned and unencrypted in Phase 1.
- **Interfaces.** The bus through the node's transceiver; [Nexus-STM32-App](Nexus-STM32-App.md) through the memory map; the CAN matrix by a pinned tag.
- **Allocated functions.** From [Nexus-Physical-01](Nexus-Physical-01.md): 503 F4, 504 F1 to F3.
- **Modes.** Idle; receiving; FBL-Updater running.

## Requirements

### Nexus-STM32-FBL-R001

**Statement.** When a software-update request arrives, the bootloader shall pull the image from the requesting host by Cyphal file transfer.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-STM32-FBL-R002

**Statement.** When the image is received, the bootloader shall erase and program the application region with the image.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R003

**Statement.** When the application region is programmed, the bootloader shall compute the CRC of the programmed image.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Physical-01-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R004

**Statement.** When the CRC of the programmed image matches, the bootloader shall jump to the application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R005

**Statement.** If a download is interrupted, then the bootloader shall remain reachable over the bus.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Physical-01-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R006

**Statement.** If the application region holds no valid image, then the bootloader shall remain reachable over the bus.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Physical-01-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R007

**Statement.** The bootloader shall reside in the bootloader region that the memory map of the repository fixes.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R009
- Allocated-to: -
- Phase: 1
- Verification: Inspection The memory map in the repository
- Realised-by: SW

### Nexus-STM32-FBL-R008

**Statement.** The FBL-Updater target shall be an image that the bootloader downloads and starts as an application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-STM32-FBL-R009

**Statement.** The FBL-Updater target shall rewrite the bootloader region with a new bootloader.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-STM32-FBL-R010

**Statement.** The FBL-Updater target shall verify the rewritten bootloader region.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Physical-01-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-STM32-FBL-R011

**Statement.** While idle, the bootloader shall show the idle pattern that the repository defines.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-FBL-R012

**Statement.** While receiving an image, the bootloader shall show the receiving pattern that the repository defines.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-FBL-R013

**Statement.** While the FBL-Updater runs, the FBL-Updater shall show the FBL-Updater pattern that the repository defines.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-FBL-R014

**Statement.** When asked over the bus, the bootloader shall report the bootloader version in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R015

**Statement.** When asked over the bus, the FBL-Updater shall report the FBL-Updater version in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW
