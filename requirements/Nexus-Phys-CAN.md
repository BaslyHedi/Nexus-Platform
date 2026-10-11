# Nexus-Phys-CAN - Vehicle CAN bus

Physical, level 2. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The bus itself: the wiring between the STM32 transceiver and the FRDM connector, the two terminations, the DE-9 stub on the fascia, and the CAN matrix that defines what travels on it. Its requirements belong to neither node.
- **Interfaces.** [Nexus-Phys-STM32](Nexus-Phys-STM32.md) (SN65HVD230 on PD0 and PD1), [Nexus-Phys-FRDM](Nexus-Phys-FRDM.md) (on-board transceiver, 2x5 connector). **The PC adapter**, external, joins at the DE-9 stub.
- **Allocated functions.** 401 F01; the bus half of 503 F04 and 504 F01.
- **Modes.** Idle; carrying traffic; faulted (error frames or bus-off).

## Requirements

### Nexus-Phys-CAN-R001

**Statement.** The bus shall be classic CAN at 500 kbit/s.

- Derived-from: Nexus-SubSys-401-R001
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: HW, SW
- Decisions: HW-09, SW-01

### Nexus-Phys-CAN-R002

**Statement.** The bus shall be a twisted pair CAN_H and CAN_L with a CAN_GND reference, about 30 cm between the nodes.

- Derived-from: Nexus-SubSys-401-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The wiring matches BOM 4.3
- Realised-by: HW

### Nexus-Phys-CAN-R003

**Statement.** The bus shall be terminated with 120 ohm at each of its two ends and nowhere else.

- Derived-from: Nexus-SubSys-401-R001
- Allocated-to: -
- Phase: 1
- Verification: Test Resistance across CAN_H and CAN_L, powered off, reads about 60 ohm
- Realised-by: HW
- Decisions: HW-09, HW-18, HW-19

### Nexus-Phys-CAN-R004

**Statement.** The bus shall run for 10 minutes at the heartbeat rate with no error frame and no bus-off.

- Derived-from: Nexus-SubSys-401-R001
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: HW, SW

### Nexus-Phys-CAN-R005

**Statement.** The bus shall have a male DE-9 stub on the fascia: pin 2 CAN_L, pin 3 CAN_GND, pin 7 CAN_H, pin 9 unconnected, and no terminator.

- Derived-from: Nexus-SubSys-503-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The port is wired to CiA 303-1 as stated
- Realised-by: HW
- Decisions: HW-18, MEC-13

### Nexus-Phys-CAN-R006

**Statement.** A PC adapter on the DE-9 port shall have its own termination off and a cable of 2 m or less.

- Derived-from: Nexus-SubSys-503-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The adapter's termination switch is off
- Realised-by: SYS
- Decisions: HW-18

### Nexus-Phys-CAN-R007

**Statement.** The bus identifiers and timing shall be written down and released as a tagged version of the CAN matrix.

- Derived-from: Nexus-SubSys-401-R003
- Allocated-to: Nexus-CAN-Utils
- Phase: 1
- Verification: Integration Nexus-CAN-Utils-R001 to R003

### Nexus-Phys-CAN-R008

**Statement.** The software item of the bus, the matrix and its tools, shall have its own repository with CI building it from a clean clone.

- Derived-from: Nexus-SubSys-504-R006
- Allocated-to: Nexus-CAN-Utils
- Phase: 1
- Verification: Integration Nexus-CAN-Utils-R006

### Nexus-Phys-CAN-R009

**Statement.** The bus shall carry the image's file transfer between the host's flashing client and the FBL at the update identifiers of the tagged matrix.

- Derived-from: Nexus-SubSys-504-R001
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1
- Realised-by: HW, SW
- Decisions: SW-01
