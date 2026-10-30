#!/usr/bin/env python3
"""The carrier tray to make by hand (MEC-17): a 1:1 cutting and drilling template, and the hole table, for a sheet of 3 or 4 mm plastic (3 mm ABS is the one bought).

    python3 carrier-tray-hand.py [out.svg]        # -> ../renders/carrier-tray-hand-template.svg, A4 landscape, 1 unit = 1 mm

Print it at 100 % (no "fit to page"); the 100 mm bar must measure 100 mm. Tape it to the sheet, centre-punch every cross, drill, then saw
along the heavy outline (an all right-angle outline: twelve straight cuts, no curves).

What the printed tray (carrier-tray.scad) has and this one does not, because they are hard to do by hand and not needed:
  - plate 2's ~45 own holes and slots, copied; three cable windows are kept (the outer 4 mm of each of the plate's two slots, which the Bauer's 12 V
    wires use, stay open because the tray's edges at y 31 and y 89 do not cover them);
  - the hex nut pockets: the four fixing holes are tapped M2.5 (or take a nut glued on top), the Bauer's two M3;
  - the Bauer's rim, the lettering, the splice outlines and the splice wings (S6 and S7 go back on plate 2's top face, beside the tray);
  - the corner pads and the 6 mm counterbores: the 11 board holes are countersunk from below for flat-head M2.5 screws instead.
The tray sits flat on plate 2. At 4 mm every height in MEC-17 is unchanged; at 3 mm the boards stand 11 mm above plate 2.

Positions are plate 2's layout frame (x from the front, y from the vehicle's right), the same numbers as the printed tray; the table gives
them again from the tray's own top left corner, for marking with a ruler. Mark the board holes through the real boards if you can: the
corner inset (2.5 mm) is an estimate (MEC-17).
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "renders", "carrier-tray-hand-template.svg")

# ---- the design (plate 2 layout frame, mm) --------------------------------------------------------------------------------------
OUTLINE = [(9, 31), (83.5, 31), (83.5, 23.2), (115, 23.2), (115, 3.6), (191.5, 3.6),       # twelve straight cuts, all right angles
           (191.5, 113), (115, 113), (115, 97.2), (83.5, 97.2), (83.5, 89), (9, 89)]
BOARDS = {"A": (117.00, 187.00, 5.11, 55.11), "B": (119.54, 189.54, 81.15, 111.15), "C": (85.50, 115.50, 25.20, 95.20)}   # B a 3x7 since 2026-10-26
CORNER_INSET = 2.5                                  # estimated, not measured (MEC-17)
BAUER = (11.0, 75.0, 32.0, 89.0)                    # body 64 x 57; lies on the tray with its leads edge at y 89
HOLE_BOARD, DRILL_M25, DRILL_M3, WINDOW_D = 3.4, 2.1, 2.5, 8.0

HOLES = []                                           # name, x, y, drill diameter, what it is
for name, (x0, x1, y0, y1) in BOARDS.items():
    for k, (x, y) in enumerate([(x0 + CORNER_INSET, y0 + CORNER_INSET), (x1 - CORNER_INSET, y0 + CORNER_INSET),
                                (x0 + CORNER_INSET, y1 - CORNER_INSET), (x1 - CORNER_INSET, y1 - CORNER_INSET)], 1):
        if (name, k) != ("B", 1):                    # B's front inboard corner takes no screw: the CN7 socket ends 2 mm from it (MEC-17)
            HOLES.append((f"{name}{k}", x, y, HOLE_BOARD, f"board {name} standoff screw, countersink from below"))
HOLES += [("T1", 24.82, 60.24, DRILL_M25, "to plate 2, tap M2.5 (under the Bauer)"),
          ("T3", 99.24, 81.76, DRILL_M25, "to plate 2, tap M2.5 (under board C)"),
          ("T4", 120.06, 35.94, DRILL_M25, "to plate 2, tap M2.5 (under board A)"),
          ("T5", 148.18, 81.76, DRILL_M25, "to plate 2, tap M2.5 (under board B)"),
          ("E1", 16.0, 63.0, DRILL_M3, "Bauer, tap M3"),
          ("E2", 70.0, 63.0, DRILL_M3, "Bauer, tap M3"),
          ("W1", 114.5, 60.0, WINDOW_D, "cable window beside C (6 V pair)"),
          ("W2", 127.0, 48.0, WINDOW_D, "cable window under board A (6 V pair, I2C lead)"),
          ("W3", 127.0, 73.0, WINDOW_D, "cable window beside board B")]

X0, Y0 = min(p[0] for p in OUTLINE), min(p[1] for p in OUTLINE)          # the tray's top left corner on plate 2
W = max(p[0] for p in OUTLINE) - X0
H = max(p[1] for p in OUTLINE) - Y0

# ---- checks ----------------------------------------------------------------------------------------------------------------
def inside(px, py, poly):
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
            c = not c
    return c


def edge_distance(px, py, poly):
    best = 1e9
    for i in range(len(poly)):
        (ax, ay), (bx, by) = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(px - ax - t * dx, py - ay - t * dy))
    return best


problems = []
for n, x, y, d, _ in HOLES:
    if not inside(x, y, OUTLINE) or edge_distance(x, y, OUTLINE) < d / 2 + 2.0:
        problems.append(f"{n} is too close to the edge ({edge_distance(x, y, OUTLINE):.1f} mm from it)")
for i, a in enumerate(HOLES):
    for b in HOLES[i + 1:]:
        gap = math.hypot(a[1] - b[1], a[2] - b[2]) - (a[3] + b[3]) / 2
        if gap < 2.0:
            problems.append(f"{a[0]} and {b[0]} leave only {gap:.1f} mm between them")
if problems:
    sys.exit("template not written:\n  " + "\n  ".join(problems))

# ---- the page --------------------------------------------------------------------------------------------------------------------
PAGE_W, PAGE_H = 297, 210
OX, OY = (PAGE_W - W) / 2, 24            # where the tray's top left corner goes on the page
o = []
w = o.append
w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" viewBox="0 0 {PAGE_W} {PAGE_H}" font-family="system-ui, Segoe UI, Roboto, sans-serif">')
w(f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="#ffffff"/>')
w(f'<text x="10" y="11" font-size="5" font-weight="700">NEXUS carrier tray - hand-made - 1:1 template (MEC-17)</text>')
w(f'<text x="10" y="17" font-size="2.7" fill="#444">3 or 4 mm sheet, at least {math.ceil(W) + 6} x {math.ceil(H) + 6} mm. Top view, front of the vehicle to the LEFT, vehicle right at the TOP. Print at 100 %, no fit-to-page: the bar below must measure 100 mm.</text>')
w(f'<text x="10" y="21.5" font-size="2.7" fill="#444">Centre-punch every cross, drill, then saw along the heavy line (12 straight cuts), file the edges, tap or countersink as the table says.</text>')


def px(x):
    return f"{OX + x - X0:.2f}"


def py(y):
    return f"{OY + y - Y0:.2f}"


# boards and the Bauer, for placement (dashed), under the cut line
for name, (x0, x1, y0, y1) in BOARDS.items():
    w(f'<rect x="{px(x0)}" y="{py(y0)}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="none" stroke="#047857" stroke-width="0.25" stroke-dasharray="1.6 1"/>')
    w(f'<text x="{px(x0 + 7)}" y="{py((y0 + y1) / 2)}" font-size="3.2" fill="#047857" font-weight="700">board {name}</text>')
bx0, bx1, by0, by1 = BAUER
w(f'<rect x="{px(bx0)}" y="{py(by0)}" width="{bx1 - bx0:.2f}" height="{by1 - by0:.2f}" fill="none" stroke="#be123c" stroke-width="0.25" stroke-dasharray="1.6 1"/>')
w(f'<text x="{px((bx0 + bx1) / 2)}" y="{py((by0 + by1) / 2 - 10)}" font-size="3.2" fill="#be123c" text-anchor="middle" font-weight="700">Bauer 50 W (64 x 57)</text>')
w(f'<text x="{px((bx0 + bx1) / 2)}" y="{py(by1 - 2)}" font-size="2.2" fill="#be123c" text-anchor="middle">leads edge</text>')
# the outline: the cut line
d = " ".join(("M" if i == 0 else "L") + f"{px(x)} {py(y)}" for i, (x, y) in enumerate(OUTLINE)) + " Z"
w(f'<path d="{d}" fill="#f4f4f4" fill-opacity="0.0" stroke="#000" stroke-width="0.6"/>')
# holes: true size circle, a cross, the name
for n, x, y, dia, what in HOLES:
    w(f'<circle cx="{px(x)}" cy="{py(y)}" r="{dia / 2:.2f}" fill="none" stroke="#1d4ed8" stroke-width="0.2"/>')
    w(f'<path d="M{OX + x - X0 - 3:.2f} {py(y)} h6 M{px(x)} {OY + y - Y0 - 3:.2f} v6" stroke="#1d4ed8" stroke-width="0.2"/>')
    w(f'<text x="{OX + x - X0 + 2.4:.2f}" y="{OY + y - Y0 - 2.2:.2f}" font-size="2.6" fill="#1d4ed8" font-weight="700">{n}</text>')
# the 100 mm bar and the page frame marks
w(f'<path d="M10 {PAGE_H - 8} h100 M10 {PAGE_H - 10} v4 M60 {PAGE_H - 9} v2 M110 {PAGE_H - 10} v4" stroke="#000" stroke-width="0.4"/>')
w(f'<text x="112" y="{PAGE_H - 6.5}" font-size="3">100 mm</text>')
w(f'<text x="{PAGE_W - 10}" y="{PAGE_H - 6.5}" font-size="2.4" fill="#666" text-anchor="end">dimensions in the tables are from the tray\'s top left corner, x to the rear, y toward the vehicle\'s left</text>')

# the tables
ty = OY + H + 8
w(f'<text x="10" y="{ty}" font-size="3.2" font-weight="700">Holes (centre from the top left corner of the tray)</text>')
rows = [f"{n:<3} x {x - X0:6.2f}  y {y - Y0:6.2f}   drill {dia:>3.1f}   {what}" for n, x, y, dia, what in HOLES]
half = (len(rows) + 1) // 2
for col in range(2):
    for i, r in enumerate(rows[col * half:(col + 1) * half]):
        w(f'<text x="{10 + col * 145}" y="{ty + 5 + i * 3.3:.1f}" font-size="2.5" font-family="ui-monospace, Menlo, Consolas, monospace" xml:space="preserve">{r}</text>')
ty2 = ty + 5 + half * 3.3 + 2
w(f'<text x="10" y="{ty2}" font-size="3.2" font-weight="700">Outline corners, in the same measure (saw straight between them)</text>')
corner_txt = "   ".join(f"({x - X0:.1f}, {y - Y0:.1f})" for x, y in OUTLINE)
w(f'<text x="10" y="{ty2 + 4.5}" font-size="2.5" font-family="ui-monospace, Menlo, Consolas, monospace" xml:space="preserve">{corner_txt}</text>')
w(f'<text x="10" y="{ty2 + 12.5}" font-size="2.5" fill="#b45309">Better for the board holes: set the real boards, with their standoffs fitted, on the sheet in their dashed outlines and mark through the standoffs - the 2.5 mm corner inset here is an estimate.</text>')
w(f'<text x="10" y="{ty2 + 8.5}" font-size="2.5" fill="#444">Tray {W:.1f} x {H:.1f} mm. Tap M2.5 / M3 into the sheet (or open to 2.8 / 3.2 and glue a nut on top). Board holes: 3.4 mm, countersunk 90 degrees from below for flat-head M2.5 x 8.</text>')
w('</svg>')
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")
print(f"tray {W:.1f} x {H:.1f} mm, {len(HOLES)} holes, wrote {os.path.relpath(OUT)}")
print("\n".join(rows))
