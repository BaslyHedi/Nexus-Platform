# Nexus-Phys-PWR - Power: pack, protection, switching and rails

Physical, level 2. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** Everything between the 3S pack and the supplied loads: pack (BOM 3.1), charger, fuses, WAGO buses, SW1 and SW2, the 5 V converter and its split on board C, the steering UBEC, the shunt and INA226.
- **Interfaces.** Supplies [Nexus-Phys-DRV](Nexus-Phys-DRV.md) (motor driver at pack voltage, servo through the UBEC), [Nexus-Phys-STM32](Nexus-Phys-STM32.md) and [Nexus-Phys-FRDM](Nexus-Phys-FRDM.md) (5 V); carried by [Nexus-Phys-CHS](Nexus-Phys-CHS.md); the charger is external.
- **Allocated functions.** 101 F01 to F05; the power half of 201 F01, 202 F01 and 501 F02.
- **Modes.** Pack disconnected; pack connected and switches off (the segment to the switches is live); SW2 on; SW1 on.

## Requirements

### Nexus-Phys-PWR-R001

**Statement.** SW1 shall switch the motor driver and the steering UBEC, and SW2 shall switch the 5 V converter, each independently of the other.

- Derived-from: Nexus-SubSys-101-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection Harness checks of 2026-10-11 (hardware/README.md)
- Realised-by: HW
- Decisions: HW-08, HW-14

### Nexus-Phys-PWR-R002

**Statement.** No switch shall sit in the pack's main current path.

- Derived-from: Nexus-SubSys-101-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection The pack connector is the only disconnect in the main path
- Realised-by: HW
- Decisions: HW-08

### Nexus-Phys-PWR-R003

**Statement.** The pack feed shall be fused at 7.5 A, and the motor-driver and UBEC branches at 5 A each.

- Derived-from: Nexus-SubSys-101-R003
- Allocated-to: -
- Phase: 1
- Verification: Inspection Three fuses fitted, values as listed
- Realised-by: HW
- Decisions: HW-13, HW-20

### Nexus-Phys-PWR-R004

**Statement.** One 5 V converter shall feed both computers, split on board C.

- Derived-from: Nexus-SubSys-101-R004
- Allocated-to: -
- Phase: 1
- Verification: Test 5 V measured at the FRDM J1 and the STM32 5V pin with SW2 on
- Realised-by: HW
- Decisions: HW-17, HW-19

### Nexus-Phys-PWR-R005

**Statement.** The steering servo shall be supplied by a 6 V UBEC fed through SW1, and from no 5 V rail.

- Derived-from: Nexus-SubSys-101-R004
- Allocated-to: -
- Phase: 1
- Verification: Inspection The servo lead goes to the UBEC output through the carrier, not to a 5 V pin
- Realised-by: HW
- Decisions: HW-11, HW-14
