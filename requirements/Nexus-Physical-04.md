# Nexus-Physical-04 - Vehicle CAN bus

System element, level 1. Written to [../system/method.md](../system/method.md).

- **Purpose and boundary.** The bus wiring, its two terminations and the DE-9 stub on the fascia. What travels on it is defined by the CAN matrix, released by the enabling system.
- **Interfaces.** [Nexus-Physical-01](Nexus-Physical-01.md) and [Nexus-Physical-02](Nexus-Physical-02.md) at its two ends; the bench PC at the DE-9 stub.
- **Allocated functions.** See the [allocation](../system/physical-architecture.md): 401 F1, 503 F4, 504 F1.
- **Modes.** Idle; carrying traffic; faulted (error frames or bus-off).

## Requirements

### Nexus-Physical-04-R001

**Statement.** The bus shall be classic CAN at 500 kbit/s.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010, Nexus-Vehicle-R011
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: HW, SW
- Decisions: HW-09, SW-01

### Nexus-Physical-04-R002

**Statement.** The bus shall be a twisted pair CAN_H and CAN_L with a CAN_GND reference, about 30 cm between the nodes.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010
- Allocated-to: -
- Phase: 1
- Verification: Inspection The wiring matches BOM 4.3
- Realised-by: HW

### Nexus-Physical-04-R003

**Statement.** The bus shall be terminated with 120 ohm at each of its two ends and nowhere else.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010, Nexus-Vehicle-R018
- Allocated-to: -
- Phase: 1
- Verification: Test Resistance across CAN_H and CAN_L, powered off, reads about 60 ohm
- Realised-by: HW
- Decisions: HW-09, HW-18, HW-19

### Nexus-Physical-04-R004

**Statement.** The bus shall have a male DE-9 stub on the fascia, pin 2 CAN_L, pin 3 CAN_GND, pin 7 CAN_H, pin 9 unconnected, with no terminator.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Vehicle-R018
- Allocated-to: -
- Phase: 1
- Verification: Inspection The port is wired to CiA 303-1 as stated
- Realised-by: HW
- Decisions: HW-18, MEC-13

### Nexus-Physical-04-R005

**Statement.** The traffic on the bus (heartbeat, node info, update transfer) shall use the identifiers and timing of the CAN matrix released by tag in Nexus-CAN-Utils.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010, Nexus-Vehicle-R011, Nexus-Vehicle-R012
- Allocated-to: -
- Phase: 1
- Verification: Test T1.1 and T2.3, against the tagged matrix
- Realised-by: SW, SYS
- Decisions: SW-01

### Nexus-Physical-04-R006

**Statement.** The bus shall carry the heartbeats of both nodes for 10 minutes with no error frame and no bus-off.

- Function: Nexus-Logical-401-F01
- Derived-from: Nexus-Vehicle-R010
- Allocated-to: -
- Phase: 1
- Verification: Test T2.3
- Realised-by: HW, SW
