# Nexus-Physical-08 - Steering actuator

System element, level 1. Realised in hardware; the recursion stops here. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The LD-1501MG servo and the Ackermann linkage.
- **Interfaces.** Supplied and commanded through the servo lead from [Nexus-Physical-01](Nexus-Physical-01.md) (6 V from [Nexus-Physical-05](Nexus-Physical-05.md), PWM from Phase 2); the environment through the front wheels.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 202 F1.
- **Modes.** Unpowered; powered and idle (Phase 1).

## Requirements

### Nexus-Physical-08-R001

**Statement.** The LD-1501MG servo on the front axle shall steer the front wheels through the Ackermann linkage.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection The servo is fitted and the linkage moves freely by hand
- Realised-by: HW
