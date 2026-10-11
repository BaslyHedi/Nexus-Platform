# System Definition

What NEXUS must **do**, decomposed top-down. This is the logical view of the vehicle architecture ([method.md](method.md)) - it names functions and
the sub-systems that own them, not the boards that run them. Hardware allocation comes later
and lives in [`../hardware/README.md`](../hardware/README.md), with the reasoning in
[`../decisions/README.md`](../decisions/README.md).

Each drawing is an `.svg` - the editable source and the only copy. **No PDFs.** They are
generated once, when the design is frozen; until then the SVG is the truth and a stale PDF
beside it is just a second thing to get wrong. To read one, open the SVG in a browser; to
render, point headless Chrome at it. Same rule as [`../hardware/README.md`](../hardware/README.md).

| Drawing | Owns |
|---|---|
| [Nexus-Platform-Logical-Architecture](renders/Nexus-Platform-Logical-Architecture.svg) | The sub-system decomposition - every `Nexus-SubSys-DNN` ID, its name, the phase it first exists in and key flows. **Generated** by [`scripts/Nexus-Platform-Logical-Architecture.py`](scripts/Nexus-Platform-Logical-Architecture.py): edit the script, never the SVG, and `python3 tools/check-drawings.py` fails if they drift |
| [Nexus-Platform-Physical-Architecture](renders/Nexus-Platform-Physical-Architecture.svg) | The physical view: every system element `Nexus-Phys-NN`, what it is built from, its phase and the connections between elements. **Generated** by [`scripts/Nexus-Platform-Physical-Architecture.py`](scripts/Nexus-Platform-Physical-Architecture.py) |
| [physical-architecture.md](physical-architecture.md) | How the physical view relates to the logical view, ahead of the allocation |
| [method.md](method.md) | The systems engineering method, using the concepts of ISO/IEC/IEEE 15288:2023 and 42010:2022, SEBoK, the NASA SE Handbook and SysML, with no conformance claimed: system of interest and recursion, the logical and physical views, allocation, requirements ([SYS-03](../decisions/SYS-System-Decisions.md)) |
| [phases.md](phases.md) | The five phases, the goal and exit criteria of each, Phase 1 in full including the repositories ([SYS-02](../decisions/SYS-System-Decisions.md)) |

The layout owns the list of sub-systems. Do not restate it here; link to it.

## IDs

| Level | Format | Example |
|---|---|---|
| Sub-system | `Nexus-SubSys-DNN` - D = functional domain (1–5), NN = sub-system in it | `Nexus-SubSys-203` |
| Function | `Nexus-SubSys-DNN-Fnn` | `Nexus-SubSys-203-F02` |
| Physical element | `Nexus-Phys-NN` ([physical-architecture.md](physical-architecture.md)) | `Nexus-Phys-01` |

IDs are never reused. A retired sub-system keeps its number.

## Workflow

1. **Logical architecture** - settle the decomposition, and which phase each sub-system starts in. *Draft B*
2. **Physical architecture** - the physical view: the system elements and the connections between them. *Draft B, for review*
3. **Allocation** - each function of the logical architecture to the physical element or elements that realise it.
4. **One drawing per sub-system** - `Nexus-SubSys-DNN-<Name>.svg`, showing the
   functions it realises and its interfaces to other sub-systems.
5. **Requirements**, derived level by level and allocated, per [method.md](method.md), traced to the `-Fnn` IDs. *a first pass is in [requirements/](../requirements/README.md); it predates steps 2 and 3 and is redone on them*
