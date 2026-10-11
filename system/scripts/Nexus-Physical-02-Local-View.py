#!/usr/bin/env python3
"""The local physical view of the FRDM node, Nexus-Physical-02 (../method.md: the node as a system-of-interest in turn).

    python3 Nexus-Physical-02-Local-View.py      # -> ../renders/Nexus-Physical-02-Local-View.svg
    python3 ../../tools/check-drawings.py        # fails if the SVG is not what this script writes

Same conventions as Nexus-Physical-01-Local-View.py, whose helpers it loads. The board facts come from the FRDM-IMX91S
schematic SCH-95020 rev B (vendor design files, not committed): CAN on header J7 pins 8 and 10 from a TJA1051T/3,
termination R139 + R144 through JP1, boot source on SW1[4:1]. Edit this script, never the SVG.
"""
import importlib.util, os, sys
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('stm32_view', os.path.join(HERE, 'Nexus-Physical-01-Local-View.py'))
N = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(N)
element, flow, write, header, neighbour, group, key = N.element, N.flow, N.write, N.header, N.neighbour, N.group, N.key
MONO = N.MONO

OUT = os.path.join(HERE, '..', 'renders', 'Nexus-Physical-02-Local-View.svg')


def build():
    o = []
    header(o, 'Nexus-Physical-02 · FRDM Node · Local View',
           'The FRDM node as a system-of-interest: its elements, hardware and software, and the connections between them · '
           'requirements are allocated to these elements, never to the repositories that implement the software ones',
           f'ID scheme <tspan font-family="{MONO}" font-weight="700">Nexus-Physical-02-NN</tspan> · numbers in brackets are BOM items · '
           'board facts from the FRDM-IMX91S schematic SCH-95020 rev B')
    o += ['<rect x="232" y="104" width="1146" height="626" rx="8" fill="none" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2 3"/>',
          '<text x="240" y="118" font-size="9" font-weight="700" fill="#9ca3af" letter-spacing="1">NEXUS-PHYSICAL-02 · FRDM NODE - BOUNDARY</text>']

    o += neighbour(30, 140, 170, 70, 'Vehicle CAN bus', 'Nexus-Physical-04')
    o += neighbour(30, 222, 170, 70, 'Bench PC', 'enabling system, console')
    o += neighbour(30, 770, 260, 70, 'Power supply and distribution', 'Nexus-Physical-05')

    o += element('Nexus-Physical-02-01', 'FRDM board', 1, 260, 140, 740, 120, [
        'FRDM-IMX91S (1.1)', 'TJA1051T/3, header J7: pin 8 CAN_H, pin 10 CAN_L', 'Termination R139 + R144 through JP1'], [
        'Boot switch SW1 = 0011: SD card', 'USB-C J1: 5 V in, no power delivery', 'USB-C J11: UART console'])
    o += element('Nexus-Physical-02-02', 'SD card', 1, 1060, 140, 280, 110, [
        'microSD (5.3)', 'Holds the Linux image'])

    group(o, 260, 380, 1100, 330, 'SOFTWARE ELEMENTS · ON THE SD CARD, RUN BY THE I.MX 91', 'Nexus-Physical-02')
    o += element('Nexus-Physical-02-03', 'Linux image', 1, 275, 395, 1070, 105, [
        'BSP, kernel and device tree, root file system', 'Boots to a login prompt'], [
        'SocketCAN on the FlexCAN controller, candump', 'Carries each released application at its tag'])
    o += element('Nexus-Physical-02-04', 'Heartbeat program', 1, 275, 560, 340, 135, [
        'Publishes the FRDM heartbeat', 'Logs each STM32 heartbeat', 'Prints its name and version'])
    o += element('Nexus-Physical-02-05', 'Flashing client', 1, 640, 560, 340, 135, [
        'Cyphal file server for the bootloader', 'Logs each download', 'Also runs on the bench PC'])
    o += element('Nexus-Physical-02-06', 'Test applications', 1, 1005, 560, 340, 135, [
        'Two throwaway programs', 'Each prints its name and version'])

    FL = flow
    o += FL('M200,175 L258,175', 'i', start=True, size=8, anchor='start', labels=[(204, 167, 'CAN · J7')])
    o += FL('M200,250 L258,250', 'i', start=True, size=8, anchor='start', labels=[(204, 242, 'console · J11')])
    o += FL('M160,768 L160,740 L245,740 L245,282 L300,282 L300,262', 'e', size=8, anchor='start', labels=[(166, 760, '5 V · J1')])
    o += FL('M1058,195 L1002,195', 'p', size=8, labels=[(1030, 187, 'boot')])
    o += FL('M1200,378 L1200,252', 'p', start=True, size=8, anchor='start', labels=[(1206, 320, 'stored on')])
    o += FL('M630,262 L630,393', 'i', size=8, anchor='start', labels=[(636, 330, 'runs')])
    for x in (445, 810, 1175):
        o += FL(f'M{x},502 L{x},558', 'p', size=8)
    o.append('<text x="451" y="534" font-size="8" fill="#c2410c">carried at release tags</text>')

    key(o, 880, 'Nexus-Physical-02')
    o += ['</g>', '</svg>']
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else OUT, build())
