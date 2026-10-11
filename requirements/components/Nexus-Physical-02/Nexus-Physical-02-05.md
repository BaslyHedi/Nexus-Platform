# Nexus-Physical-02-05 - Flashing client

Software element, level 2, handed over: the repository in the [configuration table](../../system/Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** The Cyphal file server that offers images to the bootloader (SW-01). The same program runs on the bench PC, as part of the enabling system.
- **Interfaces.** The bus through SocketCAN; the bootloader [01-04](../Nexus-Physical-01/Nexus-Physical-01-04.md) at the far end.
- **Allocated functions.** 503 F4, 504 F1.
- **Modes.** Idle; serving.

## Requirements

### Nexus-Physical-02-05-R001

**Statement.** When a node requests an image, the flashing client shall serve the image as a Cyphal file server.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
- Decisions: SW-01

### Nexus-Physical-02-05-R002

**Statement.** The flashing client shall run on Linux.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-02-05-R003

**Statement.** The flashing client shall log each download with the image version and the result.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-Physical-02-05-R004

**Statement.** When asked on the console, the flashing client shall print the name and the version of the flashing client.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-02-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW
