# Nexus-SubSys-503 - Diagnostics & Data Logging

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-503-F01` Monitor sub-system health
  - `Nexus-SubSys-503-F02` Record fault codes & event data
  - `Nexus-SubSys-503-F03` Log & replay bus and sensor data
  - `Nexus-SubSys-503-F04` Provide debug access (CAN port, UART, SWD)

  *Phase 1 scope.* F03 and F04 in their Phase 1 forms: `candump` capture of the demo, and the CAN port, SWD and UART. F01 and F02 are Phase 2.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-503-R001

**Statement.** The sub-system shall let a PC join the bus as a further node without affecting the bus when it is absent.

- Function: Nexus-SubSys-503-F04
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Phys-CAN
- Phase: 1
- Verification: Integration Nexus-Phys-CAN-R005 and Nexus-Phys-CAN-R006

### Nexus-SubSys-503-R002

**Statement.** The sub-system shall give access to the MCU's programming and debug interface and to the Linux board's console.

- Function: Nexus-SubSys-503-F04
- Derived-from: Nexus-Vehicle-R012
- Allocated-to: Nexus-Phys-STM32, Nexus-Phys-FRDM
- Phase: 1
- Verification: Integration Nexus-Phys-STM32-R008 and Nexus-Phys-FRDM-R003

### Nexus-SubSys-503-R003

**Statement.** The sub-system shall capture the bus traffic with timestamps as evidence.

- Function: Nexus-SubSys-503-F03
- Derived-from: Nexus-Vehicle-R007
- Allocated-to: Nexus-Phys-FRDM
- Phase: 1
- Verification: Integration Nexus-Phys-FRDM-R004

### Nexus-SubSys-503-R004

**Statement.** The sub-system shall indicate which software state the MCU is in, without tools.

- Function: Nexus-SubSys-503-F04
- Derived-from: Nexus-Vehicle-R010
- Allocated-to: Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-STM32-R009
