# VEH - NEXUS vehicle

Level 0. The vehicle as a black box; the only SoI with no parent. The requirements are written next.

- **Purpose and boundary.** The assembled vehicle: everything inside the system boundary of the
  [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg). The operator, remote station,
  charger, environment and the PC adapter are outside it.
- **Interfaces.** Operator, remote station, charger, environment.
- **Allocated functions.** All of them; this is the root.
- **Modes.** Defined with the supervision requirements.
