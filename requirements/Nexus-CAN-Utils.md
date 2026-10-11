# Nexus-CAN-Utils - CAN matrix, generators and flashing client (repository)

Component, level 3. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The CAN matrix (bit rate, IDs, Cyphal data types and subject and service IDs), its generators, and the Cyphal flashing client, which runs on Linux so it works from the PC adapter now and from the i.MX 91 later ([SW-01](../decisions/SW-Software-Decisions.md)).
- **Interfaces.** Consumed, by tag, by the FBL, the app, the Linux apps and the Yocto image; the flashing client serves images to [Nexus-STM32-FBL](Nexus-STM32-FBL.md).
- **Allocated functions.** From the bus: the matrix and its release. From the FRDM node: the flashing client.
- **Modes.** None.

## Requirements

### Nexus-CAN-Utils-R001

**Statement.** The repository shall hold the CAN matrix: bit rate, node IDs, and the subjects and services for update, heartbeat and node info, as Cyphal data types.

- Derived-from: Nexus-Phys-CAN-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection The matrix is in the repository
- Realised-by: SW
- Decisions: SW-01

### Nexus-CAN-Utils-R002

**Statement.** Each matrix change shall be released under a tag vMAJOR.MINOR.PATCH.

- Derived-from: Nexus-Phys-CAN-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection The tag exists (deliverable 1.2)
- Realised-by: SW

### Nexus-CAN-Utils-R003

**Statement.** The repository shall generate C and Linux bindings from the matrix, so that no consumer copies a message definition by hand.

- Derived-from: Nexus-Phys-CAN-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection A consumer builds against a pinned tag
- Realised-by: SW

### Nexus-CAN-Utils-R004

**Statement.** The flashing client shall serve an image as a Cyphal file server to a node that requests it, and shall run on Linux.

- Derived-from: Nexus-Phys-FRDM-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-CAN-Utils-R005

**Statement.** The flashing client shall log each download with the image version and the result.

- Derived-from: Nexus-Phys-FRDM-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-CAN-Utils-R006

**Statement.** The repository shall build in CI from a clean clone and cite decision IDs back to Nexus-Platform.

- Derived-from: Nexus-Phys-CAN-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection The CI run
- Realised-by: SW
