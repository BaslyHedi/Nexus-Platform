# NEXUS Platform

The **definition** of NEXUS: what the vehicle is, why it is that way, and what it is
made of. A personal Ackermann-steering autonomous robot built as a miniature of a
modern automotive E/E architecture - high-level compute and real-time control with a
network in between. [`CLAUDE.md`](CLAUDE.md) owns the platform overview.

This repository holds **no firmware or application code**: those live in their own repositories
(below) and cite this one. What is here is the definition, plus the small scripts that generate the drawings and
models from it.

## What this is, and where it stands

NEXUS is a learning platform: a 4-wheel Ackermann robot with an **NXP i.MX 91** (Embedded Linux, Yocto) for
high-level compute and an **STM32F407** (real-time control) on a **CAN** bus between them. It is built to get
hands-on with the architecture of a modern vehicle, and the repository is written the way such a project would be:
numbered decisions with their reasons and the options rejected, a bill of materials, a functional decomposition, and
a phase plan with testable exit criteria.

The pace is set by learning, not by the calendar, so nothing here has a date. **Phase 1 (Foundation) is under way**:
the vehicle hardware is largely defined and built, and the software repositories below were created on
2026-10-11 and are still empty. What each phase delivers is in [`system/phases.md`](system/phases.md).

Worth reading first: [`decisions/`](decisions/README.md) (why it is this way), [`system/phases.md`](system/phases.md)
(what is built when), and [`system/renders/Nexus-Platform-Logical-Architecture.svg`](system/renders/Nexus-Platform-Logical-Architecture.svg)
(the decomposition).

## Repositories

| Repository | What it holds |
|---|---|
| **Nexus-Platform** (this one) | Definition: system, decisions, hardware, mechanical, BOM, phase plan |
| [Nexus-STM32-FBL](https://github.com/BaslyHedi/Nexus-STM32-FBL) | Bare-metal flash bootloader for the STM32, updated over CAN with Cyphal |
| [Nexus-STM32-App](https://github.com/BaslyHedi/Nexus-STM32-App) | The Zephyr application the bootloader loads |
| [Nexus-CAN-Utils](https://github.com/BaslyHedi/Nexus-CAN-Utils) | The CAN matrix, its generators and the flashing client |
| [Nexus-IMX91-Yocto](https://github.com/BaslyHedi/Nexus-IMX91-Yocto) | The Yocto build (`kas`) of the Linux image for the FRDM-IMX91 |

Each Linux application will get its own repository, with its own CI and releases.

## How it is made

The architecture, the decisions and the hardware are the author's. The documentation, the drawing generators and the
records are written with **Claude Code** (Anthropic) as a pairing assistant, and commits made that way carry a
`Co-Authored-By` trailer.

## Licence and attribution

Free to use, reuse and adapt **as long as you credit the source**. Code and tooling are
**Apache-2.0** ([`LICENSE`](LICENSE)); the documents, drawings and print files are **CC BY 4.0**
([`LICENSE-docs`](LICENSE-docs)). [`NOTICE`](NOTICE) says which applies to what. A suitable credit line:

> Based on NEXUS Platform by Hedi Basly, https://github.com/BaslyHedi/Nexus-Platform

## Where the numbers come from

Dimensions, pinouts and ratings of third-party parts are **measured or derived** from the vendors' documents and CAD
(for example the chassis plate outline, traced from Hiwonder's CAD export, and the FRDM board outline, taken from
NXP's design files). **No vendor document is redistributed here**; see below.

## Layout

| Folder | Owns |
|---|---|
| [`requirements/`](requirements/README.md) | The requirements, one Markdown file per system of interest or element, derived and allocated per [`system/method.md`](system/method.md) |
| [`system/README.md`](system/README.md) | What NEXUS must **do** - the logical and physical views of the architecture with their `Nexus-Logical-DNN` and `Nexus-Physical-NN` IDs, the method, the **phase plan** (`phases.md`); its diagram is in `renders/`, written by the script in `scripts/` |
| [`decisions/README.md`](decisions/README.md) | Every settled decision and the reasoning behind it, split **HW / MEC / SYS / SW**. Its README owns the numbering rules |
| [`hardware/README.md`](hardware/README.md) | Build drawings, to scale - chassis layout, wiring schematic, STM32 carrier - the SVGs in `renders/`, the script that writes the carrier's in `scripts/` |
| [`mechanical/README.md`](mechanical/README.md) | The parts we make, in `cad/` (`fascia.scad` is the source of truth, plus the print files and the proposed carrier tray), the scripts that build and animate the model in `scripts/`, and their output in `renders/` |
| [`bom/README.md`](bom/README.md) | What it is made of - [`bom/BOM.md`](bom/BOM.md) for status, price and sourcing; `parts/<item>/SPECS.md` for measured numbers |

Every folder that draws or renders something follows one pattern: **`scripts/`** holds what makes
it and **`renders/`** holds what comes out (SVGs, images, videos).

## How the code repositories will use this

Decision numbers are the interface. They are **unique across the project, never reused
and never renumbered**, precisely so that a drawing, a spec or a line of firmware can
name one and have it resolve to exactly one place:

```c
/* DE-9 pinout, and why the PC joins the bus unterminated: HW-18. */
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

Two generated meshes are ignored in `mechanical/cad/` for a different reason - size and
churn. One of them, `chassis-3deck-fascia.obj`, is a **seed the script rewrites in place**
rather than pure output, so it cannot be rebuilt from the repository alone. Keep a local
backup.

## Checking the links

Every cross-reference in here is a relative link, and they are the thing that breaks
when files move:

```bash
python3 tools/check-links.py
```

## Checking the drawings

The drawings in `hardware/renders/` and `system/renders/` are written by the scripts of the same name in `hardware/scripts/` and `system/scripts/`. Edit the script, never
the SVG; this fails if an SVG has drifted from its script:

```bash
python3 tools/check-drawings.py
```

## Checking the requirements

Requirements are Markdown blocks with fixed fields. This checks their format, links, trace to the drawings and writing
rules, and fails when the generated `requirements/TRACE.md` or `requirements/renders/traceability.svg` is stale (`--write`
regenerates both):

```bash
python3 tools/check-requirements.py
```
