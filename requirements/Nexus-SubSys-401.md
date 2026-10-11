# Nexus-SubSys-401 - In-Vehicle Communication

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-401-F01` Exchange signals between nodes (CAN)
  - `Nexus-SubSys-401-F02` Time-synchronise nodes
  - `Nexus-SubSys-401-F03` Route between CAN and service middleware
  - `Nexus-SubSys-401-F04` Publish services / topics (ROS 2, SOME/IP)

  *Phase 1 scope.* Only F01 is in Phase 1: the bus, the flashing identifiers, a heartbeat and SocketCAN. F02 to F04 are later.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-401-R001

**Statement.** The sub-system shall carry messages between the vehicle's computers on a shared bus.

- Function: Nexus-SubSys-401-F01
- Derived-from: Nexus-Vehicle-R007
- Allocated-to: Nexus-Phys-CAN, Nexus-Phys-STM32, Nexus-Phys-FRDM
- Phase: 1
- Verification: Integration Nexus-Phys-CAN-R001 to R004, Nexus-Phys-STM32-R001 and Nexus-Phys-FRDM-R001

### Nexus-SubSys-401-R002

**Statement.** The sub-system shall have each computer announce itself periodically and observe the other's announcements.

- Function: Nexus-SubSys-401-F01
- Derived-from: Nexus-Vehicle-R007
- Allocated-to: Nexus-Phys-STM32, Nexus-Phys-FRDM
- Phase: 1
- Verification: Test T2.3

### Nexus-SubSys-401-R003

**Statement.** The sub-system shall define the bus's identifiers and timing in one released document.

- Function: Nexus-SubSys-401-F01
- Derived-from: Nexus-Vehicle-R007, Nexus-Vehicle-R008
- Allocated-to: Nexus-Phys-CAN
- Phase: 1
- Verification: Integration Nexus-Phys-CAN-R007
