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
| [`system/README.md`](system/README.md) | What NEXUS must **do** - the top-down functional decomposition and the `Nexus-SubSys-DNN` IDs |
| [`decisions/README.md`](decisions/README.md) | Every settled decision and the reasoning behind it, split **HW / MEC / SYS / SW**. Its README owns the numbering rules |
| [`hardware/README.md`](hardware/README.md) | Build drawings, to scale - chassis layout, wiring schematic, STM32 carrier |
| [`mechanical/README.md`](mechanical/README.md) | The parts we make - `fascia.scad` is the source of truth, plus the print files and the assembly script |
| [`bom/README.md`](bom/README.md) | What it is made of - [`bom/BOM.md`](bom/BOM.md) for status, price and sourcing; `parts/<item>/SPECS.md` for measured numbers |

## How the code repositories will use this

Decision numbers are the interface. They are **unique across the project, never reused
and never renumbered**, precisely so that a drawing, a spec or a line of firmware can
name one and have it resolve to exactly one place:

```c
/* CAN bitrate and the reasoning behind it: SW-04, HW-18. */
```

A code repository cites `HW-nn` / `SW-nn` back to [`decisions/README.md`](decisions/README.md).
It never restates them. The direction the facts travel is one way, out of here.

## Vendor documents are not in this repository

One rule, no exceptions: **no vendor document is committed.** Datasheets, user manuals,
board design packages and the chassis CAD are all copyrighted and not ours to
redistribute, so none of them is here - not the 28 MB of PDFs, not NXP's design package,
not Hiwonder's 186 MB `.3dm`.

What is here is **the record of them**, which is the part that was written here: the
vendor, the exact title and document number, the revision and date, and an honest grade
of how much each one is worth. [`bom/README.md`](bom/README.md) owns that record and
[`bom/parts/<item>/`](bom/) carries the measurements taken from each document. Nothing a
decision rests on is lost by the file being absent.

**On a fresh clone the documents are not there and have to be fetched by hand.** The
vendor and title are enough to search for; `bom/README.md` also lists which ones are
already known to be stale and which have never been found at all. On this machine they
live in an untracked `vendor/` beside these folders.

Two generated meshes are ignored in `mechanical/` for a different reason - size and
churn. One of them, `chassis-3deck-fascia.obj`, is a **seed the script rewrites in place**
rather than pure output, so it cannot be rebuilt from the repository alone. Keep a local
backup.

## Checking the links

Every cross-reference in here is a relative link, and they are the thing that breaks
when files move:

```bash
python3 tools/check-links.py
```
