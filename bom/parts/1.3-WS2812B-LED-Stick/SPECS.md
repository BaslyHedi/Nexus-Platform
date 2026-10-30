# 1.3 - WS2812B 8-LED stick

Captured 2026-10-27 from the seller's listing (**Joycabin**, *WS2812 RGB LED Module 8 Bit 5050 LED
Stick Pack of 10*, Amazon.de B0G648ST2C) and its dimensioned image. The image is the seller's and is
**not in the repository**. The protocol below is from Worldsemi's *WS2812B Intelligent control LED
integrated light source* datasheet, which is not held here either. **Decided 2026-10-27, not ordered
yet** (BOM 1.3); nothing below is measured.

## Dimensions and pads

| | Value |
|---|---|
| **Board** | **62 × 12 mm** (listing image), 3 g |
| LEDs | 8 × 5050 RGB with a built-in driver, about 5 × 5 mm each, on one face |
| **Mounting** | **two holes**, between LEDs 3/4 and 6/7 (photo); diameter and spacing not given, about M2-M2.5 by eye |
| Pads, input end | GND · DI · 4-7VDC · GND (back face, printed) |
| Pads, output end | GND · DO · 4-7VDC · GND, to chain a second stick |
| Supply | 4-7 V per the listing; the WS2812B datasheet says 3.5-5.3 V. **Up to about 60 mA per LED** at full white, so ~480 mA for the stick; dim status patterns take ~20 mA |
| Reverse polarity | the listing claims protection; do not rely on it |

## On NEXUS

- **Where:** on top of plate 3, just behind the FRDM, LEDs facing the rear (Hedi, 2026-10-27). How it
  stands, bracket or the 3M tape (BOM 3.25), is decided when plate 3 is assembled.
- **Wiring:** a 3-wire lead to the 1×3 header at the rear of carrier board B: DIN from **PC12**
  (SPI3_MOSI, CN7-3), 5 V and GND from B's 5V IN, never from the Nucleo (MEC-15, HW-22). The lead is
  made when the stick is mounted.
- **No level shifter** (Hedi). At 5 V the first LED wants ≥ 3.5 V on DI and PC12 gives 3.3 V. If it
  misreads, PC12 goes open-drain with a 1 kΩ pull-up from DIN to 5 V (PC12 is 5 V tolerant, HW-22).

## The protocol, in short

One wire, no clock: each bit is a high pulse then a low, **1.25 µs per bit (800 kbit/s)**.

| Bit | High | Low |
|---|---|---|
| 0 | 0.40 µs | 0.85 µs |
| 1 | 0.80 µs | 0.45 µs |

Tolerance is about ±150 ns per phase. Each LED takes **24 bits, green, red, blue, MSB first**, keeps
the first 24 it receives and re-drives the rest out of DO at its own 5 V; its place in the chain is its
address. **A low of more than 50 µs latches** the frame (newer WS2812B revisions want ~280 µs: use
300). One frame for the stick is 192 bits, about 240 µs. There is no acknowledge and no read-back.

**Consequence for firmware** (the application repository owns the design): the timing is too tight for
GPIO with interrupts on, so the waveform comes from hardware. Zephyr's `worldsemi,ws2812-spi` sends
each LED bit as several SPI bits on MOSI only (for example 3 bits at 2.4 MHz: `100` for 0, `110` for 1);
MOSI must idle low between frames.

## To check on arrival

- The hole diameter and the hole spacing, for the bracket or the screws.
- The board thickness and the LED height, for how it stands.
- Which LED it really is (WS2812B or SK6812, the listing names both kinds of stick): same protocol, the
  latch time differs.
- First light on the bench from the Nucleo at 3.3 V data: all 8 LEDs show the colour sent, warm and cold.
