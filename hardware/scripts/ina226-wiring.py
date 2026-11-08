#!/usr/bin/env python3
"""How the INA226 module is wired: high-side shunt in the pack (+) line, V+ sense from the (+) bus, V- (which IS the module's GND) to
the (-) bus, and the I2C lead to carrier header I2C-A (HW-03, HW-07, HW-20, HW-22, MEC-15, MEC-16).

    python3 ina226-wiring.py             # -> ../renders/ina226-wiring.svg
    python3 ../../tools/check-drawings.py   # fails if the SVG is not what this script writes

Drawn after the 2026-11-08 fault: V- had been landed on the + line, which lifted the module's GND, and through I2C-A the whole
carrier ground, to battery +. Terminal order is the module's own, left to right with the terminal block at the top (GERUI R002
module, BOM 3.9). Edit this script, never the SVG.
"""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawing import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders', 'ina226-wiring.svg')
I = '  '

# same net colours as wiring-schematic.py
NET = {'pack': '#d92b2b', 'gnd': '#111827', 'i2c': '#7c3aed', 'v33': '#0891b2'}
W, H = 1200, 940

# terminal block, left to right as on the module: (x, label, block colour, role)
TERM_Y = 200
TERMS = [(470, 'V+', '#fdba74', 'bus voltage sense'),
         (560, 'I+', '#fdba74', 'current in'),
         (650, 'I−', '#86efac', 'current out'),
         (740, 'V− = GND', '#86efac', 'voltage reference')]
# I2C header on the module, left to right, and where each pin lands on the carrier
PIN_Y = 404
PINS = [(520, 'GND', 'B·A7', 'GND', NET['gnd']),
        (580, 'SCL', 'B·B7', 'PB6', NET['i2c']),
        (640, 'SDA', 'B·C7', 'PB7', NET['i2c']),
        (700, 'VCC', 'B·D7', '3V3', NET['v33'])]

PBUS_X, PBUS_PORTS = 905, [(80, 'INA V+ sense', True), (120, 'INA I− out', True), (160, 'S8 switch feed → SW1, SW2', False),
                           (200, 'spare', False), (240, 'spare', False)]
NBUS_X, NBUS_PORTS = 860, [(340, 'INA V− (the spare port)', True), (380, 'battery −', False), (420, 'S4 motor driver −', False),
                           (460, 'S5 UBEC − and switch LEDs', False), (500, 'S7 Bauer − (carrier GND via board C)', False)]

CHECKS = [('INA GND pin', 'battery −', 'beep'),
          ('INA GND pin', 'battery +', 'NO beep'),
          ('I+', 'main fuse output', 'beep'),
          ('I−', '(+) bus', 'beep'),
          ('V+', '(+) bus', 'beep'),
          ('V−', '(−) bus', 'beep'),
          ('carrier I2C-A GND', 'battery +', 'NO beep'),
          ('bare module: GND', 'V+, I+, I−', 'NO beep (V− beeps by design)')]


def t(x, y, s, size=11, **kw):
    kw.setdefault('fill', '#1f2937')
    return text(PX, x, y, s, font_size=size, **kw)


def build():
    o = []
    w = o.append
    w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">')
    w(I + el('rect', width=W, height=H, fill='#fbfaf8'))
    w(I + t(40, 32, 'NEXUS - INA226 wiring (high-side shunt)', 18, font_weight=700, fill='#1a1a1a'))
    w(I + t(40, 48, 'HW-03 fuse before shunt · HW-07 high-side sensing · HW-20 three fuses · MEC-16 buses on plate 2 · '
            'I²C on carrier header I2C-A (HW-22, MEC-15)', 11, fill='#666'))

    w(I + comment('battery and main fuse'))
    w(I + rect(PX, 40, 90, 140, 80, fill='#e5e7eb', stroke='#374151', stroke_width=1.6, rx=3))
    w(I + t(110, 120, '3S LiPo', 12, font_weight=700, text_anchor='middle'))
    w(I + t(110, 137, '9.0 - 12.6 V', 10, fill='#4b5563', text_anchor='middle'))
    w(I + t(172, 106, '+', 12, font_weight=700, fill='#b91c1c'))
    w(I + line(PX, 110, 170, 110, 196, stroke=NET['gnd'], stroke_width=3))
    w(I + t(110, 212, 'battery − → (−) bus', 10, text_anchor='middle'))
    w(I + line(PX, 180, 110, 200, 110, stroke=NET['pack'], stroke_width=4))
    w(I + path('M200 110 L200 94 L220 94', fill='none', stroke=NET['pack'], stroke_width=4))
    w(I + rect(PX, 220, 76, 120, 36, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.6, rx=2))
    w(I + t(280, 92, 'MAIN FUSE 7.5 A', 10, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + t(280, 105, 'first in the chain', 8.5, fill='#991b1b', text_anchor='middle'))

    w(I + comment('the module'))
    w(I + rect(PX, 420, 160, 370, 270, fill='#fef2f2', stroke='#b91c1c', stroke_width=2, rx=6))
    w(I + t(240, 170, 'INA226 module', 12, font_weight=700, fill='#7f1d1d'))
    w(I + t(240, 186, 'GERUI, R002 · BOM 3.9', 10, fill='#991b1b'))
    w(I + t(240, 202, 'terminals at the top,', 10, fill='#991b1b'))
    w(I + t(240, 216, 'as in the vendor photo', 10, fill='#991b1b'))
    for x, lab, col, role in TERMS:
        w(I + rect(PX, x - 30, TERM_Y - 26, 60, 52, fill=col, stroke='#374151', stroke_width=1.2, rx=3))
        w(I + circle(PX, x, TERM_Y, 13, fill='#e5e7eb', stroke='#374151', stroke_width=1.2))
        w(I + line(PX, x - 8, TERM_Y, x + 8, TERM_Y, stroke='#374151', stroke_width=1.5))
        w(I + t(x, TERM_Y + 44, lab, 11, font_weight=700, text_anchor='middle'))
        w(I + t(x, TERM_Y + 58, role, 8.5, fill='#4b5563', text_anchor='middle'))
    # shunt between I+ and I-
    w(I + path('M560 266 L560 286 L578 286', fill='none', stroke=NET['pack'], stroke_width=2))
    w(I + path('M632 286 L650 286 L650 266', fill='none', stroke=NET['pack'], stroke_width=2))
    w(I + rect(PX, 578, 276, 54, 20, fill='#1f2937', rx=2))
    w(I + t(605, 290, 'R002', 10, font_weight=700, fill='#f9fafb', text_anchor='middle'))
    w(I + t(605, 308, '2 mΩ shunt', 8.5, fill='#4b5563', text_anchor='middle'))
    # chip, address
    w(I + rect(PX, 590, 322, 70, 34, fill='#111827', rx=2))
    w(I + t(625, 343, 'INA226', 10, font_weight=700, fill='#f9fafb', text_anchor='middle'))
    w(I + t(440, 340, 'A0, A1 open', 9, fill='#4b5563'))
    w(I + t(440, 353, '→ address 0x40', 9, fill='#4b5563'))
    # V- is GND on the board
    w(I + path('M740 266 L740 372 L520 372 L520 392', fill='none', stroke=NET['gnd'], stroke_width=1.6, stroke_dasharray='5 4'))
    w(I + t(748, 330, 'on the PCB:', 9.5, font_weight=700, fill='#111827'))
    w(I + t(748, 343, 'V− IS GND', 9.5, font_weight=700, fill='#111827'))
    for x, lab, *_ in PINS:
        w(I + rect(PX, x - 6, PIN_Y - 6, 12, 12, fill='#d4a017', stroke='#78350f', stroke_width=1))
        w(I + t(x, PIN_Y - 12, lab, 9.5, font_weight=700, text_anchor='middle'))

    w(I + comment('the four terminal wires'))
    # I+ from the fuse, hopping over the V+ sense wire
    w(I + path('M340 94 L462 94 A8 8 0 0 1 478 94 L560 94 L560 174', fill='none', stroke=NET['pack'], stroke_width=4))
    w(I + t(370, 88, 'fuse out → I+   (16-18 AWG)', 9.5, fill='#7f1d1d'))
    # V+ sense to (+) bus port 1
    w(I + path(f'M470 174 L470 66 L890 66 L890 80 L{PBUS_X} 80', fill='none', stroke=NET['pack'], stroke_width=1.8))
    w(I + t(600, 60, 'V+ sense → (+) bus   (22 AWG or thicker, short)', 9.5, fill='#7f1d1d'))
    # I- to (+) bus port 2
    w(I + path(f'M650 174 L650 120 L{PBUS_X} 120', fill='none', stroke=NET['pack'], stroke_width=4))
    w(I + t(668, 113, 'I− → (+) bus   (16-18 AWG)', 9.5, fill='#7f1d1d'))
    # V- to (-) bus spare port
    w(I + path(f'M740 174 L740 146 L840 146 L840 340 L{NBUS_X} 340', fill='none', stroke=NET['gnd'], stroke_width=1.8))
    w(I + t(748, 140, 'V− → (−) bus, never the + line', 9.5, font_weight=700, fill='#111827'))

    w(I + comment('buses'))
    w(I + t(PBUS_X + 15, 52, '(+) WAGO BUS', 9.5, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + rect(PX, PBUS_X, 62, 30, 196, fill='#fecaca', stroke='#b91c1c', stroke_width=2, rx=3))
    for y, lab, new in PBUS_PORTS:
        w(I + circle(PX, PBUS_X + 15, y, 4, fill='#b91c1c'))
        w(I + t(PBUS_X + 40, y + 4, lab + ('   NEW' if lab == 'INA V+ sense' else ''), 10, font_weight=700 if new else 400,
                fill='#7f1d1d' if new else '#6b7280'))
    w(I + t(NBUS_X + 15, 316, '(−) WAGO BUS', 9.5, font_weight=700, fill='#111827', text_anchor='middle'))
    w(I + rect(PX, NBUS_X, 322, 30, 196, fill='#e5e7eb', stroke='#111827', stroke_width=2, rx=3))
    for y, lab, new in NBUS_PORTS:
        w(I + circle(PX, NBUS_X + 15, y, 4, fill='#111827'))
        w(I + t(NBUS_X + 40, y + 4, lab + ('   NEW' if new else ''), 10, font_weight=700 if new else 400,
                fill='#111827' if new else '#6b7280'))

    w(I + comment('I2C lead to the carrier'))
    w(I + rect(PX, 470, 560, 280, 86, fill='#ede9fe', stroke='#6d28d9', stroke_width=1.6, rx=3))
    for x, lab, hole, net, col in PINS:
        w(I + line(PX, x, PIN_Y + 6, x, 574, stroke=col, stroke_width=2.2))
        w(I + rect(PX, x - 6, 574, 12, 12, fill='#d4a017', stroke='#78350f', stroke_width=1))
        w(I + t(x, 602, net, 10, font_weight=700, text_anchor='middle'))
        w(I + t(x, 616, hole, 9, fill='#4b5563', text_anchor='middle'))
    w(I + t(610, 638, 'carrier board B, header I2C-A', 10, font_weight=700, fill='#4c1d95', text_anchor='middle'))
    w(I + t(470, 664, 'Pins drawn in matching order, not as placed: on the carrier I2C-A reads 3V3, SDA, SCL, GND left to right', 9.5, fill='#4b5563'))
    w(I + t(470, 678, 'from above. Connect by NAME: GND to GND, SCL to SCL, SDA to SDA, VCC to 3V3. VCC is 3.3 V, never 5 V.', 9.5, fill='#4b5563'))
    # the carrier ground's own way back
    w(I + path(f'M750 600 L800 600 L800 500 L{NBUS_X} 500', fill='none', stroke=NET['gnd'], stroke_width=1.4, stroke_dasharray='2 4'))
    w(I + t(806, 560, 'carrier GND returns', 9, fill='#4b5563'))
    w(I + t(806, 572, 'via 5V IN and board C', 9, fill='#4b5563'))
    w(I + t(806, 584, '(loop accepted, HW-19)', 9, fill='#4b5563'))

    w(I + comment('the fault'))
    w(I + rect(PX, 40, 260, 340, 150, fill='#fff7ed', stroke='#c2410c', stroke_width=1.6, rx=4))
    w(I + t(56, 284, 'Fault found 2026-11-08', 12, font_weight=700, fill='#9a3412'))
    for i, s in enumerate(['V− had been landed on the + line. V− is the', 'module\'s GND, so the INA GND, and through I2C-A',
                           'the whole carrier ground, sat at battery +:', '13 V between the Bauer ground and every I²C pin.',
                           'The only terminal that goes to ground is V−.', 'The other three are all on the + side.']):
        w(I + t(56, 306 + 16 * i, s, 10.5, fill='#7c2d12', font_weight=700 if i >= 4 else 400))

    w(I + comment('checks'))
    w(I + t(40, 720, 'Before the first power-up: power OFF, meter on continuity', 13, font_weight=700, fill='#1a1a1a'))
    w(I + line(PX, 40, 728, 1160, 728, stroke='#e2e8f0'))
    for i, (a, b, exp) in enumerate(CHECKS):
        col, row = i // 4, i % 4
        x, y = 40 + 560 * col, 752 + 24 * row
        bad = exp.startswith('NO')
        w(I + t(x, y, a, 11, font_weight=700))
        w(I + t(x + 170, y, '↔  ' + b, 11, fill='#374151'))
        w(I + t(x + 340, y, exp, 11, font_weight=700, fill='#c2410c' if bad else '#15803d'))

    w(I + comment('key'))
    for i, (net, lab, sw) in enumerate([('pack', 'main current, 16-18 AWG', 4), ('pack', 'V+ sense, 22 AWG+', 1.8),
                                        ('gnd', 'ground / V− sense', 1.8), ('i2c', 'I²C', 2.2), ('v33', '3V3 from the carrier', 2.2)]):
        x = 40 + 220 * i
        w(I + line(PX, x, 890, x + 30, 890, stroke=NET[net], stroke_width=sw))
        w(I + t(x + 38, 894, lab, 10, fill='#374151'))
    w(I + t(40, 920, 'Generated by hardware/scripts/ina226-wiring.py. Edit the script, never this file.', 9, fill='#9ca3af'))
    w('</svg>')
    return o


write(OUT, build())
