# Physical architecture

The L2 view of [method.md](method.md): the physical elements of the vehicle, what each contains, and what passes between them.
The logical view is the [logical architecture](renders/Nexus-Platform-Logical-Architecture.svg), and the join between the
two is allocation, kept in the requirements ([`../requirements/`](../requirements/README.md)): every requirement says
which element answers for it, and the generated trace shows each element's functions. Wiring, drawings and parts are
owned elsewhere: [`../hardware/README.md`](../hardware/README.md), [`../mechanical/README.md`](../mechanical/README.md),
[`../bom/BOM.md`](../bom/BOM.md). This file names the elements and their interfaces and restates none of them.

## Elements

Each has a SoI file with its definition card and its requirements.

| Element | Contains | Level 3 below it |
|---|---|---|
| [Nexus-Phys-PWR](../requirements/Nexus-Phys-PWR.md) | Pack, charger, fuses, WAGO buses, SW1 and SW2, the 5 V converter and board C, the steering UBEC, the shunt and INA226 | none |
| [Nexus-Phys-CHS](../requirements/Nexus-Phys-CHS.md) | The three-deck chassis, trays and pads, the harness board, the rear fascia | none |
| [Nexus-Phys-DRV](../requirements/Nexus-Phys-DRV.md) | Two rear motors, the Encoder Motor Module, the steering servo and linkage | none |
| [Nexus-Phys-CAN](../requirements/Nexus-Phys-CAN.md) | Bus wiring, the two terminations, the DE-9 stub, the CAN matrix | [Nexus-CAN-Utils](../requirements/Nexus-CAN-Utils.md) |
| [Nexus-Phys-STM32](../requirements/Nexus-Phys-STM32.md) | STM32F4DISCOVERY on its carrier, the CAN transceiver, the LEDs | [FBL](../requirements/Nexus-STM32-FBL.md), [FBL-Updater](../requirements/Nexus-STM32-FBL-Updater.md), [App](../requirements/Nexus-STM32-App.md) |
| [Nexus-Phys-FRDM](../requirements/Nexus-Phys-FRDM.md) | FRDM-IMX91S on the compute tray, the SD card | [Yocto image](../requirements/Nexus-IMX91-Yocto.md), [Linux apps](../requirements/Nexus-Linux-App.md), [CAN-Utils](../requirements/Nexus-CAN-Utils.md) client |

The CAN bus is an element of its own because its requirements belong to neither node and T2.3 verifies them. The
Raspberry Pi 5 joins in Phase 4 and has no element yet.

**Outside the boundary:** the operator, the charger, the environment and the **PC adapter**, which joins the bus at the DE-9
stub as a third node and is test equipment, not part of the vehicle.

## Interfaces

Between elements, and to the outside. The decisions own the detail.

| From | To | What passes | Owned by |
|---|---|---|---|
| PWR | DRV | Pack voltage to the motor driver through SW1 and a 5 A fuse; 6 V to the servo through the UBEC | HW-08, HW-11, HW-14, HW-20 |
| PWR | STM32 and FRDM | One 5 V rail, split on board C: the STM32's 5 V pin, and USB-C to the FRDM | HW-17, HW-19 |
| STM32 | CAN | CAN1 on PD0 and PD1 through an SN65HVD230 | HW-09 |
| FRDM | CAN | The on-board transceiver, CAN_H and CAN_L on the 2x5 connector | HW-09, BOM 4.2 |
| CAN | PC adapter | A male DE-9, pins 2, 3 and 7, an unterminated stub | HW-18 |
| STM32 | DRV | I2C on PB10 and PB11, servo PWM on PE9 (prepared, not driven in Phase 1) | HW-10, HW-21 |
| STM32 | PC | SWD through the on-board ST-LINK, USB on the fascia | MEC-05 |
| FRDM | PC | UART console, USB on the fascia; the SD card as boot media | MEC-05, BOM 5.2 |
| CHS | every element | Mechanical fixing, per the plate allocation | MEC-12 |

The FRDM and the STM32 meet only on the bus: there is no other signal between them.
