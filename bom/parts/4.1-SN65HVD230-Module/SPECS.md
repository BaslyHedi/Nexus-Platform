# 4.1 - SN65HVD230 CAN transceiver module

Captured 2026-10-03 from the seller's dimensioned listing image (**GERUI**, *SN65HVD230 CAN Bus
Module 3.3V CAN Transceiver*) and from photos of the part. The image is the seller's and is
**not in the repository**; the numbers below are the whole of what it gave us.

## Dimensions

| | Value |
|---|---|
| **Overall length** | **26.98 mm**, from the outer face of the pin header's plastic to the far end of the board |
| Header plastic to the screw terminal | 23.24 mm |
| Screw terminal, along the length | ~3.7 mm of board under it, at the far end (listing: 3.68) |
| **Width** | **10.24 mm** |
| Pin header | 4 pins, 2.54 mm, **straight, in the board's plane**, out of one short end |
| Pin order | **3.3V · GND · CAN RX · CAN TX**, reading across the header with the components up and the header to the left, 3.3V on top |
| Screw terminal | 2 ways, **CANL · CANH** (CANL on the 3.3V side), wire entries out of the far end |
| **2-pin CANH / CANL header** | beside the terminal, marked CANL / CANH, on the component side: **17.25 mm** from the header face (scaled off the listing image), in line with the **GND** (CANL) and **CAN RX** (CANH) pins. A second tap of the bus, not a jumper. **This is what the carrier uses** |
| Not given | board thickness (assume 1.6 mm) and the screw terminal's height (assume ~10 mm until measured) |

## Design consequence: it lies flat on the carrier

The header pins point **along** the board, so a module plugged into an upright female socket
stands vertical. Upright on carrier board B it would reach about 50 mm above plate 2: 11.6 mm of
standoff and board, 8.5 mm of socket, 2.5 mm of header spacer and 27 mm of module. Plate 3 is
only **40 mm** above plate 2. So the module lies **flat**, either with its four pins bent 90° at
the spacer or with its header swapped for a right-angle one from the 5.11 kit.

**As bent (2026-10-03) it is face DOWN**: the pins were bent toward the component side, so the chip,
the screw terminal and the 2-pin header all point at board B. That reverses the header across the
socket, to CTX, CRX, GND, 3V3. The 2-pin CANH / CANL header then points straight down and plugs into
a 1×2 socket, seven holes behind the 4-pin row (17.55 mm on the module, 17.78 mm on the grid: set the
bend to suit). **The screw terminal is not used**, and it hangs about 1.5 mm off the board. Where it
all sits on board B is MEC-15's business
(revision 2026-10-03), drawn in [`../../../hardware/renders/stm32-carrier.svg`](../../../hardware/renders/stm32-carrier.svg).

**Still to measure:** the screw terminal's height. **Termination (2026-10-11):** the module's own 120 Ω stays on and is the STM32 end's terminator (HW-09); the carrier's TERM jumper is left open.
