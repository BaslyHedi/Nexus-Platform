# Nexus-Physical-01-05 - FBL-Updater

Software element, level 2, handed over: the repository in the [configuration table](Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** An image whose only job is to rewrite the bootloader region, since a bootloader cannot overwrite itself while it runs.
- **Interfaces.** Started by the bootloader [01-04](Nexus-Physical-01-04.md) like an application.
- **Allocated functions.** 503 F4, 504 F1 and F2.
- **Modes.** Running.

## Requirements

### Nexus-Physical-01-05-R001

**Statement.** The FBL-Updater shall be an image for the application region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-Physical-01-05-R002

**Statement.** The FBL-Updater shall rewrite the bootloader region with a new bootloader.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-Physical-01-05-R003

**Statement.** The FBL-Updater shall verify the rewritten bootloader region.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Physical-01-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-Physical-01-05-R004

**Statement.** While running, the FBL-Updater shall show the FBL-Updater pattern on the four LEDs.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R013
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-Physical-01-05-R005

**Statement.** When asked over the bus, the FBL-Updater shall report the FBL-Updater version in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-01-R014
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW
