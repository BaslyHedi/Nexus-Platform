# Requirements

The requirements of NEXUS, written to the method in [`../system/method.md`](../system/method.md): **one file per
system-of-interest, system element or software item**, named by its ID. Phase 1 is written in full: 84 requirements
in 14 files.

**The checker is not brought to this format yet.** [`../tools/check-requirements.py`](../tools/check-requirements.py) still
checks an earlier format and fails on these files; updating it, and generating the trace and allocation matrices from
these files, is the next step.

## The files

| Level | File | What it is |
|---|---|---|
| 0 | [Nexus-Vehicle](Nexus-Vehicle.md) | The system requirements, black box: they name the vehicle and its actors, never an element |
| 0 | [Nexus-Enabling](Nexus-Enabling.md) | The **enabling system** (ISO/IEC/IEEE 15288): repositories, CI, release tags, the `kas` build, the bench PC. Not part of the vehicle, so not derived from it |
| 1 | [Nexus-Physical-01](Nexus-Physical-01.md) STM32 node, [02](Nexus-Physical-02.md) FRDM node, [04](Nexus-Physical-04.md) CAN bus, [05](Nexus-Physical-05.md) power, [06](Nexus-Physical-06.md) chassis, [07](Nexus-Physical-07.md) rear drive, [08](Nexus-Physical-08.md) steering | The system elements of the [physical view](../system/physical-architecture.md) that exist in Phase 1. 03 (Pi 5) and 09 (sensors) start in Phase 4 |
| 2 | [Nexus-STM32-FBL](Nexus-STM32-FBL.md), [Nexus-STM32-App](Nexus-STM32-App.md) | Software items of the STM32 node. The FBL-Updater is a target of the FBL repository, not an item of its own |
| 2 | [Nexus-IMX91-Yocto](Nexus-IMX91-Yocto.md), [Nexus-Linux-Apps](Nexus-Linux-Apps.md), [Nexus-CAN-Utils](Nexus-CAN-Utils.md) | Software items of the FRDM node. `Nexus-Linux-Apps` is a class: each application gets its own file when its repository is created |

**Where the recursion stops.** The hardware elements 04 to 08 are realised directly, so their requirements are leaves. The
nodes recurse one level, into software items, which are handed over: each repository derives its own software requirements
from the ones here and cites their IDs. Bought boards (the Discovery, the FRDM) are not written as files; what the node needs
of them is a hardware leaf on the node.

**Logical components have no file.** Requirements trace to their functions (`Function`) and are met by physical elements.
The Phase 1 allocation of functions to elements is in [`../system/physical-architecture.md`](../system/physical-architecture.md).

## A file

It opens with the **definition card** of the method (purpose and boundary, interfaces, allocated functions, modes), then
one block per requirement:

```markdown
### Nexus-Physical-01-R005

**Statement.** The node shall verify an image's CRC before it starts it.

- Function: Nexus-Logical-504-F02
- Derived-from: Nexus-Vehicle-R011
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R003
```

| Field | Rule | SysML |
|---|---|---|
| **ID** | `<file ID>-Rnnn`; numbers never reused | |
| **Statement** | One sentence with "shall"; one verifiable thing; a limit where one exists | |
| **Function** | The `Nexus-Logical-DNN-Fnn` it concerns, one or more. A derived requirement may bring in a supporting function its parent does not name (the bus serving an update) | *trace* |
| **Derived-from** | The requirements one level up it comes from; `-` at level 0. Absent in the enabling system | *deriveReqt* |
| **Allocated-to** | The elements or items one level down that meet it. **Plain**: each holds requirements derived from this one. **`(as-is)`**: the element meets it unchanged and no child is written. `-`: a leaf, met here | *satisfy* |
| **Phase** | 1 to 5; never later than a parent's | |
| **Verification** | On every requirement: `Test`, `Inspection`, `Analysis` or `Demo` and the reference, or `Integration` and the children whose passing verifies it. `T1.1`-style references are the tests of [phases.md](../system/phases.md) | *verify* |
| **Realised-by** | `HW`, `SW` or `SYS` (a procedure), several allowed. Required where nothing is derived below; absent elsewhere | |
| **Decisions** | Optional; the `HW-`, `MEC-`, `SYS-` or `SW-` entries that shaped it | |

## Open points

- **The heartbeat rate has no number.** The requirements say "the rate set in the CAN matrix": the Cyphal values in
  [SW-01](../decisions/SW-Software-Decisions.md) are still to be confirmed from the specification.
- **Phase 1 start-up is traced to `Nexus-Logical-501-F01`** (manage vehicle modes and transitions), its first form being the
  Linux side booting from its own storage. The function proper is Phase 2.
- **Verifications are planned, not performed.** Only the harness checks have run; each `Test` waits for its bench test.
- **102 F4, heat and vibration, has no requirement**: there is no measured limit to write it against.
