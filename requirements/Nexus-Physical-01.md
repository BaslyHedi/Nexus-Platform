# Nexus-Physical-01 - STM32 node: real-time control

System element, level 1. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The STM32F4DISCOVERY on its carrier boards with the CAN transceiver and the LEDs, and the software in its flash. Elements below it: the Discovery board and the carrier (hardware, realised here), the software items [Nexus-STM32-FBL](Nexus-STM32-FBL.md) and [Nexus-STM32-App](Nexus-STM32-App.md).
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md); 5 V from [Nexus-Physical-05](Nexus-Physical-05.md); I2C and PWM to [Nexus-Physical-07](Nexus-Physical-07.md) and [Nexus-Physical-08](Nexus-Physical-08.md), prepared and not driven in Phase 1; SWD to the bench PC.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 401 F1, 503 F4, 504 F1 to F3, and the prepared interfaces of 201 F1 and 202 F1.
- **Modes.** Bootloader idle; bootloader receiving; FBL-Updater running; application running.

## Requirements

### Nexus-Physical-01-R001

**Statement.** The node shall reach the bus through an SN65HVD230 transceiver on CAN1, PD0 receive and PD1 transmit.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010, Nexus-Vehicle-R011
- Allocated-to: -
- Phase: 1
- Verification: Inspection The transceiver is wired to PD0 and PD1
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-01-R002

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010
- Allocated-to: Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-App-R001

### Nexus-Physical-01-R003

**Statement.** The node shall show on an LED that it receives the FRDM node's heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010
- Allocated-to: Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-App-R002

### Nexus-Physical-01-R004

**Statement.** On request over the bus, the node shall receive an image, program it into its application region and start it, with no debug probe.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R011, Nexus-Vehicle-R012
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R001, Nexus-STM32-FBL-R002 and Nexus-STM32-App-R003

### Nexus-Physical-01-R005

**Statement.** The node shall verify an image's CRC before it starts it.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R003

### Nexus-Physical-01-R006

**Statement.** The node shall remain reachable for a new download after an interrupted download, a failed verification or an absent image.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Vehicle-R013
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R004

### Nexus-Physical-01-R007

**Statement.** The node's flash shall keep the bootloader region apart from the application region, so that an image run from the application region can rewrite the bootloader region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R014
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R005 and Nexus-STM32-FBL-R006

### Nexus-Physical-01-R008

**Statement.** The node's four LEDs shall show a pattern distinct for each state: bootloader idle, bootloader receiving, FBL-Updater running, application running.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R015
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R007 and Nexus-STM32-App-R004

### Nexus-Physical-01-R009

**Statement.** The node shall report the version of the program it runs in its node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R016
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R008 and Nexus-STM32-App-R005

### Nexus-Physical-01-R010

**Statement.** The node shall give SWD access through its on-board ST-LINK, brought to the fascia by USB.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R019
- Allocated-to: -
- Phase: 1
- Verification: Inspection The ST-LINK is reached from the fascia
- Realised-by: HW
- Decisions: MEC-05

### Nexus-Physical-01-R011

**Statement.** The node shall bring out I2C on PB10 and PB11 to the motor driver.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection PB10 and PB11 reach the motor driver header
- Realised-by: HW
- Decisions: HW-10

### Nexus-Physical-01-R012

**Statement.** The node shall bring out the servo PWM on PE9 through a 1 kohm series resistor.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection PE9 reaches the servo header through R4
- Realised-by: HW
- Decisions: HW-19, HW-21
