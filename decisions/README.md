# Design decisions

Every settled decision on NEXUS, with the reasoning that produced it. One entry per decision.
An entry is **settled** - revisit one only if something concrete contradicts it, and when that
happens, supersede it rather than editing history (see *Changing a decision* below).

## The files

| File | Owns |
|---|---|
| [`HW-Electrical-Decisions.md`](HW-Electrical-Decisions.md) | Power, protection, grounding, wiring, on-vehicle networking |
| [`MEC-Mechanical-Decisions.md`](MEC-Mechanical-Decisions.md) | Packaging, deck stack, printed parts, fixings |
| [`SYS-System-Decisions.md`](SYS-System-Decisions.md) | Behaviour no single discipline owns - hardware + firmware + operator together |
| [`SW-Software-Decisions.md`](SW-Software-Decisions.md) | Firmware and Linux side - RTOS, CAN matrix in software, services, OTA |

## Numbering

`<DISCIPLINE>-nn`, zero-padded, allocated in order within its file: **HW**, **MEC**, **SYS**, **SW**.

- **Unique across the project, and never reused.** A retired entry keeps its number.
- **Discipline is decided by what the decision constrains**, not by who made it. "The servo never
  touches a 5 V rail" is HW even though it is about a mechanical part; "power domain low, compute
  domain high" is MEC because it is about where things physically sit.
- **A decision spanning two disciplines lives in the one it constrains most**, and links to the
  other. Do not copy it into both - one fact, one owning file.
- **Nothing is renumbered when a file is reorganised.** Numbers are how other documents, drawings
  and source comments refer to decisions.

## Adding one

Append to the right file, take the next free number, and follow the shape the existing entries use:

```markdown
## HW-19 · One line saying what was decided

**Decision (YYYY-MM-DD).** What is now true, in the present tense.

**Why.**

- The reason that actually drove it, not a list of generic virtues.
- What was rejected, and what would have to change for the answer to differ.

**Consequences.** What this now forces elsewhere, including the awkward parts.

**To confirm.** Anything the decision rests on that has not been measured yet.
```

Two habits that keep this useful:

- **Record the dead ends.** MEC-07 says rings were tried and rejected because they locate but do
  not clamp. That is what stops the idea coming back a month later.
- **Put numbers in.** A decision with measurements in it can be checked; one without cannot.

## Changing a decision

Write the **new** entry with the next free number, then add one line at the top of the old one:

```markdown
**Updated by MEC-09:** the gaps are 50 and 40 mm, so the panels are different parts.
```

The old entry stays where it is. The reasoning chain is the point - a decision that was reversed
is usually more informative than one that never moved.

## Old HD numbers

These entries were one file, `Architecture/Hardware/Hardware-Design-Decisions.md`, numbered
`HD-nn` in one sequence. That file is gone: its entries were split by discipline into the files
in **this** folder, `decisions/`, and every reference in the project was updated. The prefix in
the **Now** column names the file that holds the entry:

| Prefix | File |
|---|---|
| `HW-` | [`HW-Electrical-Decisions.md`](HW-Electrical-Decisions.md) |
| `MEC-` | [`MEC-Mechanical-Decisions.md`](MEC-Mechanical-Decisions.md) |
| `SYS-` | [`SYS-System-Decisions.md`](SYS-System-Decisions.md) |

No `HD-` entry became an `SW-` one, so [`SW-Software-Decisions.md`](SW-Software-Decisions.md)
took none of them.

The table below is here for anything outside the project - notes, chat history, a photo caption:

| Was | Now |
|---|---|
| HD-01 | **HW-01** |
| HD-02 | **HW-02** |
| HD-03 | **HW-03** |
| HD-04 | **HW-04** |
| HD-05 | **HW-05** |
| HD-06 | **HW-06** |
| HD-07 | **HW-07** |
| HD-08 | **SYS-01** |
| HD-09 | **HW-08** |
| HD-10 | **HW-09** |
| HD-11 | **HW-10** |
| HD-12 | **MEC-01** |
| HD-13 | **HW-11** |
| HD-14 | **HW-12** |
| HD-15 | **MEC-02** |
| HD-16 | **HW-13** |
| HD-17 | **HW-14** |
| HD-18 | **HW-15** |
| HD-19 | **HW-16** |
| HD-20 | **HW-17** |
| HD-21 | **HW-18** |
| HD-22 | **MEC-03** |
| HD-23 | **MEC-04** |
| HD-24 | **MEC-05** |
| HD-25 | **MEC-06** |
| HD-26 | **MEC-07** |
| HD-27 | **MEC-08** |
| HD-28 | **MEC-09** |

## Still open

Closed on 2026-10-11 and removed from this table: the switch harness depth (MEC-14), the P1/P2 pin direction (MEC-08, resolved 2026-09-20), the clip, fuse-holder, battery and driver check (MEC-16), and the UBEC input lead (HW-20).

Questions that block a decision, or that a decision rests on and nobody has measured yet.

| Question | Blocks |
|---|---|
| SM-2P battery connector temperature under load | HW-13 - XT30 if it runs warm |
| FRDM loaded current draw | compute branch fuse sizing |
| Which USB-CAN adapter, and is its 120 Ω switchable? | HW-18 - must be OFF |
| Does the Encoder Motor Module time out when I²C commands stop? | HW-17 - decides whether the HW-12 relay is needed before autonomy |
