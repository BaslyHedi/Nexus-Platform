# 3.1 - Hiwonder 11.1 V lithium pack

Supplied with the Hiwonder advanced bundle. Label reads *lithium battery · 11.1V · 6000mAh ·
Hiwonder*. Physical facts below are from the pack in hand, photographed 2026-09-21; the
footprint was measured 2026-09-20 and `hardware/renders/chassis-layout.svg` draws it at
that size, **77 mm along the vehicle**.

| Parameter | Value |
|---|---|
| Nominal | 11.1 V (3S) |
| Full charge | 12.6 V (4.2 V/cell) |
| Empty | 9.0 V (3.0 V/cell) - **never go below** |
| Working alarm point | 9.9-10.5 V (3.3-3.5 V/cell) |
| Capacity | **6000 mAh on the label; the geometry says 4300-5000.** Measure it (see below) |
| Construction | **Shrink-wrapped cylindrical cell pack. Not a hard case.** |
| Discharge lead | red/black pair, **SM-2P**, out of one corner |
| Charge lead | **female DC barrel socket** on a 20 AWG pigtail, out of the opposite corner of the same face |
| Lead face | the **63 mm face**, confirmed 2026-09-21 - so with 77 along the vehicle the leads point front or rear |
| Balance connector | **none** - no per-cell visibility is possible (see BOM 3b) |
| Dimensions | **63 × 77 × 20 mm**, confirmed 2026-09-21 · 3 × 21700 in a single row |

## It is a soft pack, and that changes how it is held

The 2026-09-21 photographs show heat-shrink over bare cylindrical cells, with the wrap folded
and creased at the edges. The earlier "hard-cased" note in the BOM was wrong. Consequences, all
of which feed `hardware/renders/chassis-layout.svg`:

- **No cable ties directly on the pack.** A 3 mm tie tensioned on shrink wrap cuts it, and a cut
  wrap on a cell pack is a short circuit waiting for vibration.
- **Straps must be wide and flat**, 20 mm or more, to spread the load.
- **A pad underneath is mandatory, not optional.** The pack sits across the 23.9 × 10.3 strap
  slots and the 22.7 × 35.4 opening, and anodised plate edges will abrade the wrap.
- Nothing rigid should clamp it. A printed cradle has to cradle, not grip.

## Both leads leave the same face

The SM-2P discharge lead and the DC charge socket come out of **one face, at opposite corners**.
That is useful: one face carries all the wiring, so it should point at the WAGO column and the
other three faces stay clean.

They leave at the **two corners**, not out of the middle, which is what saves the layout. The
pack ends at x 132 and the WAGO column starts at x 135, and 3 mm would be hopeless for a lead
going straight back - but a lead leaving a corner turns straight into the **clear channel beside
the pack**: y 0-30 on the vehicle's right, y 93-120 on its left. Nothing has to move.

Which corner gets which is free, because flipping the pack over swaps them. The layout picks:

- **SM-2P on the vehicle's right (y 30 corner)**, because the whole (+) chain lives there:
  main fuse, then the INA226 shunt at x 135-161 y 3-25, then the (+) bus. The (−) crosses to the
  (−) bus, which is the shorter of the two possible crossings.
- **Charge socket on the vehicle's left (y 93 corner)**, parked in the open channel where it can
  be reached from the side of the vehicle **without unstrapping the pack**.

**The charge socket is live and it is loose.** A female barrel on a flying lead inside an
aluminium chassis has to be tied down and insulated, not left to rattle.

## The height is 20 mm, and that identifies the pack

Confirmed 2026-09-21. **63 × 77 × 20 with the leads on a 63 face is three 21700 cells in a
single row**, and every number falls out of that:

| From the cells | Measured |
|---|---|
| 3 × ⌀21.0 side by side = 63.0 | **63** |
| cell length 70 + wrap and the lead exit | **77** |
| cell diameter 21 | **20** |
| terminals are at the cell ends, so the leads leave the 3-cell-wide face | **leads on the 63 face** |

Single-row cylindrical packing is about 79 % of the box, which is exactly what 72.7 cm³ of cell
in a 97 cm³ box gives. The geometry is self-consistent and it was the earlier guess of a taller
pack that was wrong.

### ⚠️ But then the label is optimistic

Three 21700s in series is **3S1P**, so pack capacity is one cell's capacity. Real 21700s are
4000-5000 mAh, and 72.7 cm³ of cell at ~650 Wh/L is **about 47 Wh, or 4.3 Ah at 11.1 V**. The
label says 6000 mAh = 66.6 Wh, which would need half as much cell again as physically fits.

**Take the usable capacity as 4300-5000 mAh, not 6000.** This is not cosmetic: 6000 mAh is the
denominator for coulomb counting on the STM32 (BOM 3b), and using it would make state of charge
read roughly 20-40 % optimistic all the way down the discharge curve. **Measure the real
capacity on the first full discharge through the INA226** and record it here; that number, not
the label, is the one the BMS service uses.

The pack has no built-in over-discharge protection beyond whatever internal PCM the two-wire
charging implies. Protection is layered instead: STM32 sensing (3.9) and graceful shutdown.
See `../../BOM.md`.
