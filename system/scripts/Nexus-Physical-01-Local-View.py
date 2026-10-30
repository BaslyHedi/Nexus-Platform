#!/usr/bin/env python3
"""The local physical view of the STM32 node, Nexus-Physical-01 (../method.md: the node as a system-of-interest in turn).

    python3 Nexus-Physical-01-Local-View.py      # -> ../renders/Nexus-Physical-01-Local-View.svg
    python3 ../../tools/check-drawings.py        # fails if the SVG is not what this script writes

Every element of the node, hardware and software, with its hierarchical ID Nexus-Physical-01-NN, and the connections
between them and to the neighbouring elements outside the node (drawn dashed, with their own IDs). The element list
is owned here, as the vehicle's is by the physical architecture drawing; ../physical-architecture.md tabulates it and
the requirements are in ../../requirements/Nexus-Physical-01-NN.md. Helpers come from the physical architecture script.
Everything is in pixels; there is no scale. Edit this script, never the SVG.
"""
import importlib.util, os, sys
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('physical', os.path.join(HERE, 'Nexus-Platform-Physical-Architecture.py'))
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
element, external, flow, pill, esc, write = P.element, P.external, P.flow, P.pill, P.esc, P.write
MONO, MARKERS, system_colour = P.MONO, P.MARKERS, P.system_colour
NODE = 'Nexus-Physical-01'

OUT = os.path.join(HERE, '..', 'renders', 'Nexus-Physical-01-Local-View.svg')
W, H = 1640, 960


def header(o, title, sub1, sub2):
    o += [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
          f'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">', '<defs>']
    for mid, c in MARKERS:
        o.append(f'<marker id="{mid}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">'
                 f'<path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>')
        o.append(f'<marker id="{mid}s" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto" markerUnits="userSpaceOnUse">'
                 f'<path d="M8,0 L0,4 L8,8 z" fill="{c}"/></marker>')
    o += ['</defs>', f'<rect width="{W}" height="{H}" fill="#fbfaf8"/>',
          f'<text x="30" y="40" font-size="22" font-weight="700" fill="#1a1a1a">{esc(title)}</text>',
          f'<text x="30" y="62" font-size="11.5" fill="#555">{sub1}</text>',
          f'<text x="30" y="80" font-size="11.5" fill="#555">{sub2}</text>',
          '<text x="1610" y="40" font-size="11" font-weight="700" fill="#b45309" text-anchor="end">DRAFT A · for review</text>',
          '<text x="1610" y="58" font-size="10" fill="#777" text-anchor="end">2026-10-11</text>',
          '<g transform="translate(0,14)">']


def neighbour(x, y, w, h, title, sub):
    """A neighbouring element outside the node: the external box of the logical drawing."""
    return external(x, y, w, h, title, sub)


def group(o, x, y, w, h, label, node):
    ink = system_colour(node)[0]
    o += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{ink}" stroke-width="1" stroke-dasharray="3 3"/>',
          f'<text x="{x + 10}" y="{y - 6}" font-size="8.5" font-weight="700" fill="{ink}" letter-spacing="1">{esc(label)}</text>']


def key(o, y, node):
    stroke, fill = system_colour(node)
    o += [f'<line x1="30" y1="{y}" x2="1610" y2="{y}" stroke="#e5e7eb"/>',
          f'<text x="30" y="{y + 22}" font-size="10" font-weight="700" fill="#1a1a1a">CONNECTIONS</text>']
    for x, kind, text in [(120, 'e', 'energy'), (230, 'i', 'signal / data'), (390, 'c', 'command'), (520, 'p', 'storage / physical')]:
        o += flow(f'M{x},{y + 18} L{x + 34},{y + 18}', kind)
        o.append(f'<text x="{x + 42}" y="{y + 22}" font-size="10" fill="#374151">{text}</text>')
    o += [f'<rect x="30" y="{y + 37}" width="16" height="14" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>',
          f'<text x="52" y="{y + 48}" font-size="10" fill="#374151"><tspan font-weight="700">element of the node</tspan>: '
          f'{node}-NN, in the colour of the node · dashed grey boxes are neighbouring elements outside the node</text>',
          f'<text x="760" y="{y + 48}" font-size="10" font-weight="700" fill="#1a1a1a">FIRST PHASE</text>']
    o += pill(838, y + 37, 1)
    o.append(f'<text x="{838 + P.PILL_W + 8}" y="{y + 48}" font-size="10" fill="#374151">every element of the node exists from Phase 1</text>')


def build():
    o = []
    header(o, 'Nexus-Physical-01 · STM32 Node · Local View',
           'The STM32 node as a system-of-interest: its elements, hardware and software, and the connections between them · '
           'requirements are allocated to these elements, never to the repositories that implement the software ones',
           f'ID scheme <tspan font-family="{MONO}" font-weight="700">Nexus-Physical-01-NN</tspan> · numbers in brackets are BOM items · '
           'the carrier wiring is owned by the stm32-carrier drawing (HW-19), the memory map by the bootloader')
    o += ['<rect x="232" y="104" width="1146" height="626" rx="8" fill="none" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2 3"/>',
          '<text x="240" y="118" font-size="9" font-weight="700" fill="#9ca3af" letter-spacing="1">NEXUS-PHYSICAL-01 · STM32 NODE - BOUNDARY</text>']

    o += neighbour(30, 160, 170, 80, 'Bench PC', 'enabling system, ST-LINK')
    o += neighbour(30, 440, 170, 80, 'Vehicle CAN bus', 'Nexus-Physical-04')
    o += neighbour(30, 770, 260, 70, 'Power supply and distribution', 'Nexus-Physical-05')
    o += neighbour(1440, 560, 170, 70, 'Rear drive', 'Nexus-Physical-07')
    o += neighbour(1440, 650, 170, 70, 'Steering actuator', 'Nexus-Physical-08')

    o += element('Nexus-Physical-01-01', 'MCU board', 1, 600, 140, 740, 115, [
        'NUCLEO-H533RE, board MB1814 (1.2)', 'STM32H533: FDCAN2 on PB12 / PB13', 'I2C1 on PB6 / PB7, TIM4 channel 4 on PC2'], [
        'User LED LD2', 'STLINK-V3EC, SWD over USB-C', 'Runs from 5 V on E5V, CN7-6'])

    group(o, 600, 360, 740, 185, 'SOFTWARE ELEMENTS · IN THE FLASH OF THE STM32H533', NODE)
    ink, fill = system_colour(NODE)
    o += [f'<rect x="610" y="370" width="220" height="16" rx="2" fill="{fill}"/>',
          f'<text x="720" y="381.5" font-size="8.5" font-weight="700" fill="{ink}" text-anchor="middle">BOOTLOADER REGION</text>',
          f'<rect x="840" y="370" width="490" height="16" rx="2" fill="{fill}"/>',
          f'<text x="1085" y="381.5" font-size="8.5" font-weight="700" fill="{ink}" text-anchor="middle">APPLICATION REGION · ONE IMAGE AT A TIME</text>']
    o += element('Nexus-Physical-01-04', 'Bootloader', 1, 610, 395, 220, 140, [
        'Bare-metal, Cyphal (SW-01)', 'Receives, programs, checks CRC', 'Stays reachable on failure', 'Idle and receiving patterns'])
    o += element('Nexus-Physical-01-05', 'FBL-Updater', 1, 840, 395, 240, 140, [
        'Rewrites the bootloader region', 'Verifies the new bootloader', 'Started like an application', 'Own LED pattern'])
    o += element('Nexus-Physical-01-06', 'Application', 1, 1090, 395, 240, 140, [
        'Zephyr', 'Heartbeat out, heartbeat in', 'Version in node info', 'Own LED pattern'])

    o += element('Nexus-Physical-01-03', 'CAN transceiver module', 1, 260, 420, 280, 125, [
        'SN65HVD230 (4.1)', '3.3 V logic side', "Own 120 Ω: this end's termination"])
    o += element('Nexus-Physical-01-02', 'Carrier boards A and B', 1, 260, 580, 1100, 135, [
        'Kit boards A and B (5.11), drawn in stm32-carrier', '5 V into E5V, CN7 pin 6', 'PB12, PB13 to the transceiver; no termination',
        'PB6, PB7 to the motor driver header'], [
        'PC2 through R4, 1 kΩ, to the servo header', '6 V from the UBEC to the servo header', 'C2, 470 µF, across the servo header'])

    FL = flow
    o += FL('M200,200 L598,200', 'i', start=True, size=8, labels=[(400, 192, 'SWD, ST-LINK USB at the fascia')])
    o += FL('M200,480 L258,480', 'i', start=True, size=8, anchor='start', labels=[(204, 470, 'CAN_H, CAN_L')])
    o += FL('M400,547 L400,578', 'i', start=True, size=8, anchor='start', labels=[(406, 566, 'RXD, TXD')])
    o += FL('M570,578 L570,240 L598,240', 'i', start=True, size=8, anchor='end', labels=[(564, 330, 'headers P1, P2')])
    o += FL('M970,257 L970,358', 'p', start=True, size=8, anchor='start', labels=[(976, 312, 'stored in, run from the flash')])
    o += FL('M160,768 L160,700 L258,700', 'e', size=8, anchor='start', labels=[(166, 740, '5 V (board C), 6 V (UBEC)')])
    o += FL('M1362,605 L1438,605', 'c', start=True, size=8, labels=[(1400, 597, 'I2C')])
    o += FL('M1362,690 L1438,690', 'c', size=8, labels=[(1400, 682, '6 V + PWM')])

    key(o, 880, NODE)
    o += ['</g>', '</svg>']
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else OUT, build())
