# Requirements method

How NEXUS requirements are written, derived and allocated. This file owns the method; the reasoning for
choosing it is [SYS-03](../decisions/SYS-System-Decisions.md). The requirements themselves are not here yet:
this is the method only.

## The idea in one paragraph

A requirement belongs to exactly one **system of interest** (SoI). **Allocating** it to a child SoI produces a
**derived** requirement on that child. Repeat down four levels. Derivation is the vertical link between
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
| **L0** | Vehicle | Needs and phase goals, written as "the vehicle shall ..." | here |
| **L1** | Logical | Sub-systems and their functions, `Nexus-SubSys-DNN-Fnn` | here, drawn in [Nexus-Platform-Logical-Architecture](renders/Nexus-Platform-Logical-Architecture.svg) |
| **L2** | Physical | The nodes, the bus, power distribution, chassis | here |
| **L3** | Component | Parts of a node, down to **the repository** | here, as far as "allocated to repository X" |

**L0 to L1 is derivation**: the same question, refined. **L1 to L2 is allocation**: the question changes from
*what* to *who does it*, and it is many-to-many (501 Supervision is partly fuses and switches, partly the STM32,
partly Linux). **L2 to L3 is allocation plus derivation** again.

**The stopping point.** This repository holds the definition and no code, so requirements stop at "allocated
to repository X". Each repository then chooses its solution and writes its own requirements, derived from ours,
citing our IDs. Facts travel one way, out of here.

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
   interface requirement. Example: 504 "deliver an update" becomes *serve an image* (FRDM, or the PC adapter),
   *receive, verify and boot it* (STM32) and *carry it at 500 kbit/s* (the bus).
2. **Every requirement derives from one above**, except at L0, and every non-leaf requirement has at least one
   child. The checker, when it exists, fails on an orphan or a dead end.
3. **Every leaf has a verification**: test, inspection, analysis or demonstration. The bench tests T1.1 to T2.3 in
   [phases.md](phases.md) are the verification cases of the L0 requirements.
4. **Phase is an attribute**, not a separate tree. "Phase 1" is a filter over the one set.
5. **Requirements say what, decisions say why.** A requirement links to the `HW-`, `MEC-`, `SYS-` or `SW-` entry
   that shaped it; it does not restate the reasoning.
6. **Logical requirements name no implementation.** "Verify the image before it runs" holds whether a CRC, a
   signature or a person does it. The mechanism enters at L2 or L3.
7. **Requirements are written to be checked**: one statement, "shall", a measurable limit where one exists, no
   "and" joining two verifiable things.

## Worked example

| Level | Requirement |
|---|---|
| L0 | The vehicle shall allow its STM32 application to be replaced over the vehicle CAN bus without a debug probe (verified by T1.1) |
| L1 | `Nexus-SubSys-504`: deliver an image and verify it before it runs (first form: CRC, then jump) |
| L2 | FRDM or PC adapter: serve an image. CAN bus: carry it at 500 kbit/s. STM32 node: accept, verify and boot it |
| L3 | FBL: receive by Cyphal file transfer, erase, write, verify, jump. FBL: remain reachable if the image is bad. CAN-Utils: define the update identifiers |

## Not yet decided

- **File format** for the requirements and the checker that validates links: Markdown with a fixed block per
  requirement and `tools/check-requirements.py` generating the trace and allocation matrices (leaning), or YAML
  as source with generated Markdown.
- **ID format**: proposed `VEH-R012`, `STM-R004`, `FBL-R010` (SoI code, then number). Never reused, like every
  other ID here. Decision IDs keep their prefixes.
- **Scope of the first pass**: the Phase 1 sub-systems (101, 102, 201 and 202 as hardware only, 401, 501 as
  the hardware switches, 503, 504).
