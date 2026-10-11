# Nexus-SubSys-202 - Steering

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-202-F01` Set front wheel angle (Ackermann)
  - `Nexus-SubSys-202-F02` Enforce steer angle & rate limits
  - `Nexus-SubSys-202-F03` Report steering state

  *Phase 1 scope.* Phase 1 is hardware only: the servo fitted and powered, not driven. F01 carries the Phase 1 form. F02 and F03 are Phase 2.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-202-R001

**Statement.** The sub-system shall be fitted at the front axle with Ackermann geometry and supplied at the actuator's own voltage, ready to be commanded.

- Function: Nexus-SubSys-202-F01
- Derived-from: Nexus-Vehicle-R006
- Allocated-to: Nexus-Phys-DRV, Nexus-Phys-PWR (as-is), Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-DRV-R002 and Nexus-Phys-STM32-R011
