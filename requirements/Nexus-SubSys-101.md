# Nexus-SubSys-101 - Energy Storage & Distribution

Logical, level 1. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The sub-system of this name in the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg), which owns its name, phase and boundary.
- **Interfaces.** Its siblings in the logical architecture and the flows drawn there.
- **Allocated functions.** Functions, numbered in the order of the sub-system's card in the drawing script. The drawing owns the names; they are copied here only to carry the numbers.
  - `Nexus-SubSys-101-F01` Store energy (3S LiPo)
  - `Nexus-SubSys-101-F02` Protect circuits (fuses)
  - `Nexus-SubSys-101-F03` Switch drive & logic branches
  - `Nexus-SubSys-101-F04` Accept charge from the charger
  - `Nexus-SubSys-101-F05` Convert supply rails (5 V, 6 V)
  - `Nexus-SubSys-101-F06` Measure pack voltage & current
  - `Nexus-SubSys-101-F07` Estimate state of charge

  *Phase 1 scope.* F01 to F05 are in Phase 1 (the hardware is fitted). F06 and F07 are Phase 2: the INA226 is fitted but not tested.
- **Modes.** None at this level.

## Requirements

### Nexus-SubSys-101-R001

**Statement.** The sub-system shall store, on board, the energy the vehicle needs to operate.

- Function: Nexus-SubSys-101-F01
- Derived-from: Nexus-Vehicle-R001
- Allocated-to: Nexus-Phys-PWR (as-is)
- Phase: 1
- Verification: Inspection The 3S 6000 mAh pack is fitted and charged
- Realised-by: HW

### Nexus-SubSys-101-R002

**Statement.** The sub-system shall switch the drive branch and the logic branch independently of each other.

- Function: Nexus-SubSys-101-F03
- Derived-from: Nexus-Vehicle-R002
- Allocated-to: Nexus-Phys-PWR
- Phase: 1
- Verification: Integration Nexus-Phys-PWR-R001 and Nexus-Phys-PWR-R002

### Nexus-SubSys-101-R003

**Statement.** The sub-system shall clear an overcurrent in any branch before the conductor or board in it is damaged.

- Function: Nexus-SubSys-101-F02
- Derived-from: Nexus-Vehicle-R003
- Allocated-to: Nexus-Phys-PWR
- Phase: 1
- Verification: Integration Nexus-Phys-PWR-R003

### Nexus-SubSys-101-R004

**Statement.** The sub-system shall supply each class of load at the voltage it needs: the computers at 5 V and the steering at 6 V.

- Function: Nexus-SubSys-101-F05
- Derived-from: Nexus-Vehicle-R001
- Allocated-to: Nexus-Phys-PWR
- Phase: 1
- Verification: Integration Nexus-Phys-PWR-R004 and Nexus-Phys-PWR-R005

### Nexus-SubSys-101-R005

**Statement.** The sub-system shall accept charge from the supplied charger.

- Function: Nexus-SubSys-101-F04
- Derived-from: Nexus-Vehicle-R001
- Allocated-to: Nexus-Phys-PWR (as-is)
- Phase: 1
- Verification: Demo The pack charges from the supplied charger
- Realised-by: HW
