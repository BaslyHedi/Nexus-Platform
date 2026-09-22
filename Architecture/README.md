# Architecture

Two folders: **why** the vehicle is the way it is, and **what** it physically looks like.

| Folder | Owns |
|---|---|
| [`Design-Decisions/`](Design-Decisions/README.md) | Every settled decision and the reasoning behind it, split by discipline - **HW / MEC / SYS / SW**. Its README owns the numbering rules and how to add one |
| [`Hardware/`](Hardware/) | Build drawings, to scale |

| Drawing | Owns |
|---|---|
| [Hardware/chassis-layout.svg](Hardware/chassis-layout.svg) | Physical placement on the three decks, plate holes, deck stack |
| [Hardware/wiring-schematic.svg](Hardware/wiring-schematic.svg) | Electrical connections, fuses, switches, gauges, signal buses |
| [Hardware/stm32-carrier.svg](Hardware/stm32-carrier.svg) | The STM32 perfboard carrier - see MEC-08 |

Printed parts and the chassis CAD live in [`../RnD-Docs/3D-Drawings/`](../RnD-Docs/3D-Drawings/README.md).
Component status, part choices and prices live in [`../RnD-Docs/BOM.md`](../RnD-Docs/BOM.md).

Still to draw: the CAN matrix (message IDs, rates, payloads).
