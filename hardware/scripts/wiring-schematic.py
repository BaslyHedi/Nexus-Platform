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
    (360, 834, 'pwm', 'servo PWM'),
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
    w(I + text(PX, 40, 52, 'Rear-wheel drive Ackermann · 2 drive motors + 1 steering servo · every load returns to the (−) WAGO bus · all fuses inline · all harness wire 18 AWG', font_size=11, fill='#666'))
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
    w(I + text(PX, 440, 177, 'SHUNT R002', font_size=10, font_weight=700, fill='#164e63', text_anchor='middle'))
    w(I + text(PX, 440, 191, '2 mΩ · high-side', font_size=8.5, fill='#155e75', text_anchor='middle'))
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
    w(I + line(PX, 626, 168, 760, 168, stroke=NET['pack'], stroke_width=3))
    w(I + line(PX, 626, 330, 760, 330, stroke=NET['pack'], stroke_width=3))
    w(I + text(PX, 693, 321, 'no fuse - main covers it (HW-20)', font_size=7.5, fill='#991b1b', text_anchor='middle'))
    w('')
    w(I + comment('(−) bus bar and battery return'))
    w(I + rect(PX, 540, 430, 80, 18, fill='#374151', stroke='#111827', stroke_width=1.6, rx=3))
    w(I + circle(PX, 552, 439, 2.5, fill='#e5e7eb') + circle(PX, 566, 439, 2.5, fill='#e5e7eb') + circle(PX, 580, 439, 2.5, fill='#e5e7eb') + circle(PX, 594, 439, 2.5, fill='#e5e7eb') + circle(PX, 608, 439, 2.5, fill='#e5e7eb'))
    w(I + text(PX, 630, 466, '(−) WAGO BUS - 1 × 221-415 · star ground', font_size=9, font_weight=700, fill='#111827', text_anchor='middle'))
    w(I + text(PX, 630, 479, '5 of 5: battery, motor module, UBEC, Bauer, switch LEDs joined at the switches (MEC-16)', font_size=7.5, fill='#475569', text_anchor='middle'))
    w(I + path('M210,240 L228,240 L228,439 L540,439', fill='none', stroke=NET['gnd'], stroke_width=3))
    w(I + text(PX, 380, 455, 'battery return', font_size=9, fill='#374151', text_anchor='middle'))
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


def power_train_lane():
    """SW1 to the 5 A fuses, the Encoder Motor Module with the rear motors, and the UBEC with the servo."""
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
    w(I + rect(PX, 894, 161, 28, 14, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.2, rx=2))
    w(I + text(PX, 908, 171, '5 A', font_size=7, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + line(PX, 922, 168, 950, 168, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 950, 138, 170, 60, fill='#faf5ff', stroke='#9333ea', stroke_width=1.6, rx=3))
    w(I + text(PX, 1035, 155, 'Encoder Motor Module', font_size=10, font_weight=700, fill='#6b21a8', text_anchor='middle'))
    w(I + text(PX, 1035, 168, 'Hiwonder V1.4 · 12 V in', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 1035, 180, 'I²C slave · no servo output', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 1035, 208, '⚠ VM in: 2-pin 2.5 mm, ~3 A - needs an adapter', font_size=7, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w(I + text(PX, 1035, 192, '⏚ to (−) bus', font_size=8, fill='#7e22ce', text_anchor='middle'))
    w(I + line(PX, 1120, 168, 1160, 168, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 1160, 143, 135, 50, fill='#ede9fe', stroke='#6d28d9', stroke_width=1.4, rx=2))
    w(I + text(PX, 1227, 161, '2 × REAR MOTOR', font_size=10, font_weight=700, fill='#4c1d95', text_anchor='middle'))
    w(I + text(PX, 1227, 175, '12 V · 8.3 W · 2.3 A stall', font_size=8.5, fill='#5b21b6', text_anchor='middle'))
    w(I + text(PX, 1227, 187, 'encoder AB → module', font_size=8, fill='#5b21b6', text_anchor='middle'))
    w('')
    w(I + rect(PX, 894, 231, 28, 14, fill='#fee2e2', stroke='#b91c1c', stroke_width=1.2, rx=2))
    w(I + text(PX, 908, 241, '5 A', font_size=7, font_weight=700, fill='#7f1d1d', text_anchor='middle'))
    w(I + line(PX, 922, 238, 950, 238, stroke=NET['switched'], stroke_width=3))
    w(I + rect(PX, 950, 213, 170, 50, fill='#ccfbf1', stroke='#0f766e', stroke_width=1.6, rx=2))
    w(I + text(PX, 1035, 231, 'ZHITING UBEC', font_size=10, font_weight=700, fill='#134e4a', text_anchor='middle'))
    w(I + text(PX, 1035, 245, '3S → 6.0 V · 3 A / 5 A pk', font_size=9, fill='#115e59', text_anchor='middle'))
    w(I + text(PX, 1035, 257, 'jumper on 6 V · rev-pol protected', font_size=7.5, fill='#0f766e', text_anchor='middle'))
    w(I + line(PX, 1120, 238, 1160, 238, stroke=NET['v6'], stroke_width=3))
    w(I + text(PX, 1140, 231, '6 V', font_size=8, fill='#0f766e', text_anchor='middle'))
    w(I + rect(PX, 1160, 213, 135, 50, fill='#ede9fe', stroke='#6d28d9', stroke_width=1.4, rx=2))
    w(I + text(PX, 1227, 231, 'STEERING SERVO', font_size=10, font_weight=700, fill='#4c1d95', text_anchor='middle'))
    w(I + text(PX, 1227, 245, 'LD-1501MG · 6–8.4 V', font_size=9, fill='#5b21b6', text_anchor='middle'))
    w(I + text(PX, 1227, 257, 'PWM ← STM32 · ⏚ to bus', font_size=7.5, fill='#5b21b6', text_anchor='middle'))
    w('')
    return o


def logic_lane():
    """SW2 to the Bauer 50 W and on to the FRDM and the STM32."""
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
    w('')
    w(I + rect(PX, 950, 305, 170, 50, fill='#fef3c7', stroke='#b45309', stroke_width=1.6, rx=2))
    w(I + text(PX, 1035, 323, 'Bauer 50 W', font_size=10, font_weight=700, fill='#7c2d12', text_anchor='middle'))
    w(I + text(PX, 1035, 337, '12 V → 5 V · 10 A', font_size=9, fill='#92400e', text_anchor='middle'))
    w(I + text(PX, 1035, 349, '470–1000 µF · feeds both boards', font_size=7.5, fill='#a16207', text_anchor='middle'))
    w(I + line(PX, 1120, 330, 1160, 330, stroke=NET['v5'], stroke_width=3))
    w(I + circle(PX, 1145, 330, 3.2, fill='#15803d'))
    w(I + path('M1145,330 L1145,400 L1160,400', fill='none', stroke=NET['v5'], stroke_width=3))
    w(I + text(PX, 1132, 323, '5 V', font_size=8, fill='#15803d', text_anchor='middle'))
    w(I + text(PX, 1035, 368, '5 V split on board C (HW-19)', font_size=7.5, fill='#15803d', text_anchor='middle'))
    w(I + rect(PX, 1160, 305, 135, 50, fill='#dbeafe', stroke='#1d4ed8', stroke_width=1.6, rx=2))
    w(I + text(PX, 1227, 323, 'FRDM-IMX91S', font_size=10, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 1227, 337, 'J1 USB-C · 10 kΩ Rp', font_size=9, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 1227, 349, 'dumb 5 V, no PD', font_size=8, fill='#3b5bb5', text_anchor='middle'))
    w('')
    w(I + rect(PX, 1160, 375, 135, 50, fill='#dcfce7', stroke='#15803d', stroke_width=1.6, rx=2))
    w(I + text(PX, 1227, 393, 'STM32F4DISCOVERY', font_size=10, font_weight=700, fill='#14532d', text_anchor='middle'))
    w(I + text(PX, 1227, 407, 'MB997B · 5 V pin, P2', font_size=9, fill='#166534', text_anchor='middle'))
    w(I + text(PX, 1227, 419, '⏚ to (−) bus', font_size=8, fill='#3f7d52', text_anchor='middle'))
    w('')
    return o


def signals():
    """SIGNALS: INA226, STM32, CAN to the FRDM, the debug port, I2C to the motor module and PWM to the servo."""
    o = []
    w = o.append
    w(I + comment('===================== SIGNALS ====================='))
    w(I + text(PX, 40, 500, 'SIGNALS', font_size=13, font_weight=700, fill='#1a1a1a'))
    w(I + line(PX, 40, 508, 1280, 508, stroke='#e2e8f0'))
    w('')
    w(I + rect(PX, 60, 545, 170, 70, fill='#cffafe', stroke='#0e7490', stroke_width=1.6, rx=3))
    w(I + text(PX, 145, 568, 'INA226', font_size=11, font_weight=700, fill='#164e63', text_anchor='middle'))
    w(I + text(PX, 145, 584, 'pack V + I', font_size=9, fill='#155e75', text_anchor='middle'))
    w(I + text(PX, 145, 600, 'ALERT → bus under-volt', font_size=8.5, fill='#155e75', text_anchor='middle'))
    w(I + line(PX, 230, 580, 328, 580, stroke=NET['i2c'], stroke_width=2.5, marker_end='url(#a)'))
    w(I + text(PX, 280, 572, 'I²C2', font_size=9, font_weight=600, fill='#5b21b6', text_anchor='middle'))
    w(I + text(PX, 280, 596, 'PB10 SCL · PB11 SDA', font_size=8, fill='#6d28d9', text_anchor='middle'))
    w('')
    w(I + rect(PX, 330, 530, 210, 110, fill='#dcfce7', stroke='#15803d', stroke_width=1.8, rx=3))
    w(I + text(PX, 435, 555, 'STM32F407', font_size=11, font_weight=700, fill='#14532d', text_anchor='middle'))
    w(I + text(PX, 435, 571, 'real-time + BMS', font_size=9, fill='#166534', text_anchor='middle'))
    w(I + text(PX, 435, 589, 'CAN1 AF9: PD0 RX · PD1 TX', font_size=8.5, fill='#3f7d52', text_anchor='middle'))
    w(I + text(PX, 435, 604, 'PB9 = Audio_SDA - do not use', font_size=8.5, fill='#3f7d52', text_anchor='middle'))
    w(I + text(PX, 435, 622, 'SWD only, no VCP → USB-TTL', font_size=8.5, fill='#3f7d52', text_anchor='middle'))
    w('')
    w(I + line(PX, 540, 560, 620, 560, stroke=NET['can'], stroke_width=2.5))
    w(I + text(PX, 580, 552, 'TX/RX', font_size=8.5, fill='#1e3a8a', text_anchor='middle'))
    w(I + rect(PX, 620, 530, 160, 60, fill='#dbeafe', stroke='#1d4ed8', stroke_width=1.6, rx=3))
    w(I + text(PX, 700, 552, 'SN65HVD230', font_size=10, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 700, 567, '3.3 V transceiver', font_size=9, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 700, 580, '120 Ω on board - verify', font_size=8, fill='#3b5bb5', text_anchor='middle'))
    w(I + line(PX, 780, 560, 1000, 560, stroke=NET['can'], stroke_width=3))
    w(I + text(PX, 890, 524, 'twisted pair · 120 Ω at each end, nowhere else', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w(I + text(PX, 890, 551, 'CAN BUS - H · L · GND', font_size=9, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + rect(PX, 1000, 525, 260, 80, fill='#dbeafe', stroke='#1d4ed8', stroke_width=1.8, rx=3))
    w(I + text(PX, 1130, 548, 'FRDM-IMX91S', font_size=11, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 1130, 565, '2×5 connector - CAN_H / CAN_L', font_size=9, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 1130, 580, 'on-board transceiver ✓ · 2× ADC · I²C/I³C', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w(I + text(PX, 1130, 596, 'termination: check SW4 before adding 120 Ω', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w('')
    w(I + comment('CAN debug port: third node, stub off the middle of the bus (HW-18)'))
    w(I + circle(PX, 890, 560, 3.4, fill='#1d4ed8'))
    w(I + line(PX, 890, 560, 890, 616, stroke=NET['can'], stroke_width=2.5))
    w(I + rect(PX, 795, 616, 190, 64, fill='#eff6ff', stroke='#1d4ed8', stroke_width=1.6, stroke_dasharray='5,3', rx=3))
    w(I + text(PX, 890, 634, 'CAN DEBUG PORT - DE-9 male', font_size=10, font_weight=700, fill='#1e3a8a', text_anchor='middle'))
    w(I + text(PX, 890, 648, 'pin 2 CAN_L · 3 CAN_GND · 7 CAN_H', font_size=8.5, fill='#1e40af', text_anchor='middle'))
    w(I + text(PX, 890, 661, '→ PC USB-CAN adapter, F-F cable', font_size=8.5, fill='#3b5bb5', text_anchor='middle'))
    w(I + text(PX, 890, 674, 'stub · adapter 120 Ω must be OFF', font_size=8.5, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w('')
    w(I + comment('STM32 outputs: I2C to motor module, PWM to servo'))
    w(I + line(PX, 365, 640, 365, 688, stroke=NET['i2c'], stroke_width=2.5, marker_end='url(#a)'))
    w(I + text(PX, 372, 668, 'I²C', font_size=8, fill='#6d28d9'))
    w(I + rect(PX, 250, 690, 230, 74, fill='#faf5ff', stroke='#9333ea', stroke_width=1.6, rx=3))
    w(I + text(PX, 365, 710, 'Encoder Motor Module V1.4', font_size=10, font_weight=700, fill='#6b21a8', text_anchor='middle'))
    w(I + text(PX, 365, 725, 'MM32F103 owns PWM + encoder counting', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 365, 740, '4 ports M1–M4 · use <tspan font-weight="700">M1 + M3</tspan>, both on the rear edge', font_size=8.5, fill='#7e22ce', text_anchor='middle'))
    w(I + text(PX, 365, 755, 'IIC 5 V is an OUTPUT - wire SCL/SDA/GND only', font_size=8.5, font_weight=700, fill='#b91c1c', text_anchor='middle'))
    w('')
    w(I + path('M505,640 L505,670 L660,670 L660,688', fill='none', stroke=NET['pwm'], stroke_width=2.5, marker_end='url(#a)'))
    w(I + text(PX, 582, 664, 'PWM', font_size=8, fill='#78350f', text_anchor='middle'))
    w(I + rect(PX, 560, 690, 200, 60, fill='#ede9fe', stroke='#6d28d9', stroke_width=1.4, rx=3))
    w(I + text(PX, 660, 710, 'STEERING SERVO - signal', font_size=10, font_weight=700, fill='#4c1d95', text_anchor='middle'))
    w(I + text(PX, 660, 725, '500–2500 µs, direct from STM32', font_size=8.5, fill='#5b21b6', text_anchor='middle'))
    w(I + text(PX, 660, 740, '3.3 V logic - confirm on first power-up', font_size=8.5, fill='#5b21b6', text_anchor='middle'))
    w('')
    w(I + text(PX, 800, 705, 'electronic differential across the two rear wheels', font_size=8.5, fill='#6b7280'))
    w(I + text(PX, 800, 719, 'is done in STM32 firmware - the axle is not a diff', font_size=8.5, fill='#6b7280'))
    w(I + text(PX, 800, 733, 'motor-module I²C may share the INA226 bus (different addresses)', font_size=8.5, fill='#6b7280'))
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
    w(I + text(PX, 560, 874, 'Switches: same 22 mm part - red = power train, green = logic; label the deck. Relay deferred (HW-12).', font_size=9.5, fill='#666'))
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
