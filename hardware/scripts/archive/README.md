# Archive - how the chassis layout started

These are the early scripts for `hardware/renders/chassis-layout.svg`, recovered from the 2026-09-20 session that wrote them.
**They do not make today's drawing:** the SVG was then edited as text for two weeks. Since 2026-10-05 the drawing is written by
[`../chassis-layout.py`](../chassis-layout.py) (see [`../../README.md`](../../README.md)); these only show how it started.

| File | What it does | Status |
|---|---|---|
| [`extract-plate-outline.py`](extract-plate-outline.py) | Reads Hiwonder's CAD export in `mechanical/cad/`, takes plate 1's silhouette (34 points), writes `plate.json` | **Checked 2026-10-05:** with the layout's 1.7 px/mm transform it reproduces the plate outline in today's SVG to 0.05 px; that outline is now the `OUTLINE` table in `chassis-layout.py` |
| [`gen-layout-2026-09-20.py`](gen-layout-2026-09-20.py) | Draws the first three-deck layout from `plate.json` | Runs and writes a valid SVG, but that is the 20 Sept version, not the current one |

**Not recovered.** The hole survey behind MEC-10 (64 holes per plate in three diameters) has no script in any session; its result
is the `HOLES` and `SLOTS` tables in `chassis-layout.py`, read back from the drawing. The system diagram's generator from 17 Sept also
exists in a transcript, but has been edited by hand since and no longer matches `system/renders/`.
