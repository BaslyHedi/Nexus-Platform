# SYS · System design decisions

Behaviour that no single discipline owns - protection strategies, modes, and anything where hardware, firmware and the operator each carry part of the answer.

Numbering is `SYS-nn`, unique across the project and never reused. Format, and how to add one: [README](README.md). Parts, prices and status: [`../bom/BOM.md`](../bom/BOM.md).

| # | Decision |
|---|---|
| **SYS-01** | Layered over-discharge protection, not a cutoff module |
| **SYS-02** | Five phases, paced by learning; Phase 1 is foundation, not driving |
| **SYS-03** | Conventional systems engineering: one physical hierarchy, logical and physical views at each level |

---

## SYS-01 · Layered over-discharge protection, not a cutoff module

*Formerly HD-08.*

**Decision.** No hardware low-voltage disconnect. Protection is: the pack's own internal PCB,
then STM32 sensing, then graceful shutdown in software.

**Why.** A hard cutoff on the compute rail is worse than none - yanking 5 V from a running
Linux board mid-write is exactly the corruption the two-rail split exists to prevent. Hard
cutoff is only safe on the drive branch.

**XH-M609 modules were rejected**: their operating range starts at 12 V, and a 3S pack sits
below that for most of its discharge curve; they also draw <1.5 W continuously (~135 mA), which
would flatten the pack they are meant to protect.

**The buzzer alarm was cancelled** once the battery arrived in spec: the Hiwonder pack is hard
cased with a 2-pin discharge lead and a barrel charge jack and **has no balance connector**, so
a balance-lead alarm cannot be fitted. Charging over two wires implies an internal protection
PCB, which is the backstop the buzzer would have been.

**Consequence.** Per-cell voltage is permanently unobservable on this pack. Pack-level V and I
is the whole available signal. Capacity is known - 6000 mAh - so coulomb counting has its
denominator from day one.

---

## SYS-02 · Five phases, paced by learning; Phase 1 is foundation, not driving

**Decision.** The project is built in five phases - **Foundation, Drive, Platform, Perception, Autonomy** -
each with a goal and exit criteria, owned by [`../system/phases.md`](../system/phases.md). Phase 1 is
the assembled vehicle, a CAN flash bootloader with a minimal STM32 app, a
minimal FRDM image, and the repository structure. It drives nothing and contains no control loops.

**Why.** The first plan had two buckets, "Phase 1" and "later", and everything that was not wiring was
later. That hides the real order of dependency: the bus contract has to exist before either side of it, and
the means of updating the MCU has to exist before the MCU runs anything worth updating. The project exists
to learn C++, Rust, Embedded Linux, Yocto, Zephyr, CAN, secure boot and OTA, so the order is chosen for what each
step makes learnable, and no phase has a date.

**Consequence.** The drawing marks each sub-system with the phase it **first exists in**, which moved some of
its earlier tags: Software Update (504) is Phase 1 because the FBL is its first form, Operator Interface (402)
and External Connectivity (403) are Phase 2, Cybersecurity (502) is Phase 3, and perception and
localization (301, 302) are Phase 4 with planning (303) in Phase 5. Phase 1's repositories, and the `SW-` entries
that settle the matrix and the flash protocol, are listed in the phase plan.

---

## SYS-03 · Conventional systems engineering: one physical hierarchy, logical and physical views at each level

**Decision (2026-10-11).** NEXUS is defined with the conventional concepts of systems engineering, after ISO/IEC/IEEE 15288,
ISO/IEC/IEEE 42010, the INCOSE and NASA handbooks and SysML, and uses their terms. The method is
[`../system/method.md`](../system/method.md).

- The hierarchy is the **physical breakdown**. The vehicle is the first system of interest, and each system element becomes
  one in turn (recursion), until a bought part or a software item, which is handed over to its repository.
- At each level the architecture has a **logical view** and a **physical view** of the same system, related by
  **allocation**. The sub-systems of the logical architecture are logical components, not levels of the hierarchy.
- A requirement is **allocated** to an element as it is, or **derived** into new requirements where the architecture adds
  something. Requirements trace to functions and are allocated to physical elements. Every requirement has a verification.
- Physical elements are `Nexus-Phys-NN`; logical components keep `Nexus-SubSys-DNN`.
- Requirements are Markdown, one file per system of interest or element, validated by `tools/check-requirements.py`.

**Why.**

- **The standards already answer this**, and a home-made method would have to rediscover the same answers. A first draft did:
  it stacked the logical architecture above the physical one as two levels, which made a 1:1 pair such as 401 and the CAN
  bus look like two systems, and needed a "merge" rule to undo it. As two views of one level, they are simply one allocation.
- Allocating requirements to the domains HW, SW and SYS gives no root and no tree. Domain stays a property of a leaf.
- The hand-over at the software item matches the automotive split (ASPICE SYS to SWE) and keeps this repository free of code.
- Markdown rather than YAML as the source: the PR is where this is reviewed, and a Markdown block reads and diffs there
  while the checker gives the same link guarantees.

**Consequence.** The physical view is drawn ([`../system/physical-architecture.md`](../system/physical-architecture.md)); the
allocation of functions to elements is next, then the requirements. A first pass of requirements written before the method
settled is parked in [`../requirements/`](../requirements/README.md) and is redone on it.
