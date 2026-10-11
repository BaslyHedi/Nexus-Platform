# SW · Software design decisions

Firmware and Linux-side decisions - RTOS choice and configuration, the CAN matrix in software,
service layout, build and OTA. Numbering is `SW-nn`, unique across the project and never reused.
Format, and how to add one: [README](README.md).

| # | Decision |
|---|---|
| **SW-01** | The flash bootloader speaks OpenCyphal, not UDS |

The rest of what Phase 1 has to settle is listed in [`../system/phases.md`](../system/phases.md) under
*Decided in Phase 1*: the CAN matrix and its tooling, the FBL's memory map, the Zephyr board port, the
repository and CI template, and how the STM32 reports a fault to the i.MX 91. Related hardware constraints are
[HW-10](HW-Electrical-Decisions.md) (I²C pins) and [SYS-01](SYS-System-Decisions.md) (over-discharge protection).

---

## SW-01 · The flash bootloader speaks OpenCyphal, not UDS

**Decision (2026-10-11).** The STM32 flash bootloader (FBL) receives its application image over
**Cyphal/CAN** (OpenCyphal v1) on the 500 kbit/s classic-CAN bus. The host sends a software-update command to
the node, and the bootloader then **pulls** the image from a file server block by block, verifies it and jumps
to it. The FBL stays **bare-metal and small**. The host side is a file server in `Nexus-CAN-Utils`, which must
run on Linux so it works from the PC adapter now and from the i.MX 91 later.

**Why.**

- **The project exists to learn new ground**, and the author already knows UDS and AUTOSAR bootloaders well.
  Cyphal is a different design (publish/subscribe, node-pulled file transfer, typed data from DSDL) used in
  robotics and aviation, which is where NEXUS is heading.
- **It fits the hardware.** Cyphal/CAN runs on classic CAN, which is all the STM32F407's bxCAN and the SN65HVD230
  do. `libcanard` (C, MIT, compact) is built for exactly this kind of deeply embedded target.
- **There is a reference for the bootloader.** Zubax's Kocherga is a platform-agnostic Cyphal/DroneCAN bootloader
  library. It is read as a design reference, not adopted wholesale, so the FBL is still written here.
- Adoption data gathered 2026-10-11 (GitHub and PyPI): `libcanard` 450 stars, `pycyphal` about 7.8k downloads a month,
  against DroneCAN's roughly 68k, ArduPilot 16k stars and PX4 12.8k. It is small next to DroneCAN, and
  Kocherga's last commit is April 2024. For a two-node learning vehicle that is acceptable, since interoperability
  with other vendors' parts is not needed.

**Rejected.**

- **UDS over ISO-TP**: the automotive standard and the cheaper option, since it is familiar. Rejected because the
  familiarity is exactly why it teaches little here. It stays the fallback if Cyphal proves a poor fit.
- **DroneCAN (UAVCAN v0)**: more widely deployed and with the same pull model, but it is the legacy line that
  Cyphal replaces.
- **STM32 ROM bootloader, mcumgr/SMP, DFU**: fast to use, but none of them is a bootloader that the project writes,
  and none runs over the bus the vehicle already has.

**Consequences.**

- `Nexus-CAN-Utils` ships a **Cyphal file server** as the flashing client, and the Linux side needs a Cyphal stack
  (libcanard in C, libcyphal in C++, or `pycyphal` for tooling). The language choice is still open.
- The bootloader needs a **node ID** and a fixed set of subjects and services. Its identifiers, and any ID ranges
  the application uses, are part of the CAN matrix.
- **The application layer is not decided here.** Whether the vehicle's own messages (motion request, state,
  heartbeat) are also Cyphal, with the matrix as a set of DSDL types and a subject-ID table, or a plain-ID matrix
  sharing the bus, is a separate entry. Running both on one bus is possible but needs the ID ranges kept apart.
- Diagnostics (Phase 2) can use Cyphal services instead of UDS. That is also left to its own
  entry.

**To confirm.**

- That `libcanard` builds and runs cleanly on the F407 at 500 kbit/s with the bare-metal FBL's flash and RAM budget.
- That the FBL's size stays small. Kocherga's own footprint is the yardstick to compare against, and it has not been measured.
- The Cyphal services and subject names, from the specification, before the matrix is written. They were recalled
  from memory when this entry was drafted.

---
