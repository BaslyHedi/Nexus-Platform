#!/usr/bin/env python3
"""The chassis deck layout drawing: three identical plates, the harness board seen from below, the deck stack (MEC-09, MEC-10, MEC-16).

    python3 chassis-layout.py            # -> ../renders/chassis-layout.svg
    python3 ../../tools/check-drawings.py   # fails if the SVG is not what this script writes

The plate (outline, 32 slots, 64 holes, 4 standoffs, 2 clamp holes) is data in millimetres, surveyed from Hiwonder's CAD, and is drawn
once per plan, so a hole added to the tables appears on all four. Parts are drawn in the plan they sit in (positions in mm, from
MEC-11, MEC-15, MEC-16 and mechanical/scripts/plate1.py); annotations and the tables at the right are in pixels. Edit this script,
never the SVG.

Plans are 1.7 px/mm with the front of the vehicle to the LEFT and the vehicle's left at the BOTTOM; the harness board is seen from
below, so its y runs the other way (a flipped plan).
"""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawing import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders', 'chassis-layout.svg')

# the outline's look: plates 3 and 2 are drawn pale and dashed (the decks above the one being read), plate 1 and the harness board solid
PALE = dict(fill='#f8fafc', stroke='#94a3b8', stroke_width=1.8, stroke_dasharray='7 4')
SOLID = dict(fill='#ffffff', stroke='#334155', stroke_width=1.8)

# plans: pixel row of the plate's right edge (y = 0). The harness board is seen from below, so its y is flipped.
P3 = plan('plate 3', 132.0)
P2 = plan('plate 2, top face', 390.0)
P1 = plan('plate 1', 971.0)
PB = plan('plate 2, lower face', 871.15, flip=True)

OUTLINE = [   # the plate, mm: x from the front, y from the vehicle's right (traced from Hiwonder's CAD)
    (0, 33.35), (0.53, 32), (1.53, 31.06), (40, 8.29), (47, 0.99),
    (48, 0.41), (50, 0), (52, 0.41), (53.53, 1.48), (68.53, 17.42),
    (70, 18.05), (87.53, 17.95), (113, 2.83), (114.53, 2.47), (251.53, 0.89),
    (253.53, 1.58), (268.53, 10.59), (269.53, 11.65), (269.53, 108.88), (268.53, 109.94),
    (252.53, 119.47), (114, 118), (112.53, 117.42), (87.53, 102.58), (70, 102.48),
    (68.53, 103.12), (53, 119.53), (51, 120.42), (49, 120.42), (46.53, 119.05),
    (40, 112.23), (1.53, 89.47), (0.53, 88.53), (0, 87.18),
]

SLOTS = [   # chassis slots: x, y (edge nearest the vehicle's right), width, height; rounded ends
    (161.18, 30.42, 14.6, 59.76), (110.29, 42.53, 22.7, 35.35), (260.29, 23.55, 5.36, 73.4),
    (219.47, 26.12, 4.3, 68.3), (235.47, 26.12, 4.3, 68.3), (203.47, 26.12, 4.3, 68.3),
    (187.47, 26.12, 4.3, 68.3), (109.35, 9.88, 48.3, 5.3), (109.35, 105.34, 48.3, 5.3),
    (56.18, 26.94, 23.9, 10.3), (56.18, 83.17, 23.9, 10.3), (3, 38.62, 3.2, 43.2),
    (41.35, 55.76, 9, 9), (13.35, 55.76, 9, 9), (41.35, 34.17, 4.3, 4.3),
    (41.35, 82.06, 4.3, 4.3), (43.71, 42.11, 4.3, 4.3), (43.71, 74.12, 4.3, 4.3),
    (232.76, 11.69, 4.3, 4.3), (232.76, 104.52, 4.3, 4.3), (205.88, 104.52, 4.3, 4.3),
    (10.53, 34.17, 4.3, 4.3), (254.71, 20, 4.3, 4.3), (205.88, 11.69, 4.3, 4.3),
    (10.53, 82.06, 4.3, 4.3), (254.71, 96.18, 4.3, 4.3), (90.47, 34.17, 4.3, 4.3),
    (25.18, 20, 4.3, 4.3), (90.47, 82.06, 4.3, 4.3), (25.18, 96.18, 4.3, 4.3),
    (34, 33.83, 4.2, 4.2), (34, 82.47, 4.2, 4.2),
]

HOLES = [   # round holes: x, y, diameter. 3.18 takes M3, 2.71 takes M2.5, 2.47 is the tight M2.5 / M2 class (MEC-10)
    (186.12, 9.71, 3.18), (186.12, 110.82, 3.18), (245.88, 96.77, 3.18), (245.88, 81.77, 3.18), (196.88, 38.76, 3.18),
    (196.88, 81.77, 3.18), (196.88, 96.77, 3.18), (245.88, 38.76, 3.18), (262.94, 16.41, 3.18), (196.88, 23.76, 3.18),
    (245.88, 23.76, 3.18), (262.94, 104.05, 3.18), (99.24, 38.76, 3.18), (148.18, 23.76, 3.18), (45.82, 67.24, 3.18),
    (10.82, 60.23, 3.18), (99.24, 23.76, 3.18), (52.82, 60.23, 3.18), (148.18, 81.77, 3.18), (45.82, 53.24, 3.18),
    (38.82, 60.23, 3.18), (148.18, 38.76, 3.18), (24.82, 60.23, 3.18), (99.24, 81.77, 3.18), (148.18, 96.77, 3.18),
    (17.82, 53.24, 3.18), (99.24, 96.77, 3.18), (17.82, 67.24, 3.18), (50, 115.52, 3.18), (104.41, 19.59, 3.18),
    (104.41, 100.95, 3.18), (50, 5, 3.18), (227.88, 14.23, 2.71), (169.88, 100.23, 2.71), (227.88, 100.23, 2.71),
    (169.88, 14.23, 2.71), (86.94, 80.23, 2.71), (86.94, 40.23, 2.71), (120.06, 35.94, 2.71), (96.71, 52.65, 2.71),
    (96.71, 67.88, 2.71), (143.47, 67.88, 2.71), (143.47, 52.65, 2.71), (120.06, 84.53, 2.71), (16.94, 32.24, 2.71),
    (16.94, 88.24, 2.71), (49, 84.53, 2.71), (25.65, 67.88, 2.71), (169.88, 106.24, 2.71), (25.65, 52.65, 2.71),
    (72.41, 52.65, 2.71), (169.88, 20.23, 2.71), (227.88, 106.24, 2.71), (49, 35.94, 2.71), (72.41, 67.88, 2.71),
    (227.88, 20.23, 2.71), (102.18, 72.24, 2.71), (148.18, 72.24, 2.71), (148.18, 48.24, 2.71), (102.18, 48.24, 2.71),
    (251.29, 112.35, 2.47), (251.29, 8.17, 2.47), (162.06, 16.7, 2.47), (162.06, 103.83, 2.47),
]

STANDOFFS = [(256.82, 22.17), (256.82, 98.36), (27.35, 22.17), (27.35, 98.36)]   # the four chassis standoffs, 6.0 mm across the flats
CLAMPS = [(262.94, 16.41), (262.94, 104.05)]                 # fascia clamp holes, M3, on every deck (MEC-07)

RUNS = [   # plate 1 wiring, on plate 2's harness board (MEC-16, HW-20): #, run, wire, cut length in cm, ends and clips.
           # Cut lengths come from mechanical/scripts/plate1.py (modelled length x 1.2 + 22 mm strip)
    ('1', 'Battery + → main fuse', 'SM-2P + · fuse lead', '5 · 3', 'SM-2P is the battery disconnect · S1'),
    ('2', 'Main fuse → INA226 IN+', 'fuse lead 16 AWG', '~12', 'ferrule into the screw terminal'),
    ('3', 'INA226 IN− → (+) bus', '18 red', '9', 'ferrule · WAGO'),
    ('4', 'Battery − → (−) bus', 'SM-2P mate −', '12', 'across the opening · WAGO'),
    ('5', '(+) bus → SW1 C', '18 red', '27', 'trunk over the motors · 4.8 mm receptacle'),
    ('6', '(+) bus → SW2 C', '18 red', '27', 'trunk over the motors · 4.8 mm receptacle'),
    ('7', 'SW1 NO → split', '18 red', '12', 'receptacle · 3-port'),
    ('8', 'split → F-MOT → S2 · VM+ pigtail', 'fuse lead · 18 red', '5 · 4 · 8 ↓', '3-port · S2 · driver VM plug, from the side'),
    ('9', 'split → F-UBEC → S3 · UBEC +', 'fuse lead 16 AWG', '5 · 4', "3-port · S3 · UBEC's own lead"),
    ('10', 'UBEC 6 V → board A 6V IN', '18 red + black', '21', 'up through the opening · A terminal'),
    ('11', 'UBEC − → S5 → (−) bus', '18 black', '11', "UBEC's own lead · S5 · WAGO"),
    ('12', 'VM− pigtail → S4 → (−) bus', '18 black', '8 ↓ · 9', 'driver VM plug · S4 · WAGO'),
    ('13', 'LED − SW1 ↔ SW2, then → (−)', '18 black', '8 + 23', 'receptacles · trunk · WAGO'),
    ('14', 'LED + ↔ NO, on each switch', '18 red', '2 × 4', 'receptacles, at the switch'),
    ('15', 'SW2 NO → S6 → Bauer +', '18 red', '32', 'receptacle · up the left slot beside the Bauer · S6 on the tray'),
    ('16', 'Bauer − → S7 → (−) bus', '18 black', '22', 'S7 on the tray, right of the Bauer · up the right slot · WAGO'),
]


def slot(view, x, y0, w, h):
    """A chassis slot with round ends; y0 is the edge nearest the vehicle's right, so a flipped plan draws it from y0 + h."""
    return rect(view, x, y0 + h if view.flip else y0, w, h, rx=f'{min(w, h) * SCALE / 2:.1f}', fill='#eef2f6', stroke='#b8c2cc', stroke_width=0.6)


def hole(view, x, y, d):
    """A round hole of diameter d mm (the radius in px is d * scale / 2)."""
    return circle(view, x, y, f'{d * SCALE / 2:.1f}', fill='#eef2f6', stroke='#b8c2cc', stroke_width=0.6)


def plate(view, **style):
    """One plate, outline first: the same slots, holes, standoffs and clamp holes on every deck. `style` is the outline's look."""
    o = [outline(view, OUTLINE, **style)]
    o += [slot(view, *s) for s in SLOTS]
    o += [hole(view, *h) for h in HOLES]
    o += [circle(view, x, y, 3.4, fill='#fde68a', stroke='#a16207', stroke_width=1.2) for x, y in STANDOFFS]
    o += [circle(view, x, y, 4, fill='none', stroke='#7c3aed', stroke_width=1.5) + circle(view, x, y, 1.5, fill='#7c3aed') for x, y in CLAMPS]
    return o


def header():
    """Page, marker definitions, title and the two lines under it."""
    o = []
    w = o.append
    w('<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="1272" viewBox="0 0 1320 1272" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">')
    w('<defs><marker id="d" markerWidth="8" markerHeight="8" refX="1" refY="3" orient="auto"><path d="M6,0 L0,3 L6,6 z" fill="#64748b"/></marker><marker id="e" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#64748b"/></marker></defs>')
    w(el('rect', width=1320, height=1272, fill='#fbfaf8'))
    w(text(PX, 40, 32, 'NEXUS - chassis deck layout', font_size=18, font_weight=700, fill='#1a1a1a'))
    w(text(PX, 40, 52, 'Hiwonder Ackermann advanced kit · three identical plates, outline traced from Hiwonder\'s own CAD · 1.7 px/mm · front of vehicle to the LEFT · <tspan font-weight="700">viewed from above, so the vehicle\'s own LEFT is at the BOTTOM of each plan</tspan>', font_size=11, fill='#666'))
    w(text(PX, 40, 68, 'Deck gaps measured on the built kit 2026-09-20: <tspan font-weight="700">lower 50 mm, upper 40 mm</tspan> - two standoff lengths, not one. Fascia panels are 52 and 42 mm tall.', font_size=11, fill='#166534'))
    return o


def plate3_heading():
    """Upper deck title."""
    o = []
    w = o.append
    w(text(PX, 60, 110, 'UPPER DECK - plate 3', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(text(PX, 60, 124, 'top face z 123.12 · compute tray: FRDM-IMX91S, Pi 5 later', font_size=9.5, fill='#64748b'))
    return o


def plate2_heading():
    """Middle deck, top face, title."""
    o = []
    w = o.append
    w(text(PX, 60, 368, 'MIDDLE DECK - plate 2, TOP FACE', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(text(PX, 60, 382, 'top face z 81.12 · STM32 carrier (boards A, B), 5 V split (board C) and the 5 V converter', font_size=9.5, fill='#64748b'))
    return o


def plate1_heading():
    """Lower deck title."""
    o = []
    w = o.append
    w(text(PX, 60, 949.0, 'LOWER DECK - plate 1', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(text(PX, 60, 963.0, 'top face z 29.12 · floor only - <tspan fill="#be185d" font-weight="700">the harness is taped under plate 2</tspan> (MEC-16)', font_size=9.5, fill='#64748b'))
    return o


def frdm():
    """The compute tray's boards on plate 3, and the fascia clamp note (MEC-18)."""
    o = []
    w = o.append
    # FRDM-IMX91S: about 95 x 65, turned across the vehicle at x 184-249, y 6.75-101.75 (40-pin header to the right, USB to the left, CAN / microSD to the rear)
    w(rect(P3, 184.0, 6.75, 65, 95, rx=2, fill='#eef2ff', fill_opacity=0.92, stroke='#4338ca', stroke_width=1.8))
    for u in (3.5, 52.5):
        for v in (3.5, 61.5):
            w(circle(P3, 184 + 65 - v, 6.75 + u, 3.6, fill='none', stroke='#4338ca', stroke_width=1.4))
    w(text(P3, 216.5, 52.0, 'FRDM-IMX91S  ~95 × 65', font_size=9.5, font_weight=700, fill='#4338ca', text_anchor='middle'))
    w(text(P3, 216.5, 61.0, '6 mm standoffs', font_size=7.2, fill='#4338ca', text_anchor='middle'))
    # Raspberry Pi 5 (later phase): across the vehicle at x 94-150, ports to the left
    w(rect(P3, 94.0, 17.75, 56, 85, rx=3, fill='#ecfdf5', fill_opacity=0.92, stroke='#047857', stroke_width=1.6, stroke_dasharray='6 3'))
    for a in (3.5, 61.5):
        for b in (3.5, 52.5):
            w(circle(P3, 94 + 56 - b, 17.75 + a, 3.2, fill='none', stroke='#047857', stroke_width=1.4))
    w(text(P3, 122.0, 56.0, 'Pi 5 (later)', font_size=9.5, font_weight=700, fill='#047857', text_anchor='middle'))
    w(text(P3, 122.0, 65.0, '8 or 10 mm standoffs', font_size=7.2, fill='#047857', text_anchor='middle'))
    w(text(P3, 56.0, 62.0, 'spare pad (drill)', font_size=9.5, font_weight=700, fill='#64748b', text_anchor='middle'))
    w(text(PX, 300, 346, 'compute tray (MEC-18): one 236.6 × 108 × 4 mm plate, x 14-250: spare pad · Pi 5 · plug gap · FRDM', font_size=7.8, fill='#64748b', text_anchor='middle'))
    # the fascia upper panel clamps here (MEC-07)
    w(text(PX, 300, 358, 'fascia upper panel clamps at the two purple holes - 2 × M3×8 driven down from the top (MEC-07)', font_size=8.0, fill='#7c3aed', text_anchor='middle'))
    return o


TRAY = [   # the carrier tray's outline on plate 2, mm (mechanical/cad/carrier-tray.scad, PART="outline"; MEC-17)
    (185.1, 3.05), (186.26, 3.36), (186.8, 3.63), (187.3, 3.96), (188.15, 4.81),
    (188.75, 5.85), (189.1, 7.61), (188.94, 8.8), (188.48, 9.91), (187.75, 10.86),
    (187, 11.46), (187, 48.76), (187.75, 49.36), (188.48, 50.31), (188.94, 51.42),
    (189.1, 52.61), (188.94, 53.8), (188.48, 54.91), (187.75, 55.86), (187, 56.46),
    (187, 58.89), (187.64, 58.93), (188.8, 59.24), (189.84, 59.84), (190.29, 60.24),
    (190.69, 60.69), (191.29, 61.73), (191.64, 63.49), (191.48, 64.68), (191.02, 65.79),
    (190.29, 66.74), (189.54, 67.34), (189.54, 104.64), (190.29, 105.24), (191.02, 106.19),
    (191.48, 107.3), (191.64, 108.49), (191.29, 110.25), (190.69, 111.29), (189.84, 112.14),
    (188.8, 112.74), (187.04, 113.09), (185.85, 112.93), (185.28, 112.74), (184.24, 112.14),
    (183.19, 110.99), (125.89, 110.99), (124.84, 112.14), (123.8, 112.74), (122.04, 113.09),
    (120.85, 112.93), (120.28, 112.74), (119.24, 112.14), (118.39, 111.29), (117.79, 110.25),
    (117.48, 109.09), (117.48, 107.89), (117.79, 106.73), (118.39, 105.69), (119.54, 104.64),
    (119.54, 94.16), (119.25, 94.76), (118, 95.2), (116.85, 95.2), (115.8, 96.35),
    (114.76, 96.95), (113, 97.3), (111.81, 97.14), (110.7, 96.68), (109.75, 95.95),
    (109.15, 95.2), (91.85, 95.2), (91.25, 95.95), (90.3, 96.68), (89.19, 97.14),
    (88, 97.3), (86.81, 97.14), (85.7, 96.68), (84.75, 95.95), (84.15, 95.2),
    (80, 95.2), (80, 100.5), (70, 100.5), (64, 106), (60.6, 110),
    (39.5, 110), (34, 107), (24, 100.9), (24, 94.75), (9.5, 91.5),
    (8.5, 90.5), (8.5, 30), (9.5, 29), (24, 25.66), (24, 19.6),
    (34, 13.5), (39.5, 10.5), (60.6, 10.5), (64, 14.5), (70, 20),
    (80, 20), (80, 25.2), (84.15, 25.2), (84.75, 24.45), (85.7, 23.72),
    (86.81, 23.26), (88, 23.1), (89.19, 23.26), (90.3, 23.72), (91.25, 24.45),
    (91.85, 25.2), (109.15, 25.2), (109.75, 24.45), (110.7, 23.72), (111.81, 23.26),
    (113, 23.1), (114.19, 23.26), (115.3, 23.72), (116.25, 24.45), (116.85, 25.2),
    (117, 25.2), (117, 11.46), (116.25, 10.86), (115.52, 9.91), (115.06, 8.8),
    (114.9, 7.61), (115.25, 5.85), (115.85, 4.81), (116.7, 3.96), (117.74, 3.36),
    (118.31, 3.17), (119.5, 3.01), (121.26, 3.36), (122.3, 3.96), (123.35, 5.11),
    (180.65, 5.11), (181.7, 3.96), (182.74, 3.36), (183.9, 3.05),
]

# the tray's six fixings to plate 2 (MEC-17): screw from below into a nut held in the tray; the heads are under plate 2
FIXINGS = [('T1', 24.82, 60.24), ('T2', 52.82, 60.24), ('T3', 99.24, 81.76), ('T4', 120.06, 35.94), ('T5', 148.18, 81.76), ('T6', 148.18, 96.76)]

# the S6 / S7 splices (Bauer 12 V + and -) in a lane either side of the Bauer, 18.6 x 13 mm
SPLICES = [('S6', 42.0, 96.0), ('S7', 42.0, 11.5)]

# the Bauer 50 W (BOM 3.4a, seller's drawing): body 64 x 57, corners cut 8 x 6.5; its two mounting holes are 5 mm in from each end and
# 26 mm from the edge the four leads leave by (here y 89, the vehicle's left), 54 mm apart
BAUER = (11.0, 28.5, 64.0, 64.5)      # x, y, along x, across: the side walls stand outside the 57 mm base (photo, 2026-10-06; MEC-17)
BAUER_LEADS = [(38.0, '#eab308'), (42.0, '#111827'), (46.0, '#111827'), (50.0, '#dc2626')]   # x on the leads edge: OUT+, OUT-, IN-, IN+
BAUER_HOLES = [(16.0, 63.0), (70.0, 63.0)]


def bauer_outline(x0, y0, w, h, cx=8.0, cy=6.5):
    return [(x0 + cx, y0), (x0 + w - cx, y0), (x0 + w, y0 + cy), (x0 + w, y0 + h - cy), (x0 + w - cx, y0 + h), (x0 + cx, y0 + h),
            (x0, y0 + h - cy), (x0, y0 + cy)]


def screw_mark(view, x, y, label, colour='#4338ca'):
    """An M2.5 screw into a chassis hole (the legend's cross), with its name."""
    return (circle(view, x, y, 4.2, fill='none', stroke=colour, stroke_width=1.8) + line(view, x - 3.82, y, x + 3.82, y, stroke=colour, stroke_width=1.3)
            + line(view, x, y - 3.82, x, y + 3.82, stroke=colour, stroke_width=1.3) + text(view, x + 3.4, y - 2.6, label, font_size=7, fill=colour, font_weight=700, text_anchor='start'))


def carrier_and_bauer():
    """Plate 2 top face: the carrier tray with boards A, B, C, the Bauer 50 W and the two splices (MEC-15, MEC-17)."""
    o = []
    w = o.append
    w(comment('Carrier tray (MEC-17): boards A and B (P1, P2 sides), the Discovery above, board C = 5 V split, the Bauer and S6 / S7 all sit on it'))
    w(outline(P2, TRAY, fill='#0f766e', fill_opacity=0.09, stroke='#0f766e', stroke_width=1.3, stroke_dasharray='6 3'))
    w(rect(P2, 117, 5.12, 70, 50, rx=3, fill='#ecfdf5', fill_opacity=0.92, stroke='#047857', stroke_width=1.6))
    w(rect(P2, 119.53, 61, 70, 50, rx=3, fill='#ecfdf5', fill_opacity=0.92, stroke='#047857', stroke_width=1.6))
    w(rect(P2, 124.06, 27.59, 60.94, 5.06, rx=1.5, fill='#99f6e4', stroke='#0f766e', stroke_width=0.8))
    w(rect(P2, 124.06, 78.35, 60.94, 5.06, rx=1.5, fill='#fed7aa', stroke='#b45309', stroke_width=0.8))
    w(rect(P2, 120.53, 22.53, 97, 66, rx=3, fill='#eef2ff', fill_opacity=0.55, stroke='#4338ca', stroke_width=1.3, stroke_dasharray='5 3'))
    w(rect(P2, 85.53, 25.18, 30, 70, rx=3, fill='#ecfdf5', fill_opacity=0.92, stroke='#047857', stroke_width=1.6))
    w(text(P2, 120.53, 12, 'A · 5×7 · P1 side', font_size=7.5, fill='#047857', font_weight=700, text_anchor='start'))
    w(text(P2, 120.53, 106, 'B · 5×7 · P2 side', font_size=7.5, fill='#047857', font_weight=700, text_anchor='start'))
    w(text(P2, 166.53, 52, 'STM32F4DISCOVERY 66 × 97', font_size=8.2, fill='#4338ca', text_anchor='middle'))
    w(text(P2, 166.53, 59.47, 'CN1 at the rear, x 217.5', font_size=7, fill='#4338ca', text_anchor='middle'))
    w(text(P2, 100.47, 58, 'C', font_size=9, fill='#047857', font_weight=700, text_anchor='middle'))
    w(text(P2, 100.47, 64, '5 V split', font_size=6.5, fill='#047857', text_anchor='middle'))
    w(text(PX, 342.2, 603.4, 'carrier 100.6 × 106: A·X.. at x 181.20, B and header row 1 at x 183.74 (as built) · 8 mm standoffs on the 4 mm tray, T1-T6 below (MEC-17)', font_size=7.8, fill='#047857', text_anchor='middle'))
    for name, x, y in FIXINGS:
        w(screw_mark(P2, x, y, name))
    # the Bauer on the tray, with its leads edge on the vehicle's left
    w(outline(P2, bauer_outline(*BAUER), fill='#fff1f2', stroke='#be123c', stroke_width=1.4))
    w(text(P2, 43, 47.06, 'BAUER 50 W', font_size=9, font_weight=700, fill='#be123c', text_anchor='middle'))
    w(text(P2, 43, 52.94, '64 x 64.5 x 22', font_size=7, fill='#be123c', text_anchor='middle'))
    w(text(P2, 43, 72, 'M3 through its own 2 holes', font_size=7, fill='#be123c', text_anchor='middle'))
    for x, y in BAUER_HOLES:
        w(circle(P2, x, y, 5.8, fill='none', stroke='#be123c', stroke_width=1.6) + circle(P2, x, y, 1.6, fill='#be123c'))
    for x, colour in BAUER_LEADS:
        w(line(P2, x, 93, x, 97, stroke=colour, stroke_width=2))
    w(text(P2, 43, 89, 'leads wall ▼', font_size=6, fill='#be123c', text_anchor='middle'))
    w(text(P2, 104, 12, 'carrier tray', font_size=7, font_weight=700, fill='#0f766e', text_anchor='middle'))
    for name, x, y in SPLICES:
        w(rect(P2, x, y, 18.6, 13, rx=1.5, fill='#fed7aa', stroke='#c2410c', stroke_width=1.2) + text(P2, x + 9.3, y + 8.2, name, font_size=7, font_weight=700, fill='#c2410c', text_anchor='middle'))
    # the note column at the right
    w(text(P2, 243, 38, 'one M3×12 here', font_size=7, fill='#7c3aed', text_anchor='middle'))
    w(text(P2, 243, 43.47, 'clamps BOTH', font_size=7, fill='#7c3aed', text_anchor='middle'))
    w(text(P2, 243, 49, 'fascia panels', font_size=7, fill='#7c3aed', text_anchor='middle'))
    w(text(P2, 243, 54.47, '(MEC-07)', font_size=7, fill='#7c3aed', text_anchor='middle'))
    w(text(P2, 243, 68, 'gap ABOVE: the', font_size=7, fill='#b45309', text_anchor='middle'))
    w(text(P2, 243, 73.53, '3 debug ports', font_size=7, fill='#b45309', text_anchor='middle'))
    w(text(P2, 243, 79, 'gap BELOW: the', font_size=7, fill='#b45309', text_anchor='middle'))
    w(text(P2, 243, 84.47, 'switch bodies', font_size=7, fill='#b45309', text_anchor='middle'))
    return o


def tray_heads():
    """The tray's six screw heads under plate 2, seen from below (they sit among the taped parts, MEC-17)."""
    o = []
    for name, x, y in FIXINGS:
        o.append(circle(PB, x, y, 3.9, fill='#ffffff', stroke='#4338ca', stroke_width=1.6) + circle(PB, x, y, 1.4, fill='#4338ca')
                 + text(PB, x + 3.4, y + 2.4, name, font_size=6, font_weight=700, fill='#4338ca', text_anchor='start'))
    return o


def plate1_parts():
    """Plate 1: servo, linkage, battery, motors, driver, switches."""
    o = []
    w = o.append
    # steering servo and the axle (front)
    w(rect(P1, 19.29, 40.29, 28.82, 40, rx=3, fill='#fff7ed', stroke='#c2410c', stroke_width=1.4))
    w(text(P1, 33.71, 58.53, 'SERVO', font_size=8.5, font_weight=700, fill='#c2410c', text_anchor='middle'))
    w(text(P1, 33.71, 65.59, 'LD-1501MG', font_size=7.5, fill='#c2410c', text_anchor='middle'))
    w(comment("Steering linkage behind the servo, from Hiwonder's CAD - the pack cannot sit forward of it (MEC-16)"))
    w(rect(P1, 46.88, 33.12, 21.29, 54.41, fill='#e2e8f0', stroke='#64748b', stroke_width=1, stroke_dasharray='3 2', rx=1.5))
    w(rect(P1, 76.82, 36, 4, 48.59, fill='#cbd5e1', stroke='#475569', stroke_width=1))
    w(rect(P1, 72.12, 6.29, 13.41, 29.71, fill='#e2e8f0', stroke='#64748b', stroke_width=1, rx=1.5))
    w(rect(P1, 72.12, 84.59, 13.41, 29.71, fill='#e2e8f0', stroke='#64748b', stroke_width=1, rx=1.5))
    w(text(P1, 78.82, 33.53, 'tie rod 15-19 high', font_size=5.4, font_weight=700, fill='#475569', text_anchor='middle', transform='rotate(-90 194.0 1028.0)'))
    w(comment('Battery as fixed on the vehicle 2026-09-28: lengthwise behind the tie rod, felt pad, two felt straps + zip ties. Leads leave the FRONT face'))
    w(rect(P1, 85, 30, 77, 63, rx=2.5, fill='#fef2f2', stroke='#b91c1c', stroke_width=1.4))
    w(rect(P1, 92, 28, 20, 67, fill='#f8fafc', fill_opacity=0.8, stroke='#94a3b8', stroke_width=0.8))
    w(rect(P1, 136, 28, 20, 67, fill='#f8fafc', fill_opacity=0.8, stroke='#94a3b8', stroke_width=0.8))
    w(text(P1, 124, 58, '3S 11.1 V pack', font_size=8.5, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(text(P1, 124, 64, '63 x 77 x 21 + 3 felt', font_size=6, font_weight=400, fill='#b91c1c', text_anchor='middle'))
    w(text(P1, 124, 69.47, 'as fixed 28 Sep, felt straps', font_size=6, font_weight=700, fill='#047857', text_anchor='middle'))
    w(circle(P1, 85, 34, 3.2, fill='#b91c1c'))
    w(circle(P1, 85, 91, 3.2, fill='#334155'))
    w(rect(P1, 85, 21, 6, 16, rx=1, fill='#ffffff', stroke='#334155', stroke_width=1))
    w(text(P1, 98, 19, 'SM-2P', font_size=5.4, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(path('M204.5 1125.7 L230.0 1158.0 L366.0 1161.4', fill='none', stroke='#334155', stroke_width=2.4))
    w(rect(P1, 180, 107.53, 18, 9, rx=3, fill='#334155'))
    w(text(P1, 150, 117.53, 'charge lead parks here', font_size=5.4, font_weight=700, fill='#334155', text_anchor='middle'))
    w(text(PX, 95, 1123.0, 'Front axle', font_size=8.5, font_weight=700, fill='#475569'))
    w(text(PX, 95, 1134.0, 'as supplied', font_size=7.8, fill='#475569'))
    # the two rear motors from the CAD (JGB37-520)
    w(rect(PX, 405.4, 960.9, 62.7, 40.8, rx=2, fill='#e0e7ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(P1, 203.18, 11.76, 36.88, 9.71, rx=2, fill='#eef2ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(P1, 205.18, 21.47, 32.88, 29.41, rx=2, fill='#eef2ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(P1, 204.59, 44.29, 34, 12.41, rx=2, fill='#eef2ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(PX, 431.4, 937.3, 10.4, 62.9, rx=2, fill='#cbd5e1', stroke='#4338ca', stroke_width=1.1))
    w(text(P1, 221.65, 4.88, 'MOTOR R', font_size=7.5, font_weight=700, fill='#4338ca', text_anchor='middle'))
    w(text(P1, 221.65, 10.76, 'gearbox', font_size=6.5, fill='#4338ca', text_anchor='middle'))
    w(rect(PX, 405.4, 1145.2, 62.7, 40.8, rx=2, fill='#e0e7ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(P1, 203.18, 99.06, 36.88, 9.71, rx=2, fill='#eef2ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(P1, 205.18, 69.71, 32.88, 29.41, rx=2, fill='#eef2ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(P1, 204.59, 63.88, 34, 12.41, rx=2, fill='#eef2ff', stroke='#4338ca', stroke_width=1.1))
    w(rect(PX, 431.8, 1146.7, 10.4, 62.9, rx=2, fill='#cbd5e1', stroke='#4338ca', stroke_width=1.1))
    w(text(P1, 221.65, 113.29, 'MOTOR L', font_size=7.5, font_weight=700, fill='#4338ca', text_anchor='middle'))
    w(text(P1, 221.65, 119.18, 'gearbox', font_size=6.5, fill='#4338ca', text_anchor='middle'))
    # Hiwonder motor driver, as mounted 21 Sep, and its connectors
    w(rect(P1, 168, 22.59, 42, 58, rx=4, fill='#f5f3ff', fill_opacity=0.82, stroke='#6d28d9', stroke_width=1.4))
    w(text(P1, 185.59, 45.29, 'MOTOR DRIVER', font_size=8.2, font_weight=700, fill='#6d28d9', text_anchor='middle'))
    w(text(P1, 185.59, 50.88, '42 x 58 x 10', font_size=6.6, fill='#6d28d9', text_anchor='middle'))
    w(text(P1, 185.59, 55.88, 'holes 32.4 x 48.4', font_size=6.4, fill='#7c3aed', text_anchor='middle'))
    w(text(P1, 185.59, 60.88, 'as mounted 21 Sep', font_size=6.2, font_weight=700, fill='#047857', text_anchor='middle'))
    w(line(P1, 168, 22.59, 210, 22.59, stroke='#7c3aed', stroke_width=2.6))
    w(rect(P1, 176.41, 19.06, 5.29, 3.53, fill='#ddd6fe', stroke='#7c3aed', stroke_width=0.9))
    w(rect(P1, 181.88, 17.88, 13.29, 4.71, fill='#ddd6fe', stroke='#7c3aed', stroke_width=0.9))
    w(rect(P1, 195.53, 19.06, 5, 3.53, fill='#ddd6fe', stroke='#7c3aed', stroke_width=0.9))
    w(text(P1, 185.59, 13.82, 'VM · 3-pin · I2C', font_size=6.6, font_weight=700, fill='#7c3aed', text_anchor='middle'))
    w(text(P1, 185.59, 8.82, 'harness fans out', font_size=6.2, fill='#7c3aed', text_anchor='middle'))
    w(circle(P1, 205.18, 27.41, 3.2, fill='#ffffff', stroke='#047857', stroke_width=1.6) + circle(P1, 205.18, 27.41, 1.4, fill='#047857'))
    w(circle(P1, 205.18, 75.82, 3.2, fill='#ffffff', stroke='#047857', stroke_width=1.6) + circle(P1, 205.18, 75.82, 1.4, fill='#047857'))
    w(circle(P1, 172.82, 27.41, 3.2, fill='#ffffff', stroke='#0891b2', stroke_width=1.6, stroke_dasharray='2.2 1.8'))
    w(circle(P1, 172.82, 75.82, 3.2, fill='#ffffff', stroke='#0891b2', stroke_width=1.6, stroke_dasharray='2.2 1.8'))
    w(path('M350.6 1014.4 L345.0 1008.8 M353.8 1103.1 L353.8 1109.5', stroke='#0891b2', stroke_width=1.3, stroke_dasharray='2.2 1.8'))
    w(rect(P1, 165.29, 35.53, 3.53, 4.12, rx=1, fill='#ddd6fe', stroke='#6d28d9', stroke_width=1))
    w(rect(P1, 165.29, 63.53, 3.53, 4.12, rx=1, fill='#ddd6fe', stroke='#6d28d9', stroke_width=1))
    w(text(P1, 170.59, 39.06, 'M3 - R motor', font_size=6.4, font_weight=700, fill='#6d28d9'))
    w(text(P1, 170.59, 67.06, 'M1 - L motor', font_size=6.4, font_weight=700, fill='#6d28d9'))
    w(text(PX, 366, 1116.5, '2 × M3 + spacers, slot x 203.5', font_size=6.2, font_weight=700, fill='#047857', text_anchor='middle'))
    w(circle(P1, 160.59, 90, 5, fill='#dc2626'))
    w(text(P1, 160.59, 91.65, '?', font_size=7.5, font_weight=700, fill='#ffffff', text_anchor='middle'))
    w(text(P1, 165.29, 91.65, 'front pair: add 2 ties', font_size=6.2, fill='#b91c1c'))
    w(comment("Plate 2's lower face is the harness board (MEC-16): fuses, buses, INA226, UBEC and splices are taped there, so they are not drawn on this plan. Positions: MEC-16 and mechanical/plate1.py"))
    w(comment('Switch bodies reaching in from the lower fascia panel, 15-35 mm above plate 1 (MEC-14)'))
    # switch bodies SW1 (drive) and SW2 (logic)
    w(rect(P1, 248, 72, 22, 20, rx=3, fill='#fee2e2', fill_opacity=0.7, stroke='#b91c1c', stroke_width=1.2, stroke_dasharray='3 2'))
    w(text(P1, 259, 81.18, 'SW1', font_size=6.4, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(text(P1, 259, 85.88, 'DRIVE', font_size=5.2, fill='#b91c1c', text_anchor='middle'))
    w(rect(P1, 248, 28, 22, 20, rx=3, fill='#dcfce7', fill_opacity=0.7, stroke='#15803d', stroke_width=1.2, stroke_dasharray='3 2'))
    w(text(P1, 259, 37.18, 'SW2', font_size=6.4, font_weight=700, fill='#15803d', text_anchor='middle'))
    w(text(P1, 259, 41.88, 'LOGIC', font_size=5.2, fill='#15803d', text_anchor='middle'))
    w(text(P1, 259, 54.41, '+ ↑ Bauer', font_size=5.2, fill='#15803d', text_anchor='middle'))
    return o


def plate1_notes():
    """Dimension line and the notes under plate 1."""
    o = []
    w = o.append
    # dimension line and notes under plate 1
    w(text(PX, 66, 1194.0, 'JGB37-520 ×2 from the CAD: ⌀37 gearbox outboard · ⌀33 can · encoder inboard', font_size=8, fill='#4338ca'))
    w(text(PX, 66, 1206.0, 'motors reach to 29.8 mm from the rear edge - switches stop ~8 mm short', font_size=8, fill='#b45309'))
    w(text(PX, 66, 1218.0, "the driver's rear 7 mm sits over the cans - clearance is vertical only, set by the spacer height", font_size=8, fill='#b45309'))
    w(line(PX, 60, 1222.0, 518, 1222.0, stroke='#94a3b8', stroke_width=1, marker_start='url(#d)', marker_end='url(#e)'))
    w(text(PX, 289, 1236.0, '270 mm', font_size=9, fill='#64748b', text_anchor='middle'))
    w(text(PX, 289, 1250.0, 'widest 120.4 mm at the front axle · 84.7 mm at the waist · 94.2 mm across the rear flat', font_size=8.5, fill='#64748b', text_anchor='middle'))
    w(text(PX, 63, 1236.0, '◀ FRONT', font_size=9, fill='#64748b'))
    w(text(PX, 515, 1236.0, 'REAR ▶', font_size=9, fill='#64748b', text_anchor='end'))
    return o


def lower_face_heading():
    """Middle deck, lower face (the harness board), comment and title."""
    o = []
    w = o.append
    w(comment('MIDDLE DECK, LOWER FACE - the harness board (MEC-16). Seen from BELOW, as it lies upside down on the bench: mirrored, vehicle right at the bottom. Positions from mechanical/plate1.py'))
    w(text(PX, 60, 614.3, 'MIDDLE DECK - plate 2, LOWER FACE: the harness board', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(text(PX, 60, 628.3, 'seen from <tspan font-weight="700">below</tspan>, upside down on the bench - <tspan font-weight="700" fill="#be185d">mirrored: vehicle RIGHT at the BOTTOM</tspan> · 3M foam tape', font_size=9.5, fill='#64748b'))
    return o


def harness_board():
    """The harness parts taped under plate 2, seen from below."""
    o = []
    w = o.append
    # the harness board seen from below (MEC-16): fuse holders, buses, INA226, UBEC, splices
    w(gopen(stroke_linejoin='round'))
    w(rect(PB, 162, 76.97, 86, 4, fill='#64748b', fill_opacity=0.22, stroke='#64748b', stroke_width=0.8, stroke_dasharray='3 2'))
    w(rect(PB, 200, 64.03, 48, 5.47, fill='#64748b', fill_opacity=0.22, stroke='#64748b', stroke_width=0.8, stroke_dasharray='3 2'))
    w(rect(PB, 203, 120.5, 37, 120.47, fill='none', stroke='#6d28d9', stroke_width=0.8, stroke_dasharray='2 2'))
    w(text(PB, 205, 28.03, 'motors below:', font_size=5.4, font_weight=400, fill='#6d28d9', text_anchor='start') + text(PB, 205, 21.97, '9 mm, wires only', font_size=5.4, font_weight=400, fill='#6d28d9', text_anchor='start'))
    w(rect(PB, 96, 31.97, 50, 30, rx=3, fill='#1f2937', stroke='#be185d', stroke_width=1.3))
    w(rect(PB, 152, 31.97, 50, 30, rx=3, fill='#1f2937', stroke='#be185d', stroke_width=1.3))
    w(rect(PB, 152, 118.03, 50, 30, rx=3, fill='#1f2937', stroke='#be185d', stroke_width=1.3))
    w(line(PB, 108, 1.97, 134, 1.97, stroke='#be185d', stroke_width=3))
    w(line(PB, 164, 1.97, 190, 1.97, stroke='#be185d', stroke_width=3))
    w(line(PB, 164, 118.03, 190, 118.03, stroke='#be185d', stroke_width=3))
    w(rect(PB, 88, 70.03, 18.59, 30, rx=2, fill='#fecaca', stroke='#b91c1c', stroke_width=1.3))
    w(rect(PB, 134, 70.03, 18.59, 30, rx=2, fill='#e2e8f0', stroke='#334155', stroke_width=1.3))
    w(line(PB, 106.59, 40.03, 106.59, 70.03, stroke='#b91c1c', stroke_width=2))
    w(line(PB, 134, 40.03, 134, 70.03, stroke='#334155', stroke_width=2))
    w(rect(PB, 108, 100.03, 26, 22, rx=2, fill='#ecfeff', stroke='#0e7490', stroke_width=1.3))
    w(line(PB, 110, 78.03, 132, 78.03, stroke='#0e7490', stroke_width=2.4))
    w(rect(PB, 178, 69.38, 18.59, 18.41, rx=2, fill='#fed7aa', stroke='#c2410c', stroke_width=1.2))
    w(rect(PB, 100, 111.97, 35, 12, rx=2, fill='#fef08a', stroke='#a16207', stroke_width=1.2))
    w(rect(PB, 83, 39.62, 13, 18.59, rx=1.5, fill='#fed7aa', stroke='#c2410c', stroke_width=1))
    w(rect(PB, 157, 48.03, 18.59, 13, rx=1.5, fill='#fed7aa', stroke='#c2410c', stroke_width=1))
    w(rect(PB, 138.71, 116.97, 18.59, 13, rx=1.5, fill='#fed7aa', stroke='#c2410c', stroke_width=1))
    w(GCLOSE)
    # its labels
    w(gopen())
    w(text(PB, 121, 15.03, 'MAIN 7.5 A', font_size=6.4, font_weight=700, fill='#ffffff', text_anchor='middle'))
    w(text(PB, 177, 15.03, 'MOTORS 5 A', font_size=6.4, font_weight=700, fill='#ffffff', text_anchor='middle'))
    w(text(PB, 177, 100.97, 'UBEC 5 A', font_size=6.4, font_weight=700, fill='#ffffff', text_anchor='middle'))
    w(text(PB, 97.29, 56.97, '(+)', font_size=7.5, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(text(PB, 97.29, 50.97, '3 of 5', font_size=5.2, font_weight=400, fill='#b91c1c', text_anchor='middle'))
    w(text(PB, 143.29, 56.97, '(−)', font_size=7.5, font_weight=700, fill='#334155', text_anchor='middle'))
    w(text(PB, 143.29, 50.97, '5 of 5', font_size=5.2, font_weight=400, fill='#334155', text_anchor='middle'))
    w(text(PB, 121, 86.97, 'INA226', font_size=6.4, font_weight=700, fill='#0e7490', text_anchor='middle'))
    w(text(PB, 121, 81.97, 'terminals ↓', font_size=5, font_weight=400, fill='#0e7490', text_anchor='middle'))
    w(text(PB, 187.29, 61.97, 'SW1', font_size=5.4, font_weight=700, fill='#c2410c', text_anchor='middle'))
    w(text(PB, 187.29, 56.97, 'split', font_size=5.4, font_weight=700, fill='#c2410c', text_anchor='middle'))
    w(text(PB, 117.53, 105.03, 'UBEC 6 V', font_size=5.8, font_weight=700, fill='#a16207', text_anchor='middle'))
    w(text(PB, 89.53, 29.03, 'S1', font_size=5.4, font_weight=700, fill='#c2410c', text_anchor='middle'))
    w(text(PB, 166.29, 40.5, 'S2/S4', font_size=5.4, font_weight=700, fill='#c2410c', text_anchor='middle'))
    w(text(PB, 148, 109.5, 'S3/S5', font_size=5.4, font_weight=700, fill='#c2410c', text_anchor='middle'))
    w(text(PB, 121.47, 61.97, 'opening', font_size=5.4, font_weight=400, fill='#be185d', text_anchor='middle'))
    w(text(PB, 121.47, 56.97, 'wires up', font_size=5.4, font_weight=400, fill='#be185d', text_anchor='middle'))
    w(text(PB, 225, 65.97, 'trunk to SW1 / SW2', font_size=5.4, font_weight=400, fill='#475569', text_anchor='middle'))
    w(GCLOSE)
    w(text(PX, 66, 893.3, 'Only two plugs cross to plate 1, both from the right side once closed: SM-2P at S1, driver VM at S2/S4. The switch panel rides with plate 2. Thick edge = fuse lid.', font_size=8, fill='#b45309'))
    w(text(PX, 66, 905.3, 'Nominal sizes (MEC-16 "To confirm"). The six tray screw heads T1-T6 are drawn; each is at least 0.8 mm clear of the taped parts (MEC-17).', font_size=8, fill='#b45309'))
    return o


def stack_elevation():
    """Deck stack, side elevation."""
    o = []
    w = o.append
    # deck stack, side elevation: the two measured gaps
    w(text(PX, 600, 110, 'DECK STACK - side elevation', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(line(PX, 600, 118, 1280, 118, stroke='#e2e8f0'))
    w(rect(PX, 600, 156.0, 300, 4.7, fill='#cbd5e1', stroke='#94a3b8'))
    w(text(PX, 908, 161.7, 'plate 3  z 121.12–123.12', font_size=9, font_weight=700, fill='#334155'))
    w(rect(PX, 600, 254.7, 300, 4.7, fill='#cbd5e1', stroke='#94a3b8'))
    w(text(PX, 908, 260.4, 'plate 2  z 79.12–81.12', font_size=9, font_weight=700, fill='#334155'))
    w(rect(PX, 600, 376.9, 300, 4.7, fill='#cbd5e1', stroke='#94a3b8'))
    w(text(PX, 908, 382.6, 'plate 1  z 27.12–29.12', font_size=9, font_weight=700, fill='#334155'))
    w(rect(PX, 600, 160.7, 300, 94.0, fill='#f8fafc', stroke='#cbd5e1', stroke_dasharray='4 3'))
    w(text(PX, 750, 203.7, 'UPPER GAP 40 mm - measured', font_size=8.5, font_weight=700, fill='#334155', text_anchor='middle'))
    w(text(PX, 750, 216.7, 'fascia upper panel, 42 mm tall: USB-C · DE-9 · Mini-B', font_size=8, fill='#64748b', text_anchor='middle'))
    w(rect(PX, 600, 259.4, 300, 117.5, fill='#f8fafc', stroke='#cbd5e1', stroke_dasharray='4 3'))
    w(text(PX, 750, 314.1, 'LOWER GAP 50 mm - measured', font_size=8.5, font_weight=700, fill='#334155', text_anchor='middle'))
    w(text(PX, 750, 327.1, 'fascia lower panel, 52 mm tall: DRIVE / LOGIC switches', font_size=8, fill='#64748b', text_anchor='middle'))
    w(text(PX, 600, 395.6, 'below plate 1: running gear, wheels, ground clearance - nothing mounted', font_size=8.5, fill='#64748b'))
    return o


def run_table():
    """What is fixed, and the wire run table (one row per RUNS entry)."""
    o = []
    w = o.append
    # text block: what is fixed, what is not
    w(text(PX, 600, 470, 'WHAT IS FIXED, AND WHAT IS NOT', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(line(PX, 600, 478, 1280, 478, stroke='#e2e8f0'))
    w(text(PX, 600, 498, 'Deck spacing - settled 2026-09-20', font_size=9.5, font_weight=700, fill='#166534'))
    w(text(PX, 600, 512, 'Measured on the built kit: 50 mm below, 40 mm above. The kit ships two standoff lengths; the', font_size=9, fill='#475569'))
    w(text(PX, 600, 525, 'single-plate CAD only ever had the 50 and our 3-deck model repeated it for both gaps. The fascia', font_size=9, fill='#475569'))
    w(text(PX, 600, 538, 'panels are therefore 52 and 42 mm tall and are no longer one blank (MEC-09).', font_size=9, fill='#475569'))
    w(text(PX, 600, 557, "Plate 1 wiring - every run, on plate 2's harness board, 2026-09-28 (MEC-16, HW-20)", font_size=9.5, font_weight=700, fill='#1e293b'))
    w(gopen(font_size=7.6, font_weight=700, fill='#64748b') + text(PX, 600, 572, '#') + text(PX, 614, 572, 'Run') + text(PX, 772, 572, 'Wire') + text(PX, 862, 572, 'Cut, cm') + text(PX, 906, 572, 'Ends and clips') + GCLOSE)
    w(line(PX, 600, 576, 1280, 576, stroke='#e2e8f0'))
    for i, (n, run, wire, cut, ends) in enumerate(RUNS):
        y = f'{587.0 + 12.2 * i:.1f}'
        w(gopen(font_size=7.8, fill='#475569') + text(PX, 600, y, n, font_weight=700) + text(PX, 614, y, run)
          + text(PX, 772, y, wire) + text(PX, 862, y, cut) + text(PX, 906, y, ends) + GCLOSE)
    w(text(PX, 600, 786, '18 AWG cut: ~1.5 m red, ~1.1 m black, of 2.5 + 2.5 m bought · clips: 2 × 221-415, 1 × 3-port, 7 × 2-port', font_size=8, font_weight=700, fill='#1e293b'))
    w(text(PX, 600, 798, 'Measured off the 3D model (plate1.py) + 22 mm strip + 20 %. ↓ = drop to plate 1, plugged from the right side once closed. Nominal heights.', font_size=8, fill='#b45309'))
    return o


def legend():
    """Legend."""
    o = []
    w = o.append
    # legend
    w(text(PX, 600, 812, 'LEGEND', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(line(PX, 600, 820, 1280, 820, stroke='#e2e8f0'))
    w(rect(PX, 600, 832, 18, 12, rx=2, fill='none', stroke='#dc2626', stroke_width=1.8, stroke_dasharray='4 2.5'))
    w(circle(PX, 618, 832, 4.5, fill='#dc2626'))
    w(text(PX, 618, 835, '?', font_size=7, font_weight=700, fill='#fff', text_anchor='middle'))
    w(text(PX, 634, 840, 'Size or fixing NOT resolved - do not commit this position yet', font_size=8.8, fill='#475569'))
    w(circle(PX, 609, 856, 4.2, fill='none', stroke='#4338ca', stroke_width=1.8))
    w(line(PX, 602.5, 856, 615.5, 856, stroke='#4338ca', stroke_width=1.3))
    w(line(PX, 609, 849.5, 609, 862.5, stroke='#4338ca', stroke_width=1.3))
    w(text(PX, 634, 859, 'M2.5 screw into an existing chassis hole - washer spans the 0.34 mm slop (MEC-10)', font_size=8.8, fill='#475569'))
    w(circle(PX, 609, 875, 4.2, fill='none', stroke='#047857', stroke_width=1.8))
    w(circle(PX, 609, 875, 1.5, fill='#047857'))
    w(text(PX, 634, 878, 'M3 screw into a 3.18 mm chassis hole - close fit, ease the part not the plate', font_size=8.8, fill='#475569'))
    w(circle(PX, 609, 894, 4, fill='none', stroke='#7c3aed', stroke_width=1.5))
    w(circle(PX, 609, 894, 1.5, fill='#7c3aed'))
    w(text(PX, 634, 897, 'Fascia clamp hole, M3, present on every deck (MEC-07)', font_size=8.8, fill='#475569'))
    w(circle(PX, 609, 913, 4, fill='none', stroke='#a16207', stroke_width=1.5))
    w(text(PX, 634, 916, 'Chassis standoff, 6.0 mm A/F hex', font_size=8.8, fill='#475569'))
    w(circle(PX, 609, 932, 4.2, fill='#ffffff', stroke='#047857', stroke_width=1.6) + circle(PX, 609, 932, 1.4, fill='#047857'))
    w(text(PX, 634, 935, 'M3 through a 4.29 mm chassis <tspan font-weight="700">slot</tspan> - free to slide along it, washer under the head', font_size=8.8, fill='#475569'))
    w(circle(PX, 609, 951, 4.2, fill='#ffffff', stroke='#0891b2', stroke_width=1.6, stroke_dasharray='2.2 1.8'))
    w(path('M609 951 L621 951', stroke='#0891b2', stroke_width=1.3, stroke_dasharray='2.2 1.8'))
    w(text(PX, 634, 954, "Cable tie through the part's own hole into the slot or cutout under it - no chassis hole exists there", font_size=8.8, fill='#475569'))
    w(rect(PX, 601, 964, 16, 10, rx=1.5, fill='#0f766e', fill_opacity=0.14, stroke='#0f766e', stroke_width=1, stroke_dasharray='3 2') + rect(PX, 601, 964, 16, 3.4, fill='#0f766e', fill_opacity=0.38))
    w(text(PX, 634, 973, 'Felt strap over the pack, held by zip ties through the chassis slots - as fitted 2026-09-28', font_size=8.8, fill='#475569'))
    return o



def build():
    o = []
    o += header()
    o += plate3_heading() + plate(P3, **PALE)
    o += plate2_heading() + plate(P2, **PALE)
    o += plate1_heading() + plate(P1, **SOLID)
    o += frdm()
    o += carrier_and_bauer()
    o += plate1_parts()
    o += plate1_notes()
    o += lower_face_heading() + plate(PB, **SOLID)
    o += harness_board()
    o += tray_heads()
    o += stack_elevation()
    o += run_table()
    o += legend()
    o.append('</svg>')
    return o


if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else OUT, build())
