# Nexus-Vehicle - NEXUS vehicle

System-of-interest, level 0. Its requirements are the system requirements, written as a black box. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The assembled vehicle, inside the system boundary of both [architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg) [views](../system/renders/Nexus-Platform-Physical-Architecture.svg). It names no element of its own.
- **Interfaces.** Operator, charger, environment, and a PC with the USB-CAN adapter at the diagnostic port (test equipment, part of the enabling system). The remote station joins in Phase 2.
- **Allocated functions.** All functions of the logical view; Phase 1 uses those listed in the [allocation](../system/physical-architecture.md).
- **Modes.** Unpowered; computing only (logic switch on); drive and computing (both switches on).

## Requirements

### Nexus-Vehicle-R001

**Statement.** The vehicle shall operate from its on-board battery alone, with no external supply.

- Function: Nexus-Logical-101-F01, Nexus-Logical-101-F05
- Derived-from: -
- Allocated-to: Nexus-Physical-05
- Phase: 1
- Verification: Demo The vehicle powers up from its battery with the harness checks passed (deliverable 1.1)

### Nexus-Vehicle-R002

**Statement.** The vehicle shall let the operator switch the power to the drive on and off independently of the power to its computing.

- Function: Nexus-Logical-101-F03, Nexus-Logical-501-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-05, Nexus-Physical-06
- Phase: 1
- Verification: Demo The drive switch off: the drive is unpowered and the computing stays up

### Nexus-Vehicle-R003

**Statement.** The vehicle shall interrupt an overcurrent before it damages its wiring or its electronics.

- Function: Nexus-Logical-101-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-05
- Phase: 1
- Verification: Integration Nexus-Physical-05-R005 and Nexus-Physical-05-R006

### Nexus-Vehicle-R004

**Statement.** The vehicle shall accept charge from its supplied charger.

- Function: Nexus-Logical-101-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-05 (as-is)
- Phase: 1
- Verification: Demo The pack charges from the supplied charger
- Realised-by: HW

### Nexus-Vehicle-R005

**Statement.** The vehicle shall hold every component in a defined place.

- Function: Nexus-Logical-102-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-06
- Phase: 1
- Verification: Integration Nexus-Physical-06-R001

### Nexus-Vehicle-R006

**Statement.** The vehicle shall protect its wiring and electronics against contact.

- Function: Nexus-Logical-102-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-06 (as-is)
- Phase: 1
- Verification: Inspection The harness board is closed under plate 2 and every board sits in its tray
- Realised-by: HW
- Decisions: MEC-16

### Nexus-Vehicle-R007

**Statement.** The vehicle shall present its power switches and its service ports on one face, reachable without opening it.

- Function: Nexus-Logical-102-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-06
- Phase: 1
- Verification: Integration Nexus-Physical-06-R002

### Nexus-Vehicle-R008

**Statement.** The vehicle shall carry a rear-wheel drive and an Ackermann front steering, fitted and supplied with power, ready to be commanded.

- Function: Nexus-Logical-201-F01, Nexus-Logical-202-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-07, Nexus-Physical-08, Nexus-Physical-05, Nexus-Physical-01
- Phase: 1
- Verification: Inspection The motors, driver and servo are fitted, supplied and wired to the controller

### Nexus-Vehicle-R009

**Statement.** The vehicle shall not drive its wheels without a command.

- Function: Nexus-Logical-201-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-07 (as-is)
- Phase: 1
- Verification: Demo Drive switch on with no command sent: the wheels do not turn
- Realised-by: HW

### Nexus-Vehicle-R010

**Statement.** The vehicle shall publish its heartbeats on its diagnostic CAN port at the rate set in the CAN matrix, for 10 minutes with no error frame, bus-off or missed heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-04, Nexus-Physical-01, Nexus-Physical-02
- Phase: 1
- Verification: Test T2.3

### Nexus-Vehicle-R011

**Statement.** The vehicle shall accept new control software through its diagnostic CAN port, with no debug probe and without being opened.

- Function: Nexus-Logical-504-F01, Nexus-Logical-504-F02
- Derived-from: -
- Allocated-to: Nexus-Physical-04, Nexus-Physical-01
- Phase: 1
- Verification: Test T1.1

### Nexus-Vehicle-R012

**Statement.** The vehicle shall update its control software with no external tool attached.

- Function: Nexus-Logical-504-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-02, Nexus-Physical-04, Nexus-Physical-01
- Phase: 1
- Verification: Test T1.1

### Nexus-Vehicle-R013

**Statement.** An interrupted or failed update shall leave the vehicle able to receive a new one.

- Function: Nexus-Logical-504-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-01
- Phase: 1
- Verification: Test T1.1

### Nexus-Vehicle-R014

**Statement.** The vehicle shall accept a new version of its update mechanism through the same port.

- Function: Nexus-Logical-504-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-01
- Phase: 1
- Verification: Test T1.2

### Nexus-Vehicle-R015

**Statement.** The vehicle shall show, without tools, the state of its control software: update idle, update receiving, update mechanism being replaced, application running.

- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-01
- Phase: 1
- Verification: Test T1.3

### Nexus-Vehicle-R016

**Statement.** The vehicle shall report the name and version of every program it runs.

- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-01, Nexus-Physical-02
- Phase: 1
- Verification: Test T1.1, T2.1 and T2.2

### Nexus-Vehicle-R017

**Statement.** The vehicle shall start its software from on-board storage, with no host connection.

- Function: Nexus-Logical-501-F01
- Derived-from: -
- Allocated-to: Nexus-Physical-02
- Phase: 1
- Verification: Test T2.2

### Nexus-Vehicle-R018

**Statement.** The vehicle shall let a PC join its CAN bus at the diagnostic port without disturbing the bus, whether the PC is present or not.

- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-04
- Phase: 1
- Verification: Test T2.3

### Nexus-Vehicle-R019

**Statement.** The vehicle shall give external access to the debug interface of its control software and to the console of its other software.

- Function: Nexus-Logical-503-F04
- Derived-from: -
- Allocated-to: Nexus-Physical-01, Nexus-Physical-02
- Phase: 1
- Verification: Inspection Both are reached from the rear fascia with the vehicle closed

### Nexus-Vehicle-R020

**Statement.** The vehicle shall record its CAN traffic on board, with timestamps.

- Function: Nexus-Logical-503-F03
- Derived-from: -
- Allocated-to: Nexus-Physical-02
- Phase: 1
- Verification: Test T2.3
