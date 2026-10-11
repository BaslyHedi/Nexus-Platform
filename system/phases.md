# Phases

What NEXUS is built in, in what order, and **when each phase is finished**. This file owns the phase
plan; the drawing carries only the phase a logical component first appears in
([`renders/Nexus-Platform-Logical-Architecture.svg`](renders/Nexus-Platform-Logical-Architecture.svg)), and the reasoning
for having phases at all is [SYS-02](../decisions/SYS-System-Decisions.md).

**Pace is set by learning, not by the calendar.** Nothing here has a date. A phase is done when its exit
criteria are true, and it is fine, even intended, to build a thing twice if the second time teaches the
technology properly. Where a shortcut exists that would skip the learning (a vendor bootloader, a ready-made
image, a library that hides the protocol), the plan says so and takes the longer road.

**Where the learning is.** The builder is an experienced firmware and AUTOSAR engineer, so CAN, UDS,
bootloaders, drivers and RTOS fundamentals are known ground. The new ground is **embedded Linux and Yocto,
Zephyr, robotics and cybersecurity**. Plans put the effort there; the familiar parts are kept deliberately
small and standard so they do not eat the phase.

## At a glance

| Phase | Name | Goal in one line | Logical components that start |
|---|---|---|---|
| **1** | Foundation | An assembled vehicle, a bootloader that can update the MCU over CAN, a first Linux image built from released apps, a heartbeat between the two computers, and the repositories everything else lives in | 101 102 201 202 401 501 503 504 |
| **2** | Drive | The vehicle drives under closed-loop control, supervised, from a remote station | 203 402 403 |
| **3** | Platform | The software stack is production-shaped: Yocto product image, containers, secure boot, signed updates, CI/CD | 502 |
| **4** | Perception | The vehicle senses and localises itself: Raspberry Pi 5, ROS 2, camera and range sensors | 301 302 |
| **5** | Autonomy | The vehicle plans and drives a mission by itself | 303 |

A logical component starting in a phase does not mean it is finished there. 201, 202, 501, 503 and 504 start in Phase 1 with
a thin first cut (201 and 202 as hardware only, not yet driven) and grow in later phases; the table at the end says which functions land when.

---

## Phase 1 - Foundation

> **Goal.** The vehicle exists, its two computers can talk to each other over CAN, the MCU can be re-flashed
> over that bus with no debugger attached, a first Linux image boots from built, released apps, and the
> project's repositories are in place so every later phase has somewhere to go.

**Phase 1 is deliberately not about driving.** No motors, no control loops, no autonomy, no teleop. The success
case is a boring one: each test below passes, on the real vehicle, with its evidence kept. The most important
deliverable is the last one, the structure.

**Each test is its own milestone, closed on its own time.** None is meant to be finished in one session; the
pace is set by what is being learned on the way (see the top of this file). A test closes when its pass
criteria are met and the evidence named in it exists, and not before.

### Deliverables

| # | Deliverable | Done when |
|---|---|---|
| 1.1 | **Assembled vehicle** | Everything in [`../bom/BOM.md`](../bom/BOM.md) marked Phase 1 is fitted per [`../hardware/README.md`](../hardware/README.md); powers up from the battery with the harness checks passed; the fascia is on |
| 1.2 | **CAN IDs for flashing** | The bus bit rate and timing (500 kbit/s, classic CAN) and the identifiers the bootloader uses (Cyphal node IDs, subjects and services for update, heartbeat and node info) are written down and **tagged as a release** in `Nexus-CAN-Utils`. **The application messages are not part of Phase 1**: their layer and content are decided in Phase 2 |
| 1.3 | **Bench demo** | The tests below pass |
| 1.4 | **STM32 FBL** (flash bootloader) | A small bare-metal resident bootloader that, on request over CAN, receives an image by Cyphal file transfer, erases, writes and verifies it, then jumps to it. A broken or absent image leaves the FBL reachable. Unsigned and unencrypted: security is Phase 3 |
| 1.5 | **STM32 app and FBL-Updater** | Two images the FBL can download: a **minimal app** (Zephyr: LED pattern, Cyphal heartbeat, shows what it hears) and an **FBL-Updater**, an image (toolchain decided when it is written) whose only job is to rewrite the FBL's own flash region, since a bootloader cannot overwrite itself while running |
| 1.6 | **FRDM image and apps** | The Yocto repository and the first Linux apps (one repository each) described in tests T2.1 and T2.2 |
| 1.7 | **Project structure** | The repositories below exist, each builds in CI from a clean clone and cites decision IDs back to this one |

### Bench demo: tests and pass criteria

**STM32 side**

| Test | What it proves | Pass criteria | Evidence |
|---|---|---|---|
| **T1.1** Flashable app | The FBL can take a new application over CAN, with no ST-LINK | An app image is sent from the PC adapter, then from the FRDM once T2.3 passes. The FBL verifies it and the STM32 boots into it. **10 consecutive cycles** with two different builds, each shown by the version in its node info. A download interrupted by pulling the CAN cable or the power leaves the FBL reachable and the next download succeeds | `candump` of one full download; the flasher's log of the 10 cycles |
| **T1.2** Flashable FBL-Updater | The FBL itself can be replaced over CAN | The FBL-Updater is downloaded exactly like an app, runs, and rewrites the FBL region with a new build. After a power cycle the new FBL is the one running (shown by its version), and T1.1 still passes with it. The very first FBL goes on with the ST-LINK, which stays the recovery path | Flasher log; node info before and after |
| **T1.3** LED patterns | You can tell by looking what the STM32 is running | The four on-board LEDs show a pattern **distinct for each state**: FBL idle, FBL receiving, FBL-Updater running, app running. Each is recognisable at arm's length without the others being confused with it, and the patterns are written down in the FBL's and app's repositories | A short video showing all four states |

**FRDM side**

| Test | What it proves | Pass criteria | Evidence |
|---|---|---|---|
| **T2.1** Apps and their CI | One repository per Linux app works as a unit | At least two throwaway apps, each in **its own repository**, that print their own name and version. Each repository's CI builds from a clean clone on every push (cross-built for the i.MX 91) and publishes a **release artifact on a tag** | The CI runs and the two releases |
| **T2.2** Yocto image | The image is reproducible and carries the released apps | A separate Yocto repository, built with `kas` from a clean clone, **fetches the apps at their release tags** and builds a minimal image that **boots from the SD card on the FRDM-IMX91**. Logging in, both apps are present and print their names and versions | The boot log; the `kas` config and build log |
| **T2.3** CAN exchange | The two nodes talk | On the vehicle's bus at 500 kbit/s, **the FRDM sends a Cyphal heartbeat and the STM32 shows that it receives it**, and **the STM32 sends one that the FRDM sees**, at the heartbeat rate, for **10 minutes with no error frames, bus-off or missed heartbeat**. The PC adapter, as the third node on the DE-9 port, sees both streams. The Linux side needs a small program for this, which is a third app repository | `candump` from the FRDM and from the PC adapter |

### Exit criteria

Phase 1 is finished when **T1.1 to T1.3 and T2.1 to T2.3 have all passed**, the evidence for each is committed or
linked, and the repositories of 1.7 exist.

### Not tested in Phase 1

The motors, steering servo, encoders, INA226 and fascia controls. They are exercised when the STM32 application
work starts, as the first step of Phase 2 (see its table), so the "every part is functional" check is
split: the **bus, both computers and the update path** in Phase 1, the **actuators and sensors** in Phase 2.

### Learning focus

**New:** **OpenCyphal** (the protocol the bootloader speaks, [SW-01](../decisions/SW-Software-Decisions.md)); the **Yocto** workflow end to end (layers, recipes, `kas`, the NXP BSP, machine and image
configuration, device tree and kernel configuration for the FRDM-IMX91); **embedded Linux user space**
(SocketCAN, writing and cross-building a C++ program, the Cyphal file server and flashing client running on Linux); **Zephyr** (west,
devicetree, Kconfig, a board definition for the carrier, how it differs from an AUTOSAR-style stack); and **CI
and repository structure** across firmware, Linux and tooling.

**Known, so kept lean:** CAN itself, the bootloader mechanics (flash, vector table, CRC, jump) and the repo
layout. The FBL is bare-metal and small and built to the usual pattern; only the protocol on top of it is new. The point of Phase 1 is that they work and are structured well,
so the new ground has something solid to stand on.

### Repositories (Phase 1.7)

The rule from [`../README.md`](../README.md) stands: **this repository is the definition and holds no code.**
Every repository below carries a short `README.md` and a `CLAUDE.md`, a CI workflow, and cites `HW-` / `SYS-` /
`SW-` IDs back here rather than restating them. Names follow `Nexus-<Name>`, like this one.

| Repository | Owns | Produces | Consumes |
|---|---|---|---|
| **Nexus-Platform** (exists) | Definition: system, decisions, hardware, mechanical, BOM, phases | Decision IDs | |
| **Nexus-STM32-FBL** | The flash bootloader: **bare-metal, small by design** (no RTOS, no HAL beyond what the CAN and flash drivers need), its memory map and its protocol implementation | `fbl.elf` | CAN-Utils release (bootloader frames) |
| **Nexus-CAN-Utils** | **The CAN matrix** (document, ID plan, and the Cyphal data types and subject/service IDs that carry it), its **generators** (C and Linux bindings, which will keep moving), and the **Cyphal flashing client**: a file server that offers an app image to the FBL, which pulls it ([SW-01](../decisions/SW-Software-Decisions.md)). The client is Linux-portable, so it runs from the PC adapter now and from the i.MX 91 later. Capture/replay and the bench-demo runner start here too, and can be split out if they grow | **Tagged releases** `vMAJOR.MINOR.PATCH`; the flasher binary | Decision IDs |
| **Nexus-STM32-App** | The Zephyr application the FBL loads (west workspace, own board definition for the carrier) | `app.bin` | CAN-Utils release, the FBL's memory map |
| **Nexus-IMX91-Yocto** | The Yocto layer `meta-nexus`, the build manifest, the image recipe, kernel and device-tree changes | Bootable image | NXP BSP, apps by tag |
| **One repository per Linux app** (`Nexus-<AppName>`, names as they are made) | One program each, with **its own CI, versioning and releases** (C++ first, Rust where it earns its place). Phase 1 has two throwaway name-printing apps and the heartbeat program (T2.1, T2.3) | A release artifact per tag | CAN-Utils release, where it speaks CAN |

Three relationships carry the whole structure:

- **Matrix to everyone.** The matrix is one shared artifact with its own repository, because the interface it
  generates will keep changing. Nothing hand-copies a message definition: the STM32 App, the FBL and the Linux
  programs each **pin a CAN-Utils tag** and build against what it generates. A matrix change that breaks a consumer
  shows in the consumer's CI.
- **Open: how a consumer takes the tag.** A git submodule, a pinned fetch in the build (for Linux, a Yocto recipe
  that fetches the release and generates bindings at build time), or a published release artifact. It can differ
  per consumer and is the first `SW` entry of each. It must make a mismatch a build error.
- **Apps to image.** The Yocto recipe fetches an app repository at a tag, so Linux-side software is built and
  versioned on its own and the image only assembles it. This is the pattern Phase 3's containers and OTA will
  extend.

**Decided already (2026-10-11):** the FBL is bare-metal, to keep it small and fast; the CAN matrix and the flashing client share one repository, `Nexus-CAN-Utils`; the Yocto build is driven by `kas`. The flash protocol is **OpenCyphal** ([SW-01](../decisions/SW-Software-Decisions.md)). The others get their `SW-` entry when written down.

**Decided in Phase 1, recorded as `SW-nn` as each one is made:** the flashing IDs and bus timing, the language of the
flashing client (it must run on Linux, which points at C++ or Rust), and how each consumer takes a release; the
CI service and repository template; the branching and tag rules shared by all repositories. **The STM32 decisions
(flash memory map, how a valid app is recognised, entry rules for the FBL, the pin map, the board definition, the
LED patterns) are recorded when the STM32 repositories are created and the work starts**, not before. The
application layer and the matrix beyond flashing are **Phase 2**.

### Out of Phase 1

The application messages of the CAN matrix, motors, steering, encoders and the INA226 (first thing in Phase 2), closed-loop speed and steering control, odometry, the IMU, operator input beyond bench tools, Wi-Fi teleop,
containers, secure boot, signed images, OTA of the Linux side, the Pi 5, ROS 2, any sensor. None is forbidden if it comes free, but none gates the phase.

---

## Phase 2 - Drive

> **Goal.** The vehicle drives properly: speed and steering in closed loop on the MCU, supervised by a mode
> manager, commanded from the Linux side and from a remote station over Wi-Fi.

| Deliverable | Notes |
|---|---|
| Actuator and sensor bring-up | First step: test the motors both ways, the steering through its range, the encoders (including whether the Encoder Motor Module times out when I²C commands stop, [HW-17](../decisions/HW-Electrical-Decisions.md)), the INA226 and the fascia controls, from the STM32 app |
| Application layer and CAN matrix | Decide whether the application messages are also Cyphal, then write the matrix: message set, cycle times, time-outs, versioning ([SW-01](../decisions/SW-Software-Decisions.md)) |
| Speed and steering loops on the STM32 | Encoder feedback, PID with limits on speed, acceleration, jerk and steer rate; kinematics from speed + curvature to wheel setpoints (Ackermann) |
| Motion state and odometry | Wheel speed to pose; the IMU joins here if it is bought |
| Vehicle modes and safe stop | A small state machine (off, standby, manual, fault), watchdogs, command time-outs end to end, emergency stop, low-pack shutdown from the pack measurement ([SYS-01](../decisions/SYS-System-Decisions.md)) |
| Diagnostics on the bus | fault codes and live data over the bus (Cyphal services or UDS, decided then); the data logger and replay on the Linux side |
| Linux services | A motion gateway and a status service as proper C++/Rust services with a defined lifecycle, not a script |
| Operator interface and link | Gamepad or keyboard teleop from a laptop over Wi-Fi, vehicle status on the fascia LEDs and in a telemetry stream |

**Done when** the vehicle can be driven around a room from a laptop with a visible speed and steering response
that matches the commanded values within stated limits, loses the link and stops by itself, and every stop and
fault is explained by a logged event.

**Learning focus:** Linux services done properly (systemd, IPC, lifecycle, logging), the network link and teleop
from the Linux side, the vehicle model (Ackermann kinematics, odometry), and Zephyr in depth. Control loops
and safety state machines are known ground, kept simple.

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

**Learning focus:** the **cybersecurity** stack on a real part: the i.MX 91 chain of trust and trusted
execution, key management, signed and measured boot, authenticated messaging, A/B and rollback design,
containers on embedded Linux, and release engineering.

## Phase 4 - Perception

> **Goal.** The vehicle knows what is around it and where it is.

| Deliverable | Notes |
|---|---|
| Raspberry Pi 5 joins the bus | Second vehicle computer; power, mounting and network decided in a new `HW`/`MEC` entry first |
| ROS 2 | Middleware on the Pi 5 (and a gateway to the i.MX 91 side); the service-middleware half of Nexus-Logical-401 |
| Sensors | Camera first, then a range sensor or LiDAR; time-synchronised with the vehicle |
| Perception | Obstacle and free-space detection, with a confidence output |
| Localization | Odometry, IMU and perception fused into a pose; a map |

**Done when** the vehicle, driven by hand, builds a map of a room and reports its own pose against it with a
confidence that drops when it should.

**Learning focus:** robotics from scratch: ROS 2 (nodes, transforms, time), sensor integration, SLAM and sensor fusion.

## Phase 5 - Autonomy

> **Goal.** The vehicle drives a mission by itself and stops safely when it cannot.

| Deliverable | Notes |
|---|---|
| Mission and route | A goal in the map and a route to it |
| Behaviour and trajectory | Driving behaviour, collision-free trajectory, issued as speed + curvature requests into Nexus-Logical-203 |
| Arbitration | Autonomous requests arbitrated with manual and teleop; the operator can always take over |
| Safety case | The supervision layer treats the planner as an untrusted source |

**Done when** the vehicle drives a short course it has not driven before, avoids an obstacle placed in its
path, and hands control back on request.

**Learning focus:** planning and behaviour for a vehicle (route, trajectory, obstacle avoidance) and treating an autonomy stack as an untrusted source from the safety side.

---

## What each logical component carries, by phase

Logical components that start in Phase 1 but continue after it, and what lands when. Anything not listed arrives whole
in its starting phase.

| Logical component | Phase 1 | Later |
|---|---|---|
| 201 Propulsion, 202 Steering | The motors, servo and driver fitted and powered, **not driven** | **2:** bring-up, then driven from the STM32 app |
| 203 Vehicle Motion Control | Starts in Phase 2 | **2:** translate requests to setpoints, close the loops, limits, odometry, safe-stop. **5:** arbitrate autonomous requests |
| 501 Supervision & Safety | The hardware switches and fuse protection already built (HW-03, HW-08, HW-20) | **2:** command time-out and watchdog, modes and transitions, safe stop, fault handling, low-pack shutdown |
| 503 Diagnostics & Data Logging | The DE-9 CAN port, SWD, UART; `candump` capture of the demo | **2:** fault codes and event data, logging and replay. **3:** health monitoring in CI |
| 504 Software Update & Config. | **FBL: download an app over CAN, verify by CRC, jump** | **2:** configuration and calibration parameters. **3:** signed images, OTA with A/B slots and rollback |
| 401 In-Vehicle Communication | The bus, the flashing identifiers, a heartbeat, SocketCAN | **2:** the application layer and matrix. **3:** message protection (with 502). **4:** ROS 2 / SOME/IP, time synchronisation |

## Changing the plan

Moving a logical component between phases, or an item between deliverables, is an edit here plus the `PHASES`/card
entry in [`scripts/Nexus-Platform-Logical-Architecture.py`](scripts/Nexus-Platform-Logical-Architecture.py) and a regenerated
drawing; the decision that shaped the split is [SYS-02](../decisions/SYS-System-Decisions.md). A phase's exit
criteria change only by an explicit decision, and a change made because the phase is hard is the one to avoid.
