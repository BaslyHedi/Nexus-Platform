# Systems engineering method

How NEXUS is defined, from what it must do down to the repositories that build it. This file owns the method; the
reasoning for choosing it is [SYS-03](../decisions/SYS-System-Decisions.md).

**The method is not invented here.** It uses the concepts and terms of the references below. **NEXUS claims conformance
with none of them**: it is not assessed or certified, and it applies a small part of each. The table says, for each one,
what is taken from it and where the method goes further on its own account, so a reader can tell the two apart.

| Reference | Taken from it | NEXUS's own application |
|---|---|---|
| **ISO/IEC/IEEE 15288:2023**, *Systems and software engineering: System life cycle processes* | The terms **system-of-interest**, **system element** and **enabling system**, and their recursive use: an element can be treated as a system-of-interest in turn. The technical processes used here: stakeholder needs and requirements definition, system requirements definition, system architecture definition, integration, verification, validation | Where the recursion stops (a bought part, a software item handed over to its repository) |
| **ISO/IEC/IEEE 42010:2022**, *Software, systems and enterprise: Architecture description* | An architecture description is made of **views**, each governed by a **viewpoint**, with **correspondences** between elements of different views. The standard prescribes no method, notation or particular viewpoints | The two viewpoints, **logical** and **physical**, and the use of allocation as the correspondence between them |
| **SEBoK** (Systems Engineering Body of Knowledge, INCOSE, IEEE Computer Society and SERC), articles *System Requirements Definition*, *Logical Architecture*, *System Architecture Design Definition* | The logical architecture is "as much as possible, independent of implementation decisions". Physical items "provide a design implementation for the corresponding logical element". Allocation "is the process by which the requirements at one level of the physical architecture are assigned" | The drawing conventions and IDs of the two views |
| **NASA Systems Engineering Handbook**, NASA/SP-2016-6105 Rev 2 | Requirements flow down to lower-level elements, which then hold **allocated requirements** (assigned from the parent) and **derived requirements**: "requirements arising from constraints, ... factors introduced by the selected architecture, and the design" (Figure 4.2-3, glossary) | The label **as-is** for an allocated requirement that the element meets unchanged, with no child text |
| **OMG SysML** (v1.x requirement and allocation relations) | The relations: *deriveReqt* between requirements, *satisfy* from an element to a requirement it meets, *verify* from a test case to a requirement, *allocate* from a function to the structure that performs it, *trace* as the generic link | Markdown fields in place of a model (see the relations below) |
| **Automotive SPICE**, PAM 4.0 (VDA QMC) | The shape of the V: SYS.1 Requirements Elicitation, SYS.2 System Requirements Analysis, SYS.3 System Architectural Design, SYS.4 System Integration and Integration Verification, SYS.5 System Verification, and the hand-over from system to software processes (SWE.1 onward) | Used as orientation only; no assessment, no work products as such |

Functional safety (ISO 26262), SOTIF (ISO 21448) and cybersecurity (ISO/SAE 21434) are **not** part of this method. Where a
later phase needs hazard analysis or a safety case, it is added as its own decision.

## Terms

| Term, and where it comes from | In NEXUS |
|---|---|
| System-of-interest (15288) | The element being defined at the moment: the vehicle first, then each element in turn |
| Stakeholder needs (15288) | The goals and tests of each phase in [phases.md](phases.md) |
| System requirements (15288) | The vehicle's requirements, `Nexus-Vehicle` |
| Logical view (42010 view, SEBoK logical architecture): logical components and functions | The [logical architecture](renders/Nexus-Platform-Logical-Architecture.svg): components `Nexus-Logical-DNN`, functions `Nexus-Logical-DNN-Fnn`. They were called sub-systems (`Nexus-SubSys-DNN`) until 2026-10-11 and kept their numbers. They are **logical components**, not part of the hierarchy |
| Physical view (42010 view), system elements (15288) | The [physical architecture](renders/Nexus-Platform-Physical-Architecture.svg): elements `Nexus-Physical-NN` |
| Correspondence (42010), allocation (SysML *allocate*) | Which physical element performs which logical function ([physical-architecture.md](physical-architecture.md)) |
| Enabling system (15288) | What the vehicle needs through its life cycle without being part of it: repositories, CI, release tags, the image build, the bench PC. Its own requirements, `Nexus-Enabling`, not derived from the vehicle's |
| Function number | The `Fnn` printed before each function on the logical drawing |

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
Vehicle (system-of-interest)          requirements · logical view · physical view · allocation
  └─ Nexus-Physical-01 STM32 node     requirements · local physical view · allocation to its elements
       ├─ 01-01 Discovery board        hardware, bought: recursion stops (COTS)
       ├─ 01-02 Carrier boards         hardware, designed here (hardware/): recursion stops at the drawing
       ├─ 01-03 Transceiver module     hardware, bought
       ├─ 01-04 Bootloader             software element: handed over
       ├─ 01-05 FBL-Updater            software element: handed over
       └─ 01-06 Application            software element: handed over
```

**Element IDs are hierarchical**: an element inside `Nexus-Physical-01` is `Nexus-Physical-01-NN`, so its parent shows in its ID.
A node is decomposed into **all** its elements, hardware and software, and its requirements are allocated across them.

**Where the recursion stops.** At a **bought part**, whose requirements state what the vehicle relies on from it and are
checked against its vendor documentation; at a **hardware element designed here**, whose requirements its drawing must
satisfy; and at a **software element**, which is handed over. The team of a software element writes its software
requirements from ours (ASPICE SWE.1 onward) and cites our IDs; facts travel one way, out of this repository, which holds no code.

**Requirements are allocated to elements, never to repositories.** A repository is configuration management, part of the
enabling system: it holds the implementation of one or more software elements (the bootloader and the FBL-Updater share
one). The configuration table in [`../requirements/Nexus-Enabling.md`](../requirements/Nexus-Enabling.md) says which
repository and which build target implement each software element.

## Requirements and their relations

A requirement belongs to **one** system of interest or element and is written in that element's file. Its relations:

| Field | Meaning | SysML relation |
|---|---|---|
| **Derived from** | The requirement one level up that it comes from. Reads the other way as *decomposed to* | *deriveReqt* |
| **Allocated to** | The element that must meet it. **As-is** (NEXUS label): the element meets it unchanged and no new text is written. Otherwise the element gets **derived** requirements, each pointing back with *Derived from* | *satisfy*, from the element to the requirement |
| **Function** | The function of the logical view that the requirement concerns. Requirements are not written on logical components; they trace to functions and are met by physical elements | *trace* |
| **Verified by** | The test, inspection, analysis or demonstration that shows it is met, or the **integration** of the requirements derived from it | *verify* |
| **Decisions** | The `HW-`, `MEC-`, `SYS-` or `SW-` entries that shaped it. Requirements say what, decisions say why | none (NEXUS) |

The allocation of a **function** to a physical element is SysML *allocate*. It is kept separately from the requirements
([physical-architecture.md](physical-architecture.md)).

HW, SW and SYS are not elements and not targets of allocation: they describe how a requirement on a leaf is realised.

## Rules

**Requirement rules** are in [`../requirements/rules.md`](../requirements/rules.md): the INCOSE Guide to Writing Requirements
(characteristics C1 to C15, rules R1 to R42), ISO/IEC/IEEE 29148 and the EARS sentence patterns, with what each level adds.

**Architecture rules**, for the two views:

1. **The logical view names no technology.** The mechanism enters in the physical view and in the requirements derived for it.
2. **Each component and element keeps its own ID.** The two views are related by allocation only.
3. **Phase is an attribute**, of a component, an element and a requirement, not a separate tree. Phase 1 is a filter.

## The V

Each level of recursion has its verification on the right side of the V:

| Left: define | Right: verify |
|---|---|
| Stakeholder needs (phase goals) | Validation: the phase does what it was for |
| Vehicle requirements | **System verification**: the bench tests T1.1 to T2.3 |
| Vehicle architecture: elements and interfaces | **Integration**: the elements working together over their interfaces |
| Element requirements | **Element verification**, and the same again one level down |
| Software element, handed over | Software verification by the team of the element (SWE.4 to SWE.6) |

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
5. Recursion into each element that is neither a bought part, nor a hardware element drawn here, nor a software element.
