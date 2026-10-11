# Nexus-Physical-07 - Rear drive

System element, level 1. Realised in hardware; the recursion stops here. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** Two encoder gear motors and the Encoder Motor Module.
- **Interfaces.** Supplied by [Nexus-Physical-05](Nexus-Physical-05.md); commanded by [Nexus-Physical-01](Nexus-Physical-01.md) over I2C from Phase 2; the environment through the wheels.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 201 F1.
- **Modes.** Unpowered; powered and idle (Phase 1).

## Requirements

### Nexus-Physical-07-R001

**Statement.** The element shall drive the rear wheels with two 12 V encoder gear motors through the Encoder Motor Module.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection The motors and the module are fitted and wired
- Realised-by: HW
