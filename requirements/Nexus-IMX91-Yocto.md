# Nexus-IMX91-Yocto - FRDM Yocto image (repository)

Component, level 3. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The `meta-nexus` layer, the `kas` manifest and the image recipe: kernel and device-tree changes and the assembly of released apps into a bootable image.
- **Interfaces.** Fetches applications by tag, including [Nexus-Linux-App](Nexus-Linux-App.md) repositories and the [Nexus-CAN-Utils](Nexus-CAN-Utils.md) flashing client; the NXP BSP.
- **Allocated functions.** From the FRDM node: boot, SocketCAN, the apps, the flashing client.
- **Modes.** Build time and run time.

## Requirements

### Nexus-IMX91-Yocto-R001

**Statement.** The image shall build with kas from a clean clone and fetch each application at its release tag.

- Derived-from: Nexus-Phys-FRDM-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-IMX91-Yocto-R002

**Statement.** The image shall boot from the SD card on the FRDM-IMX91 to a login.

- Derived-from: Nexus-Phys-FRDM-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-IMX91-Yocto-R003

**Statement.** The image shall carry every released application, and each shall run and print its name and version.

- Derived-from: Nexus-Phys-FRDM-R006
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: SW

### Nexus-IMX91-Yocto-R004

**Statement.** The image shall include SocketCAN support for the FRDM's CAN controller and candump.

- Derived-from: Nexus-Phys-FRDM-R004
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: SW

### Nexus-IMX91-Yocto-R005

**Statement.** The image shall include the flashing client from a tagged Nexus-CAN-Utils release.

- Derived-from: Nexus-Phys-FRDM-R005
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: SW

### Nexus-IMX91-Yocto-R006

**Statement.** The Yocto repository shall build the image in CI from a clean clone and cite decision IDs back to Nexus-Platform.

- Derived-from: Nexus-Phys-FRDM-R007
- Allocated-to: -
- Phase: 1
- Verification: Inspection The CI run
- Realised-by: SW
