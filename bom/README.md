# Part documents

One folder per BOM line item under [`parts/`](parts/), named `<BOM item>-<part>`. The BOM
([`BOM.md`](BOM.md)) owns status, price and sourcing; this tree owns **the record of the
documents, not the documents themselves**.

**No vendor document is in this repository.** They are copyrighted and not ours to
redistribute - see the root [README](../README.md). The table below carries the vendor and
the exact title of each one, which is what you search for; on a fresh clone the file itself
has to be fetched by hand.

Where a vendor publishes nothing - which is true of every Amazon power component - the
folder carries a `SPECS.md` recording what the listing claimed, with the date it was
captured and what still has to be measured on arrival. Most of the bought modules are in that
position, which is why `SPECS.md` is often the only thing there.

| Folder | Vendor documents it draws on - **not held here** | Written here | Notes |
|---|---|---|---|
| `1.1-FRDM-IMX91S` | **NXP** · *FRDM-IMX91S Quick Start Guide* · *UM12262, FRDM-IMX91 Board User Manual*, Rev 3.0, 22 Apr 2025 · *FRDM-IMX91 Design Files*, Rev A1 | `NOTES.md` | UM12262 covers the **non-S** variant - see `NOTES.md` |
| `1.2-NUCLEO-H533RE` | **STMicroelectronics** · *DS14539, STM32H533xx datasheet*, Rev 3, March 2026 · *UM3121, STM32H5 Nucleo-64 board (MB1814)*, Rev 1 | - | **MB1814 schematic**, rev C02 (in hand 2026-10-27: PA15 is tied to the ST-LINK's JTDI through SB9, HW-22). **RM0481** reference manual still missing |
| `1.2-STM32F407-Discovery` | **STMicroelectronics** · *DS8626, STM32F405/407 datasheet* · *UM1472, Discovery kit for STM32F407/417* · *STM32F4DISCOVERY data brief* | - | Now BOM 1.2a, failed 2026-10-25; kept as the record of the Discovery-era decisions. RM0090 never fetched |
| `1.3-WS2812B-LED-Stick` | none published by the seller (**Joycabin** listing) · **Worldsemi** · *WS2812B Intelligent control LED integrated light source* datasheet | `SPECS.md` | Decided, not ordered; holes not dimensioned |
| `2.1-Hiwonder-Ackermann-Chassis` | **Hiwonder** · *Ackermann chassis introduction and installation* · *docs index* (both printed from docs.hiwonder.com) · *Ackermann Chassis (Single Layer)* `.3dm` CAD | `SPECS.md` | Rear geometry measured in Hiwonder's CAD |
| `2.3-Servo-LD-1501MG` | **ThinkRobotics** · *Ackerman metal chassis listing, motor and servo specs* · **Power HD** · *HD-1501MG datasheet* | `SPECS.md` | Servo is **6–8.4 V**, not 5 V |
| `2.4-Encoder-Motor-Module` | none published | `SPECS.md` + 1:1 hole template | Vendor publishes no drawing - geometry **measured off a photo on 5 mm graph paper**, 2026-09-21 |
| `3.1-Battery-3S-LiPo` | none published | `SPECS.md` | Almost everything TBC until it arrives |
| `3.4a-Bauer-50W` | none published | `SPECS.md` | Compute rail |
| `3.4b-Bauer-15W` | none published | `SPECS.md` | MCU rail |
| `3.8-Geloo-Fuse-Block` | none published | `SPECS.md` | Includes why FULARR was rejected |
| `3.9-INA226` | **Texas Instruments** · *INA226*, SBOS547C, Aug 2026 | `SPECS.md` | Verify the module's shunt is 2 mΩ |
| `3.10-LiPo-Alarm` | none published | `SPECS.md` | Set to 3.3–3.5 V/cell |
| `4.1-SN65HVD230-Module` | **GERUI** · *SN65HVD230 CAN Bus Module 3.3V CAN Transceiver* (dimensioned listing image) | `SPECS.md` | **26.98 × 10.24 mm**; too tall to stand upright under plate 3, so it lies flat |

## Audit - 2026-09-13

Every document was opened, page-counted, text-extracted and date-checked before being set
aside. The grades are why the files are worth hunting down again - or not:

| Document | Grade | Why |
|---|---|---|
| `UM12262` FRDM-IMX91 Board UM, Rev 3.0, Apr 2025 | ✅ current, ⚠️ **wrong variant** | Authoritative and recent, but written for the **non-S** board |
| `INA226` TI SBOS547C, Aug 2026 | ✅ current | 41 pp, genuine TI datasheet |
| `FRDM-IMX91S` QSG | ✅ correct board | Only 8 pp - a getting-started card, not a manual |
| `DS8626` STM32F405/407 datasheet | ⚠️ **stale** | Mirror copy dated **September 2016**; ST is now at Rev 12, March 2026 |
| `UM1472` Discovery kit UM | ⚠️ **stale** | Dated **January 2014**. Also check which board you own: `STM32F4DISCOVERY` (ST-LINK/V2) vs `STM32F407G-DISC1` (ST-LINK/V2-A) - the silkscreen tells you |
| Hiwonder docs index | ❌ near-worthless | 1 page, 626 characters - a navigation stub that printed without its content |
| Hiwonder intro/installation | 🟡 thin | 6 pp of real text, but a JS docs site printed to PDF loses figures |
| ThinkRobotics capture | 🟡 record, not a source | A shop page. Useful because it carries the only motor/servo numbers found, but not authoritative |

Three files arrived mislabelled from the mirrors and were corrected: two ST documents had
their names swapped, and one claimed to be the STM32F407 datasheet but was actually the
**F427/429** part - deleted, and the correct DS8626 sourced elsewhere.

## Known gaps

- **FRDM-IMX91S board user manual** - does not appear to be published separately. This is
  the document that would settle the board's power input for *our* variant; UM12262 answers
  it only for the non-S board. Highest-value missing item.
- **RM0481** (STM32H52x/H53x/H56x/H57x reference manual) for the NUCLEO-H533RE - `st.com` is unreachable from this machine (connection refused, not a 404);
  Mouser and DigiKey serve bot-check pages. Fetch by hand. RM0090, the F4 manual, is no longer needed.
- **i.MX 91 SoC datasheet and reference manual** - NXP doc paths did not resolve; the RM is
  usually behind an NXP account. From nxp.com/imx91.
- **CAN transceiver** - no folder; part not chosen (BOM 4.1).
- Fresh **DS8626 Rev 12** and **UM1472 Rev 5** to replace the stale mirror copies.
