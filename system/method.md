# Systems engineering method

How NEXUS is defined, from what it must do down to the repositories that build it. This file owns the method; the
reasoning for choosing it is [SYS-03](../decisions/SYS-System-Decisions.md).

**The method is not invented here.** It follows the conventional concepts of systems engineering and uses their terms.
Clause numbers are not cited; the summary below is what each source contributes.

| Source | What NEXUS takes from it |
|---|---|
| **ISO/IEC/IEEE 15288** (system life cycle processes) | The system of interest, system elements, and **recursion**: each system element can become a system of interest of its own. The technical processes, in order: stakeholder needs, system requirements, architecture definition, then integration, verification, validation |
| **ISO/IEC/IEEE 42010** (architecture description) | An architecture is described in several **views**. The logical view and the physical view are two views of the **same** architecture, related by **correspondences** |
| **INCOSE SE Handbook**, **NASA SE Handbook** | The logical (functional) architecture is technology-independent and the physical architecture realises it; functions are **allocated** to physical elements. A requirement passed to an element unchanged is **allocated**, one created by the design at that level is **derived** |
| **OMG SysML** | The names of the relations: *derive*, *allocate*, *satisfy*, *verify* |
| **Automotive SPICE** (SYS.1 to SYS.5, SWE), **ISO 26262-4** | System requirements are allocated to system elements (hardware, software, mechanics) during system architectural design; each software element then starts its own cycle |

## Terms

| Standard term | In NEXUS |
|---|---|
| System of interest | The element being defined at the moment: the vehicle first, then each element in turn |
| Stakeholder needs | The goals and tests of each phase in [phases.md](phases.md) |
| System requirements | The vehicle's requirements, `Nexus-Vehicle` |
| Logical view: logical components and functions | The [logical architecture](renders/Nexus-Platform-Logical-Architecture.svg): components `Nexus-SubSys-DNN`, functions `Nexus-SubSys-DNN-Fnn`. They are called sub-systems there for history; in this method they are **logical components**, not part of the hierarchy |
| Physical view: system elements | The [physical architecture](renders/Nexus-Platform-Physical-Architecture.svg): elements `Nexus-Phys-NN` |
| Correspondence, allocation | Which physical element realises which logical function ([physical-architecture.md](physical-architecture.md)) |

## The system of interest and recursion

The hierarchy is the **physical breakdown**: what is built, bought or configured. At every level the same steps are
applied to the system of interest:

1. **Requirements** of the system of interest. At the top they are a black box: they name the system and its external
   actors, never its elements.
2. **Architecture definition**, in two views of the same level:
   - **Logical view**: the functions needed to meet the requirements, grouped into logical components, with the flows
     between them. It names no technology.
   - **Physical view**: the system elements the system of interest is built from, and the interfaces between them.
3. **Allocation**: every function of the logical view to the element or elements that realise it. A 1:1 case (the
   CAN bus realises the physical layer of 401) is simply one allocation; the two keep their own identities.
4. **Element requirements**: each requirement of the system of interest is **allocated** to an element as it is, or
   **derived** into new requirements on elements where the architecture adds something (a split, an interface, a number).

Each element then becomes the system of interest at the next level, with its own requirements (those of step 4), its
own logical and physical views, its own allocation.

```text
Vehicle                     requirements · logical view · physical view · allocation
  └─ STM32 node             requirements · logical view · physical view · allocation
       ├─ Discovery board    bought: the recursion stops at a BOM part
       ├─ carrier boards
       ├─ FBL software item  hand-over: the repository Nexus-STM32-FBL, targets FBL and FBL-Updater
       └─ App software item  hand-over: the repository Nexus-STM32-App
```

**Where the recursion stops.** At a **bought part** (a BOM item), and at a **software item**, which is handed over to
its repository. That repository writes its own software requirements derived from ours (SWE.1 onward) and cites our
IDs; facts travel one way, out of this repository, which holds no code. A software item is a repository; a build
target inside it (the FBL-Updater in the FBL repository) is not an element of its own.

## Requirements and their relations

A requirement belongs to **one** system of interest or element and is written in that element's file. Its relations:

| Relation | Meaning |
|---|---|
| **Derived from** | The requirement one level up that it comes from. Reads the other way as *decomposed to* |
| **Allocated to** | The element below that must meet it. **As-is**: the element meets the requirement unchanged and no new text is written. **Derived**: the element gets new requirements derived from it |
| **Function** | The function of the logical view that the requirement concerns. Requirements are not written on logical components; they trace to functions and are allocated to physical elements |
| **Verified by** | The test, inspection, analysis or demonstration that shows it is met, or the **integration** of the requirements derived from it |
| **Decisions** | The `HW-`, `MEC-`, `SYS-` or `SW-` entries that shaped it. Requirements say what, decisions say why |

HW, SW and SYS are not elements and not targets of allocation: they describe how a requirement on a leaf is realised.

## Rules

1. **One requirement, one element.** A requirement that two elements share is split into one for each and an interface
   requirement on what connects them.
2. **Write a requirement on an element only if it says something its parent did not.** Otherwise allocate the parent as-is.
3. **The logical view names no technology.** The mechanism enters in the physical view and the requirements derived for it.
4. **Black box at the top.** A vehicle requirement names the vehicle and its actors, never the STM32, the FRDM or the bus.
5. **Every requirement has a verification**, at every level.
6. **Phase is an attribute** of a requirement, not a separate tree. Phase 1 is a filter.
7. **Written to be checked**: one statement with "shall", one verifiable thing, a limit where one exists.

## The V

Each level of recursion has its verification on the right side of the V:

| Left: define | Right: verify |
|---|---|
| Stakeholder needs (phase goals) | Validation: the phase does what it was for |
| Vehicle requirements | **System verification**: the bench tests T1.1 to T2.3 |
| Vehicle architecture: elements and interfaces | **Integration**: the elements working together over their interfaces |
| Element requirements | **Element verification**, and the same again one level down |
| Software item, handed over | Verification inside the repository |

Each phase is one pass through the V over a growing scope.

## Format

Markdown, one file per system of interest or element in [`../requirements/`](../requirements/README.md), a fixed block
per requirement, checked by `tools/check-requirements.py`, which also generates the trace and the allocation matrix.
YAML as the source was weighed and rejected ([SYS-03](../decisions/SYS-System-Decisions.md)): Markdown is read and diffed in
the PR, and the checker gives the same guarantees.

## Order of work

1. Vehicle requirements (black box) from the phase goals.
2. Vehicle architecture: the logical view (exists, Draft B) and the physical view (Draft A).
3. Allocation of the logical functions to the physical elements, and the interfaces.
4. Element requirements, allocated or derived.
5. Recursion into each element that is neither a bought part nor a software item.
