# NEXUS Platform

A personal 4-wheel **Ackermann-steering autonomous robot**, built as a learning and
engineering platform rather than a hobby RC car. It is a miniature of a modern
automotive E/E and software architecture, used to get hands-on with the real thing.

## Target

Evolve a manually controlled robot into an **autonomous-driving demonstrator** carrying a
modern automotive-style software stack. The platform is the vehicle for learning:

C++ · Rust · Embedded Linux · Yocto · MCU/RTOS · CAN · autonomous-driving concepts ·
sensors and actuator control · secure boot and trusted execution · OTA updates ·
containerised / service-oriented architecture · CI/CD.

The defining principle is the automotive split between **high-level compute** and
**real-time control**, with a network in between - not one board doing everything.

## Platform definition

```text
                        3S 11.1 V LiPo
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        Hiwonder drive   5 V DC-DC        (future nodes)
         /steering            │
                              ▼
                      ┌───────────────┐
                      │   i.MX 91     │  Embedded Linux · Yocto
                      │   (MPU)       │  C++/Rust · networking · security · OTA
                      └───────┬───────┘
                              │ CAN
                      ┌───────┴───────┐
                      │  STM32F407    │  real-time control · RTOS (Zephyr)
                      │  (MCU)        │  motor + steering loops · sensors · safety
                      └───────┬───────┘
                              ▼
                     Motors / Steering servo
                              │
                      Ackermann chassis
```

### Compute

| Role | Part | Responsibility |
|---|---|---|
| High-level compute | **NXP i.MX 91** | Embedded Linux, Yocto, application software, networking, security, OTA |
| Real-time control | **STM32F407VGT6 Discovery** | motor and steering control loops, sensor acquisition, safety, CAN |
| Future node | **Raspberry Pi 5** | ROS 2, vision/AI, second vehicle computer - *not* a Phase-1 dependency |

### Chassis and power

- **Hiwonder advanced bundle** - 4-wheel chassis, **2 driven rear motors + front Ackermann steering servo**, drive hardware.
- **3S 11.1 V LiPo** + charger. The battery never feeds a compute board directly; a single
  **5 V DC-DC buck converter** provides the regulated rail for both compute boards, and the
  steering servo runs off its own 6 V UBEC.

### Network

CAN is the link between compute and control. The STM32F407 has an **integrated CAN
controller** and reaches the bus through an external **SN65HVD230**; the FRDM-IMX91S carries
its own transceiver on board and presents CAN_H/CAN_L on its 2×5 connector. A **DE-9 debug
port** on the rear fascia lets a PC join the bus as a third node.

## Decisions already made

| # | Decision | Rationale |
|---|---|---|
| 1 | **Ackermann**, not differential drive | closer to a real vehicle; better for control and AD learning |
| 2 | Name is **NEXUS** | chosen over APEX |
| 3 | **i.MX 91** as main computer, not the Pi 5 | automotive/embedded-oriented; better for Linux, security, production-style work |
| 4 | **STM32F407** as the real-time MCU | already owned; integrated CAN; good Zephyr target |
| 5 | Pi 5 deferred to a later phase | keeps the initial platform from getting needlessly complex |
| 6 | **3S 11.1 V** battery | comes with the Hiwonder setup |
| 7 | Regulated 5 V via **DC-DC**, never direct battery | protects the compute boards |
| 8 | STM32 internal CAN controller + **external transceiver** | no external controller needed |

Treat these as settled. Revisit one only if asked, or if something concrete contradicts it.

## Phase 1

Get the stack above physically working end to end: battery → regulated 5 V → i.MX 91,
CAN to the STM32, STM32 driving motors and steering. Everything else (Yocto images,
Rust services, ROS 2, sensors, security, OTA) builds on top of that once it moves.

### Open hardware items

**The power stage is bought and in hand** (delivered 18 Sep 2026) - converter, fuses, wire,
distribution, UBEC, current sensor, CAN transceiver and the USB-C feed. No *selection* blocks
a powered-up Phase 1: the converter, both CAN transceivers and the board variant are settled.
What remains is bench verification, and the connectors that break CAN out of the two boards -
of which the FRDM's 2×5 mating connector is the only real blocker, and it is free to resolve.

Component status and quantities live in [`bom/BOM.md`](bom/BOM.md); the electrical
and mechanical rationale, and the list of what is still open, lives in
[`decisions/`](decisions/README.md).
Those two files own them; do not restate them here.

## The video series

NEXUS is the subject of a long-form video series on **The Embedded Stack**. The
engine that makes those videos lives in `~/work/EmbeddedStack-VideoGen`, and
**that repo owns everything about the videos** - the series plan, the playlist,
the per-video briefs, what is scheduled and what is blocked:

- `~/work/EmbeddedStack-VideoGen/notes/series/nexus-platform.md`
  - the four videos, the playlist title, and what each one is waiting for.

Nothing about the videos is recorded in this project, and nothing about the
platform is restated over there. The direction the facts travel is **one way**:
the files here are the source, and a brief quotes them with a link back at the
moment it is written.

Two consequences worth knowing while working here:

- **A design document is not `--reference` material.** The video engine's
  grounding flags mean "output a tool printed" and "source a human wrote in a
  public repo". `BOM.md` and the `Design-Decisions/` files are neither, so
  their facts reach a script through the brief. `fascia.scad` is the one file
  here that genuinely fits `--source`.
- **A real capture is worth making deliberately.** A `candump` off the finished
  CAN bus, a boot log from the i.MX 91, `openscad` rendering the clash check
  empty - each of those turns a video from "narrated" to "grounded". When one
  of those moments arrives, capture it even if no video needs it yet.

## Repository conventions

- **Not under source control yet.** Source code goes under git later; these folders stay
  untracked for now. Do not run `git init` here without asking.
- **No em-dashes anywhere.** Not in drawings, not in decision records, not in prose. Use a
  spaced hyphen, a colon or a comma instead. This applies to every file in the project, not
  only the drawing sheets.
- Folder names are **capitalised, no spaces, no `&`** - paths get referenced by build
  scripts and Yocto layers, and shell metacharacters are not worth the friction.

| Folder | Holds |
|---|---|
| `System-Definition/` | Functional decomposition - system layout, sub-systems, their functions and requirements |
| `Architecture/` | E/E decisions, CAN matrix, board-level architecture |
| `Architecture/Design-Decisions/` | **Every settled decision and its reasoning**, split by discipline - HW / MEC / SYS / SW |
| `Architecture/Hardware/` | Physical and electrical build drawings - chassis layout, wiring schematic |
| `Platform/` | the code - Yocto layers, STM32 firmware, Linux services |
| `RnD-Docs/` | part evaluations, datasheets, experiment notes |
| `Roadmap-Milestones/` | phase plan and what "done" means for each phase |

This file owns the platform baseline. Detail belongs in the folder that owns it - link
here rather than restating it.
