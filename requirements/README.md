# Requirements

The requirements of NEXUS, written to the method in [`../system/method.md`](../system/method.md) and the rules in
[rules.md](rules.md), with the terms of [glossary.md](glossary.md): **one file per system-of-interest or system element**, named
by its ID. Phase 1 is written in full: 154 requirements in 21 files, 39 at level 0, 54 at level 1, 61 at level 2. Each
statement is in an EARS pattern.

**Checked and traced by one tool**, [`../tools/check-requirements.py`](../tools/check-requirements.py). It checks the format,
the links between levels, the trace to the drawings and the allocation table, and the mechanical writing rules, and it
generates two views that must stay in step with the files:

- [TRACE.md](TRACE.md): needs, tests, function allocation and the derivation tree, as tables;
- [renders/traceability.html](renders/traceability.html): the interactive view, opened in a browser. Each system is a card in
  its colour from the drawings, in three columns by level; its requirements are bubbles, and lines join each parent to its
  children. Cards fold one by one, by column or all at once; clicking a bubble highlights its lineage and opens its fields;
  a filter, and light, dark or automatic theme.

```bash
python3 tools/check-requirements.py            # fails on any problem, and when a generated view is stale
python3 tools/check-requirements.py --write    # regenerates TRACE.md and renders/traceability.html
```

## The files

| Level | File | What it is |
|---|---|---|
| 0 | [Nexus-Vehicle](Nexus-Vehicle.md) | The system requirements, black box: they name the vehicle and its actors, never an element |
| 0 | [Nexus-Enabling](Nexus-Enabling.md) | The **enabling system** (ISO/IEC/IEEE 15288): repositories, CI, release tags, the `kas` build, the bench PC. Not part of the vehicle, so not derived from it |
| 1 | [Nexus-Physical-01](Nexus-Physical-01.md) STM32 node, [02](Nexus-Physical-02.md) FRDM node, [04](Nexus-Physical-04.md) CAN bus, [05](Nexus-Physical-05.md) power, [06](Nexus-Physical-06.md) chassis, [07](Nexus-Physical-07.md) rear drive, [08](Nexus-Physical-08.md) steering | The system elements of the [physical view](../system/physical-architecture.md) that exist in Phase 1. 03 (Pi 5) and 09 (sensors) start in Phase 4 |
| 2 | [01-01](Nexus-Physical-01-01.md) Discovery board, [01-02](Nexus-Physical-01-02.md) carrier boards, [01-03](Nexus-Physical-01-03.md) transceiver module, [01-04](Nexus-Physical-01-04.md) bootloader, [01-05](Nexus-Physical-01-05.md) FBL-Updater, [01-06](Nexus-Physical-01-06.md) application | The elements of the STM32 node, hardware and software |
| 2 | [02-01](Nexus-Physical-02-01.md) FRDM board, [02-02](Nexus-Physical-02-02.md) SD card, [02-03](Nexus-Physical-02-03.md) Linux image, [02-04](Nexus-Physical-02-04.md) heartbeat program, [02-05](Nexus-Physical-02-05.md) flashing client, [02-06](Nexus-Physical-02-06.md) test applications | The elements of the FRDM node, hardware and software |

**Element IDs are hierarchical**: `Nexus-Physical-01-04` is element 04 of `Nexus-Physical-01`. The local view of each node,
its elements and their connections, is in [`../system/physical-architecture.md`](../system/physical-architecture.md).

**Where the recursion stops.** The hardware elements 04 to 08 state their requirements at part level, so they are leaves.
Each node is decomposed into all its elements: a bought part states what the node relies on from it; the carrier boards
state what their drawing must satisfy; a software element is handed over, and its team derives the software requirements
from the ones here.

**Requirements are allocated to elements, never to repositories.** Which repository implements which software element is
the configuration table in [Nexus-Enabling](Nexus-Enabling.md).

**Logical components have no file.** Requirements trace to their functions (`Function`) and are met by physical elements.
The Phase 1 allocation of functions to elements is in [`../system/physical-architecture.md`](../system/physical-architecture.md).

## A file

It opens with the **definition card** of the method (purpose and boundary, interfaces, allocated functions, modes), then
one block per requirement:

```markdown
### Nexus-Physical-01-R009

**Statement.** If a download is interrupted, then the node shall remain ready for a new download.

- Function: Nexus-Logical-504-F03
- Derived-from: Nexus-Vehicle-R014
- Allocated-to: Nexus-Physical-01-04
- Phase: 1
- Verification: Integration Nexus-Physical-01-04-R006
```

| Field | Rule | SysML |
|---|---|---|
| **ID** | `<file ID>-Rnnn`; numbers never reused | |
| **Statement** | One sentence in an EARS pattern, written to [rules.md](rules.md) | |
| **Need** | Level 0 only: the phase-plan item it comes from, a goal, deliverable or test of [phases.md](../system/phases.md) | *trace* |
| **Function** | The `Nexus-Logical-DNN-Fnn` it concerns, one or more. A derived requirement may bring in a supporting function its parent does not name (the bus serving an update) | *trace* |
| **Derived-from** | The requirements one level up it comes from; `-` at level 0. Absent in the enabling system | *deriveReqt* |
| **Allocated-to** | The elements one level down that meet it. **Plain**: each holds requirements derived from this one. **`(as-is)`**: the element meets it unchanged and no child is written. `-`: a leaf, met here | *satisfy* |
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
