# Requirements

The requirements of NEXUS, written to the method in [`../system/method.md`](../system/method.md) and
checked by [`../tools/check-requirements.py`](../tools/check-requirements.py). **One file per system of
interest (SoI)**, named by its code: `VEH.md`, and so on. [`TRACE.md`](TRACE.md) is generated from them:
edit the requirements, run the checker with `--write`, never edit `TRACE.md`.

```bash
python3 tools/check-requirements.py            # exits 1 on a broken link, a gap or a stale TRACE.md
python3 tools/check-requirements.py --write    # regenerates requirements/TRACE.md
```

## Systems of interest

This table is the registry. A code is never reused. The check reads it, so a requirement can only belong to
a SoI that is listed here, and every row needs its file.

| Code | Name | Kind | Level |
|---|---|---|---|
| VEH | NEXUS vehicle | Vehicle | 0 |

Logical rows (`Nexus-SubSys-DNN`, from the logical architecture) and physical and component rows are added as
each is defined. Kind is `Vehicle`, `Logical`, `Physical` or `Component`; level is 0 to 3.

## A SoI file

The file opens with the **definition card** of the method (purpose and boundary, interfaces, allocated functions,
modes), then one block per requirement:

```markdown
### STM-R004

**Statement.** The STM32 node shall boot an application image only after its CRC has verified.

- Derived-from: VEH-R001
- Allocated-to: FBL
- Phase: 1
- Verification: Test T1.1
- Decisions: SW-01
```

| Field | Rule |
|---|---|
| **ID** | `<CODE>-Rnnn`, the code of the file it is in; numbers never reused |
| **Statement** | One sentence containing "shall"; one verifiable thing; a limit where one exists; no implementation in a logical SoI |
| **Derived-from** | IDs of the parent requirements, all one level up; `-` only at level 0 |
| **Allocated-to** | SoI codes one level down that must satisfy it; each must hold a requirement derived from this one. `-` makes it a **leaf** |
| **Phase** | 1 to 5; never later than a parent's, since a parent is not met before its children are |
| **Verification** | `Test`, `Inspection`, `Analysis` or `Demo`, then the reference. A `T1.1`-style reference must exist in [`../system/phases.md`](../system/phases.md). Required on every leaf and at level 0 |
| **Realised-by** | `HW`, `SW` or `SYS` (a procedure). Required on a leaf, absent elsewhere |
| **Decisions** | Optional; `HW-`, `MEC-`, `SYS-` or `SW-` IDs that must exist |

## What the check fails on

An unknown SoI, a missing file, a duplicate ID, an ID in the wrong file, a parent that does not exist or is not one
level up, an allocation with no matching child (and a child whose SoI the parent did not allocate to), a leaf without
verification or realisation, a child in a later phase than its parent, an unknown decision or test, an em-dash,
and a `TRACE.md` that is not what the requirements generate.
