# SW · Software design decisions

Firmware and Linux-side decisions - RTOS choice and configuration, the CAN matrix in software,
service layout, build and OTA. Numbering is `SW-nn`, unique across the project and never reused.
Format, and how to add one: [README](README.md).

**None recorded yet.** Phase 1 is still hardware and packaging; the first entries here will
likely be the Zephyr board port, the CAN message set, and how the STM32 reports a fault to the
i.MX 91. Related hardware constraints they will have to respect are
[HW-10](HW-Electrical-Decisions.md) (I²C pins) and
[SYS-01](SYS-System-Decisions.md) (over-discharge protection).
