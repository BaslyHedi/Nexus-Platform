# Nexus-Physical-02 - FRDM node: Linux compute

System element, level 1. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The FRDM-IMX91S with its SD card and the Linux software. Elements below it: the board (bought) and the software items [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md), [Nexus-Linux-Apps](Nexus-Linux-Apps.md) and [Nexus-CAN-Utils](Nexus-CAN-Utils.md).
- **Interfaces.** The bus [Nexus-Physical-04](Nexus-Physical-04.md); 5 V by USB-C from [Nexus-Physical-05](Nexus-Physical-05.md); the UART console to the bench PC.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 401 F1, 501 F1, 503 F3 and F4, 504 F1.
- **Modes.** Booting; running; off.

## Requirements

### Nexus-Physical-02-R001

**Statement.** The node shall reach the bus through its on-board transceiver, CAN_H and CAN_L on pins 8 and 10 of its 2x5 header, with JP1 fitted to terminate this end.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010, Nexus-Vehicle-R012
- Allocated-to: -
- Phase: 1
- Verification: Inspection The wiring and JP1 as stated
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-02-R002

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix and log each heartbeat it receives from the STM32 node.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010
- Allocated-to: Nexus-Linux-Apps
- Phase: 1
- Verification: Integration Nexus-Linux-Apps-R001

### Nexus-Physical-02-R003

**Statement.** The node shall serve an application image to the STM32 node's bootloader on request.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Vehicle-R012
- Allocated-to: Nexus-CAN-Utils, Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-CAN-Utils-R001, Nexus-CAN-Utils-R002 and Nexus-IMX91-Yocto-R004

### Nexus-Physical-02-R004

**Statement.** The node shall boot from its SD card into an image that carries the released applications.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Vehicle-R017
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R001 and Nexus-IMX91-Yocto-R002

### Nexus-Physical-02-R005

**Statement.** Each program the node runs shall report its own name and version.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R016
- Allocated-to: Nexus-Linux-Apps
- Phase: 1
- Verification: Integration Nexus-Linux-Apps-R002

### Nexus-Physical-02-R006

**Statement.** The node shall present its CAN controller as a SocketCAN interface on which candump records the traffic with timestamps.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Vehicle-R020
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R003

### Nexus-Physical-02-R007

**Statement.** The node's UART console shall be reachable through its USB-C debug port, brought to the fascia.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R019
- Allocated-to: -
- Phase: 1
- Verification: Inspection A console session opens from the fascia port
- Realised-by: HW
- Decisions: MEC-05
