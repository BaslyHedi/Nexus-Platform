# Nexus-STM32-FBL-Updater - STM32 FBL-Updater (repository, proposed)

Component, level 3. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** An image whose only job is to rewrite the FBL's own flash region, since a bootloader cannot overwrite itself while running. **The 1.7 repository table does not list it and its toolchain is undecided**, so the code is proposed.
- **Interfaces.** Downloaded and started by [Nexus-STM32-FBL](Nexus-STM32-FBL.md) like an app; shares its memory map.
- **Allocated functions.** From the STM32 node: rewrite the FBL region, one LED pattern.
- **Modes.** Running.

## Requirements

### Nexus-STM32-FBL-Updater-R001

**Statement.** The updater shall rewrite the FBL region with a new FBL image and verify it.

- Derived-from: Nexus-Phys-STM32-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-STM32-FBL-Updater-R002

**Statement.** The updater shall show its own LED pattern while it runs.

- Derived-from: Nexus-Phys-STM32-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T1.3
- Realised-by: SW

### Nexus-STM32-FBL-Updater-R003

**Statement.** The updater shall be built to the application image format, so the FBL accepts it without a special case.

- Derived-from: Nexus-Phys-STM32-R013
- Allocated-to: -
- Phase: 1
- Verification: Test T1.2
- Realised-by: SW

### Nexus-STM32-FBL-Updater-R004

**Statement.** The updater repository shall build in CI from a clean clone and cite decision IDs back to Nexus-Platform.

- Derived-from: Nexus-Phys-STM32-R014
- Allocated-to: -
- Phase: 1
- Verification: Inspection The CI run
- Realised-by: SW
