#!/usr/bin/env python3
"""The physical architecture drawing (L2 of ../method.md): every physical element of the vehicle, what it is made of, its phase and the connections between them.

    python3 Nexus-Platform-Physical-Architecture.py   # -> ../renders/Nexus-Platform-Physical-Architecture.svg
    python3 ../../tools/check-drawings.py             # fails if the SVG is not what this script writes

This is the physical view of the vehicle's architecture; the logical view is the logical architecture drawing, and the two are related by
allocation (../physical-architecture.md), never on this drawing. Every element has its own Nexus-Physical-NN ID. The parts listed on a card name their BOM item; the BOM owns the parts, the decisions own the wiring. The pill is the first phase
the element exists in. The helpers (pill, external, flow) are the logical architecture's, loaded from its script so the two
drawings look alike. Everything is in pixels; there is no scale. Edit this script, never the SVG.
"""
import importlib.util, os, sys
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('logical', os.path.join(HERE, 'Nexus-Platform-Logical-Architecture.py'))
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)
esc, pill, external, flow, write = L.esc, L.pill, L.external, L.flow, L.write
MONO, PHASES, PILL_W, MARKERS = L.MONO, L.PHASES, L.PILL_W, L.MARKERS

OUT = os.path.join(HERE, '..', 'renders', 'Nexus-Platform-Physical-Architecture.svg')
W, H = 1640, 1010
SLATE = ('#334155', '#e2e8f0')


def element(eid, name, phase, x, y, w, h, *columns):
    """An element card: ID, name, first phase, and the parts it is built from."""
    stroke, head = SLATE
    o = [f'<g id="{eid}">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#ffffff" stroke="{stroke}" stroke-width="1.6"/>',
         f'<path d="M{x},{y + 4} a4,4 0 0 1 4,-4 h{w - 8} a4,4 0 0 1 4,4 v38 h-{w} z" fill="{head}"/>',
         f'<line x1="{x}" y1="{y + 42}" x2="{x + w}" y2="{y + 42}" stroke="{stroke}" stroke-width="0.8"/>',
         f'<text x="{x + 12}" y="{y + 16}" font-size="9.5" font-weight="700" fill="{stroke}" font-family="{MONO}">{eid}</text>',
         f'<text x="{x + 12}" y="{y + 34}" font-size="13" font-weight="700" fill="#111827">{esc(name)}</text>',]
    o += pill(x + w - 10 - PILL_W, y + 7, phase)
    for ci, col in enumerate(columns):
        bx = float(x + 16 + 300 * ci)
        row = y + 58.5
        for line in col:
            o.append(f'<circle cx="{bx}" cy="{row}" r="1.8" fill="{stroke}"/>')
            o.append(f'<text x="{bx + 7}" y="{int(row + 3.5)}" font-size="10.5" fill="#374151">{esc(line)}</text>')
            row += 16
    o.append('</g>')
    return o


def build():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">', '<defs>']
    for mid, c in MARKERS:
        o.append(f'<marker id="{mid}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">'
                 f'<path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>')
        o.append(f'<marker id="{mid}s" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto" markerUnits="userSpaceOnUse">'
                 f'<path d="M8,0 L0,4 L8,8 z" fill="{c}"/></marker>')
    o += ['</defs>', f'<rect width="{W}" height="{H}" fill="#fbfaf8"/>',
          '<text x="30" y="40" font-size="22" font-weight="700" fill="#1a1a1a">Nexus Platform Physical Architecture</text>',
          '<text x="30" y="62" font-size="11.5" fill="#555">Physical view of the vehicle architecture · the system elements and the connections between them · '
          'says <tspan font-style="italic">what it is built from</tspan>; the logical view says what it does, and allocation relates the two</text>',
          f'<text x="30" y="80" font-size="11.5" fill="#555">ID scheme <tspan font-family="{MONO}" font-weight="700">Nexus-Physical-NN</tspan>'
          f' - one number per element, never reused. Numbers in brackets are BOM items.</text>',
          '<text x="1610" y="40" font-size="11" font-weight="700" fill="#b45309" text-anchor="end">DRAFT B · for review</text>',
          '<text x="1610" y="58" font-size="10" fill="#777" text-anchor="end">2026-10-11</text>',
          '<g transform="translate(0,14)">']

    o += external(30, 118, 170, 90, 'Remote station', 'laptop over Wi-Fi')
    o += external(30, 300, 170, 230, 'PC + USB-CAN adapter', 'bench and debug (BOM 4.7)')
    o += external(30, 590, 170, 90, 'Operator', 'at the rear fascia')
    o += external(30, 760, 170, 80, 'Charger', 'off-board (BOM 3.2)')
    o += external(1440, 118, 170, 532, 'Environment', 'floor · obstacles · light')
    o += ['<rect x="232" y="94" width="1146" height="770" rx="8" fill="none" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2 3"/>',
          '<text x="240" y="108" font-size="9" font-weight="700" fill="#9ca3af" letter-spacing="1">NEXUS VEHICLE - SYSTEM BOUNDARY</text>']

    # --- row 1: compute above the bus, the perception sensors by the environment
    o += element('Nexus-Physical-02', 'FRDM node: Linux compute', 1, 250, 118, 330, 160, [
        'FRDM-IMX91S (1.1)', 'On-board CAN transceiver, 2×5 header P12', 'microSD card, boot media (5.3)',
        'Wi-Fi on board', 'UART console, USB-C J11'])
    o += element('Nexus-Physical-03', 'Raspberry Pi 5 node', 4, 700, 118, 330, 160, [
        'Raspberry Pi 5, 8 GB (6.1)', 'CAN hardware (6.2, later)', 'Power, mounting, network: to decide'])
    o += element('Nexus-Physical-09', 'Perception sensors', 4, 1120, 118, 240, 160, [
        'Camera first', 'Then a range sensor or LiDAR', 'To be selected (6.3)'])

    # --- the bus: a banner, as in the logical drawing
    stroke, head = SLATE
    o += ['<g id="Nexus-Physical-04">',
          f'<rect x="250" y="330" width="1110" height="70" rx="4" fill="#f8fafc" stroke="{stroke}" stroke-width="1.6"/>',
          f'<text x="262" y="348" font-size="9.5" font-weight="700" fill="{stroke}" font-family="{MONO}">Nexus-Physical-04</text>',
          '<text x="262" y="368" font-size="13" font-weight="700" fill="#111827">Vehicle CAN bus</text>',]
    for (cx, cy, t) in [(440, 359.5, 'Classic CAN, 500 kbit/s'), (440, 376.5, '120 Ω at both ends (module, FRDM JP1)'),
                        (730, 359.5, 'Twisted pair H / L and GND, about 30 cm (4.3)'),
                        (730, 376.5, 'DE-9 stub on the fascia, unterminated (4.5)')]:
        o += [f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{stroke}"/>',
              f'<text x="{cx + 7}" y="{int(cy + 3.5)}" font-size="10.5" fill="#374151">{esc(t)}</text>']
    o += pill(1308, 337, 1)
    o.append('</g>')

    # --- row 2: the real-time node and the actuators it will command
    o += element('Nexus-Physical-01', 'STM32 node: real-time control', 1, 250, 450, 420, 200, [
        'STM32F4DISCOVERY, MB997B (1.2)', 'Carrier boards A and B (5.11)', 'SN65HVD230 CAN transceiver (4.1)',
        'Four user LEDs', 'ST-LINK/V2 on board, SWD', 'I²C PB10 / PB11 · servo PWM PE9'])
    o += element('Nexus-Physical-08', 'Steering actuator', 1, 1120, 450, 240, 95, [
        'LD-1501MG servo (2.3)', 'Ackermann linkage (2.1)'])
    o += element('Nexus-Physical-07', 'Rear drive', 1, 1120, 560, 240, 90, [
        'Two encoder gear motors, 12 V (2.2)', 'Encoder Motor Module V1.4 (2.4)'])

    # --- row 3: energy and structure
    o += element('Nexus-Physical-05', 'Power supply and distribution', 1, 250, 700, 600, 140, [
        '3S LiPo, 11.1 V, 6000 mAh (3.1)', 'Fuses: 7.5 A main, 2 × 5 A (3.7)', 'SW1 DRIVE, SW2 LOGIC (3.5a, 3.5c)',
        'WAGO (+) and (−) buses (3.8)'], [
        'Shunt 2 mΩ and INA226 (3.9)', '5 V converter, 50 W (3.4a), board C', '6 V UBEC for the servo (3.18)'])
    o += element('Nexus-Physical-06', 'Chassis and enclosure', 1, 900, 700, 460, 140, [
        'Hiwonder three-deck chassis (2.1)', 'Printed trays and pads (3.28)', 'Harness board, plate 2 (MEC-16)',
        'Rear fascia, two panels (3.29)'])
    o.append('<text x="1344" y="828" font-size="9" font-style="italic" fill="#334155" text-anchor="end">carries and locates every element</text>')

    FL = flow
    # energy
    o += FL('M400,700 L400,652', 'e', anchor='start', size=8, labels=[(406, 682, '5 V (board C) · 6 V servo (UBEC)')])
    o += FL('M690,700 L690,300 L560,300 L560,280', 'e', size=8, anchor='start', labels=[(696, 430, '5 V, USB-C')])
    o += FL('M820,700 L820,635 L1118,635', 'e', size=8, labels=[(990, 628, 'pack voltage, SW1, 5 A')])
    o += FL('M200,800 L248,800', 'e', size=8, labels=[(224, 792, 'charge')])
    # bus attachments
    o += FL('M420,280 L420,328', 'i', start=True, size=8, anchor='start', labels=[(426, 310, 'CAN · P12')])
    o += FL('M420,402 L420,448', 'i', start=True, size=8, anchor='start', labels=[(426, 430, 'CAN1 PD0 / PD1')])
    o += FL('M865,280 L865,328', 'i', start=True, dashed=True, size=8, anchor='start', labels=[(871, 310, 'CAN (later)')])
    o += FL('M200,365 L248,365', 'i', start=True, size=8, labels=[(224, 357, 'DE-9')])
    # signals and commands
    o += FL('M600,700 L600,652', 'i', size=8, anchor='start', labels=[(606, 682, 'I²C: pack V, I')])
    o += FL('M672,497 L1118,497', 'c', size=8, labels=[(895, 489, 'servo lead: 6 V + PWM PE9 (via R4)')])
    o += FL('M672,605 L1118,605', 'c', start=True, size=8, labels=[(895, 597, 'I²C PB10 / PB11: speed, encoders')])
    o += FL('M1118,200 L1032,200', 'i', size=8, labels=[(1075, 192, 'images, ranges')])
    # debug and remote
    o += FL('M200,320 L225,320 L225,250 L248,250', 'i', start=True, size=8, anchor='end', labels=[(221, 290, 'console')])
    o += FL('M200,500 L248,500', 'i', start=True, size=8, labels=[(224, 492, 'SWD')])
    o += FL('M200,160 L248,160', 'i', start=True, dashed=True, size=8, labels=[(224, 152, 'Wi-Fi')])
    o += FL('M200,640 L225,640 L225,720 L248,720', 'p', size=8, anchor='start', labels=[(206, 632, 'SW1, SW2')])
    # physical interaction with the environment
    o += FL('M1438,200 L1362,200', 'p', size=8, labels=[(1400, 192, 'light, range')])
    o += FL('M1362,497 L1438,497', 'p', size=8, labels=[(1400, 489, 'wheel angle')])
    o += FL('M1362,605 L1438,605', 'p', size=8, labels=[(1400, 597, 'traction')])

    # --- key
    o += ['<line x1="30" y1="902" x2="1610" y2="902" stroke="#e5e7eb"/>',
          '<text x="30" y="924" font-size="10" font-weight="700" fill="#1a1a1a">CONNECTIONS</text>']
    for x, kind, text in [(120, 'e', 'energy'), (230, 'i', 'signal / data (dashed = later)'), (470, 'c', 'command'),
                          (600, 'p', 'physical interaction')]:
        o += flow(f'M{x},920 L{x + 34},920', kind)
        o.append(f'<text x="{x + 42}" y="924" font-size="10" fill="#374151">{text}</text>')
    o.append('<text x="30" y="950" font-size="10" font-weight="700" fill="#1a1a1a">FIRST PHASE</text>')
    x = 108
    for p in PHASES:
        o += pill(x, 939, p)
        x += PILL_W + 6
    o.append(f'<text x="{x + 2}" y="950" font-size="10" fill="#374151">first phase the element exists in (phases.md) · which functions each element realises is the allocation, kept out of this view</text>')
    o += ['</g>', '</svg>']
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else OUT, build())
