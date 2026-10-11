# Nexus-Physical-02-02 - SD card

Hardware element, level 2, bought: its requirements state what the node relies on, checked against the vendor documentation; the recursion stops here. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The microSD card the board boots from (BOM 5.3).
- **Interfaces.** The FRDM board [02-01](Nexus-Physical-02-01.md).
- **Allocated functions.** 501 F1.
- **Modes.** None.

## Requirements

### Nexus-Physical-02-02-R001

**Statement.** The SD card shall hold the Linux image.

- Function: Nexus-Logical-501-F01
- Derived-from: Nexus-Physical-02-R007
- Allocated-to: -
- Phase: 1
- Verification: Test T2.2
- Realised-by: HW
