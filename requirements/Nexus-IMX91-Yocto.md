# Nexus-IMX91-Yocto - FRDM Linux image (software item)

Software item, level 2, handed over to the repository `Nexus-IMX91-Yocto`. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The `meta-nexus` layer, the image recipe, kernel and device-tree changes.
- **Interfaces.** Assembles [Nexus-Linux-Apps](Nexus-Linux-Apps.md) and the [Nexus-CAN-Utils](Nexus-CAN-Utils.md) client by tag; the NXP BSP.
- **Allocated functions.** From [Nexus-Physical-02](Nexus-Physical-02.md): 501 F1, 503 F3, 504 F1.
- **Modes.** Booting; running.

## Requirements

### Nexus-IMX91-Yocto-R001

**Statement.** When the FRDM-IMX91 powers up, the image shall boot from the SD card to a login prompt.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Physical-02-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-IMX91-Yocto-R002

**Statement.** The image shall carry each released application at the release tag of the application.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-IMX91-Yocto-R003

**Statement.** The image shall include SocketCAN support for the FlexCAN controller.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Physical-02-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-IMX91-Yocto-R004

**Statement.** The image shall include the candump tool.

- Function: Nexus-Logical-503-F03
- Derived-from: Nexus-Physical-02-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-IMX91-Yocto-R005

**Statement.** The image shall include the flashing client of a tagged Nexus-CAN-Utils release.

- Function: Nexus-Logical-504-F01
- Derived-from: Nexus-Physical-02-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW
