# Requirements method

How NEXUS requirements are written, derived and allocated. This file owns the method; the reasoning for
choosing it is [SYS-03](../decisions/SYS-System-Decisions.md). The requirements are in
[`../requirements/`](../requirements/README.md).

## The idea in one paragraph

A requirement belongs to exactly one **system of interest** (SoI). **Allocating** it to a child SoI either passes
it on unchanged (**as-is**) or produces a **derived** requirement on that child, when the allocation adds something. Repeat down four levels. Derivation is the vertical link between
requirements, and it reads both ways: *derived from* going up, *decomposed to* going down. Allocation is the
link from a requirement or function to the SoI that must satisfy it. HW, SW and SYS are **not** allocation
targets: they are an attribute of a leaf ("realised by hardware, software or procedure").

## System of interest

Any element treated as a black box with a boundary at that moment. It is logical or physical, and the kind
is declared, because it decides what an allocation to it means.

| Kind | Example | Carries | Its requirements say |
|---|---|---|---|
| **Vehicle** | NEXUS | The whole; the only SoI with no parent | What it must do for the operator and the environment |
| **Logical** | `Nexus-SubSys-504` Software Update | A grouping of functions, no location | What function is performed and the behaviour at its interfaces, **independent of implementation** |
| **Physical** | STM32 node, CAN bus, power distribution, chassis | A thing you can touch, with a place and a BOM entry | What it does, **plus** physical constraints: power, size, timing, capacity |
| **Component** | FBL, Yocto image, carrier board | A part inside a physical node, usually a repository | The same, scoped to its own boundary |

The same real thing can appear at two levels: the STM32 is a physical SoI at L2, while "flash bootloader
capability" is a logical function at L1. They are linked by allocation and are not the same item. That is how
one set of requirements yields a logical and a physical architecture.

The **CAN bus is its own physical SoI**, not a part of either node. Its requirements (bit rate, termination,
bus-off behaviour) belong to neither end, and they are what T2.3 verifies. The PC adapter is **external test
equipment**, outside the vehicle boundary, and is an actor in the context of the bus.

## The four levels

| Level | Name | Content | Where it lives |
|---|---|---|---|
| **L0** | Vehicle | Needs and phase goals, written as "the vehicle shall ..." | [`../requirements/`](../requirements/README.md) |
| **L1** | Logical | Sub-systems and their functions, `Nexus-SubSys-DNN-Fnn` | drawn in [Nexus-Platform-Logical-Architecture](renders/Nexus-Platform-Logical-Architecture.svg) |
| **L2** | Physical | The nodes, the bus, power distribution, chassis, drive train | [physical-architecture.md](physical-architecture.md) |
| **L3** | Component | Parts of a node, down to **the repository** | the repository names of [phases.md](phases.md) |

**L0 to L1 is derivation**: the same question, refined. **L1 to L2 is allocation**: the question changes from
*what* to *who does it*, and it is many-to-many (501 Supervision is partly fuses and switches, partly the STM32,
partly Linux). **L2 to L3 is allocation plus derivation** again.

**The stopping point.** This repository holds the definition and no code, so requirements stop at "allocated
to repository X". Each repository then chooses its solution and writes its own requirements, derived from ours,
citing our IDs. Facts travel one way, out of here. Hardware stops one level earlier: the BOM lists parts and not
sub-assemblies, so a hardware requirement is a leaf on its physical node.

**SoI codes are the IDs that already exist.** A logical SoI is `Nexus-SubSys-DNN`, a component is its repository
name, and a requirement is `<code>-Rnnn`. Only the vehicle and the physical elements needed a new code.

## Allocated and derived

The logical and the physical architecture would collide if every L1 requirement became an L2 requirement with a
new subject, so the two are told apart:

- An **allocated (as-is)** requirement passes to an element **unchanged**. It is a link and has no new text. The element
  inherits it and answers for it.
- A **derived** requirement is new text. It exists only because the allocation added something: a number, an
  interface, a split, or a physical property.

**Write a requirement on an element only if it says something its parent did not.** Two cases show it. Where a
logical sub-system and a physical element are almost one thing (401 In-Vehicle Communication and the CAN bus), the
bus inherits the logical requirement as is and adds only what is physical: 500 kbit/s, the terminations, the DE-9
stub. Where a function is cut up (504 delivering an image), each part is a derived requirement on the element that
does it, and the cut leaves an interface requirement on the bus between them.

The logical level stays implementation-free, and a physical card reads as what it **inherits** (the as-is
allocations) and what it **adds** (its own requirements). Both are generated from the requirements, so neither is written twice.

## The definition card

Every SoI, at every level, has the same short card:

- **Purpose and boundary**: what it is for, what is inside and what is not
- **Interfaces**: its **siblings** at the parent level, and what passes between them
- **Allocated functions**: what it must do, from the level above
- **Modes**: for example FBL idle, receiving, running an app

The interfaces are where split functions leave their trace. Where a function is allocated to two SoIs, the split
creates an interface requirement on whatever connects them.

## Rules

1. **One requirement, one SoI.** A requirement that spans two elements is split into one requirement each plus an
   interface requirement. Example: 504 "deliver an update" becomes *serve an image* (FRDM), *receive, verify and
   boot it* (STM32) and *carry it at 500 kbit/s* (the bus).
2. **Every requirement derives from one above**, except at L0, and every plain allocation has at least one child
   in the element it names. A requirement allocated only as-is ends there and is a leaf.
3. **Every requirement has a verification**: test, inspection, analysis or demonstration where nothing is derived
   below it, and **integration** of its children where something is. The bench tests T1.1 to T2.3 in
   [phases.md](phases.md) are the system verification of the L0 requirements.
4. **Phase is an attribute**, not a separate tree. "Phase 1" is a filter over the one set.
5. **Requirements say what, decisions say why.** A requirement links to the `HW-`, `MEC-`, `SYS-` or `SW-` entry
   that shaped it; it does not restate the reasoning.
6. **Logical requirements name no implementation.** "Verify the image before it runs" holds whether a CRC, a
   signature or a person does it. The mechanism enters at L2 or L3.
7. **Requirements are written to be checked**: one statement, "shall", a measurable limit where one exists, no
   "and" joining two verifiable things.

## The V

The method is the left side of a V in the manner of Arcadia and INCOSE. The mapping to ASPICE is from memory.

| Our level | Specify (left) | ASPICE | Arcadia | Verify (right) |
|---|---|---|---|---|
| Phase goals | Stakeholder needs | SYS.1 | Operational analysis | Validation |
| **L0** | System requirements | SYS.2 | System analysis | **System verification**: the bench tests T1.1 to T2.3 |
| **L1** | Functional architecture | SYS.3 | Logical architecture | Integration of the elements the function is allocated to |
| **L2** | Physical architecture and interfaces | SYS.3 | Physical architecture | **Integration**: the nodes and the bus together |
| **L3** | Hand-over to each repository | SWE.1 onward | End-product breakdown | Verification inside each repository |

Each phase is one pass through the V over a growing scope, so phase being an attribute is what the V needs. The
logical and physical split is a refinement of ASPICE's single architecture step, not a departure from it, and the
as-is allocation is how Arcadia avoids the same duplication.

## Worked example

| Level | Requirement |
|---|---|
| L0 | The vehicle shall allow its STM32 application to be replaced over the vehicle CAN bus without a debug probe (verified by T1.1) |
| L1 | `Nexus-SubSys-504`: deliver an image and verify it before it runs (first form: CRC, then jump) |
| L2 | FRDM node: serve an image. CAN bus: carry it at the update identifiers. STM32 node: accept, verify and boot it |
| L3 | FBL: receive by Cyphal file transfer, erase, write, verify, jump. FBL: remain reachable if the image is bad. CAN-Utils: define the update identifiers |

## Format

Markdown, one file per SoI in [`../requirements/`](../requirements/README.md), a fixed block per requirement,
checked by `tools/check-requirements.py`, which also generates the trace and the allocation matrix. The block
format and the field rules are in that README. YAML as source was weighed and rejected ([SYS-03](../decisions/SYS-System-Decisions.md)):
Markdown is read and diffed in the PR, and the checker gives the same guarantees.
