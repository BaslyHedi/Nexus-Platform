# Phases

What NEXUS is built in, in what order, and **when each phase is finished**. This file owns the phase
plan; the drawing carries only the phase a sub-system first appears in
([`renders/Nexus-Platform-System-Layout.svg`](renders/Nexus-Platform-System-Layout.svg)), and the reasoning
for having phases at all is [SYS-02](../decisions/SYS-System-Decisions.md).

**Pace is set by learning, not by the calendar.** Nothing here has a date. A phase is done when its exit
criteria are true, and it is fine, even intended, to build a thing twice if the second time teaches the
technology properly. Where a shortcut exists that would skip the learning (a vendor bootloader, a ready-made
image, a library that hides the protocol), the plan says so and takes the longer road.

## At a glance

| Phase | Name | Goal in one line | Sub-systems that start |
|---|---|---|---|
| **1** | Foundation | An assembled vehicle, a released CAN matrix, a bootloader that can update the MCU over it, a first Linux image, and the repositories everything else lives in | 101 102 201 202 203 401 501 503 504 |
| **2** | Drive | The vehicle drives under closed-loop control, supervised, from a remote station | 402 403 |
| **3** | Platform | The software stack is production-shaped: Yocto product image, containers, secure boot, signed updates, CI/CD | 502 |
| **4** | Perception | The vehicle senses and localises itself: Raspberry Pi 5, ROS 2, camera and range sensors | 301 302 |
| **5** | Autonomy | The vehicle plans and drives a mission by itself | 303 |

A sub-system starting in a phase does not mean it is finished there. 203, 501, 503 and 504 start in Phase 1 with
a thin first cut and grow in later phases; the table at the end says which functions land when.

---

## Phase 1 - Foundation

> **Goal.** The vehicle exists, its two computers speak a defined and released language, the MCU can be
> re-flashed over that language with no debugger attached, and the project's repositories are in place so every
> later phase has somewhere to go.

**Phase 1 is deliberately not about driving well.** No control loops, no autonomy, no teleop. The success
case is a boring one: a bench demo that proves every part works and every wire is right, and a software
structure that will not need to be torn up in Phase 2. The most important deliverable is the last one, the
structure.

### Deliverables

| # | Deliverable | Done when |
|---|---|---|
| 1.1 | **Assembled vehicle** | Everything in [`../bom/BOM.md`](../bom/BOM.md) marked Phase 1 is fitted per [`../hardware/README.md`](../hardware/README.md); powers up from the battery with the harness checks passed; the fascia is on |
| 1.2 | **CAN matrix v1.0, defined and released** | A machine-readable matrix (DBC) and a short document exist for the 500 kbit/s classic-CAN bus: ID plan, every message with its signals, cycle time, owner and receiver, timeout behaviour, byte order and scaling, the bootloader frames, the versioning rule. It is **tagged and released**, and both sides consume the tag rather than a copy |
| 1.3 | **Wiring and parts demo** | A scripted bench run, checklist and result logged, that exercises every part once: both rails and the pack measurement, CAN loopback on both nodes and from the PC, each motor both ways, the steering through its range, the encoders, the fascia controls. A real `candump` of the run is captured |
| 1.4 | **STM32 FBL** (flash bootloader) | A small resident bootloader that, on request over CAN, erases, receives, verifies (CRC) and writes an application image, then jumps to it. A broken or absent app leaves the FBL reachable. A new app goes on with **no ST-LINK**. Unsigned and unencrypted: security is Phase 3 |
| 1.5 | **STM32 minimal app** | The thing the FBL downloads. Zephyr on the F407; decodes the matrix's command frames, drives motors and steering **open loop**, stops if commands stop (command time-out), and sends a heartbeat and a state frame. Nothing smarter |
| 1.6 | **FRDM minimal image** | A first Yocto build for the FRDM-IMX91 (NXP BSP, own layer, own image recipe) that boots, brings `can0` up at the matrix's bit rate, and runs a small program that sends the matrix's messages and prints what comes back |
| 1.7 | **Project structure** | The repositories below exist, each builds in CI from a clean clone, each cites decision IDs back to this one, and the matrix flows to both firmware and Linux as a pinned release |

### Exit criteria

Phase 1 is finished when, on the finished vehicle, with no ST-LINK connected:

1. The i.MX 91 (or the PC adapter) flashes a new STM32 app over CAN, the STM32 boots into it, and the heartbeat
   in the matrix shows the new app's version.
2. The FRDM sends a motion command from the released matrix and the vehicle moves; stopping the commands stops
   the vehicle.
3. The demo (1.3) passes end to end and its log is committed or linked.
4. Changing a signal in the matrix is a version bump and a PR in one repository, after which the firmware and the
   Linux program both pick it up by version, and a mismatch is a build error and not a bench surprise.

### Learning focus

CAN at the frame level (arbitration, bit timing, error states) and the matrix as an interface contract; a
flash bootloader and the flash/vector-table mechanics behind it; Zephyr (devicetree, Kconfig, west, drivers,
threads) on a board that is not the usual one; the first Yocto build (layers, recipes, `kas` or manifest, BSP, device
tree); SocketCAN; CI for embedded targets; and repository structure as an engineering product.

### Repositories (Phase 1.7)

The rule from [`../README.md`](../README.md) stands: **this repository is the definition and holds no code.**
Every repository below carries a short `README.md` and a `CLAUDE.md`, a CI workflow, and cites `HW-` / `SYS-` /
`SW-` IDs back here rather than restating them. Names follow `Nexus-<Name>`, like this one.

| Repository | Owns | Produces | Consumes |
|---|---|---|---|
| **Nexus-Platform** (exists) | Definition: system, decisions, hardware, mechanical, BOM, phases | Decision IDs | |
| **Nexus-CAN-Matrix** | The contract: DBC, the document, the bootloader frame set, and a generator for the C header and the Linux-side bindings | **Tagged releases** `vMAJOR.MINOR.PATCH` | Decision IDs |
| **Nexus-STM32-FBL** | The flash bootloader, its memory map and its protocol implementation | `fbl.elf` | Matrix release |
| **Nexus-STM32-App** | The Zephyr application the FBL loads (west workspace, own board definition for the carrier) | `app.bin` | Matrix release, the FBL's memory map |
| **Nexus-IMX91-Linux** | The Yocto layer `meta-nexus`, the build manifest, the image recipe, kernel and device-tree changes | Bootable image | NXP BSP, apps by tag |
| **Nexus-IMX91-Apps** | Linux-side programs (C++ first, Rust where it earns its place); starts as the minimal CAN sender | Binaries, packaged by a Yocto recipe | Matrix release |
| **Nexus-Host-Tools** | PC-side: the CAN flasher for the FBL, the bench-demo runner, log capture and replay | Python/Rust CLI | Matrix release |

Two relationships carry the whole structure:

- **Matrix to everyone.** Nothing hand-copies a message definition. The matrix repo generates, the consumers
  pin a tag. A matrix change that breaks a consumer shows in the consumer's CI.
- **Apps to image.** The Yocto recipe fetches an app repository at a tag, so Linux-side software is built and
  versioned on its own and the image only assembles it. This is the pattern Phase 3's containers and OTA will
  extend.

**Decided in Phase 1, recorded as `SW-nn` as each one is made:** the matrix's ID plan and tooling; the flash
protocol (a UDS-style download service set over ISO-TP is the automotive way and the better lesson, a bespoke
frame set is faster; the plan assumes UDS/ISO-TP and the first `SW` entry confirms or overturns it); the FBL's
memory map and how the app is told apart from garbage; whether the FBL is bare-metal or a Zephyr-based image
(MCUboot does not download over CAN, so it is not a shortcut here); the repository and CI template; the
build-manifest tool (`west`, `kas`, `repo`); the branching and tag rules shared by all repositories.

### Out of Phase 1

Closed-loop speed and steering control, odometry, the IMU, operator input beyond bench tools, Wi-Fi teleop,
containers, secure boot, signed images, OTA of the Linux side, the Pi 5, ROS 2, any sensor beyond what the demo
needs. None is forbidden if it comes free, but none gates the phase.

---

## Phase 2 - Drive

> **Goal.** The vehicle drives properly: speed and steering in closed loop on the MCU, supervised by a mode
> manager, commanded from the Linux side and from a remote station over Wi-Fi.

| Deliverable | Notes |
|---|---|
| Speed and steering loops on the STM32 | Encoder feedback, PID with limits on speed, acceleration, jerk and steer rate; kinematics from speed + curvature to wheel setpoints (Ackermann) |
| Motion state and odometry | Wheel speed to pose; the IMU joins here if it is bought |
| Vehicle modes and safe stop | A small state machine (off, standby, manual, fault), watchdogs, command time-outs end to end, emergency stop, low-pack shutdown from the pack measurement ([SYS-01](../decisions/SYS-System-Decisions.md)) |
| Diagnostics on the bus | UDS-style read/clear of fault codes and live data; the data logger and replay on the Linux side |
| Linux services | A motion gateway and a status service as proper C++/Rust services with a defined lifecycle, not a script |
| Operator interface and link | Gamepad or keyboard teleop from a laptop over Wi-Fi, vehicle status on the fascia LEDs and in a telemetry stream |

**Done when** the vehicle can be driven around a room from a laptop with a visible speed and steering response
that matches the commanded values within stated limits, loses the link and stops by itself, and every stop and
fault is explained by a logged event.

**Learning focus:** control loops on an RTOS and their timing, the vehicle model, state machines for safety,
UDS diagnostics, writing long-running Linux services.

## Phase 3 - Platform

> **Goal.** The software stack is shaped like a production vehicle's: a reproducible image, isolated services,
> a chain of trust, and updates that cannot brick the car.

| Deliverable | Notes |
|---|---|
| Product Yocto image | Read-only root, A/B slots, defined services, reproducible build in CI |
| Containerised services | Services in containers on the i.MX 91, with their own interfaces and resource limits |
| Secure boot | i.MX 91 secure boot with its own key hierarchy, trusted execution; measured boot where the part allows |
| Secured bootloader | The FBL from Phase 1 gains signature checking and anti-rollback; images are signed in CI |
| OTA | A/B update of the Linux side with integrity check and rollback; the MCU updated through the FBL by the Linux side |
| Message protection | Authenticated CAN messages (a SecOC-style scheme) and key provisioning |
| CI/CD | Build, test, sign and release across all repositories; hardware-in-the-loop smoke test on the real vehicle |

**Done when** a deliberately broken or unsigned update is rejected by both the MCU and the Linux side, a
failed update rolls back by itself, and a release goes from a merged PR to the vehicle without a hand-built
step.

**Learning focus:** the chain of trust, key management, A/B and rollback design, containers on embedded Linux,
release engineering.

## Phase 4 - Perception

> **Goal.** The vehicle knows what is around it and where it is.

| Deliverable | Notes |
|---|---|
| Raspberry Pi 5 joins the bus | Second vehicle computer; power, mounting and network decided in a new `HW`/`MEC` entry first |
| ROS 2 | Middleware on the Pi 5 (and a gateway to the i.MX 91 side); the service-middleware half of Nexus-SubSys-401 |
| Sensors | Camera first, then a range sensor or LiDAR; time-synchronised with the vehicle |
| Perception | Obstacle and free-space detection, with a confidence output |
| Localization | Odometry, IMU and perception fused into a pose; a map |

**Done when** the vehicle, driven by hand, builds a map of a room and reports its own pose against it with a
confidence that drops when it should.

## Phase 5 - Autonomy

> **Goal.** The vehicle drives a mission by itself and stops safely when it cannot.

| Deliverable | Notes |
|---|---|
| Mission and route | A goal in the map and a route to it |
| Behaviour and trajectory | Driving behaviour, collision-free trajectory, issued as speed + curvature requests into Nexus-SubSys-203 |
| Arbitration | Autonomous requests arbitrated with manual and teleop; the operator can always take over |
| Safety case | The supervision layer treats the planner as an untrusted source |

**Done when** the vehicle drives a short course it has not driven before, avoids an obstacle placed in its
path, and hands control back on request.

---

## What each sub-system carries, by phase

Sub-systems that start in Phase 1 but continue after it, and what lands when. Anything not listed arrives whole
in its starting phase.

| Sub-system | Phase 1 | Later |
|---|---|---|
| 203 Vehicle Motion Control | Translate a speed + curvature request to open-loop setpoints; report motion state | **2:** close the loops, limits, odometry, safe-stop. **5:** arbitrate autonomous requests |
| 501 Supervision & Safety | Command time-out, heartbeat watchdog, the hardware switches and fuse protection already built | **2:** modes and transitions, safe stop, fault handling, low-pack shutdown |
| 503 Diagnostics & Data Logging | The DE-9 CAN port, SWD, UART; `candump` capture of the demo | **2:** fault codes and event data, logging and replay. **3:** health monitoring in CI |
| 504 Software Update & Config. | **FBL: download an app over CAN, verify by CRC, jump** | **2:** configuration and calibration parameters. **3:** signed images, OTA with A/B slots and rollback |
| 401 In-Vehicle Communication | CAN matrix v1.0 and SocketCAN | **3:** message protection (with 502). **4:** ROS 2 / SOME/IP, time synchronisation |

## Changing the plan

Moving a sub-system between phases, or an item between deliverables, is an edit here plus the `PHASES`/card
entry in [`scripts/Nexus-Platform-System-Layout.py`](scripts/Nexus-Platform-System-Layout.py) and a regenerated
drawing; the decision that shaped the split is [SYS-02](../decisions/SYS-System-Decisions.md). A phase's exit
criteria change only by an explicit decision, and a change made because the phase is hard is the one to avoid.
