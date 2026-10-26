#!/usr/bin/env python3
"""The hardware wiring schematic: what connects to what - fuses, switches, 18 AWG harness, the 5 V rail, CAN, I2C, PWM
(HW-05, HW-17, HW-19, HW-20).

    python3 wiring-schematic.py          # -> ../renders/wiring-schematic.svg
    python3 ../../tools/check-drawings.py   # fails if the SVG is not what this script writes

A block diagram in pixels: three sections (power, signals, key). The wire colours are one palette, NET, shared with the key, so a
net changes colour everywhere by changing it once. Edit this script, never the SVG.
"""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawing import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders', 'wiring-schematic.svg')
I = '  '                                  # the file indents its elements two spaces

# the wire palette, as in the key at the bottom
NET = {'pack': '#d92b2b', 'switched': '#e8821a', 'v5': '#15803d', 'v6': '#0d9488', 'gnd': '#111827',
       'can': '#1d4ed8', 'i2c': '#7c3aed', 'pwm': '#78350f'}

WIRE_KEY = [   # x, y, net, label
    (140, 808, 'pack', 'pack 12 V, unswitched'),
    (360, 808, 'switched', 'switched 12 V'),
    (560, 808, 'v5', '5 V'),
    (720, 808, 'v6', '6 V servo'),
    (890, 808, 'gnd', 'ground · returns to (−) bus'),
    (140, 834, 'can', 'CAN'),
    (250, 834, 'i2c', 'I²C'),
]


def header():
    """Page, title and subtitle."""
    o = []
    w = o.append
    w('<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="890" viewBox="0 0 1320 890" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">')
    w(I + '<defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#555"/></marker></defs>')
    w(I + el('rect', width=1320, height=890, fill='#fbfaf8'))
    w('')
    w(I + text(PX, 40, 32, 'NEXUS - hardware wiring schematic', font_size=18, font_weight=700, fill='#1a1a1a'))
    w(I + text(PX, 40, 52, 'Rear-wheel drive Ackermann · 2 drive motors + 1 steering servo · every load returns to the (−) WAGO bus · all fuses inline · harness wire 18 AWG · carrier boards A, B, C shown', font_size=11, fill='#666'))
    w('')
    return o


def power_sources():
    """POWER: battery, main fuse, shunt, the (+) bus, the (-) bus and the fuse rationale."""
    o = []
    w = o.append
    w(I + comment('===================== POWER ====================='))
    w(I + text(PX, 40, 88, 'POWER', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(I + line(PX, 40, 96, 1280, 96, stroke='#e2e8f0'))
    w('')
    w(I + comment('battery'))
    w(I + rect(PX, 40, 150, 170, 100, fill='#e5e7eb', stroke='#374151', stroke_width=1.6, rx=3))
    w(I + text(PX, 125, 178, '3S LiPo', font_size=12, font_weight=700, fill='#111827', text_anchor='middle'))
    w(I + text(PX, 125, 195, '11.1 V · 6000 mAh', font_size=11, fill='#374151', text_anchor='middle'))
    w(I + text(PX, 125, 212, 'SM-2P · 22 AWG lead · PCM', font_size=9, fill='#6b7280', text_anchor='middle'))
    w(I + text(PX, 125, 227, '9.0 – 12.6 V', font_size=9, fill='#6b7280', text_anchor='middle'))
    w(I + text(PX, 216, 176, '+', font_size=11, font_weight=700, fill='#b91c1c'))
    w(I + text(PX, 213, 262, '−', font_size=13, font_weight=700, fill='#111827'))
    w('')
    w(I + comment('+ chain: main fuse first, then shunt, then (+) bus bar'))
    w(I + line(PX, 210, 180, 250, 180, stroke=NET['pack'], stroke_width=3))
    w(I + rect(PX, 250, 160, 110, 40, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.6, rx=2))
    w(I + text(PX, 305, 177, 'MAIN FUSE 7.5 A', font_size=10, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + text(PX, 305, 191, 'inline · ≤15 cm from (+)', font_size=8.5, fill='#991b1b', text_anchor='middle'))
    w(I + line(PX, 360, 180, 390, 180, stroke=NET['pack'], stroke_width=3))
    w(I + rect(PX, 390, 160, 100, 40, fill='#cffafe', stroke='#0e7490', stroke_width=1.6, rx=2))
    w(I + text(PX, 440, 177, 'INA226 SHUNT', font_size=10, font_weight=700, fill='#164e63', text_anchor='middle'))
    w(I + text(PX, 440, 191, 'R002 2 mΩ · high-side', font_size=8.5, fill='#155e75', text_anchor='middle'))
    w(I + line(PX, 490, 180, 600, 180, stroke=NET['pack'], stroke_width=3))
    w('')
    w(I + comment('(+) bus bar'))
    w(I + text(PX, 613, 122, '(+) WAGO BUS', font_size=9, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + rect(PX, 600, 130, 26, 250, fill='#fecaca', stroke='#b91c1c', stroke_width=2, rx=3))
    w(I + circle(PX, 613, 150, 3, fill='#b91c1c') + circle(PX, 613, 190, 3, fill='#b91c1c'))
    w(I + circle(PX, 613, 230, 3, fill='#b91c1c') + circle(PX, 613, 270, 3, fill='#b91c1c'))
    w(I + circle(PX, 613, 310, 3, fill='#b91c1c'))
    w(I + text(PX, 613, 396, '1 × 221-415 · 2 spare', font_size=7.5, fill='#991b1b', text_anchor='middle'))
    w('')
    w(I + comment('feeds off the (+) bar'))
    w(I + line(PX, 626, 190, 668, 190, stroke=NET['pack'], stroke_width=3))
    w(I + line(PX, 668, 168, 668, 330, stroke=NET['pack'], stroke_width=3))
    w(I + line(PX, 668, 168, 760, 168, stroke=NET['pack'], stroke_width=3))
    w(I + line(PX, 668, 330, 760, 330, stroke=NET['pack'], stroke_width=3))
    w(I + circle(PX, 668, 190, 3.2, fill='#b91c1c'))
    w(I + text(PX, 676, 252, 'one (+) bus port feeds', font_size=7.5, fill='#991b1b'))
    w(I + text(PX, 676, 263, 'both switches', font_size=7.5, fill='#991b1b'))
    w(I + text(PX, 676, 302, 'no fuse - main covers it (HW-20)', font_size=7.5, fill='#991b1b'))
    w('')
    w(I + comment('(−) bus bar and battery return'))
    w(I + rect(PX, 540, 430, 80, 18, fill='#374151', stroke='#111827', stroke_width=1.6, rx=3))
    w(I + circle(PX, 552, 439, 2.5, fill='#e5e7eb') + circle(PX, 566, 439, 2.5, fill='#e5e7eb') + circle(PX, 580, 439, 2.5, fill='#e5e7eb') + circle(PX, 594, 439, 2.5, fill='#e5e7eb') + circle(PX, 608, 439, 2.5, fill='#e5e7eb'))
    w(I + text(PX, 630, 466, '(−) WAGO BUS - 1 × 221-415 · star ground', font_size=9, font_weight=700, fill='#111827', text_anchor='middle'))
    w(I + text(PX, 630, 479, '4 of 5: battery, motor module, UBEC (with both switch LEDs), Bauer · one spare (MEC-16)', font_size=7.5, fill='#475569', text_anchor='middle'))
    w(I + path('M210,240 L228,240 L228,439 L540,439', fill='none', stroke=NET['gnd'], stroke_width=3))
    w(I + text(PX, 380, 455, 'battery return', font_size=9, fill='#374151', text_anchor='middle'))
    w(I + comment('the two switch LED returns, joined, into the (−) bus'))
    w(I + path('M740,232 L740,439 L620,439', fill='none', stroke=NET['gnd'], stroke_width=2.5))
    w(I + text(PX, 748, 278, 'LED returns', font_size=7.5, fill='#374151'))
    w('')
    w(I + comment('fuse rationale'))
    w(I + text(PX, 252, 262, 'Why the main fuse comes first:', font_size=8.5, font_weight=600, fill='#7f1d1d'))
    w(I + text(PX, 252, 277, 'it protects the battery-to-bus cable, which', font_size=8.5, fill='#555'))
    w(I + text(PX, 252, 290, 'sits upstream of every other fuse and so', font_size=8.5, fill='#555'))
    w(I + text(PX, 252, 303, 'cannot be protected by any of them. It also', font_size=8.5, fill='#555'))
    w(I + text(PX, 252, 316, 'covers the short bus → SW1 → split run.', font_size=8.5, fill='#555'))
    w(I + text(PX, 252, 335, '7.5 A main · 5 A on each power-train load = 1.5×', font_size=8.5, fill='#555'))
    w(I + text(PX, 252, 348, '3 inline fuses · 2 spare holders (HW-20).', font_size=8.5, fill='#555'))
    w('')
    return o


def tag(x, y, w_, h, name, sub, stroke, fill, ink):
    """A small carrier-board tag sitting on a wire: the board's name and what it does."""
    return (rect(PX, x, y, w_, h, fill=fill, stroke=stroke, stroke_width=1.4, rx=3)
            + text(PX, x + w_ / 2, y + 14, name, font_size=8.5, font_weight=700, fill=ink, text_anchor='middle')
            + text(PX, x + w_ / 2, y + 26, sub, font_size=6.5, fill=ink, text_anchor='middle'))


def led(x, y, colour, label):
    """A switch LED: its (+) comes from the switched side, its (−) goes to the (−) bus."""
    return (rect(PX, x, y, 44, 26, fill='#ffffff', stroke=colour, stroke_width=1.6, rx=13)
            + text(PX, x + 22, y + 12, 'LED', font_size=8.5, font_weight=700, fill=colour, text_anchor='middle')
            + text(PX, x + 22, y + 22, label, font_size=6.5, fill=colour, text_anchor='middle'))


def power_train_lane():
    """SW1 to the 5 A fuses, the Encoder Motor Module with the rear motors, and the UBEC through carrier board A to the servo."""
    o = []
    w = o.append
    w(I + comment('===== POWER TRAIN LANE ====='))
    w(I + rect(PX, 760, 146, 100, 44, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.8, rx=6))
    w(I + text(PX, 810, 162, 'SW1', font_size=10, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + text(PX, 810, 175, 'POWER TRAIN', font_size=8.5, fill='#991b1b', text_anchor='middle'))
    w(I + text(PX, 810, 186, 'red LED', font_size=7.5, fill='#b91c1c', text_anchor='middle'))
    w(I + text(PX, 810, 203, '22 mm · 20 A · latching', font_size=7.5, fill='#64748b', text_anchor='middle'))
    w('')
    w(I + line(PX, 860, 168, 894, 168, stroke=NET['switched'], stroke_width=3))
    w(I + circle(PX, 880, 168, 3.2, fill='#e8821a'))
    w(I + line(PX, 880, 168, 880, 238, stroke=NET['switched'], stroke_width=3))
    w(I + line(PX, 880, 238, 894, 238, stroke=NET['switched'], stroke_width=3))
    w('')
    w(I + comment('SW1 LED: (+) from the switched side, so it lights only when SW1 is on; (−) joins SW2 LED on the way to the (−) bus'))
    w(I + line(PX, 880, 232, 834, 232, stroke=NET['switched'], stroke_width=2))
    w(I + circle(PX, 880, 232, 2.8, fill='#e8821a'))
    w(I + line(PX, 790, 232, 740, 232, stroke=NET['gnd'], stroke_width=2))
    w(I + led(790, 219, '#b91c1c', 'red'))
    w(I + text(PX, 812, 258, 'lit only when SW1 is on', font_size=7, fill='#991b1b', text_anchor='middle'))
    w('')
    w(I + rect(PX, 894, 161, 28, 14, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.2, rx=2))
    w(I + text(PX, 908, 171, '5 A', font_size=7, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + line(PX, 922, 168, 950, 168, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 950, 138, 170, 60, fill='#faf5ff', stroke='#9333ea', stroke_width=1.6, rx=3))
    w(I + text(PX, 1035, 155, 'Encoder Motor Module', font_size=10, font_weight=700, fill='#6b21a8', text_anchor='middle'))
    w(I + text(PX, 1035, 168, 'Hiwonder V1.4 · 12 V in', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 1035, 180, 'I²C slave · no servo output', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 1035, 208, '⚠ VM in: 2-pin 2.5 mm, ~3 A - needs an adapter', font_size=7, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + text(PX, 1035, 192, '⏚ to (−) bus', font_size=8, fill='#7e22ce', text_anchor='middle'))
    w(I + line(PX, 1120, 168, 1175, 168, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 1175, 143, 120, 50, fill='#ede9fe', stroke='#6d28d9', stroke_width=1.4, rx=2))
    w(I + text(PX, 1235, 161, '2 × REAR MOTOR', font_size=10, font_weight=700, fill='#4c1d95', text_anchor='middle'))
    w(I + text(PX, 1235, 175, '12 V · 8.3 W · 2.3 A stall', font_size=8.5, fill='#5b21b6', text_anchor='middle'))
    w(I + text(PX, 1235, 187, 'encoder AB → module', font_size=8, fill='#5b21b6', text_anchor='middle'))
    w('')
    w(I + line(PX, 880, 238, 894, 238, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 894, 231, 28, 14, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.2, rx=2))
    w(I + text(PX, 908, 241, '5 A', font_size=7, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + line(PX, 922, 238, 950, 238, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 950, 213, 150, 50, fill='#ccfbf1', stroke='#0f766e', stroke_width=1.6, rx=2))
    w(I + text(PX, 1025, 231, 'ZHITING UBEC', font_size=10, font_weight=700, fill='#134e4a', text_anchor='middle'))
    w(I + text(PX, 1025, 245, '3S → 6.0 V · 3 A / 5 A pk', font_size=9, fill='#115e59', text_anchor='middle'))
    w(I + text(PX, 1025, 257, 'jumper on 6 V · rev-pol protected', font_size=7.5, fill='#0f766e', text_anchor='middle'))
    w(I + comment('the servo is fed through carrier board A: 6V IN terminal, C2 470 uF, servo header (plate 2 top face)'))
    w(I + line(PX, 1100, 238, 1175, 238, stroke=NET['v6'], stroke_width=3))
    w(I + tag(1112, 222, 48, 34, 'BOARD A', '6V IN · C2', '#0f766e', '#f0fdfa', '#134e4a'))
    w(I + rect(PX, 1175, 213, 120, 50, fill='#ede9fe', stroke='#6d28d9', stroke_width=1.4, rx=2))
    w(I + text(PX, 1235, 231, 'STEERING SERVO', font_size=10, font_weight=700, fill='#4c1d95', text_anchor='middle'))
    w(I + text(PX, 1235, 245, 'LD-1501MG · 6–8.4 V', font_size=9, fill='#5b21b6', text_anchor='middle'))
    w(I + text(PX, 1235, 257, 'PWM via carrier A · ⏚', font_size=7.5, fill='#5b21b6', text_anchor='middle'))
    w('')
    return o


def logic_lane():
    """SW2 to the Bauer 50 W, board C (the 5 V split), then the FRDM (USB-C) and the STM32 (through carrier B)."""
    o = []
    w = o.append
    w(I + comment('===== LOGIC LANE ====='))
    w(I + rect(PX, 760, 308, 100, 44, fill='#dcfce7', stroke='#15803d', stroke_width=1.8, rx=6))
    w(I + text(PX, 810, 324, 'SW2', font_size=10, font_weight=700, fill='#14532d', text_anchor='middle'))
    w(I + text(PX, 810, 337, 'LOGIC', font_size=8.5, fill='#166534', text_anchor='middle'))
    w(I + text(PX, 810, 348, 'green LED', font_size=7.5, fill='#15803d', text_anchor='middle'))
    w(I + text(PX, 810, 365, '22 mm · same part, green', font_size=7.5, fill='#64748b', text_anchor='middle'))
    w('')
    w(I + line(PX, 860, 330, 950, 330, stroke=NET['switched'], stroke_width=3))
    w(I + comment('SW2 LED: (+) from the switched side, (−) joins SW1 LED'))
    w(I + circle(PX, 900, 330, 2.8, fill='#e8821a'))
    w(I + path('M900,330 L900,391 L834,391', fill='none', stroke=NET['switched'], stroke_width=2))
    w(I + line(PX, 790, 391, 740, 391, stroke=NET['gnd'], stroke_width=2))
    w(I + circle(PX, 740, 391, 2.8, fill='#111827'))
    w(I + led(790, 378, '#15803d', 'green'))
    w(I + text(PX, 812, 418, 'lit only when SW2 is on', font_size=7, fill='#166534', text_anchor='middle'))
    w('')
    w(I + rect(PX, 950, 305, 150, 50, fill='#fef3c7', stroke='#b45309', stroke_width=1.6, rx=2))
    w(I + text(PX, 1025, 323, 'Bauer 50 W', font_size=10, font_weight=700, fill='#7c2d12', text_anchor='middle'))
    w(I + text(PX, 1025, 337, '12 V → 5 V · 10 A', font_size=9, fill='#92400e', text_anchor='middle'))
    w(I + text(PX, 1025, 349, '470–1000 µF · both boards', font_size=7.5, fill='#a16207', text_anchor='middle'))
    w(I + comment('board C: IN 5V, C1 470 uF, the USB-C socket; TO STM32 goes to carrier B'))
    w(I + line(PX, 1100, 330, 1175, 330, stroke=NET['v5'], stroke_width=3))
    w(I + tag(1112, 314, 48, 34, 'BOARD C', '5 V split', '#15803d', '#f0fdf4', '#14532d'))
    w(I + circle(PX, 1167, 330, 3.2, fill='#15803d'))
    w(I + path('M1167,330 L1167,400 L1175,400', fill='none', stroke=NET['v5'], stroke_width=3))
    w(I + text(PX, 1135, 366, 'USB-C → J1', font_size=7, fill='#15803d', text_anchor='middle'))
    w(I + text(PX, 1135, 412, 'TO STM32', font_size=7, fill='#15803d', text_anchor='middle'))
    w(I + rect(PX, 1175, 305, 120, 50, fill='#dbeafe', stroke='#1d4ed8', stroke_width=1.6, rx=2))
    w(I + text(PX, 1235, 323, 'FRDM-IMX91S', font_size=10, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 1235, 337, 'J1 USB-C · no CC used', font_size=8.5, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 1235, 349, 'dumb 5 V, no PD', font_size=8, fill='#3b5bb5', text_anchor='middle'))
    w('')
    w(I + rect(PX, 1175, 375, 120, 50, fill='#dcfce7', stroke='#15803d', stroke_width=1.6, rx=2))
    w(I + text(PX, 1235, 393, 'NUCLEO-H533RE', font_size=10, font_weight=700, fill='#14532d', text_anchor='middle'))
    w(I + text(PX, 1235, 407, '5 V via carrier B to E5V', font_size=8.5, fill='#166534', text_anchor='middle'))
    w(I + text(PX, 1235, 419, '⏚ back through board C', font_size=8, fill='#3f7d52', text_anchor='middle'))
    w('')
    return o


def carrier(x, y, w_, h, title, sub, lines, stroke, fill, ink):
    """One carrier board: a box with its name, where it sits and what is on it."""
    o = rect(PX, x, y, w_, h, fill=fill, stroke=stroke, stroke_width=1.8, rx=3)
    o += text(PX, x + w_ / 2, y + 17, title, font_size=10.5, font_weight=700, fill=ink, text_anchor='middle')
    o += text(PX, x + w_ / 2, y + 30, sub, font_size=8, fill=stroke, text_anchor='middle')
    for i, ln in enumerate(lines):
        o += text(PX, x + 8, y + 48 + 14 * i, ln, font_size=8.2, fill=ink)
    return o


def signals():
    """SIGNALS: INA226 and the motor module on carrier A, the Nucleo on carriers A and B, CAN from B to the FRDM, the debug port."""
    o = []
    w = o.append
    w(I + comment('===================== SIGNALS ====================='))
    w(I + text(PX, 40, 500, 'SIGNALS · CARRIER BOARDS', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(I + line(PX, 40, 508, 1280, 508, stroke='#e2e8f0'))
    w('')
    w(I + comment('INA226 and the motor module reach the STM32 through carrier A'))
    w(I + rect(PX, 40, 540, 160, 66, fill='#cffafe', stroke='#0e7490', stroke_width=1.6, rx=3))
    w(I + text(PX, 120, 562, 'INA226', font_size=11, font_weight=700, fill='#164e63', text_anchor='middle'))
    w(I + text(PX, 120, 578, 'pack V + I', font_size=9, fill='#155e75', text_anchor='middle'))
    w(I + text(PX, 120, 594, 'ALERT → bus under-volt', font_size=8.5, fill='#155e75', text_anchor='middle'))
    w(I + path('M200,573 L225,573 L225,655 L250,655', fill='none', stroke=NET['i2c'], stroke_width=2.5, marker_end='url(#a)'))
    w(I + text(PX, 212, 566, 'I²C1', font_size=8.5, font_weight=600, fill='#5b21b6', text_anchor='middle'))
    w(I + rect(PX, 40, 640, 160, 112, fill='#faf5ff', stroke='#9333ea', stroke_width=1.6, rx=3))
    w(I + text(PX, 120, 659, 'Encoder Motor Module', font_size=9.5, font_weight=700, fill='#6b21a8', text_anchor='middle'))
    w(I + text(PX, 120, 673, 'V1.4 · MM32F103', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 120, 687, 'owns PWM + encoder counting', font_size=8, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 120, 700, 'M1 + M3, both on the rear edge', font_size=8, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 120, 719, 'IIC 5 V is an OUTPUT:', font_size=8, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + text(PX, 120, 731, 'wire SCL / SDA / GND only', font_size=8, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + path('M200,696 L225,696 L225,675 L250,675', fill='none', stroke=NET['i2c'], stroke_width=2.5, marker_end='url(#a)'))
    w(I + text(PX, 212, 714, 'I²C', font_size=8.5, font_weight=600, fill='#5b21b6', text_anchor='middle'))
    w('')
    w(I + comment('the Nucleo plugs onto carrier A (under CN10) and carrier B (under CN7); both sit on the carrier tray on plate 2'))
    w(I + rect(PX, 250, 520, 350, 62, fill='#dcfce7', stroke='#15803d', stroke_width=1.8, rx=3))
    w(I + text(PX, 425, 540, 'NUCLEO-H533RE · STM32H533RE', font_size=11, font_weight=700, fill='#14532d', text_anchor='middle'))
    w(I + text(PX, 425, 556, 'real-time + BMS · FDCAN2: PB12 RX · PB13 TX · I²C1 PB6 SCL / PB7 SDA · PA15 PWM', font_size=8, fill='#166534', text_anchor='middle'))
    w(I + text(PX, 425, 571, 'ST-LINK V3EC with VCP · 5 V in on E5V, JP5 [5-6] · AFs per DS14539 Rev 3', font_size=8, fill='#3f7d52', text_anchor='middle'))
    w(I + line(PX, 335, 582, 335, 612, stroke='#94a3b8', stroke_width=5, marker_end='url(#a)'))
    w(I + line(PX, 515, 582, 515, 612, stroke='#94a3b8', stroke_width=5, marker_end='url(#a)'))
    w(I + text(PX, 425, 603, 'plugs into the 1×19 sockets', font_size=8, fill='#64748b', text_anchor='middle'))
    w(I + carrier(250, 612, 170, 140, 'CARRIER A', 'under CN10 · plate 2', [
        'SN65HVD230 module in a socket',
        '   (TX / RX = PB13 / PB12, 3.3 V)',
        'CAN terminal, 3-pin',
        'I²C headers under A: INA226,',
        '   motor module, 90° pointing fwd'], '#0f766e', '#f0fdfa', '#134e4a'))
    w(I + carrier(430, 612, 170, 140, 'CARRIER B', 'under CN7 · plate 2', [
        '5V IN terminal ← board C',
        '6V IN terminal ← UBEC',
        'C2 470 µF across the servo header',
        'servo header: 6 V, GND, PWM',
        '   via R4 1 kΩ from PA15'], '#1d4ed8', '#eff6ff', '#1e3a8a'))
    w('')
    w(I + comment('CAN: carrier A terminal to the FRDM J7, under carrier B; the debug port is a stub off the middle of the bus (HW-18)'))
    w(I + path('M335,752 L335,768 L615,768 L615,690 L1000,690', fill='none', stroke=NET['can'], stroke_width=3))
    w(I + text(PX, 800, 682, 'CAN BUS - H · L · GND', font_size=9, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 800, 666, 'twisted pair · 120 Ω at each end, nowhere else', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w(I + rect(PX, 1000, 640, 280, 100, fill='#dbeafe', stroke='#1d4ed8', stroke_width=1.8, rx=3))
    w(I + text(PX, 1140, 662, 'FRDM-IMX91S', font_size=11, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 1140, 679, 'J7 2×5 header: pin 8 CAN_H · 10 CAN_L · 6 GND', font_size=8.5, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 1140, 694, 'on-board TJA1051T/3, split termination + JP1', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w(I + text(PX, 1140, 709, 'read JP1 and the resistors before adding a 120 Ω', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w(I + text(PX, 1140, 724, 'J7 pins 7 / 9: I²C1 SCL / SDA · J1: 5 V in (board C)', font_size=8, fill='#3b5bb5', text_anchor='middle'))
    w(I + circle(PX, 800, 690, 3.4, fill='#1d4ed8'))
    w(I + line(PX, 800, 690, 800, 712, stroke=NET['can'], stroke_width=2.5))
    w(I + rect(PX, 705, 712, 190, 62, fill='#eff6ff', stroke='#1d4ed8', stroke_width=1.6, stroke_dasharray='5,3', rx=3))
    w(I + text(PX, 800, 728, 'CAN DEBUG PORT - DE-9 male', font_size=10, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 800, 741, 'pin 2 CAN_L · 3 GND · 7 CAN_H', font_size=8, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 800, 753, 'to the PC USB-CAN adapter, F-F cable · a stub', font_size=8, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 800, 766, 'adapter 120 Ω must be OFF', font_size=8, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + text(PX, 1000, 760, 'electronic differential across the two rear wheels is firmware;', font_size=8.5, fill='#6b7280'))
    w(I + text(PX, 1000, 773, 'the axle is not a diff. The motor-module I²C shares the INA226 bus.', font_size=8.5, fill='#6b7280'))
    w('')
    return o


def legend():
    """Wire key and the build-order notes."""
    o = []
    w = o.append
    w(I + comment('===================== LEGEND ====================='))
    w(I + line(PX, 40, 786, 1280, 786, stroke='#e2e8f0'))
    w(I + text(PX, 40, 812, 'Wire key', font_size=11, font_weight=700, fill='#1a1a1a'))
    for x, y, net, label in WIRE_KEY:
        w(I + line(PX, x, y, x + 40, y, stroke=NET[net], stroke_width=3) + text(PX, x + 46, y + 4, label, font_size=9.5, fill='#333'))
    w(I + text(PX, 560, 838, 'Build order: verify 5 V on a meter → fuse → battery last.', font_size=9.5, fill='#b91c1c'))
    w(I + text(PX, 560, 856, 'Unknowns: SM-2P connector temperature under load · FRDM loaded current · servo stall current.', font_size=9.5, fill='#666'))
    w(I + text(PX, 560, 874, 'Switches: same 22 mm part, red = power train, green = logic. Each LED is wired from the switched side, so it lights only when its switch is on. Relay deferred (HW-12).', font_size=9.5, fill='#666'))
    return o

def build():
    o = []
    o += header()
    o += power_sources()
    o += power_train_lane()
    o += logic_lane()
    o += signals()
    o += legend()
    o.append('</svg>')
    return o


if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else OUT, build())
