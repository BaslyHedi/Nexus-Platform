# Nexus-Physical-01 - STM32 node: real-time control

System element, level 1. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The STM32F4DISCOVERY on its carrier boards with the CAN transceiver and the LEDs, and the software in its flash. Elements below it: the Discovery board and the carrier (hardware, realised here), the software items [Nexus-STM32-FBL](Nexus-STM32-FBL.md) and [Nexus-STM32-App](Nexus-STM32-App.md).
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md); 5 V from [Nexus-Physical-05](Nexus-Physical-05.md); I2C and PWM to [Nexus-Physical-07](Nexus-Physical-07.md) and [Nexus-Physical-08](Nexus-Physical-08.md), prepared and not driven in Phase 1; SWD to the bench PC.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 401 F1, 503 F4, 504 F1 to F3, and the prepared interfaces of 201 F1 and 202 F1.
- **Modes.** Bootloader idle; bootloader receiving; FBL-Updater running; application running.

## Requirements

### Nexus-Physical-01-R001

**Statement.** The node shall connect to the bus through an SN65HVD230 transceiver on CAN1, with PD0 as receive and PD1 as transmit.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: -
- Phase: 1
- Verification: Inspection The transceiver wiring
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-01-R002

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-App-R001

### Nexus-Physical-01-R003

**Statement.** When the node receives a heartbeat from the FRDM node, the node shall indicate the reception on an LED.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-App-R002

### Nexus-Physical-01-R004

**Statement.** When the node receives a software-update request, the node shall receive the image over the bus.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R012, Nexus-Vehicle-R013
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R001

### Nexus-Physical-01-R005

**Statement.** When the node has received an image, the node shall program the image into the application region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R012, Nexus-Vehicle-R013
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R002

### Nexus-Physical-01-R006

**Statement.** When the CRC of the programmed image matches, the node shall start the image.

- Function: Nexus-Logical-504-F01, Nexus-Logical-504-F02
- Derived-from: Nexus-Vehicle-R012, Nexus-Vehicle-R013, Nexus-Vehicle-R015
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R003, Nexus-STM32-FBL-R004, Nexus-STM32-App-R003

### Nexus-Physical-01-R007

**Statement.** If a download is interrupted, then the node shall remain ready for a new download.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Vehicle-R014
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R005

### Nexus-Physical-01-R008

**Statement.** If the application region holds no valid image, then the node shall remain ready for a new download.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Vehicle-R015
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R006

### Nexus-Physical-01-R009

**Statement.** The flash of the node shall hold the bootloader region apart from the application region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R016
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R007

### Nexus-Physical-01-R010

**Statement.** The node shall let an image run from the application region rewrite the bootloader region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R016
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R008, Nexus-STM32-FBL-R009, Nexus-STM32-FBL-R010

### Nexus-Physical-01-R011

**Statement.** The four LEDs of the node shall show a distinct pattern for each of these states: bootloader idle, bootloader receiving, FBL-Updater running, application running.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R017
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R011, Nexus-STM32-FBL-R012, Nexus-STM32-FBL-R013, Nexus-STM32-App-R004

### Nexus-Physical-01-R012

**Statement.** When asked over the bus, the node shall report the version of the running program in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R018
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R014, Nexus-STM32-FBL-R015, Nexus-STM32-App-R005

### Nexus-Physical-01-R013

**Statement.** The node shall give SWD access through the on-board ST-LINK.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R022
- Allocated-to: -
- Phase: 1
- Verification: Inspection The ST-LINK connection
- Realised-by: HW
- Decisions: MEC-05

### Nexus-Physical-01-R014

**Statement.** The node shall bring out I2C on PB10 and PB11 to the motor driver.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: -
- Phase: 1
- Verification: Inspection PB10 and PB11 reach the motor driver header
- Realised-by: HW
- Decisions: HW-10

### Nexus-Physical-01-R015

**Statement.** The node shall bring out the servo PWM on PE9 through a 1 kΩ series resistor.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Vehicle-R009
- Allocated-to: -
- Phase: 1
- Verification: Inspection PE9 reaches the servo header through R4
- Realised-by: HW
- Decisions: HW-19, HW-21
