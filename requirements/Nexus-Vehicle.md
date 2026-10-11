# Nexus-Vehicle - NEXUS vehicle

System-of-interest, level 0. Its requirements are the system requirements, written as a black box. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The assembled vehicle, inside the system boundary of both [architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg) [views](../system/renders/Nexus-Platform-Physical-Architecture.svg). It names no element of its own.
- **Interfaces.** Operator, charger, environment, and a PC with the USB-CAN adapter at the diagnostic port (test equipment, part of the enabling system). The remote station joins in Phase 2.
- **Allocated functions.** All functions of the logical view; Phase 1 uses those listed in the [allocation](../system/physical-architecture.md).
- **Modes.** Unpowered; computing only (logic switch on); drive and computing (both switches on).

## Requirements

### Nexus-Vehicle-R001

**Statement.** The vehicle shall operate from the on-board battery without an external supply.

- Need: Deliverable 1.1
- Function: Nexus-Logical-101-F01, Nexus-Logical-101-F05
- Derived-from: -
- Allocated-to: Nexus-Physical-05
- Phase: 1
- Verification: Demo The vehicle powers up from the battery with the harness checks passed

### Nexus-Vehicle-R002

**Statement.** The vehicle shall give the operator a switch for the drive power that leaves the computing power unchanged.

- Need: Deliverable 1.1
- Function: Nexus-Logical-101-F03, Nexus-Logical-501-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-05, Nexus-Physical-06
- Phase: 1
- Verification: Demo With the drive switch off, the drive is unpowered and the computing stays powered

### Nexus-Vehicle-R003

**Statement.** If a current exceeds the rating of the conductor that carries the current, then the vehicle shall interrupt the current.

- Need: Deliverable 1.1
- Function: Nexus-Logical-101-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-05
- Phase: 1
- Verification: Integration Nexus-Physical-05-R007, Nexus-Physical-05-R008, Nexus-Physical-05-R009, Nexus-Physical-05-R010

### Nexus-Vehicle-R004

**Statement.** The vehicle shall accept charge from the supplied charger.

- Need: Deliverable 1.1
- Function: Nexus-Logical-101-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-05 (as-is)
- Phase: 1
- Verification: Demo The pack charges from the supplied charger
- Realised-by: HW

### Nexus-Vehicle-R005

**Statement.** The vehicle shall hold each component in a defined position.

- Need: Deliverable 1.1
- Function: Nexus-Logical-102-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-06
- Phase: 1
- Verification: Integration Nexus-Physical-06-R001

### Nexus-Vehicle-R006

**Statement.** The vehicle shall enclose the wiring and the electronics against contact from outside the vehicle.

- Need: Deliverable 1.1
- Function: Nexus-Logical-102-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-06 (as-is)
- Phase: 1
- Verification: Inspection The harness board is closed under plate 2 and each board sits in a tray
- Realised-by: HW
- Decisions: MEC-16

### Nexus-Vehicle-R007

**Statement.** The vehicle shall present the power switches and the service ports on one face, reachable with the vehicle closed.

- Need: Deliverable 1.1
- Function: Nexus-Logical-102-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-06
- Phase: 1
- Verification: Integration Nexus-Physical-06-R002

### Nexus-Vehicle-R008

**Statement.** The vehicle shall carry a rear-wheel drive, fitted and supplied with power.

- Need: Phase 1: 201 fitted and powered, not driven
- Function: Nexus-Logical-201-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-07, Nexus-Physical-05, Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-05-R002, Nexus-Physical-07-R001, Nexus-Physical-01-R014

### Nexus-Vehicle-R009

**Statement.** The vehicle shall carry an Ackermann front steering, fitted and supplied with power.

- Need: Phase 1: 202 fitted and powered, not driven
- Function: Nexus-Logical-202-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-08, Nexus-Physical-05, Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-05-R003, Nexus-Physical-05-R004, Nexus-Physical-08-R001, Nexus-Physical-01-R015

### Nexus-Vehicle-R010

**Statement.** While the vehicle has received no drive command, the vehicle shall keep the rear wheels stationary.

- Need: Phase 1 goal: no motors driven
- Function: Nexus-Logical-201-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-07 (as-is)
- Phase: 1
- Verification: Demo Drive switch on, no command sent: the wheels stay still
- Realised-by: HW

### Nexus-Vehicle-R011

**Statement.** The vehicle shall show continuously on the diagnostic port that the on-board software is alive.

- Need: T2.3
- Function: Nexus-Logical-401-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-04, Nexus-Physical-01, Nexus-Physical-02
- Phase: 1
- Verification: Integration Nexus-Physical-04-R001, Nexus-Physical-04-R002, Nexus-Physical-04-R003, Nexus-Physical-04-R006, Nexus-Physical-04-R007, Nexus-Physical-04-R008, Nexus-Physical-01-R001, Nexus-Physical-01-R002, Nexus-Physical-01-R003, Nexus-Physical-02-R001, Nexus-Physical-02-R002, Nexus-Physical-02-R003, Nexus-Physical-02-R004

### Nexus-Vehicle-R012

**Statement.** When an external tool sends new control software to the diagnostic port, the vehicle shall install the new control software with no debug probe attached.

- Need: T1.1
- Function: Nexus-Logical-504-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-04, Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-04-R001, Nexus-Physical-04-R006, Nexus-Physical-01-R004, Nexus-Physical-01-R005, Nexus-Physical-01-R006

### Nexus-Vehicle-R013

**Statement.** The vehicle shall install new control software held on board, with no external tool attached.

- Need: T1.1
- Function: Nexus-Logical-504-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-02, Nexus-Physical-04, Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-04-R006, Nexus-Physical-01-R004, Nexus-Physical-01-R005, Nexus-Physical-01-R006, Nexus-Physical-02-R005

### Nexus-Vehicle-R014

**Statement.** If an update is interrupted, then the vehicle shall remain ready to receive a new update.

- Need: T1.1
- Function: Nexus-Logical-504-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-01-R007

### Nexus-Vehicle-R015

**Statement.** If the new control software is invalid, then the vehicle shall remain ready to receive a new update.

- Need: T1.1
- Function: Nexus-Logical-504-F02, Nexus-Logical-504-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-01-R006, Nexus-Physical-01-R008

### Nexus-Vehicle-R016

**Statement.** When an external tool sends a new update mechanism to the diagnostic port, the vehicle shall replace the update mechanism.

- Need: T1.2
- Function: Nexus-Logical-504-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-04, Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-04-R006, Nexus-Physical-01-R009, Nexus-Physical-01-R010

### Nexus-Vehicle-R017

**Statement.** The vehicle shall show the state of the software update without tools.

- Need: T1.3
- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-01
- Phase: 1
- Verification: Integration Nexus-Physical-01-R011

### Nexus-Vehicle-R018

**Statement.** When a user requests the software versions, the vehicle shall report the name and the version of each program that the vehicle runs.

- Need: T1.1, T2.1, T2.2
- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-01, Nexus-Physical-02
- Phase: 1
- Verification: Integration Nexus-Physical-01-R012, Nexus-Physical-02-R008

### Nexus-Vehicle-R019

**Statement.** When the vehicle powers up, the vehicle shall start the on-board software from on-board storage with no host connection.

- Need: T2.2
- Function: Nexus-Logical-501-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-02
- Phase: 1
- Verification: Integration Nexus-Physical-02-R006, Nexus-Physical-02-R007

### Nexus-Vehicle-R020

**Statement.** The vehicle shall accept a PC on the diagnostic port as a further node of the CAN bus.

- Need: T2.3
- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-04
- Phase: 1
- Verification: Integration Nexus-Physical-04-R004, Nexus-Physical-04-R005

### Nexus-Vehicle-R021

**Statement.** The vehicle shall keep the CAN communication free of errors whether a PC is connected to the diagnostic port or not.

- Need: T2.3
- Function: Nexus-Logical-401-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-04
- Phase: 1
- Verification: Integration Nexus-Physical-04-R003, Nexus-Physical-04-R007, Nexus-Physical-04-R008

### Nexus-Vehicle-R022

**Statement.** The vehicle shall give external access for debugging the on-board software.

- Need: Phase 1: 503 debug access
- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-01, Nexus-Physical-02
- Phase: 1
- Verification: Integration Nexus-Physical-01-R013, Nexus-Physical-02-R011

### Nexus-Vehicle-R023

**Statement.** The vehicle shall record the internal communication on board, with a timestamp for each message.

- Need: T2.3
- Function: Nexus-Logical-503-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-02
- Phase: 1
- Verification: Integration Nexus-Physical-02-R009, Nexus-Physical-02-R010
