# Nexus-Physical-01 - STM32 node: real-time control

System element, level 1. Written to [../system/method.md](../../system/method.md) and [rules.md](../rules.md).

- **Purpose and boundary.** The NUCLEO-H533RE on its carrier boards with the CAN transceiver, and the software in its flash. Its elements, defined in [the node's local view](../../system/physical-architecture.md): MCU board [01-01](../components/Nexus-Physical-01/Nexus-Physical-01-01.md), carrier [01-02](../components/Nexus-Physical-01/Nexus-Physical-01-02.md), transceiver module [01-03](../components/Nexus-Physical-01/Nexus-Physical-01-03.md), bootloader [01-04](../components/Nexus-Physical-01/Nexus-Physical-01-04.md), FBL-Updater [01-05](../components/Nexus-Physical-01/Nexus-Physical-01-05.md), application [01-06](../components/Nexus-Physical-01/Nexus-Physical-01-06.md).
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md); 5 V and the 6 V servo supply from [Nexus-Physical-05](Nexus-Physical-05.md); I2C and PWM to [Nexus-Physical-07](Nexus-Physical-07.md) and [Nexus-Physical-08](Nexus-Physical-08.md), prepared and not driven in Phase 1; SWD to the bench PC.
- **Allocated functions.** See the [allocation](../../system/physical-architecture.md): 401 F1, 503 F4, 504 F1 to F3, and the prepared interfaces of 201 F1 and 202 F1.
- **Modes.** Bootloader idle; bootloader receiving; FBL-Updater running; application running.

## Requirements

### Nexus-Physical-01-R001

**Statement.** The node shall run from the 5 V supply of the power element.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Vehicle-R001
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-02
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R001, Nexus-Physical-01-02-R001

### Nexus-Physical-01-R002

**Statement.** The node shall connect to the bus through an SN65HVD230 transceiver on FDCAN2, with PB12 as receive and PB13 as transmit.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-02, Nexus-Physical-01-03, Nexus-Physical-01-04, Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R002, Nexus-Physical-01-02-R002, Nexus-Physical-01-02-R003, Nexus-Physical-01-02-R004, Nexus-Physical-01-03-R001, Nexus-Physical-01-04-R001, Nexus-Physical-01-06-R001
- Decisions: HW-09, HW-22

### Nexus-Physical-01-R003

**Statement.** The node shall terminate the bus at the STM32 end.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-01-03
- Phase: 1
- Verification: Integration Nexus-Physical-01-03-R002
- Decisions: HW-09

### Nexus-Physical-01-R004

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-06-R002

### Nexus-Physical-01-R005

**Statement.** When the node receives a heartbeat from the FRDM node, the node shall indicate the reception on an LED.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-06-R003

### Nexus-Physical-01-R006

**Statement.** When the node receives a software-update request, the node shall receive the image over the bus.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R012, Nexus-Vehicle-R013
- Allocated-to: Nexus-Physical-01-04
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R002

### Nexus-Physical-01-R007

**Statement.** When the node has received an image, the node shall program the image into the application region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R012, Nexus-Vehicle-R013
- Allocated-to: Nexus-Physical-01-04
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R003

### Nexus-Physical-01-R008

**Statement.** When the CRC of the programmed image matches, the node shall start the image.

- Function: Nexus-Logical-504-F01, Nexus-Logical-504-F02
- Derived-from: Nexus-Vehicle-R012, Nexus-Vehicle-R013, Nexus-Vehicle-R015
- Allocated-to: Nexus-Physical-01-04, Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R004, Nexus-Physical-01-04-R005, Nexus-Physical-01-06-R004

### Nexus-Physical-01-R009

**Statement.** If a download is interrupted, then the node shall remain ready for a new download.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Vehicle-R014
- Allocated-to: Nexus-Physical-01-04
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R006

### Nexus-Physical-01-R010

**Statement.** If the application region holds no valid image, then the node shall remain ready for a new download.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Vehicle-R015
- Allocated-to: Nexus-Physical-01-04
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R007

### Nexus-Physical-01-R011

**Statement.** The flash of the node shall hold the bootloader region apart from the application region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R016
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-04, Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R003, Nexus-Physical-01-04-R008, Nexus-Physical-01-06-R004

### Nexus-Physical-01-R012

**Statement.** The node shall let an image run from the application region rewrite the bootloader region.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R016
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-04, Nexus-Physical-01-05
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R003, Nexus-Physical-01-04-R009, Nexus-Physical-01-05-R001, Nexus-Physical-01-05-R002, Nexus-Physical-01-05-R003

### Nexus-Physical-01-R013

**Statement.** The user LED of the node shall show a distinct pattern for each of these states: bootloader idle, bootloader receiving, FBL-Updater running, application running.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R017
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-04, Nexus-Physical-01-05, Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R004, Nexus-Physical-01-04-R010, Nexus-Physical-01-04-R011, Nexus-Physical-01-05-R004, Nexus-Physical-01-06-R005

### Nexus-Physical-01-R014

**Statement.** When asked over the bus, the node shall report the version of the running program in the node info.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R018
- Allocated-to: Nexus-Physical-01-04, Nexus-Physical-01-05, Nexus-Physical-01-06
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R012, Nexus-Physical-01-05-R005, Nexus-Physical-01-06-R006

### Nexus-Physical-01-R015

**Statement.** The node shall give SWD access through the on-board ST-LINK.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R022
- Allocated-to: Nexus-Physical-01-01
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R005
- Decisions: MEC-05

### Nexus-Physical-01-R016

**Statement.** The node shall bring out I2C on PB6 and PB7 to the motor driver.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Vehicle-R008
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-02
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R006, Nexus-Physical-01-02-R005
- Decisions: HW-10, HW-22

### Nexus-Physical-01-R017

**Statement.** The node shall bring out the servo PWM on PA15 through a 1 kΩ series resistor.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Vehicle-R009
- Allocated-to: Nexus-Physical-01-01, Nexus-Physical-01-02
- Phase: 1
- Verification: Integration Nexus-Physical-01-01-R007, Nexus-Physical-01-02-R006
- Decisions: HW-19, HW-21, HW-22

### Nexus-Physical-01-R018

**Statement.** The node shall pass the 6 V servo supply from the UBEC to the servo header.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Vehicle-R009
- Allocated-to: Nexus-Physical-01-02
- Phase: 1
- Verification: Integration Nexus-Physical-01-02-R007, Nexus-Physical-01-02-R008
- Decisions: HW-14, HW-19
