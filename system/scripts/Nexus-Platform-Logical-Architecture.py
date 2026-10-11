#!/usr/bin/env python3
"""The logical view of the vehicle architecture (../method.md): every logical component Nexus-Logical-DNN, its functions, its phase and the flows between them (SYS-02, SYS-03).

    python3 Nexus-Platform-Logical-Architecture.py     # -> ../renders/Nexus-Platform-Logical-Architecture.svg
    python3 ../../tools/check-drawings.py       # fails if the SVG is not what this script writes

The logical components were called sub-systems (Nexus-SubSys-DNN) until 2026-10-11 and kept their numbers (SYS-03). Each is one card() call in drawing order: id, name,
phase, the card's box, and its functions in one or two columns (a function is a list of lines; the first line gets the bullet). Function
names are technology-free: a part, a bus or a protocol belongs to the physical view. The phase on a card is the FIRST phase in which it exists,
and `PHASES` is the one table that says what each phase is called and how its pill looks. What each phase delivers, and which functions
of a component arrive when, is owned by ../phases.md, never by this drawing. Flows are listed at the bottom in pixels.

Everything is in pixels; there is no scale. Edit this script, never the SVG.
"""
import os, sys
sys.dont_write_bytecode = True

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders', 'Nexus-Platform-Logical-Architecture.svg')

W, H = 1640, 1115
MONO = 'ui-monospace, Menlo, Consolas, monospace'

# phase -> (pill fill, pill stroke, pill text). Phase 1 keeps the green the drawing always had.
PHASES = {
    1: ('#dcfce7', '#15803d', '#15803d'),
    2: ('#e0f2fe', '#0369a1', '#0369a1'),
    3: ('#fae8ff', '#a21caf', '#a21caf'),
    4: ('#ffedd5', '#c2410c', '#c2410c'),
    5: ('#f1f5f9', '#64748b', '#475569'),
}
PILL_W = 42

# domain -> (stroke, header fill)
DOMAINS = {
    1: ('#92400e', '#fef3c7'),
    2: ('#1d4ed8', '#dbeafe'),
    3: ('#6d28d9', '#ede9fe'),
    4: ('#0f766e', '#ccfbf1'),
    5: ('#be123c', '#ffe4e6'),
}

# marker id -> colour; each has an end marker and a start marker
MARKERS = [('mi', '#374151'), ('mc', '#1d4ed8'), ('me', '#d92b2b'), ('mp', '#c2410c')]


def esc(s):
    return s.replace('&', '&amp;')


def pill(x, y, phase, text_x=None, text_y=None):
    fill, stroke, ink = PHASES[phase]
    tx = f'{x + PILL_W / 2}' if text_x is None else text_x
    ty = f'{y + 10.5}' if text_y is None else text_y
    return [f'<rect x="{x}" y="{y}" width="{PILL_W}" height="14" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>',
            f'<text x="{tx}" y="{ty}" font-size="8.5" font-weight="700" text-anchor="middle" fill="{ink}">PHASE {phase}</text>']


def card(sid, name, phase, x, y, w, h, *columns):
    """A logical component card. `columns` are lists of functions; a function is a list of lines, the first one gets the bullet."""
    d = int(sid[-3])
    stroke, head = DOMAINS[d]
    o = [f'<g id="{sid}">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#ffffff" stroke="{stroke}" stroke-width="1.6"/>',
         f'<path d="M{x},{y + 4} a4,4 0 0 1 4,-4 h{w - 8} a4,4 0 0 1 4,4 v38 h-{w} z" fill="{head}"/>',
         f'<line x1="{x}" y1="{y + 42}" x2="{x + w}" y2="{y + 42}" stroke="{stroke}" stroke-width="0.8"/>',
         f'<text x="{x + 12}" y="{y + 16}" font-size="9.5" font-weight="700" fill="{stroke}" font-family="{MONO}">{sid}</text>',
         f'<text x="{x + 12}" y="{y + 34}" font-size="13" font-weight="700" fill="#111827">{esc(name)}</text>']
    o += pill(x + w - 10 - PILL_W, y + 7, phase)
    for ci, col in enumerate(columns):
        bx = float(x + 16 + 259 * ci)
        row = y + 58.5
        for fn in col:
            for li, line in enumerate(fn):
                if li == 0:
                    o.append(f'<circle cx="{bx}" cy="{row}" r="1.8" fill="{stroke}"/>')
                o.append(f'<text x="{bx + 7}" y="{int(row + 3.5)}" font-size="10.5" fill="#374151" xml:space="preserve">'
                         f'{"  " if li else ""}{esc(line)}</text>')
                row += 16
    o.append('</g>')
    return o


def external(x, y, w, h, title, sub):
    cx, cy = x + w / 2, y + h / 2
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#f3f4f6" stroke="#6b7280" stroke-width="1.2" stroke-dasharray="5 3"/>',
            f'<text x="{cx}" y="{cy - 4}" font-size="12" font-weight="700" fill="#374151" text-anchor="middle">{title}</text>',
            f'<text x="{cx}" y="{cy + 12}" font-size="9.5" fill="#6b7280" text-anchor="middle">{sub}</text>']


def flow(d, kind, label_at=None, labels=(), start=False, dashed=False, size=9, anchor='middle', fill=None):
    """An arrow. kind: i information, c command, e energy, p physical. Labels are (x, y, text) in the arrow's own size."""
    colour = dict(mi='#374151', mc='#1d4ed8', me='#d92b2b', mp='#c2410c')['m' + kind]
    width = dict(i='1.4', c='1.8', e='2.6', p='1.6')[kind]
    dash = {'p': ' stroke-dasharray="6 3"'}.get(kind, '')
    if dashed:
        dash = ' stroke-dasharray="7 4"'
    ms = f' marker-start="url(#m{kind}s)"' if start else ''
    o = [f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}"{dash}{ms} marker-end="url(#m{kind})"/>']
    ink = fill or ('#b91c1c' if kind == 'e' else colour)
    for (x, y, t) in labels:
        o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{ink}" text-anchor="{anchor}">{esc(t)}</text>')
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
          '<text x="30" y="40" font-size="22" font-weight="700" fill="#1a1a1a">Nexus Platform Logical Architecture</text>',
          '<text x="30" y="62" font-size="11.5" fill="#555">Logical view of the vehicle architecture · the logical components and their functions · says '
          '<tspan font-style="italic">what</tspan> the vehicle must do, free of technology; the physical view says what it is built from, and allocation relates the two</text>',
          f'<text x="30" y="80" font-size="11.5" fill="#555">ID scheme <tspan font-family="{MONO}" font-weight="700">Nexus-Logical-DNN</tspan>'
          f' - D = functional domain (1–5), NN = component within it. Functions inside a component will be numbered '
          f'<tspan font-family="{MONO}" font-weight="700">Nexus-Logical-DNN-Fnn</tspan>.</text>',
          '<text x="1610" y="40" font-size="11" font-weight="700" fill="#b45309" text-anchor="end">DRAFT B · for review</text>',
          '<text x="1610" y="58" font-size="10" fill="#777" text-anchor="end">2026-10-11</text>',
          '<g transform="translate(0,14)">']

    o += external(30, 140, 170, 100, 'Operator', 'on the vehicle or remote')
    o += external(30, 420, 170, 100, 'Remote station', 'PC · laptop · later cloud')
    o += external(1440, 118, 170, 507, 'Environment', 'road · obstacles · landmarks')
    o += external(1440, 685, 170, 100, 'Charger', 'mains-powered, off-board')
    o += ['<rect x="232" y="84" width="1146" height="930" rx="8" fill="none" stroke="#9ca3af" stroke-width="1" stroke-dasharray="2 3"/>',
          '<text x="240" y="98" font-size="9" font-weight="700" fill="#9ca3af" letter-spacing="1">NEXUS VEHICLE - SYSTEM BOUNDARY</text>']

    # --- row 1: communication & interaction (402), autonomy (303, 302, 301)
    o += card('Nexus-Logical-402', 'Operator Interface', 2, 250, 118, 240, 145, [
        ['Accept local controls'], ['Show vehicle status'], ['Take manual / teleop drive input'],
        ['Take mode & mission requests'], ['Present telemetry to the operator']])
    o += card('Nexus-Logical-303', 'Planning & Decision', 5, 540, 118, 240, 145, [
        ['Manage mission & route'], ['Decide driving behaviour'], ['Plan a collision-free trajectory'],
        ['Issue motion requests', '(target speed + curvature)']])
    o += card('Nexus-Logical-302', 'Localization & Mapping', 4, 830, 118, 240, 145, [
        ['Estimate vehicle pose'], ['Fuse odometry, inertial & perception data'], ['Build & maintain the map'],
        ['Report localization confidence']])
    o += card('Nexus-Logical-301', 'Environment Perception', 4, 1120, 118, 240, 145, [
        ['Sense surroundings'], ['Detect & track obstacles'],
        ['Detect drivable space & markers'], ['Report perception confidence']])

    # --- the communication backbone is a banner, not a card
    o += ['<g id="Nexus-Logical-401">',
          '<rect x="250" y="300" width="1110" height="60" rx="4" fill="#ccfbf1" stroke="#0f766e" stroke-width="1.6"/>',
          f'<text x="262" y="318" font-size="9.5" font-weight="700" fill="#0f766e" font-family="{MONO}">Nexus-Logical-401</text>',
          '<text x="262" y="338" font-size="13" font-weight="700" fill="#111827">In-Vehicle Communication</text>',
          '<text x="262" y="352" font-size="9" fill="#0f766e">backbone - every electronic component attaches here</text>']
    for (cx, cy, t) in [(522, 321.5, 'Exchange signals between nodes'), (822, 321.5, 'Time-synchronise nodes'),
                        (522, 338.5, 'Route between signals and services'),
                        (822, 338.5, 'Publish services & topics')]:
        o += [f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="#0f766e"/>',
              f'<text x="{cx + 7}" y="{int(cy + 3.5)}" font-size="10.5" fill="#374151">{esc(t)}</text>']
    o += pill(1308, 307, 1)
    o.append('</g>')

    # --- row 2: external connectivity (403), vehicle motion control (203), actuation (201, 202)
    o += card('Nexus-Logical-403', 'External Connectivity', 2, 250, 400, 240, 145, [
        ['Link to remote station'], ['Carry remote sessions & teleop'], ['Stream telemetry off-board'],
        ['Carry update & diagnostic data']])
    o += card('Nexus-Logical-203', 'Vehicle Motion Control', 2, 540, 400, 530, 225, [
        ['Arbitrate motion requests', '(manual · teleop · autonomous)'],
        ['Translate speed + curvature into', 'wheel-speed & steer-angle setpoints'],
        ['Close speed & steering control loops']], [
        ['Enforce speed, accel. & jerk limits'],
        ['Estimate vehicle motion state', '(odometry from wheel speed, inertial data)'],
        ['Execute safe-stop requests'], ['Report motion state']])
    o += ['<rect x="1110" y="390" width="260" height="245" rx="6" fill="none" stroke="#1d4ed8" stroke-width="1" stroke-dasharray="3 3"/>',
          '<text x="1370" y="385" font-size="8.5" font-weight="700" fill="#1d4ed8" text-anchor="end" letter-spacing="1">ACTUATION</text>']
    o += card('Nexus-Logical-201', 'Propulsion', 1, 1120, 400, 240, 105, [
        ['Produce drive torque, rear wheels'], ['Track wheel-speed setpoints'], ['Measure wheel speed']])
    o += card('Nexus-Logical-202', 'Steering', 1, 1120, 520, 240, 105, [
        ['Set front wheel angle (Ackermann)'], ['Enforce steer angle & rate limits'], ['Report steering state']])

    # --- row 3: vehicle foundation
    o += card('Nexus-Logical-102', 'Structure & Enclosure', 1, 250, 675, 530, 120, [
        ['Carry & locate every component'], ['Protect harness & electronics']], [
        ['Expose controls & service access'], ['Manage heat & vibration']])
    o += card('Nexus-Logical-101', 'Energy Storage & Distribution', 1, 830, 675, 530, 120, [
        ['Store energy on board'], ['Protect circuits against overcurrent'], ['Switch drive & logic branches'],
        ['Accept charge from the charger']], [
        ['Convert energy to the supplies', 'the loads need'], ['Measure pack voltage & current'], ['Estimate state of charge']])

    # --- row 4: cross-cutting
    o.append('<text x="250" y="840" font-size="10" font-weight="700" fill="#be123c" letter-spacing="1">'
             'CROSS-CUTTING - these reach every logical component above through 401</text>')
    o += card('Nexus-Logical-501', 'Supervision & Safety', 1, 250, 850, 240, 150, [
        ['Manage vehicle modes & transitions'], ['Emergency stop & safe stop'], ['Watchdogs & command time-outs'],
        ['Detect faults, enter degraded mode'], ['Shut down gracefully on low pack'], ['Command drive-power cut-off']])
    o += card('Nexus-Logical-502', 'Cybersecurity', 3, 540, 850, 240, 150, [
        ['Secure & measured boot'], ['Store keys, trusted execution'], ['Authenticate & protect messages'],
        ['Control access to the vehicle'], ['Detect intrusions & anomalies']])
    o += card('Nexus-Logical-503', 'Diagnostics & Data Logging', 1, 830, 850, 240, 150, [
        ['Monitor component health'], ['Record fault codes & event data'], ['Log & replay bus and sensor data'],
        ['Provide debug access']])
    o += card('Nexus-Logical-504', 'Software Update & Config.', 1, 1120, 850, 240, 150, [
        ['Deliver updates'], ['Verify integrity before install'], ['Roll back a failed update'],
        ['Manage configuration &', 'calibration parameters']])

    # --- flows
    FL = flow
    o += FL('M1440,178 L1362,178', 'p', labels=[(1400, 170, 'scene')])
    o += FL('M1120,178 L1072,178', 'i', labels=[(1095, 158, 'objects'), (1095, 169, 'features')])
    o += FL('M830,178 L782,178', 'i', labels=[(806, 158, 'pose'), (806, 169, 'map')])
    o += FL('M1300,118 L1300,106 L720,106 L720,116', 'i', labels=[(1010, 102, 'tracked obstacles · free space')])
    o += FL('M200,190 L248,190', 'p', start=True, labels=[(224, 181, 'use')])
    o += FL('M200,470 L248,470', 'p', start=True, labels=[(224, 461, 'link')])
    o += FL('M370,263 L370,298', 'c', start=True, size=9, anchor='start', labels=[(378, 285, 'drive input · mode req. ↓   status ↑')])
    o += FL('M370,360 L370,398', 'i', start=True, anchor='start', labels=[(378, 384, 'sessions · telemetry · updates')])
    o += FL('M660,263 L660,298', 'c', anchor='start', labels=[(668, 285, 'motion request')])
    o += FL('M660,360 L660,398', 'c', anchor='start', labels=[(668, 384, 'motion request')])
    o += FL('M950,400 L950,362', 'i', anchor='start', labels=[(958, 384, 'vehicle motion state')])
    o += FL('M950,300 L950,265', 'i', anchor='start', labels=[(958, 285, 'motion measurements')])
    o += FL('M1070,440 L1118,440', 'c', size=8, labels=[(1095, 432, 'speed')])
    o += FL('M1120,470 L1072,470', 'i', size=8, labels=[(1095, 484, 'actual')])
    o += FL('M1070,560 L1118,560', 'c', size=8, labels=[(1095, 552, 'angle')])
    o += FL('M1120,590 L1072,590', 'i', size=8, labels=[(1095, 604, 'state')])
    o += FL('M1372,450 L1438,450', 'p', size=8, labels=[(1405, 442, 'traction')])
    o += FL('M1372,570 L1438,570', 'p', size=8, labels=[(1405, 562, 'wheel angle')])
    o += FL('M1240,675 L1240,637', 'e', anchor='start', labels=[(1248, 659, 'actuator power')])
    o += FL('M900,675 L900,627', 'e', dashed=True, anchor='start', labels=[(908, 659, 'logic supply → all electronics')])
    o += FL('M1440,735 L1362,735', 'e', labels=[(1400, 727, 'charge')])

    # --- key
    o += ['<line x1="30" y1="1028" x2="1610" y2="1028" stroke="#e5e7eb"/>',
          '<text x="30" y="1050" font-size="10" font-weight="700" fill="#1a1a1a">FLOWS</text>']
    for x, kind, text in [(80, 'c', 'command / setpoint'), (240.8, 'i', 'information / measurement'),
                          (440.8, 'e', 'energy (dashed = logic supply)'), (668.8, 'p', 'physical interaction')]:
        o += flow(f'M{x},1046 L{x + 34},1046', kind)
        o.append(f'<text x="{round(x + 42, 1)}" y="1050" font-size="10" fill="#374151">{text}</text>')
    o.append('<text x="30" y="1076" font-size="10" font-weight="700" fill="#1a1a1a">DOMAINS</text>')
    x = 92
    for d, name, adv in [(1, 'Vehicle Foundation', 158.8), (2, 'Motion', 91.6), (3, 'Autonomy', 102.8),
                         (4, 'Communication & Interaction', 209.2), (5, 'Dependability & Lifecycle', 208.0)]:
        stroke, head = DOMAINS[d]
        o += [f'<rect x="{x}" y="1065" width="16" height="14" rx="2" fill="{head}" stroke="{stroke}" stroke-width="1.2"/>',
              f'<text x="{round(x + 22, 1)}" y="1076" font-size="10" fill="#374151"><tspan font-weight="700" fill="{stroke}">{d}xx</tspan> {esc(name)}</text>']
        x = round(x + adv, 1)
    o.append(f'<text x="{x}" y="1076" font-size="10" font-weight="700" fill="#1a1a1a">FIRST PHASE</text>')
    x = round(x + 78, 1)
    for p in PHASES:
        o += pill(x, 1065, p)
        x = round(x + PILL_W + 6, 1)
    o.append(f'<text x="{x + 2}" y="1076" font-size="10" fill="#374151">first phase the component exists in (phases.md)</text>')
    o += ['</g>', '</svg>']
    return '\n'.join(o) + '\n'


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    write(sys.argv[1] if len(sys.argv) > 1 else OUT, build())
