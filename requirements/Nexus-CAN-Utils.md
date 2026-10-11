# Nexus-CAN-Utils - CAN matrix and flashing client (software item)

Software item, level 2, handed over to the repository `Nexus-CAN-Utils`. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The flashing client, which runs on the FRDM node and on the bench PC, and the CAN matrix with its generators, which the enabling system releases.
- **Interfaces.** Serves images to [Nexus-STM32-FBL](Nexus-STM32-FBL.md); carried by [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md).
- **Allocated functions.** From [Nexus-Physical-02](Nexus-Physical-02.md): 504 F1.
- **Modes.** None.

## Requirements

### Nexus-CAN-Utils-R001

**Statement.** When a node requests an image, the flashing client shall serve the image as a Cyphal file server.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-CAN-Utils-R002

**Statement.** The flashing client shall run on Linux.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-CAN-Utils-R003

**Statement.** The flashing client shall log each download with the image version and the result.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
