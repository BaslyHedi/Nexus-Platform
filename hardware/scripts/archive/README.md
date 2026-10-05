# Archive - how the chassis layout started

These are the scripts that survive for `hardware/renders/chassis-layout.svg`, recovered from the 2026-09-20 session that wrote
them. **None of them makes today's drawing.** The layout and the wiring schematic are edited as text in place; the SVG is the
source of truth (see [`../../README.md`](../../README.md)).

| File | What it does | Status |
|---|---|---|
| [`extract-plate-outline.py`](extract-plate-outline.py) | Reads Hiwonder's CAD export in `mechanical/cad/`, takes plate 1's silhouette (34 points), writes `plate.json` | **Checked 2026-10-05:** with the layout's 1.7 px/mm transform it reproduces the plate 2 and plate 3 outlines in today's SVG to 0.05 px |
| [`gen-layout-2026-09-20.py`](gen-layout-2026-09-20.py) | Draws the first three-deck layout from `plate.json` | Runs and writes a valid SVG, but that is the 20 Sept version, not the current one |

**Not recovered.** The hole survey behind MEC-10 (64 holes per plate in three diameters) has no script in any session. Its result
is the circles and slots in the SVG, which is what `mechanical/scripts/animate-tray.py` reads. `wiring-schematic.svg` was written
as hand-made SVG on 13-15 Sept and edited in place since; it never had a generator. The system diagram's generator from 17 Sept
also exists in a transcript, but has been edited by hand since and no longer matches `system/renders/`.
