# Datasheets

One folder per BOM line item, named `<BOM item>-<part>`. The BOM
([`../BOM.md`](../BOM.md)) owns status, price and sourcing; this tree owns the documents.

Where a vendor publishes nothing - which is true of every Amazon power component - the
folder carries a `SPECS.md` recording what the listing claimed, with the date it was
captured and what still has to be measured on arrival.

| Folder | Documents | Notes |
|---|---|---|
| `1.1-FRDM-IMX91S` | QSG (our board) + UM12262 board UM | UM12262 covers the **non-S** variant - see `NOTES.md` |
| `1.2-STM32F407-Discovery` | DS8626 MCU datasheet, UM1472 board UM, data brief | RM0090 reference manual still missing |
| `2.1-Hiwonder-Ackermann-Chassis` | Assembly/intro docs, docs index + `SPECS.md` | Docs from docs.hiwonder.com; rear geometry measured in Hiwonder's CAD |
| `2.3-Servo-LD-1501MG` | Chassis/motor/servo spec capture + `SPECS.md` | Servo is **6–8.4 V**, not 5 V |
| `2.4-Encoder-Motor-Module` | `SPECS.md` + 1:1 hole template | Vendor publishes no drawing - geometry **measured off a photo on 5 mm graph paper**, 2026-09-21 |
| `3.1-Battery-3S-LiPo` | `SPECS.md` | Almost everything TBC until it arrives |
| `3.4a-Bauer-50W` | `SPECS.md` | Compute rail |
| `3.4b-Bauer-15W` | `SPECS.md` | MCU rail |
| `3.8-Geloo-Fuse-Block` | `SPECS.md` | Includes why FULARR was rejected |
| `3.9-INA226` | TI SBOS547 datasheet + `SPECS.md` | Verify the module's shunt is 2 mΩ |
| `3.10-LiPo-Alarm` | `SPECS.md` | Set to 3.3–3.5 V/cell |

## Audit - 2026-09-13

Every PDF opened, page-counted, text-extracted and date-checked. Honest grading:

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
- **RM0090** (STM32F4 reference manual) - `st.com` is unreachable from this machine
  (connection refused, not a 404); Mouser and DigiKey serve bot-check pages. Fetch by hand.
- **i.MX 91 SoC datasheet and reference manual** - NXP doc paths did not resolve; the RM is
  usually behind an NXP account. From nxp.com/imx91.
- **CAN transceiver** - no folder; part not chosen (BOM 4.1).
- Fresh **DS8626 Rev 12** and **UM1472 Rev 5** to replace the stale mirror copies.
