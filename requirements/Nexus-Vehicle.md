# Nexus-Vehicle - NEXUS vehicle

Vehicle, level 0. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The assembled vehicle as a black box, and the only SoI with no parent. The boundary is the dashed system boundary of the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg): everything inside it is the vehicle.
- **Interfaces.** Operator, remote station, charger and environment (the external actors of the logical architecture), plus the **PC adapter** of the bench demo, which is test equipment outside the boundary.
- **Allocated functions.** All of it: the root. Phase 1 requirements come from the goal and the tests of [phases.md](../system/phases.md).
- **Modes.** Unpowered; logic only (SW2 on); drive and logic (SW1 and SW2 on). Vehicle modes proper are a Phase 2 function of 501.

## Requirements

### Nexus-Vehicle-R001

**Statement.** The vehicle shall operate from its on-board battery alone.

- Derived-from: -
- Allocated-to: Nexus-SubSys-101
- Phase: 1
- Verification: Demo The vehicle powers up from the battery with the harness checks passed (deliverable 1.1)

### Nexus-Vehicle-R002

**Statement.** The operator shall be able to cut the power to the wheels without powering down the computers.

- Derived-from: -
- Allocated-to: Nexus-SubSys-101, Nexus-SubSys-501
- Phase: 1
- Verification: Demo SW1 off: the drive supply is gone, the STM32 and the FRDM stay powered

### Nexus-Vehicle-R003

**Statement.** The vehicle shall clear an overcurrent fault before it damages a conductor or a board.

- Derived-from: -
- Allocated-to: Nexus-SubSys-101
- Phase: 1
- Verification: Integration Nexus-SubSys-101-R003

### Nexus-Vehicle-R004

**Statement.** The vehicle shall hold and protect every component in a defined place.

- Derived-from: -
- Allocated-to: Nexus-SubSys-102
- Phase: 1
- Verification: Inspection Every Phase 1 item of the BOM is fitted and secure

### Nexus-Vehicle-R005

**Statement.** The vehicle shall present its power switches and debug ports on one face without opening the vehicle.

- Derived-from: -
- Allocated-to: Nexus-SubSys-102
- Phase: 1
- Verification: Inspection The switches and ports are reached from the rear fascia with the vehicle closed

### Nexus-Vehicle-R006

**Statement.** The vehicle shall carry driven rear wheels and Ackermann front steering, fitted and supplied, and shall not drive them in Phase 1.

- Derived-from: -
- Allocated-to: Nexus-SubSys-201, Nexus-SubSys-202
- Phase: 1
- Verification: Inspection The motors, driver and servo are fitted and supplied; no command is ever sent

### Nexus-Vehicle-R007

**Statement.** The two computers shall exchange heartbeats over the vehicle bus for 10 minutes with no error frame, bus-off or missed heartbeat.

- Derived-from: -
- Allocated-to: Nexus-SubSys-401, Nexus-SubSys-503
- Phase: 1
- Verification: Test T2.3

### Nexus-Vehicle-R008

**Statement.** The vehicle shall allow its STM32 application to be replaced over the vehicle bus without a debug probe.

- Derived-from: -
- Allocated-to: Nexus-SubSys-504, Nexus-SubSys-401
- Phase: 1
- Verification: Test T1.1

### Nexus-Vehicle-R009

**Statement.** The vehicle shall allow its STM32 flash bootloader to be replaced over the vehicle bus.

- Derived-from: -
- Allocated-to: Nexus-SubSys-504
- Phase: 1
- Verification: Test T1.2

### Nexus-Vehicle-R010

**Statement.** The vehicle shall show without tools which software state the STM32 is in.

- Derived-from: -
- Allocated-to: Nexus-SubSys-503
- Phase: 1
- Verification: Test T1.3

### Nexus-Vehicle-R011

**Statement.** The vehicle shall let a PC join its bus as a further node.

- Derived-from: -
- Allocated-to: Nexus-SubSys-503
- Phase: 1
- Verification: Test T2.3

### Nexus-Vehicle-R012

**Statement.** The vehicle shall give access to each computer's debug interface without opening the vehicle.

- Derived-from: -
- Allocated-to: Nexus-SubSys-503, Nexus-SubSys-102
- Phase: 1
- Verification: Inspection The ST-LINK and the FRDM console are reached from the fascia

### Nexus-Vehicle-R013

**Statement.** The vehicle shall boot a Linux image assembled from separately released applications.

- Derived-from: -
- Allocated-to: Nexus-SubSys-504
- Phase: 1
- Verification: Test T2.1 and T2.2

### Nexus-Vehicle-R014

**Statement.** Every software item of the vehicle shall be built from a clean clone in CI and released under a version tag.

- Derived-from: -
- Allocated-to: Nexus-SubSys-504
- Phase: 1
- Verification: Inspection The CI runs and the release tags of every repository (deliverable 1.7)
