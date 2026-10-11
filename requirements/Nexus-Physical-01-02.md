# Nexus-Physical-01-02 - Carrier boards A and B

Hardware element, level 2, designed in this project: drawn in [stm32-carrier](../hardware/renders/stm32-carrier.svg) (MEC-15, HW-19). Its requirements are what the drawing must satisfy. Written to [../system/method.md](../system/method.md) and [rules.md](rules.md).

- **Purpose and boundary.** The two kit boards the Discovery board drops onto, with the transceiver module, the R3 jumper, R4, C2 and the headers.
- **Interfaces.** The Discovery board [01-01](Nexus-Physical-01-01.md), the transceiver module [01-03](Nexus-Physical-01-03.md), board C of the power element, the motor driver and servo headers.
- **Allocated functions.** 101 F5, 401 F1 and the prepared interfaces of 201 F1 and 202 F1.
- **Modes.** None.

## Requirements

### Nexus-Physical-01-02-R001

**Statement.** The carrier shall feed the 5 V supply into pins 3 and 4 of header P2 of the Discovery board.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Physical-01-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The carrier against the stm32-carrier drawing
- Realised-by: HW
- Decisions: HW-19

### Nexus-Physical-01-02-R002

**Statement.** The carrier shall connect PD0 to the receive output of the transceiver module.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection The carrier against the stm32-carrier drawing
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-01-02-R003

**Statement.** The carrier shall connect PD1 to the transmit input of the transceiver module.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection The carrier against the stm32-carrier drawing
- Realised-by: HW
- Decisions: HW-09

### Nexus-Physical-01-02-R004

**Statement.** The carrier shall leave the R3 termination jumper open.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Physical-01-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection The jumper
- Realised-by: HW
- Decisions: HW-19

### Nexus-Physical-01-02-R005

**Statement.** The carrier shall connect PB10 and PB11 to the motor driver header.

- Function: Nexus-Logical-201-F01
- Derived-from: Nexus-Physical-01-R016
- Allocated-to: -
- Phase: 1
- Verification: Inspection The carrier against the stm32-carrier drawing
- Realised-by: HW
- Decisions: HW-10

### Nexus-Physical-01-02-R006

**Statement.** The carrier shall connect PE9 to the servo header through R4, rated 1 kΩ.

- Function: Nexus-Logical-202-F01
- Derived-from: Nexus-Physical-01-R017
- Allocated-to: -
- Phase: 1
- Verification: Inspection The carrier against the stm32-carrier drawing
- Realised-by: HW
- Decisions: HW-19, HW-21

### Nexus-Physical-01-02-R007

**Statement.** The carrier shall pass the 6 V UBEC supply to the servo header.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Physical-01-R018
- Allocated-to: -
- Phase: 1
- Verification: Test 6 V measured at the servo header with SW1 on
- Realised-by: HW
- Decisions: HW-14

### Nexus-Physical-01-02-R008

**Statement.** The carrier shall hold C2, rated 470 µF, across the servo header.

- Function: Nexus-Logical-101-F05
- Derived-from: Nexus-Physical-01-R018
- Allocated-to: -
- Phase: 1
- Verification: Inspection C2
- Realised-by: HW
- Decisions: HW-19
