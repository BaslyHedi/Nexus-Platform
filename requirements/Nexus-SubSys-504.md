# Nexus-SubSys-504 - Software Update & Config.

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-504-F01` Deliver updates (OTA, A/B slots)
  - `Nexus-SubSys-504-F02` Verify integrity before install
  - `Nexus-SubSys-504-F03` Roll back a failed update
  - `Nexus-SubSys-504-F04` Manage configuration & calibration parameters

  *Phase 1 scope.* Phase 1 is the FBL: download an app over CAN, verify by CRC, jump. F01 also carries the first form of the Linux image and of the repositories, since [phases.md](../system/phases.md) says Phase 3 extends that pattern; no sub-system hosts "build and release software" yet, which is a gap to revisit. F04 is Phase 2.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-504-R001

**Statement.** The sub-system shall deliver an image to the MCU over the vehicle bus on request, without a debug probe.

- Function: Nexus-SubSys-504-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: Nexus-Phys-FRDM, Nexus-Phys-CAN, Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-FRDM-R005, Nexus-Phys-CAN-R009, Nexus-Phys-STM32-R004 and Nexus-Phys-STM32-R012

### Nexus-SubSys-504-R002

**Statement.** The sub-system shall verify an image's integrity before it runs.

- Function: Nexus-SubSys-504-F02
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-STM32-R006

### Nexus-SubSys-504-R003

**Statement.** The sub-system shall leave the update path usable after an interrupted or invalid delivery.

- Function: Nexus-SubSys-504-F03
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-STM32-R007

### Nexus-SubSys-504-R004

**Statement.** The sub-system shall replace the update mechanism itself over the same path.

- Function: Nexus-SubSys-504-F01
- Derived-from: Nexus-Vehicle-R009
- Allocated-to: Nexus-Phys-STM32
- Phase: 1
- Verification: Integration Nexus-Phys-STM32-R005 and Nexus-Phys-STM32-R013

### Nexus-SubSys-504-R005

**Statement.** The sub-system shall assemble the Linux-side software from independently released parts into a bootable image.

- Function: Nexus-SubSys-504-F01
- Derived-from: Nexus-Vehicle-R013
- Allocated-to: Nexus-Phys-FRDM
- Phase: 1
- Verification: Integration Nexus-Phys-FRDM-R006 and Nexus-Phys-FRDM-R008

### Nexus-SubSys-504-R006

**Statement.** The sub-system shall build every software item from a clean clone and release it under a version tag.

- Function: Nexus-SubSys-504-F01
- Derived-from: Nexus-Vehicle-R014
- Allocated-to: Nexus-Phys-STM32, Nexus-Phys-FRDM, Nexus-Phys-CAN
- Phase: 1
- Verification: Integration Nexus-Phys-STM32-R014, Nexus-Phys-FRDM-R007 and Nexus-Phys-CAN-R008
