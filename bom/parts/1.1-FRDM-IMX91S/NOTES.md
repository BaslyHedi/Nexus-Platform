# 1.1 - NXP FRDM-IMX91S

Both documents below are **NXP**, copyrighted, and **not in the repository** - search the
titles on nxp.com. Everything they settled for us is written out here.

| Document | What it is |
|---|---|
| *FRDM-IMX91S Quick Start Guide* | Official QSG for **our** board. Connector map, 40-pin pinout, boot switch table, J1/J11 |
| *UM12262, FRDM-IMX91 Board User Manual*, Rev 3.0, 22 Apr 2025 | Board user manual - **for the FRDM-IMX91, not the -IMX91S** |

⚠️ UM12262 covers the non-S board. Use it for the shared FRDM form factor and board-level
detail, but **verify anything -S-specific against the QSG**. The -S adds the IW610 wireless
module and 256 MB QSPI NAND.

## Confirmed from the QSG

- **105 × 65 mm**, 10-layer (dimension from UM12262, which is the *non-S* board). ⚠️ **The -S looks about 95 × 65 mm**: in the Quick Start Guide's top and bottom views (figures 1 and 2) the outline is 95 mm long at the scale where the six mounting holes sit 49.0 mm apart, then 39.5, on a 58 mm spacing. Photo, +-1 mm. Hedi measured **96 x 67 over the connectors** (2026-10-06), which fits: the RJ45 overhangs the board edge by about 2.5 mm and the USB-A by about 1.8 mm. **Measure the bare PCB** (MEC-18)
- i.MX 91, 1× Cortex-A55 · 512 MB LPDDR4 · 256 MB QSPI NAND (NAND boot) · microSD 3.0
- IW610: Wi-Fi 6 + BLE 5.4 + 802.15.4 · 1 Gbps Ethernet · external RTC w/ coin cell
- **Power: J1, USB-C only.** No barrel jack, no terminal block
- Debug: J11 USB-C UART, 115200 8N1
- **2×5 NXP custom connector: 1× CAN port, 2× ADC channels, I2C/I3C**
- 40-pin (2×20) expansion: 5 V on pins 2/4, 3V3 on 1/17, I2C4 on 3/5, UART3 on 8/10, SPI3, SAI3, PDM
- Boot switch SW1[4-1]: `0011` = microSD (default), `0101` = FlexSPI NAND, `0001` = serial downloader
- Kit ships a 32 GB TF card with the BSP and a USB-C→A cable

## ✅ Power input - RESOLVED 2026-09-13

**The FRDM-IMX91S boots and runs from a dumb 5 V / 1 A supply.** No PD negotiation, no
12–20 V. Confirmed on the bench.

This means **UM12262 does not describe this board's power input.** That manual is written
for the FRDM-IMX91, where §2.2 states: "The primary power supply to the FRDM-IMX91 board is
VBUS_IN (12 V - 20 V) through USB Type-C PD connector (P1)", negotiated by two PTN5110 PD
PHYs with an MP8759GD bucking VBUS_IN down to 5 V internally. **None of that applies to the
-S.** The -S evidently feeds SYS_5V directly and skips the pre-buck stage - consistent with
it being the smaller board (one Cortex-A55, no M.2/PCIe) and with the kit shipping a
USB-C-to-USB-**A** cable, which can only ever carry 5 V.

**Treat UM12262's entire power chapter as not applicable to the -S.** It remains useful for
the shared FRDM form factor and for board-level detail, but not for anything on the input side.

### What this settles

| Question | Answer |
|---|---|
| Input voltage | **5 V** |
| PD negotiation required? | **No** |
| Idle/boot draw | **< 1 A** (it ran on a 1 A supply) |
| Feed from the Bauer 50 W? | **Yes** |

### Still to measure

Draw **under load** - Wi-Fi transmitting, Ethernet up, USB host peripherals, CPU busy. 1 A
is the boot/idle figure, not the budget. The 50 W converter has ample headroom either way,
but the number is needed to size the branch fuse properly.

### Connector detail

The bench test worked through a C-to-A cable, which carries a **56 kΩ Rp** in the plug and
therefore advertises only USB default current (500–900 mA). Fine on the bench; not what you
want on the robot, because a sink that honours the advertisement could current-limit itself.

On the vehicle, feed J1 from a **USB-C source pigtail with 10 kΩ Rp on both CC pins**, which
advertises 5 V @ 3 A. Note the polarity of the role: the pigtail is the *source* and needs
**Rp pull-ups**; the 5.1 kΩ pull-*downs* found on most DIY USB-C leads are the *sink* role
and are wrong here.

## Open question this folder should answer

**Are the CAN pins on the 2×5 connector already transceived, or raw TX/RX?**
Neither the QSG nor UM12262 (non-S) settles it for this board. This decides whether the
project buys one CAN transceiver or two - see BOM 4.1 / 4.2.

## Connector positions (Quick Start Guide, figures 1 and 2, 2026-10-06)

Top view with the 40-pin header on the left; u along the long edge, v along the short, mm, +-1, from the photo. Used by the compute tray's preview (MEC-18).

| Edge | Connector | Where |
|---|---|---|
| left | 40-pin header | u 0.5-6, v 7-59 |
| top | 30-pin FPC · 2x5 NXP custom header J7 (the CAN port) · USER / ONOFF / RESET | u 27-47 · u 60.5-73.5 · u 74-88, all v 1-7 |
| right | USB-C DBG (J11) · USB-C (J5) · USB-A | v 10-19 · v 27-36 · v 43-56, at u 81-97 (overhanging the edge by about 1 mm) |
| bottom | audio jack · USB-C power (J1) · RJ45 | u 16-23 · u 31-41 · u 60-77, v 54-67 (the RJ45 overhangs by 2.5 mm) |
| underside | microSD slot | u 29-45, opening to the **top** edge |
