# Nexus-SubSys-501 - Supervision & Safety

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-501-F01` Manage vehicle modes & transitions
  - `Nexus-SubSys-501-F02` Emergency stop & safe stop
  - `Nexus-SubSys-501-F03` Watchdogs & command time-outs
  - `Nexus-SubSys-501-F04` Detect faults, enter degraded mode
  - `Nexus-SubSys-501-F05` Shut down gracefully on low pack
  - `Nexus-SubSys-501-F06` Command drive-power cut-off

  *Phase 1 scope.* Phase 1 is the hardware already built (HW-03, HW-08, HW-20). Only F02 has a requirement; F06, the relay, is deferred (HW-12).
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-501-R001

**Statement.** The sub-system shall let the operator cut the drive power by one action while the logic stays powered.

- Function: Nexus-SubSys-501-F02
- Derived-from: Nexus-Vehicle-R002
- Allocated-to: Nexus-Phys-PWR (as-is), Nexus-Phys-CHS
- Phase: 1
- Verification: Demo SW1 off: the drive supply is gone, the STM32 and the FRDM stay powered
