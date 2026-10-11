# Nexus-Phys-FRDM - FRDM node: Linux compute

Physical, level 2. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The FRDM-IMX91S on the compute tray, its SD card, and the Linux software built into the image.
- **Interfaces.** [Nexus-Phys-CAN](Nexus-Phys-CAN.md); 5 V by USB-C from [Nexus-Phys-PWR](Nexus-Phys-PWR.md); UART console to an external PC.
- **Allocated functions.** The Linux side of 504 F01, 401 F01, 503 F03 and F04.
- **Modes.** Booting; running; powered off.

## Requirements

### Nexus-Phys-FRDM-R001

**Statement.** The node shall reach the bus through its on-board transceiver, CAN_H and CAN_L on pins 8 and 10 of the 2x5 connector, with JP1 fitted to terminate this end.

- Derived-from: Nexus-SubSys-401-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The wiring and JP1 as stated
- Realised-by: HW
- Decisions: HW-09

### Nexus-Phys-FRDM-R002

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix and observe the STM32's.

- Derived-from: Nexus-SubSys-401-R002
- Allocated-to: Nexus-Linux-App
- Phase: 1
- Verification: Integration Nexus-Linux-App-R001

### Nexus-Phys-FRDM-R003

**Statement.** The node's UART console shall be reachable from the fascia.

- Derived-from: Nexus-SubSys-503-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection A console session opens through the fascia USB port
- Realised-by: HW
- Decisions: MEC-05

### Nexus-Phys-FRDM-R004

**Statement.** The node shall present its CAN controller as a SocketCAN interface on which candump runs.

- Derived-from: Nexus-SubSys-503-R003
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R004

### Nexus-Phys-FRDM-R005

**Statement.** The node shall run a flashing client that serves an application image to the STM32's FBL.

- Derived-from: Nexus-SubSys-504-R001
- Allocated-to: Nexus-CAN-Utils, Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-CAN-Utils-R004, Nexus-CAN-Utils-R005 and Nexus-IMX91-Yocto-R005

### Nexus-Phys-FRDM-R006

**Statement.** The node shall boot, from an SD card, an image assembled from released applications.

- Derived-from: Nexus-SubSys-504-R005
- Allocated-to: Nexus-IMX91-Yocto
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R001 to R003

### Nexus-Phys-FRDM-R007

**Statement.** Every software item of the node shall have its own repository with CI building it from a clean clone.

- Derived-from: Nexus-SubSys-504-R006
- Allocated-to: Nexus-IMX91-Yocto, Nexus-Linux-App
- Phase: 1
- Verification: Integration Nexus-IMX91-Yocto-R006 and Nexus-Linux-App-R003

### Nexus-Phys-FRDM-R008

**Statement.** Each Linux application shall be a separate program that reports its own name and version.

- Derived-from: Nexus-SubSys-504-R005
- Allocated-to: Nexus-Linux-App
- Phase: 1
- Verification: Integration Nexus-Linux-App-R002
