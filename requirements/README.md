# Requirements

> **Parked first pass.** These files were written before the method settled on the conventional structure
> ([SYS-03](../decisions/SYS-System-Decisions.md), [`../system/method.md`](../system/method.md)). They put requirements on
> logical components, use physical elements that the [physical view](../system/physical-architecture.md) has since
> replaced, and treat the FBL-Updater as its own repository, though it is a target of the FBL repository. They are kept
> as material and are redone after the allocation.

The requirements of NEXUS, written to the method in [`../system/method.md`](../system/method.md): **one file per
system of interest (SoI)**, named by its code. Phase 1 is written in full, from the vehicle down to the
repositories: 113 requirements in 21 files.

**The checker is not updated yet.** [`../tools/check-requirements.py`](../tools/check-requirements.py) still checks the first
format of this folder (before the as-is allocation, the `Function` field and the `Integration` method) and fails on these
files, and `TRACE.md` is not generated. Bringing the checker to this format is the next step, and it will then
generate the trace and the allocation matrix.

## Systems of interest

**Logical SoIs are the sub-systems of the [logical architecture](../system/renders/Nexus-Platform-Logical-Architecture.svg)
and are not listed here:** their code is their ID, `Nexus-SubSys-DNN`, and the drawing owns the list. Their files are
`Nexus-SubSys-DNN.md`. Phase 1 has written 101, 102, 201, 202, 401, 501, 503 and 504.

Everything else is registered here. A code is never reused, and a file named by it exists for each row.

| Code | Name | Kind | Level |
|---|---|---|---|
| Nexus-Vehicle | NEXUS vehicle | Vehicle | 0 |
| Nexus-Phys-PWR | Power: pack, protection, switching and rails | Physical | 2 |
| Nexus-Phys-CHS | Chassis, decks and fascia | Physical | 2 |
| Nexus-Phys-DRV | Drive train: motors, driver and steering | Physical | 2 |
| Nexus-Phys-CAN | Vehicle CAN bus | Physical | 2 |
| Nexus-Phys-STM32 | STM32 node: real-time MCU | Physical | 2 |
| Nexus-Phys-FRDM | FRDM node: Linux compute | Physical | 2 |
| Nexus-STM32-FBL | STM32 flash bootloader (repository) | Component | 3 |
| Nexus-STM32-FBL-Updater | STM32 FBL-Updater (repository, proposed) | Component | 3 |
| Nexus-STM32-App | STM32 minimal application (repository) | Component | 3 |
| Nexus-IMX91-Yocto | FRDM Yocto image (repository) | Component | 3 |
| Nexus-Linux-App | Linux applications (one repository each) | Component | 3 |
| Nexus-CAN-Utils | CAN matrix, generators and flashing client (repository) | Component | 3 |

Components already have an identity, the name of their repository from [phases.md](../system/phases.md), and use it.
The physical SoIs had none and are named `Nexus-Phys-<Name>`; the architecture is in
[`../system/physical-architecture.md`](../system/physical-architecture.md).

## A SoI file

The file opens with the **definition card** of the method (purpose and boundary, interfaces, allocated functions,
modes), then one block per requirement:

```markdown
### Nexus-Phys-STM32-R006

**Statement.** The node shall verify an image's CRC before it starts it.

- Derived-from: Nexus-SubSys-504-R002
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R004
```

| Field | Rule |
|---|---|
| **ID** | `<SoI code>-Rnnn`, the code of the file it is in; numbers never reused |
| **Statement** | One sentence containing "shall"; one verifiable thing; a limit where one exists; no implementation in a logical SoI |
| **Function** | Level 1 only: the `Nexus-SubSys-DNN-Fnn` it realises. `Fnn` is the position of the function in the sub-system's card in the drawing script |
| **Derived-from** | IDs of the parent requirements, all one level up; `-` only at level 0 |
| **Allocated-to** | SoI codes one level down that must satisfy it. **Plain** means the target must write a derived requirement of its own, since allocation added something. **`(as-is)`** means the requirement passes to the target unchanged, with no child text ([method.md](../system/method.md)). `-` makes it a leaf |
| **Phase** | 1 to 5; never later than a parent's |
| **Verification** | On **every** requirement. `Test`, `Inspection`, `Analysis`, `Demo`, then the reference; or `Integration`, then the child requirements whose passing verifies this one. A `T1.1`-style reference must exist in [`../system/phases.md`](../system/phases.md) |
| **Realised-by** | `HW`, `SW` or `SYS` (a procedure), several allowed. Required where nothing is derived below: a leaf, or a requirement allocated only as-is. Absent elsewhere |
| **Decisions** | Optional; `HW-`, `MEC-`, `SYS-` or `SW-` IDs that must exist |

## What the first pass found

- **No logical sub-system hosts "build and release software".** The Linux image, the apps and the CI of every
  repository are Phase 1 deliverables (T2.1, T2.2, 1.7) with no function of their own, so they are attached to
  `Nexus-SubSys-504` F01, the first form of delivery, with the Phase 3 OTA extending it. A sub-system for it may
  be worth adding.
- **`Nexus-STM32-FBL-Updater` is proposed.** It is deliverable 1.5 but has no repository in the 1.7 table.
- **`Nexus-Linux-App` is a class.** Each real application repository gets its own entry when it is created.
- **The heartbeat rate has no number.** The requirements say "the rate set in the CAN matrix", because the Cyphal
  values were recalled from memory in [SW-01](../decisions/SW-Software-Decisions.md) and are still to be confirmed.
- **Hardware stops at the physical node.** The BOM lists parts, not sub-assemblies, so a hardware requirement is a leaf
  on its node and level 3 is the software repositories.
- **Verifications are planned, not performed.** Only the harness checks of 2026-10-11 have run; every `Test` waits for its bench test.
- **102 F04, heat and vibration, has no requirement** because there is no measured limit to write it against.
