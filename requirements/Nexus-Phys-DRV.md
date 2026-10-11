# Nexus-Phys-DRV - Drive train: motors, driver and steering

Physical, level 2. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The two rear encoder gear motors, the Encoder Motor Module (the driver) on plate 1, and the LD-1501MG steering servo with the Ackermann linkage.
- **Interfaces.** Supplied by [Nexus-Phys-PWR](Nexus-Phys-PWR.md); commanded later by [Nexus-Phys-STM32](Nexus-Phys-STM32.md) over I2C (PB10, PB11) and PWM (PE9); carried by [Nexus-Phys-CHS](Nexus-Phys-CHS.md). Nothing is commanded in Phase 1.
- **Allocated functions.** 201 F01; 202 F01.
- **Modes.** Unpowered; powered and idle (Phase 1).

## Requirements

### Nexus-Phys-DRV-R001

**Statement.** Two encoder gear motors shall drive the rear wheels from the Encoder Motor Module on plate 1.

- Derived-from: Nexus-SubSys-201-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection Both motors and the module are fitted and wired
- Realised-by: HW

### Nexus-Phys-DRV-R002

**Statement.** The LD-1501MG servo on the front axle shall steer the front wheels through the Ackermann linkage.

- Derived-from: Nexus-SubSys-202-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The servo is fitted and the linkage moves freely by hand
- Realised-by: HW
