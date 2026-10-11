# Nexus-STM32-FBL - STM32 flash bootloader (repository)

Component, level 3. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The resident bootloader: **bare-metal and small by design** (decided, [phases.md](../system/phases.md)), unsigned and unencrypted in Phase 1.
- **Interfaces.** Speaks Cyphal over [Nexus-Phys-CAN](Nexus-Phys-CAN.md); consumes a [Nexus-CAN-Utils](Nexus-CAN-Utils.md) release; its memory map is shared with [Nexus-STM32-App](Nexus-STM32-App.md) and [Nexus-STM32-FBL-Updater](Nexus-STM32-FBL-Updater.md).
- **Allocated functions.** From the STM32 node: receive, verify, jump, stay reachable, report version, two LED patterns.
- **Modes.** Idle; receiving.

## Requirements

### Nexus-STM32-FBL-R001

**Statement.** On a software-update request, the FBL shall pull the image from the host by Cyphal file transfer.

- Derived-from: Nexus-Phys-STM32-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-STM32-FBL-R002

**Statement.** The FBL shall erase and program the application region with the received image and then jump to it.

- Derived-from: Nexus-Phys-STM32-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R003

**Statement.** The FBL region and the application region shall be fixed in a memory map written in the FBL repository.

- Derived-from: Nexus-Phys-STM32-R005
- Allocated-to: -
- Phase: 1
- Verification: Inspection The memory map is in the repository
- Realised-by: SW

### Nexus-STM32-FBL-R004

**Statement.** The FBL shall compute the CRC of the received image and start it only if it matches.

- Derived-from: Nexus-Phys-STM32-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R005

**Statement.** A failed or interrupted download, or an absent or broken image, shall leave the FBL running and reachable.

- Derived-from: Nexus-Phys-STM32-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R006

**Statement.** The FBL shall show one LED pattern while idle and another while receiving, both written in its repository.

- Derived-from: Nexus-Phys-STM32-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-FBL-R007

**Statement.** The FBL shall report its version in its node info.

- Derived-from: Nexus-Phys-STM32-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-FBL-R008

**Statement.** The FBL repository shall build in CI from a clean clone and cite decision IDs back to Nexus-Platform.

- Derived-from: Nexus-Phys-STM32-R014
- Allocated-to: -
- Phase: 1
- Verification: Inspection The CI run
- Realised-by: SW
