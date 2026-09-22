# SYS · System design decisions

Behaviour that no single discipline owns - protection strategies, modes, and anything where hardware, firmware and the operator each carry part of the answer.

Numbering is `SYS-nn`, unique across the project and never reused. Format, and how to add one: [README](README.md). Parts, prices and status: [`../../RnD-Docs/BOM.md`](../../RnD-Docs/BOM.md).

| # | Decision |
|---|---|
| **SYS-01** | Layered over-discharge protection, not a cutoff module |

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
