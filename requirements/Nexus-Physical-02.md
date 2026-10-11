# Nexus-Physical-02 - FRDM node: Linux compute

System element, level 1. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The FRDM-IMX91S with its SD card and the Linux software. Its elements, defined in [the node's local view](../system/physical-architecture.md): FRDM board [02-01](Nexus-Physical-02-01.md), SD card [02-02](Nexus-Physical-02-02.md), Linux image [02-03](Nexus-Physical-02-03.md), heartbeat program [02-04](Nexus-Physical-02-04.md), flashing client [02-05](Nexus-Physical-02-05.md), test applications [02-06](Nexus-Physical-02-06.md).
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md); 5 V by USB-C from [Nexus-Physical-05](Nexus-Physical-05.md); the UART console to the bench PC.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 401 F1, 501 F1, 503 F3 and F4, 504 F1.
- **Modes.** Booting; running; off.

## Requirements

### Nexus-Physical-02-R001

**Statement.** The node shall run from the 5 V supply of the power element.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Vehicle-R001
- Allocated-to: Nexus-Physical-02-01
- Phase: 1
- Verification: Integration Nexus-Physical-02-01-R001
- Decisions: HW-02

### Nexus-Physical-02-R002

**Statement.** The node shall connect to the bus through the on-board transceiver, on pins 8 and 10 of the 2x5 header.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-02-01, Nexus-Physical-02-03
- Phase: 1
- Verification: Integration Nexus-Physical-02-01-R002, Nexus-Physical-02-03-R001
- Decisions: HW-09

### Nexus-Physical-02-R003

**Statement.** The node shall terminate the bus at the FRDM end.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-02-01
- Phase: 1
- Verification: Integration Nexus-Physical-02-01-R003
- Decisions: HW-09

### Nexus-Physical-02-R004

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-02-04
- Phase: 1
- Verification: Integration Nexus-Physical-02-04-R001

### Nexus-Physical-02-R005

**Statement.** When the node receives a heartbeat from the STM32 node, the node shall log the heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Physical-02-04
- Phase: 1
- Verification: Integration Nexus-Physical-02-04-R002

### Nexus-Physical-02-R006

**Statement.** When the bootloader of the STM32 node requests an image, the node shall serve the image.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R013
- Allocated-to: Nexus-Physical-02-05, Nexus-Physical-02-03
- Phase: 1
- Verification: Integration Nexus-Physical-02-03-R006, Nexus-Physical-02-05-R001, Nexus-Physical-02-05-R002, Nexus-Physical-02-05-R003

### Nexus-Physical-02-R007

**Statement.** When the node powers up, the node shall boot from the SD card.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Vehicle-R019
- Allocated-to: Nexus-Physical-02-01, Nexus-Physical-02-02, Nexus-Physical-02-03
- Phase: 1
- Verification: Integration Nexus-Physical-02-01-R004, Nexus-Physical-02-02-R001, Nexus-Physical-02-03-R002

### Nexus-Physical-02-R008

**Statement.** The image of the node shall carry each released application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R019
- Allocated-to: Nexus-Physical-02-03
- Phase: 1
- Verification: Integration Nexus-Physical-02-03-R003

### Nexus-Physical-02-R009

**Statement.** When asked on the console, each program of the node shall report the name and the version of the program.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R018
- Allocated-to: Nexus-Physical-02-04, Nexus-Physical-02-05, Nexus-Physical-02-06
- Phase: 1
- Verification: Integration Nexus-Physical-02-04-R003, Nexus-Physical-02-05-R004, Nexus-Physical-02-06-R001

### Nexus-Physical-02-R010

**Statement.** The node shall present the CAN controller as a SocketCAN interface.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Vehicle-R023
- Allocated-to: Nexus-Physical-02-03
- Phase: 1
- Verification: Integration Nexus-Physical-02-03-R004

### Nexus-Physical-02-R011

**Statement.** The node shall record the bus traffic with candump, with a timestamp for each frame.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Vehicle-R023
- Allocated-to: Nexus-Physical-02-03
- Phase: 1
- Verification: Integration Nexus-Physical-02-03-R005

### Nexus-Physical-02-R012

**Statement.** The UART console of the node shall be reachable through the USB-C debug port.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R022
- Allocated-to: Nexus-Physical-02-01
- Phase: 1
- Verification: Integration Nexus-Physical-02-01-R005
- Decisions: MEC-05
