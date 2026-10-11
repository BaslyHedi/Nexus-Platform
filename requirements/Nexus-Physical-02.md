# Nexus-Physical-02 - FRDM node: Linux compute

System element, level 1. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The FRDM-IMX91S with its SD card and the Linux software. Elements below it: the board (bought) and the software items [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md), [Nexus-Linux-Apps](Nexus-Linux-Apps.md) and [Nexus-CAN-Utils](Nexus-CAN-Utils.md).
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md); 5 V by USB-C from [Nexus-Physical-05](Nexus-Physical-05.md); the UART console to the bench PC.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 401 F1, 501 F1, 503 F3 and F4, 504 F1.
- **Modes.** Booting; running; off.

## Requirements

### Nexus-Physical-02-R001

**Statement.** The node shall connect to the bus through the on-board transceiver, on pins 8 and 10 of the 2x5 header.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: -
- Phase: 1
- Verification: Inspection The header wiring
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-02-R002

**Statement.** The node shall terminate the bus with JP1 fitted.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: -
- Phase: 1
- Verification: Inspection JP1
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-02-R003

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Linux-Apps
- Phase: 1
- Verification: Integration Nexus-Linux-Apps-R001

### Nexus-Physical-02-R004

**Statement.** When the node receives a heartbeat from the STM32 node, the node shall log the heartbeat.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-Linux-Apps
- Phase: 1
- Verification: Integration Nexus-Linux-Apps-R002

### Nexus-Physical-02-R005

**Statement.** When the bootloader of the STM32 node requests an image, the node shall serve the image.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R013
- Allocated-to: Nexus-CAN-Utils, Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R005, Nexus-CAN-Utils-R001, Nexus-CAN-Utils-R002, Nexus-CAN-Utils-R003

### Nexus-Physical-02-R006

**Statement.** When the node powers up, the node shall boot from the SD card.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Vehicle-R019
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R001

### Nexus-Physical-02-R007

**Statement.** The image of the node shall carry each released application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R019
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R002

### Nexus-Physical-02-R008

**Statement.** When asked on the console, each program of the node shall report the name and the version of the program.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R018
- Allocated-to: Nexus-Linux-Apps
- Phase: 1
- Verification: Integration Nexus-Linux-Apps-R003

### Nexus-Physical-02-R009

**Statement.** The node shall present the CAN controller as a SocketCAN interface.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Vehicle-R023
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R003

### Nexus-Physical-02-R010

**Statement.** The node shall record the bus traffic with candump, with a timestamp for each frame.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Vehicle-R023
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R004

### Nexus-Physical-02-R011

**Statement.** The UART console of the node shall be reachable through the USB-C debug port.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R022
- Allocated-to: -
- Phase: 1
- Verification: Inspection A console session opens
- Realised-by: HW
- Decisions: MEC-05
