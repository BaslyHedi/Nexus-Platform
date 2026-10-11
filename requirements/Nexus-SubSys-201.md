# Nexus-SubSys-201 - Propulsion

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-201-F01` Produce drive torque, rear wheels
  - `Nexus-SubSys-201-F02` Track wheel-speed setpoints
  - `Nexus-SubSys-201-F03` Measure wheel speed (encoders)

  *Phase 1 scope.* Phase 1 is hardware only: the motors and driver fitted and powered, not driven. F01 carries the Phase 1 form. F02 and F03 are Phase 2.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-201-R001

**Statement.** The sub-system shall be fitted at the rear axle and supplied with drive power, ready to be commanded.

- Function: Nexus-SubSys-201-F01
- Derived-from: Nexus-Vehicle-R006
- Allocated-to: Nexus-Phys-DRV, Nexus-Phys-PWR (as-is), Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-DRV-R001 and Nexus-Phys-STM32-R010

### Nexus-SubSys-201-R002

**Statement.** The sub-system shall not move the vehicle until it is commanded.

- Function: Nexus-SubSys-201-F01
- Derived-from: Nexus-Vehicle-R006
- Allocated-to: Nexus-Phys-DRV (as-is)
- Phase: 1
- Verification: Demo SW1 on with no command sent: the wheels do not turn
- Realised-by: HW
