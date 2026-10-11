# Nexus-STM32-App - STM32 minimal application (repository)

Component, level 3. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The Zephyr application the FBL loads: LED pattern, Cyphal heartbeat, shows what it hears.
- **Interfaces.** Loaded by [Nexus-STM32-FBL](Nexus-STM32-FBL.md); consumes a [Nexus-CAN-Utils](Nexus-CAN-Utils.md) release.
- **Allocated functions.** From the STM32 node: heartbeat out and in, LED pattern, version.
- **Modes.** Running.

## Requirements

### Nexus-STM32-App-R001

**Statement.** The app shall publish a Cyphal heartbeat at the rate set in the CAN matrix.

- Derived-from: Nexus-Phys-STM32-R002
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW
- Decisions: SW-01

### Nexus-STM32-App-R002

**Statement.** The app shall show on an LED that it receives the FRDM's heartbeat.

- Derived-from: Nexus-Phys-STM32-R003
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-STM32-App-R003

**Statement.** The app shall show its own LED pattern while it runs.

- Derived-from: Nexus-Phys-STM32-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-App-R004

**Statement.** The app shall report its version in its node info.

- Derived-from: Nexus-Phys-STM32-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-App-R005

**Statement.** The app shall be linked for the application region and be started by the FBL.

- Derived-from: Nexus-Phys-STM32-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-STM32-App-R006

**Statement.** The app repository shall build in CI from a clean clone and cite decision IDs back to Nexus-Platform.

- Derived-from: Nexus-Phys-STM32-R014
- Allocated-to: -
- Phase: 1
- Verification: Inspection The CI run
- Realised-by: SW
