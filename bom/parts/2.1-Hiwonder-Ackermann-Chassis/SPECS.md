# 2.1 - Hiwonder Ackermann chassis · rear geometry

Hiwonder's online docs publish only the plate size (270 × 120.5 × 2 mm, anodised aluminium,
126 g). Everything else below was **measured in Hiwonder's own CAD** -
`../../3D-Drawings/Ackermann Chassis (Single Layer).3dm`, read part by part through its export
`chassis-3deck-fascia.obj` - on 2026-09-17. Photos of the real kit agree within what a tape
measure on a photo can show.

**Frame** (same as `fascia.scad`): x across the vehicle, **y positive towards the rear**, z up.
Deck 1 top z 29.12. **The two gaps differ - measured on the built kit 2026-09-20: lower standoff
50 mm, upper 40 mm** (MEC-09). Deck tops are therefore z 29.12 / 81.12 / 123.12. The CAD is the
single-plate version and only ever had the 50 mm standoff.

| Feature | Value |
|---|---|
| Plate rear flat edge | y **131.54**, x −44.64 … 49.60 (94.24 wide) |
| Rear taper | straight line, 0.6 mm inward per mm rearward (≈31° to the vehicle axis), from (−56.46, 114.69) / (61.42, 114.69) to the corner arcs at y 130.09 |
| Rear standoffs | **hex 6.0 mm A/F** (6.93 across corners), **50 mm**, brass; centres **x −35.61 / +40.57, y 118.46** - 76.18 apart, 13.08 in from the rear edge |
| Standoff hole in plate | ⌀4.3 - suggests **M4**, not M3; unconfirmed |
| Front standoffs | same, y −111.05 |
| Rear cross-slot (every plate) | **5.38 wide**, x −34.22 … 39.19, y 121.94 … 127.32 - back edge 4.22 from the rear edge |
| Existing M3 holes near the rear | ⌀3.2 at (−41.34, 124.54) and (46.30, 124.54); four more at y 107.5 |
| Rear motors | ⌀37, axis along x at y 83.25, z 51.45; body y 64.8 … **101.7**, z 33.0 … 69.9 - i.e. in the **lower gap** |
| Rear wheels | ⌀58.7, x ±67 … ±96, y 53.8 … 112.5 |

**Real kit, confirmed from photos:** standoffs are male–female and thread into each other through
each plate (no screw between decks); screw heads only on top of deck 3 and under deck 1.

**Still to measure on the parts:** standoff A/F with calipers (the fascia ring bore depends on it),
and the standoff thread.
