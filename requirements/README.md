# Requirements

The requirements of NEXUS, written to the method in [`../system/method.md`](../system/method.md) and the rules in
[rules.md](rules.md), with the terms of [glossary.md](glossary.md): **one file per system-of-interest or system element**, named
by its ID. Phase 1 is written in full: 154 requirements in 21 files: 39 system, 54 subsystem, 61 component. Each
statement is in an EARS pattern.

**Checked and traced by one tool**, [`../tools/check-requirements.py`](../tools/check-requirements.py). It checks the format,
the links between levels, the trace to the drawings and the allocation table, and the mechanical writing rules, and it
generates two views that must stay in step with the files:

- [TRACE.md](TRACE.md): needs, tests, function allocation and the derivation tree, as tables;
- [renders/traceability.html](renders/traceability.html): the interactive view, opened in a browser. A canvas laid out as the
  tree, system, subsystems, components, and fitted to the window: each system is a card in its colour from the drawings,
  its requirements are bubbles, and one line joins each pair of systems with a badge for how many requirements it carries.
  Drag a card by its header to move it (positions are remembered), drag the background to pan, wheel to zoom, *Fit* to see
  everything again; *Tidy* restacks and *Reset layout* starts over. Hovering a card lights up its lines; clicking a bubble
  draws only its lineage and opens its fields. *Phase* shows one phase, or with *and earlier* everything up to it; the line
  badges count only what is shown. *Links* switches to every requirement or to none; light, dark or auto theme.

```bash
python3 tools/check-requirements.py            # fails on any problem, and when a generated view is stale
python3 tools/check-requirements.py --write    # regenerates TRACE.md and renders/traceability.html
```

## The files

One folder per level of the hierarchy, named as NASA, SEBoK and ASPICE name them; components are grouped by the subsystem
they are inside. The checker fails on a file in the wrong place.

```text
system/                           the system-of-interest (the vehicle) and the enabling system
subsystems/                       the subsystems of the vehicle (ISO 15288: its system elements)
components/Nexus-Physical-01/     the components of the STM32 node
components/Nexus-Physical-02/     the components of the FRDM node
```

| Level | Files | What they are |
|---|---|---|
| System | [Nexus-Vehicle](system/Nexus-Vehicle.md) | The system requirements, black box: they name the vehicle and its actors, never an element |
| System | [Nexus-Enabling](system/Nexus-Enabling.md) | The **enabling system** (ISO/IEC/IEEE 15288): repositories, CI, release tags, the `kas` build, the bench PC. Not part of the vehicle, so not derived from it |
| Subsystem | [Nexus-Physical-01](subsystems/Nexus-Physical-01.md) STM32 node, [02](subsystems/Nexus-Physical-02.md) FRDM node, [04](subsystems/Nexus-Physical-04.md) CAN bus, [05](subsystems/Nexus-Physical-05.md) power, [06](subsystems/Nexus-Physical-06.md) chassis, [07](subsystems/Nexus-Physical-07.md) rear drive, [08](subsystems/Nexus-Physical-08.md) steering | The system elements of the [physical view](../system/physical-architecture.md) that exist in Phase 1. 03 (Pi 5) and 09 (sensors) start in Phase 4 |
| Component | [01-01](components/Nexus-Physical-01/Nexus-Physical-01-01.md) MCU board, [01-02](components/Nexus-Physical-01/Nexus-Physical-01-02.md) carrier boards, [01-03](components/Nexus-Physical-01/Nexus-Physical-01-03.md) transceiver module, [01-04](components/Nexus-Physical-01/Nexus-Physical-01-04.md) bootloader, [01-05](components/Nexus-Physical-01/Nexus-Physical-01-05.md) FBL-Updater, [01-06](components/Nexus-Physical-01/Nexus-Physical-01-06.md) application | The elements of the STM32 node, hardware and software |
| Component | [02-01](components/Nexus-Physical-02/Nexus-Physical-02-01.md) FRDM board, [02-02](components/Nexus-Physical-02/Nexus-Physical-02-02.md) SD card, [02-03](components/Nexus-Physical-02/Nexus-Physical-02-03.md) Linux image, [02-04](components/Nexus-Physical-02/Nexus-Physical-02-04.md) heartbeat program, [02-05](components/Nexus-Physical-02/Nexus-Physical-02-05.md) flashing client, [02-06](components/Nexus-Physical-02/Nexus-Physical-02-06.md) test applications | The elements of the FRDM node, hardware and software |

**Element IDs are hierarchical**: `Nexus-Physical-01-04` is element 04 of `Nexus-Physical-01`. The local view of each node,
its elements and their connections, is in [`../system/physical-architecture.md`](../system/physical-architecture.md).

**Where the recursion stops.** The subsystems 04 to 08 state their requirements at part level, so they are leaves.
Each node is decomposed into all its elements: a bought part states what the node relies on from it; the carrier boards
state what their drawing must satisfy; a software element is handed over, and its team derives the software requirements
from the ones here.

**Requirements are allocated to elements, never to repositories.** Which repository implements which software element is
the configuration table in [Nexus-Enabling](system/Nexus-Enabling.md).

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
| **Need** | System level only: the phase-plan item it comes from, a goal, deliverable or test of [phases.md](../system/phases.md) | *trace* |
| **Function** | The `Nexus-Logical-DNN-Fnn` it concerns, one or more. A derived requirement may bring in a supporting function its parent does not name (the bus serving an update) | *trace* |
| **Derived-from** | The requirements one level up it comes from; `-` at the system level. Absent in the enabling system | *deriveReqt* |
| **Allocated-to** | The elements one level down that meet it. **Plain**: each holds requirements derived from this one. **`(as-is)`**: the element meets it unchanged and no child is written. `-`: a leaf, met here | *satisfy* |
| **Phase** | 1 to 5; never later than a parent's | |
| **Verification** | On every requirement: `Test`, `Inspection`, `Analysis` or `Demo` and the reference, or `Integration` and the children whose passing verifies it. `T1.1`-style references are the tests of [phases.md](../system/phases.md) | *verify* |
| **Realised-by** | `HW`, `SW` or `SYS` (a procedure), several allowed. Required where nothing is derived below; absent elsewhere | |
| **Decisions** | Optional; the `HW-`, `MEC-`, `SYS-` or `SW-` entries that shaped it | |

## Open points

Recorded on 2026-10-11 after the Phase 1 requirements were written. Each group is a topic for its own session. The open
questions of the method itself (status, baselines, change impact, downstream trace) are in
[`../system/method.md`](../system/method.md#open-questions-of-the-method).

**1. Missing requirements on the STM32 update path.** T1.1 runs the update while the application runs, and nothing says:
- how the application hands over to the bootloader when a software-update request arrives;
- what the bootloader does at power-up: start a valid application, or stay;
- how a valid image is recognised (header, CRC, version), beyond "the CRC matches".

These are the FBL entry rules and the valid-app rule that [phases.md](../system/phases.md) leaves to Phase 1.

**2. Values cited but not yet fixed**, each waiting for its decision:
- heartbeat rate, Cyphal node IDs, subjects and services: the CAN matrix (deliverable 1.2), checked against the Cyphal specification (SW-01 "to confirm");
- the memory map and the LED patterns: the bootloader and application repositories;
- flashing-client language, CI service, repository template, how a consumer pins a tag: `SW-nn` entries;
- the repository names of the heartbeat program and the test applications.

**3. Assumptions to confirm on the hardware:**
- `Nexus-Vehicle-R010`: the Encoder Motor Module does not drive at power-up (HW-17, not measured);
- `Nexus-Physical-02-01-R006`: the FRDM boot switch SW1 is set to 0011;
- `Nexus-Physical-02-01-R005`: the UART console is on USB-C J11 (from the BOM; the schematic shows a CH342 debug UART, the connector not confirmed);
- `Nexus-Physical-01-01-R003`: the STM32H533 sector layout lets the bootloader sectors be erased separately (RM0481 not checked);
- `Nexus-Physical-01-01-R007`: PC2 is free on the board (UM3121 lists it as plain IO; checked against the MB1814 schematic only for the JTAG pins, HW-22).

**4. Verification.** Only the harness checks have run; each `Test` waits for its bench test, and there is no field yet for a
result or its evidence (method question 5).

**5. Coverage and review:**
- 102 F4 (heat and vibration) has no requirement, for lack of a measured limit;
- Phase 1 start-up is traced to `Nexus-Logical-501-F01` as its first form;
- the checker does not yet check that a `Need` names a real deliverable, that terms are in the glossary, or combinators;
- the drawings are still marked Draft A or B, and the 154 statements have been checked by the tool, not yet read through in review.
