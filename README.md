# NEXUS Platform

The **definition** of NEXUS: what the vehicle is, why it is that way, and what it is
made of. A personal Ackermann-steering autonomous robot built as a miniature of a
modern automotive E/E architecture - high-level compute and real-time control with a
network in between. [`CLAUDE.md`](CLAUDE.md) owns the platform overview.

This repository holds **no code**. Firmware, the Linux image and the applications each
get their own repository as they are written; they consume this one.

## Layout

| Folder | Owns |
|---|---|
| [`system/`](system/README.md) | What NEXUS must **do** - the top-down functional decomposition and the `Nexus-SubSys-DNN` IDs |
| [`decisions/`](decisions/README.md) | Every settled decision and the reasoning behind it, split **HW / MEC / SYS / SW**. Its README owns the numbering rules |
| [`hardware/`](hardware/README.md) | Build drawings, to scale - chassis layout, wiring schematic, STM32 carrier |
| [`mechanical/`](mechanical/README.md) | The parts we make - `fascia.scad` is the source of truth, plus the print files and the assembly script |
| [`bom/`](bom/README.md) | What it is made of - [`BOM.md`](bom/BOM.md) for status, price and sourcing; `parts/<item>/SPECS.md` for measured numbers |

## How the code repositories will use this

Decision numbers are the interface. They are **unique across the project, never reused
and never renumbered**, precisely so that a drawing, a spec or a line of firmware can
name one and have it resolve to exactly one place:

```c
/* CAN bitrate and the reasoning behind it: SW-04, HW-18. */
```

A code repository cites `HW-nn` / `SW-nn` back to [`decisions/`](decisions/README.md).
It never restates them. The direction the facts travel is one way, out of here.

## The vendor library

`vendor/` sits beside these folders on disk and is **not** tracked: the datasheets,
NXP's FRDM design-file package and Hiwonder's 186 MB chassis CAD. None of it was
written here, and [`bom/README.md`](bom/README.md) names, dates and grades every
document - so the repository records what each file is and how good it is, while the
file itself stays local. Six of the eleven BOM parts have no vendor document at all,
which is why their `SPECS.md` exists.

Two generated meshes are ignored in `mechanical/` for the same reason. One of them,
`chassis-3deck-fascia.obj`, is a **seed the script rewrites in place** rather than pure
output - it cannot be rebuilt from the repository alone. Keep a local backup.

## Checking the links

Every cross-reference in here is a relative link, and they are the thing that breaks
when files move:

```bash
python3 tools/check-links.py
```
