# Nexus-STM32-FBL - STM32 flash bootloader (software item)

Software item, level 2, handed over to the repository `Nexus-STM32-FBL`, which derives its own software requirements from these. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The resident bootloader, bare-metal and small by design ([phases.md](../system/phases.md)), and its FBL-Updater target. Unsigned and unencrypted in Phase 1.
- **Interfaces.** The bus through the node's transceiver; [Nexus-STM32-App](Nexus-STM32-App.md) through the memory map; the CAN matrix by a pinned tag.
- **Allocated functions.** From [Nexus-Physical-01](Nexus-Physical-01.md): 503 F4, 504 F1 to F3.
- **Modes.** Idle; receiving; FBL-Updater running.

## Requirements

### Nexus-STM32-FBL-R001

**Statement.** On a software-update request, the bootloader shall pull the image from the requesting host by Cyphal file transfer.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-STM32-FBL-R002

**Statement.** The bootloader shall erase and program the application region with the received image and then jump to it.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R003

**Statement.** The bootloader shall compute the CRC of the received image and start it only if it matches.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Physical-01-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R004

**Statement.** A failed or interrupted download, or an absent or broken image, shall leave the bootloader running and reachable.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Physical-01-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R005

**Statement.** The bootloader region and the application region shall be fixed in a memory map written in the repository.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection The memory map is in the repository
- Realised-by: SW

### Nexus-STM32-FBL-R006

**Statement.** The repository shall build an FBL-Updater target: an image the bootloader downloads and starts like an application, which rewrites the bootloader region with a new bootloader and verifies it.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-STM32-FBL-R007

**Statement.** The bootloader shall show one LED pattern while idle and another while receiving, and the FBL-Updater one of its own, all written in the repository.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R008
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-FBL-R008

**Statement.** The bootloader and the FBL-Updater shall each report their version in their node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1 and T1.2
- Realised-by: SW
