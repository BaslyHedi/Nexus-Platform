# SW · Software design decisions

Firmware and Linux-side decisions - RTOS choice and configuration, the CAN matrix in software,
service layout, build and OTA. Numbering is `SW-nn`, unique across the project and never reused.
Format, and how to add one: [README](README.md).

| # | Decision |
|---|---|
| **SW-01** | The flash bootloader speaks OpenCyphal, not UDS |
| **SW-02** | The FBL's Cyphal stack is written in-house, not taken from libcanard |
| **SW-03** | The FBL is written in C++17, as a freestanding subset |
| **SW-04** | The STM32 flash holds the FBL in sectors 0 to 4 and the application in sectors 5 to 11 |
| **SW-05** | The FBL uses the main SRAM only, leaves the CCM empty and does not use the FPU |

The rest of what Phase 1 has to settle is listed in [`../system/phases.md`](../system/phases.md) under
*Decided in Phase 1*: the CAN matrix and its tooling, the Zephyr board port, the
repository and CI template, and how the STM32 reports a fault to the i.MX 91. Related hardware constraints are
[HW-10](HW-Electrical-Decisions.md) (I²C pins) and [SYS-01](SYS-System-Decisions.md) (over-discharge protection).

---

## SW-01 · The flash bootloader speaks OpenCyphal, not UDS

**Updated by SW-02:** the FBL's Cyphal stack is written in-house; `libcanard` is a design reference and the fallback, not a dependency. Read the libcanard items under *Consequences* and *To confirm* against the in-house stack. The language is C++17 ([SW-03](#sw-03--the-fbl-is-written-in-c17-as-a-freestanding-subset)).

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
- **The application layer is not decided here, and is not a Phase 1 question.** Phase 1 needs only the flashing identifiers and a heartbeat; the application layer is decided in Phase 2. Whether the vehicle's own messages (motion request, state,
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

## SW-02 · The FBL's Cyphal stack is written in-house, not taken from libcanard

**Decision (2026-10-11).** The FBL carries its own implementation of Cyphal/CAN: the CAN identifier layout, the
tail byte, segmentation and reassembly of multi-frame transfers, the transfer CRC and transfer-ID handling, and the
serialization of the standard types it uses. **The scope is what the download needs and nothing more:** publish
`uavcan.node.Heartbeat`, serve `uavcan.node.GetInfo` and `uavcan.node.ExecuteCommand`, and act as a client of
`uavcan.file.Read`. The stack lives in its own folder and build target inside `Nexus-STM32-FBL`, with no dependency
on the rest of the bootloader. Whether it then moves out and is shared, with the App, `Nexus-CAN-Utils` or the
Linux programs, is decided once the FBL works, not now. `libcanard` and Kocherga stay as design references.

**Why.**

- **The protocol is the new ground in the FBL, and a library hides it.** The bootloader mechanics (flash, vector
  table, CRC, jump) are known ground ([`phases.md`](../system/phases.md), *Learning focus*). Linking `libcanard`
  would leave the one unfamiliar part as a black box. `phases.md` already says to take the longer road where a
  library hides the protocol.
- **The scope is small enough to finish.** One node, four ports, and one reassembly session at a time. That is
  a fraction of a general-purpose stack, and it is what T1.1 and T1.2 need.
- **There is an independent implementation to check against.** The PC adapter runs `yakut` and `pycyphal` over
  SocketCAN ([HW-18](HW-Electrical-Decisions.md)), so every frame the in-house stack sends or accepts can be
  tested against a stack it shares no code with.

**Rejected.**

- **`libcanard`** (C, MIT): compact, proven and made for this kind of target. Rejected only because it does the
  part that is meant to be learned. It stays the fallback if the in-house stack proves a poor use of the phase.
- **`libcyphal`** (C++): the same reason, and it is larger.
- **A general-purpose stack written now** (many ports, many sessions, both transports): rejected because no
  second user exists yet. Generality comes with the second user, if it comes.

**Consequences.**

- **Correctness has no library behind it.** The stack is tested on the host, layer by layer, against the
  specification's examples, and on the bench against `yakut`. A download that completes is not enough evidence on
  its own: the multi-frame and error paths need their own tests.
- **The four standard `uavcan` types are serialized by hand.** They belong to the Cyphal specification, not to the
  NEXUS CAN matrix, so the rule that nothing hand-copies a matrix definition ([`phases.md`](../system/phases.md),
  *Repositories*) still holds. Any NEXUS-specific type the FBL needs comes from a `Nexus-CAN-Utils` release.
- **SW-01's footprint question moves to the in-house code.** The size budget is measured on this stack, with
  Kocherga's footprint still the yardstick.
- **The Linux side's stack is still open** (SW-01). The in-house stack becomes one more candidate, which is part
  of why it is kept free of FBL dependencies.

**To confirm.**

- ~~The port IDs and type versions of the four standard types.~~ Checked against Specification v1.0, revision
  2025-05-16 (2026-10-11): Heartbeat 7509 v1.0, GetInfo 430 v1.0, ExecuteCommand 435 v1.3, file.Read 408 v1.1. The
  update command is `COMMAND_BEGIN_SOFTWARE_UPDATE` = 65533. SW-01's to-confirm on names is settled the same way.
- That the stack interoperates with `yakut` at 500 kbit/s: a full download and an interrupted one (T1.1).
- That it fits the FBL's 128 KB region (SW-04), once it is built.

---

## SW-03 · The FBL is written in C++17, as a freestanding subset

**Decision (2026-10-11).** The bootloader and its Cyphal stack ([SW-02](#sw-02--the-fbls-cyphal-stack-is-written-in-house-not-taken-from-libcanard))
are written in **C++17**, built with `arm-none-eabi-gcc`, as a freestanding subset: **no exceptions, no RTTI, no
dynamic allocation**, and no part of the standard library that allocates or pulls in I/O. **C++17 is the starting
point, not the ceiling:** a later move to C++20 is planned, made once the FBL works, as a deliberate step to learn
what the newer standard changes on a known code base. That move gets its own entry. The FBL-Updater's toolchain is
not decided here; [`phases.md`](../system/phases.md) leaves it until it is written.

**Why.**

- **C on bare metal is known ground; C++ on bare metal is not.** C++ is on the project's learning list
  ([`../CLAUDE.md`](../CLAUDE.md)). The FBL is a low-risk place to learn it: it is small, and the ST-LINK stays
  the recovery path (T1.2).
- **Cyphal maps well onto the language.** Node ID, port ID and transfer ID become distinct types, so mixing them
  up is a compile error. CRC tables are computed at compile time with `constexpr`. Buffers have a fixed capacity
  set by a template rather than a macro, with no heap.
- **The Linux side is C++ first** ([`phases.md`](../system/phases.md), *Repositories*). If the Cyphal stack is
  later shared (SW-02), it is already in the language its other users are written in.
- **C++17 is the standard MISRA C++:2023 is written for** (its title: *Guidelines for the use of C++17 in critical
  systems*). Starting on C++17 means the whole code base can sit under one published rule set, with no feature
  outside it.
- **The standard version does not change the image.** For the same source, C++17 and C++20 produce the same code;
  size and speed follow from which features are used. The choice is about how the source is written and which
  rules cover it, so starting on the more conservative standard costs nothing at run time.
- **Migrating later is a lesson in itself.** Moving a working code base to C++20 shows what each feature replaces,
  which is easier to see than starting with it.

**Rejected.**

- **C**: the default for a small bootloader and the language of `libcanard`. Rejected because it keeps the whole
  FBL on known ground.
- **C++20 from the start**: it brings `constinit` (a global that cannot be initialized at compile time becomes a
  build error), concepts, `std::span`, designated initializers and `<bit>`. Only `constinit` is more than a
  convenience, and none lets the FBL do something C++17 cannot. Rejected for now because MISRA C++:2023 would cover
  only the C++17 part of the code. It is the planned second step, not a dead end.
- **Rust**: on the learning list too, but a much larger step on a part that has to work for T1.1 and T1.2. Its
  place is on the Linux side, later.

**Consequences.**

- **The startup code has one more job.** It runs the static constructors before `main`, or the FBL has no
  non-trivial globals. Without `constinit`, that is held by discipline and checked in the map file: an empty
  `.init_array` shows nothing runs before `main`. Nothing may still be pending at the jump to the application.
- **What C++20 would give is written by hand.** A small span type of its own for buffer and length, helpers for
  byte order and bit operations, and `static_assert` on templates where a concept would state a driver's contract.
  These are the places the C++20 migration replaces, so they are kept few and easy to find.
- **Size is watched, not assumed.** A stray `std::function`, `new` or stream pulls library code into the image.
  The map file is checked and CI reports the image size on every build.
- **The coding rules are written down in `Nexus-STM32-FBL`:** MISRA C++:2023 as the reference rule set, which
  standard headers are allowed, and the compiler flags that enforce the subset.
- **Host tests are C++ too**, built for the PC from the same sources.

**To confirm.**

- That the image links with no exception-handling or RTTI support and no allocating library code, shown by the map file.
- That the image fits the FBL's 128 KB region (SW-04) with room for Phase 3's signature checking, measured once it is built.

---

## SW-04 · The STM32 flash holds the FBL in sectors 0 to 4 and the application in sectors 5 to 11

**Decision (2026-10-11).** The STM32F407VGT6 has 1 MB of flash in one bank, in 12 sectors. The map is:

| Region | Sectors | Address range | Size |
|---|---|---|---|
| FBL | 0 to 4 (4 x 16 KB, 1 x 64 KB) | `0x08000000` to `0x0801FFFF` | 128 KB |
| Application | 5 to 11 (7 x 128 KB) | `0x08020000` to `0x080FFFFF` | 896 KB |

The FBL's vector table is at `0x08000000`. The application is linked for `0x08020000`. **No configuration (CFG) region
and no non-volatile memory (NvM) region exist yet.** Both are left open, see *Consequences*.

**Why.**

- **The FBL must be in sector 0.** At reset the core reads its stack pointer and reset vector from `0x00000000`. RM0090
  Rev 22 (section 2.4) gives three boot spaces, chosen by the BOOT pins and latched on the fourth rising SYSCLK edge after
  reset: BOOT0 low is the main flash, aliased at `0x00000000` and so starting at `0x08000000`; BOOT0 high with BOOT1 low is
  the system memory (ST's ROM bootloader, `0x1FFF0000`); both high is the embedded SRAM1. **The only boot address in the
  main flash is therefore the first sector.** The F407 has no boot-address option byte, and the dual-bank boot bit (BFB2)
  belongs to the F42x and F43x. `SYSCFG_MEMRMP` can change what is mapped at `0x00000000` after the boot, which is not a
  second boot address. A region of constants in sector 0 was proposed and dropped for this reason.
- **128 KB is room, not a measured need.** The in-house FBL is expected to fit in far less, but it is not written and
  SW-02 means no library footprint exists to compare against. Phase 3 adds signature checking and anti-rollback to the
  FBL. The application's start address is the one value every application build depends on, so it is fixed generously
  now rather than moved later.
- **The application starts on a 128 KB sector boundary.** Its first erase unit is a full sector, and the region is a
  whole number of sectors of one size.
- **The FBL region is 5 sectors.** Sector 4 is 64 KB, so the FBL-Updater erases four small sectors and one 64 KB sector
  when it rewrites the region.

**Rejected.**

- **FBL of 64 KB (sectors 0 to 3), the first proposal.** Smaller, but it gives Phase 3 no room, and moving the application
  start later breaks every application build.
- **FBL in sectors 5 to 7 (384 KB).** Reset cannot reach it, and it is far larger than the FBL needs.
- **NvM in the 16 KB sectors, with the FBL in sector 0 only (32 KB).** The small sectors minimise the erase time, but a
  32 KB FBL has no room for Phase 3.

**Consequences.**

- **The ST ROM bootloader stays available as a second recovery path.** With BOOT0 high and BOOT1 low the device boots
  from the system memory and offers USART1, USART3, CAN2 and USB DFU (RM0090 section 2.4). It is not used for updates
  (SW-01) and the vehicle's bus is CAN1, but it can reflash a device whose FBL has been lost without the ST-LINK. Its
  entry depends on the BOOT0 pin being reachable on the carrier, which is a hardware question.
- **Flash erase and program stall every flash read on this single-bank part.** Code and data in SRAM keep running, but an
  application that fetches from flash waits for the erase to finish. At 3.3 V with 32-bit programming the datasheet
  (DS8626 Rev 8, Table 40) gives a typical and maximum erase time of 250 ms and 500 ms for a 16 KB sector, 550 ms and
  1.1 s for the 64 KB sector, and 1 s and 2 s for a 128 KB sector. A word takes 16 µs typical and 100 µs at most to program. For a flash-based NvM that means **erase and
  garbage collection can only happen in a safe vehicle state** (standby or off), never while a control loop runs.
  Putting the whole control path in RAM is not a practical way around it.
- **NvM is deferred to Phase 2**, where the plan places configuration and calibration parameters. The options then are
  flash with erase only in a safe state, or an external memory on I²C (no erase, no garbage collection, needs a BOM
  item and a hardware decision). If NvM is on-chip, it is carved from the top of the application region, so only the
  application's end moves and never its start.
- **The FBL-Updater rewrites sectors 0 to 4 and the rewrite is not power-fail safe.** The erase alone takes about 1.6 s
  typical and 3.1 s at most (four 16 KB sectors and the 64 KB one). A power loss from the first erase until the new
  vector table is written leaves no valid FBL, and the ST-LINK is the recovery path, as T1.2 already says.
- **The first FBL goes on with the ST-LINK, by sector erase.** A full-chip erase would also wipe any later NvM.
- **The interface headers and `memory_map.ld` in `Nexus-STM32-FBL` carry these addresses**, and both the FBL and the
  application build take them from there.

**To confirm.**

- ~~The sector layout and addresses.~~ Checked against RM0090 Rev 22, Table 5 (2026-10-11): 4 x 16 KB from `0x08000000`,
  one 64 KB sector at `0x08010000`, 7 x 128 KB from `0x08020000`, last address `0x080FFFFF`.
- That the FBL fits the region with room for Phase 3, measured once it is built.

---

## SW-05 · The FBL uses the main SRAM only, leaves the CCM empty and does not use the FPU

**Decision (2026-10-11).** The FBL places its stack, variables and buffers in the main SRAM at `0x20000000`. **The
64 KB core-coupled memory (CCM) at `0x10000000` is left empty.** The FBL is built without floating point
(`-mfloat-abi=soft`) and never enables the FPU.

**Why.**

- **Nothing in the FBL needs the CCM.** It reaches the CPU through the data bus only, so no DMA contention touches it,
  which makes accesses deterministic. The FBL has no timing that depends on that. The CCM stays free for data that
  does, when there is some.
- **The hand-off from the application is simpler in the main SRAM.** The CCM cannot hold code or DMA buffers and sits in
  a separate region, so a block that both images agree on lives in the main SRAM.
- **The FBL has no floating-point work.** The FPU is off after reset and the FBL leaves it so. The application
  enables it, which Zephyr does itself. The two images are never linked together, so their ABIs need not match.

**Rejected.**

- **Stack in the CCM from the start**: gains determinism the FBL does not need, and adds a second region to the linker
  script and the startup code.
- **Hard-float in the FBL**: no benefit, and a lazy-stacking cost on interrupt entry for no gain.

**Consequences.**

- `fbl.ld` describes one RAM region. The CCM is not in it.
- The location of the hand-off block in the main SRAM is a separate entry, with the entry rules.

**To confirm.**

- That the main SRAM contents survive the software reset by which the application hands over to the FBL. This is the
  condition for the hand-off record, and it is checked against RM0090 and then on the board.
