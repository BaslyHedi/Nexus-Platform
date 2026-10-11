# Nexus-SubSys-102 - Structure & Enclosure

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-102-F01` Carry & locate every component (3-deck chassis)
  - `Nexus-SubSys-102-F02` Protect harness & electronics
  - `Nexus-SubSys-102-F03` Expose controls & service ports (rear fascia)
  - `Nexus-SubSys-102-F04` Manage heat & vibration

  *Phase 1 scope.* F01 to F03 are in Phase 1. F04 has no requirement yet: there is no measured limit to write it against.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-102-R001

**Statement.** The sub-system shall hold every component in a defined place.

- Function: Nexus-SubSys-102-F01
- Derived-from: Nexus-Vehicle-R004
- Allocated-to: Nexus-Phys-CHS
- Phase: 1
- Verification: Integration Nexus-Phys-CHS-R001

### Nexus-SubSys-102-R002

**Statement.** The sub-system shall protect the harness and electronics against contact.

- Function: Nexus-SubSys-102-F02
- Derived-from: Nexus-Vehicle-R004
- Allocated-to: Nexus-Phys-CHS (as-is)
- Phase: 1
- Verification: Inspection The harness board is closed under plate 2 and the boards sit in their trays
- Realised-by: HW
- Decisions: MEC-16

### Nexus-SubSys-102-R003

**Statement.** The sub-system shall present the power switches and the debug ports on one face of the vehicle.

- Function: Nexus-SubSys-102-F03
- Derived-from: Nexus-Vehicle-R005, Nexus-Vehicle-R012
- Allocated-to: Nexus-Phys-CHS
- Phase: 1
- Verification: Integration Nexus-Phys-CHS-R002
