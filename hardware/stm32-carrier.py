#!/usr/bin/env python3
"""The STM32 carrier's geometry, and the drawing made from it (MEC-15, HW-19).

    python3 stm32-carrier.py            # -> stm32-carrier.svg beside this file

Everything above the sheet section is data and helpers with no side effects, so
../mechanical/animate-carrier.py imports it and builds the 3D assembly from the same
holes, parts and wires the drawing shows.
"""
import os
import sys

P = 2.54
S = 4.6                       # px per mm in the carrier views

# ---------------------------------------------------------------- geometry (mm)
# Carrier views: X along the vehicle (rear = +X, right), Y across (down = +Y).
# Header row n (pins 2n-1 / 2n) sits at X = -(n-1)*P, row 1 at the rear (CN1 end).
def RX(n):
    return -(n - 1) * P

BOARD = {
    # name: (cols, rows, Y of col 1, board Y edges, colour)
    'A': dict(cols=18, rows=24, y1=-20.32, edge=(-23.73, 26.27)),
    'B': dict(cols=18, rows=24, y1=35.56, edge=(32.15, 82.15)),
}
BX = (-64.21, 5.79)                  # both boards, 24 rows, 70 mm
DISCO = dict(x=(-63.18, 33.82), y=(-6.33, 59.67))
XMIN, XMAX = -64.21, 33.82
YMIN, YMAX = -23.73, 82.15

def cy(board, col):
    return BOARD[board]['y1'] + (col - 1) * P

COL = 'abcdefghijklmnopqr'

def ci(letter):
    return COL.index(letter) + 1

# ---------------------------------------------------------------- colours
NET = {
    '5V': '#dc2626', 'GND': '#111827', '3V3': '#db2777', '6V': '#d97706',
    'PWM': '#92400e', 'SCL': '#7c3aed', 'SDA': '#a855f7', 'CTX': '#0891b2',
    'CRX': '#0e7490', 'TERM': '#64748b', 'CANH': '#1d4ed8', 'CANL': '#60a5fa', 'CC': '#059669',
}

out = []
def w(s):
    out.append(s)

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def text(x, y, t, size=9, fill='#475569', weight=None, anchor=None, italic=False, halo=False):
    a = f' font-weight="{weight}"' if weight else ''
    a += ' stroke="#fbfaf8" stroke-width="3" paint-order="stroke"' if halo else ''
    a += f' text-anchor="{anchor}"' if anchor else ''
    a += ' font-style="italic"' if italic else ''
    w(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"{a}>{esc(t)}</text>')

# ---------------------------------------------------------------- a view
class View:
    """Maps board coordinates to px. flip=True mirrors Y (solder side)."""
    def __init__(self, ox, oy, xmin, ymin, ymax, flip=False, scale=S):
        self.ox, self.oy, self.xmin, self.ymin, self.ymax = ox, oy, xmin, ymin, ymax
        self.flip, self.s = flip, scale

    def px(self, X, Y):
        x = self.ox + (X - self.xmin) * self.s
        y = self.oy + ((self.ymax - Y) if self.flip else (Y - self.ymin)) * self.s
        return x, y

    def rect(self, X0, X1, Y0, Y1, **kw):
        xa, ya = self.px(X0, Y0)
        xb, yb = self.px(X1, Y1)
        x, y = min(xa, xb), min(ya, yb)
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
        w(f'<rect x="{x:.1f}" y="{y:.1f}" width="{abs(xb - xa):.1f}" height="{abs(yb - ya):.1f}" {attrs}/>')

# Carrier hole -> (X, Y); col may be fractional for routing channels
def hole(board, col, row):
    return RX(row), BOARD[board]['y1'] + (col - 1) * P

# ---------------------------------------------------------------- component data
# Boards A (P1 side) and B (P2 side) are both 5x7 kit boards, 18 x 24; col a of A is outboard.
# The sockets are 1x25: row 25 has no hole and its tail is snipped, so it rests on the margin.
SOCKETS = [('A', 'i', 'P1 odd'), ('A', 'j', 'P1 even'), ('B', 'g', 'P2 odd'), ('B', 'h', 'P2 even')]

# screw terminals: board, [(col,row,label)], entry side ('-Y','+Y','+X'), name, colour
TERMS = [
    ('A', [('c', 1, '+6V'), ('c', 3, 'GND')], '-Y', '6V IN', '#d97706'),
    ('B', [('m', 1, 'H'), ('o', 1, 'L'), ('q', 1, 'GND')], '+X', 'CAN', '#1d4ed8'),
    ('B', [('q', 21, '+5V'), ('q', 23, 'GND')], '+Y', '5V IN', '#dc2626'),
]
# male headers: board, [(col,row,label)], name
MALE = [
    ('A', [('c', 12, 'GND'), ('c', 13, '+6V'), ('c', 14, 'SIG')], 'SERVO'),
    ('A', [('c', 16, 'GND'), ('c', 17, 'SCL'), ('c', 18, 'SDA')], 'I2C-B'),
    ('A', [('c', 20, 'GND'), ('c', 21, '3V3'), ('c', 22, 'SCL'), ('c', 23, 'SDA')], 'I2C-A'),
    ('B', [('m', 22, ''), ('m', 23, '')], 'TERM'),
]
RES = [('A', ('h', 8), ('h', 12), 'R4 1k'), ('B', ('k', 19), ('k', 23), 'R3 120R')]
CAPS = [('A', ('c', 8), ('c', 10), 'C2')]          # (minus leg, plus leg)
XCVR_SOCKET = ('B', [('n', 13, '3V3'), ('o', 13, 'GND'), ('p', 13, 'CRX'), ('q', 13, 'CTX')])
FIX = [('A', 7.0, 14.0, 'A1', '(148.18, 23.76) ⌀3.18'), ('B', 4.07, 14.0, 'B1', '(148.2, 72.2) ⌀2.71'),
       ('A', 3.25, 5.457, 'A2', '(169.88, 14.24) ⌀2.71'), ('B', 15.11, 5.457, 'B2', '(169.88, 100.24) ⌀2.71')]

# wires: (net, board, [(col,row)...], kind)  kind: 'ins' insulated, 'bare' tinned link
WIRES = [
    # ---- board A
    ('GND', 'A', [(5, 1), (5, 20)], 'bare'),                  # GND spine, column e
    ('GND', 'A', [(5, 1), (9, 1)], 'bare'),                   # spine to P1-1 (passes h1)
    ('GND', 'A', [(3, 3), (5, 3)], 'bare'),
    ('GND', 'A', [(3, 8), (5, 8)], 'bare'),
    ('GND', 'A', [(3, 12), (5, 12)], 'bare'),
    ('GND', 'A', [(3, 16), (5, 16)], 'bare'),
    ('GND', 'A', [(3, 20), (5, 20)], 'bare'),
    ('6V', 'A', [(1, 1), (1, 13)], 'bare'),                   # 6 V spine, column a
    ('6V', 'A', [(3, 1), (1, 1)], 'bare'),
    ('6V', 'A', [(3, 10), (1, 10)], 'bare'),
    ('6V', 'A', [(3, 13), (1, 13)], 'bare'),
    ('PWM', 'A', [(9, 14), (8.5, 14), (8.5, 12), (8, 12)], 'ins'),
    ('PWM', 'A', [(8, 8), (8, 7.5), (4.5, 7.5), (4.5, 14), (3, 14)], 'ins'),
    ('SCL', 'A', [(10, 17), (10, 16.5), (3.5, 16.5), (3.5, 17), (3, 17)], 'ins'),
    ('SCL', 'A', [(3, 17), (3.5, 17), (3.5, 22), (3, 22)], 'ins'),
    ('SDA', 'A', [(9, 18), (9, 18.5), (2.5, 18.5), (2.5, 18), (3, 18)], 'ins'),
    ('SDA', 'A', [(3, 18), (2.5, 18), (2.5, 23), (3, 23)], 'ins'),
    ('3V3', 'A', [(11, 3), (11, 2.5), (5.5, 2.5), (5.5, 21.5), (3.5, 21.5), (3.5, 21), (3, 21)], 'ins'),
    ('GND', 'A', [(9, 1), (18, 1)], 'bare'),                  # GND bridge on A: j1 (P1-2) to r1
    ('3V3', 'A', [(11, 3), (18, 3)], 'bare'),                 # 3V3 bridge on A: k3 to r3, never j3 (P1-4 VDD)
    # ---- board B
    ('GND', 'B', [(1, 1), (8, 1)], 'bare'),                   # GND bridge on B: a1 to g1-h1 (P2-1, P2-2)
    ('GND', 'B', [(8, 1), (10, 1)], 'bare'),
    ('GND', 'B', [(10, 1), (10, 24)], 'bare'),                # GND spine, column j
    ('5V', 'B', [(7, 2), (8, 2)], 'bare'),                    # P2-3 = P2-4
    ('3V3', 'B', [(1, 3), (8, 3)], 'bare'),                   # 3V3 bridge on B: a3 to g3-h3 (P2-5, P2-6)
    ('GND', 'B', [(17, 1), (17, 0.5), (10, 0.5), (10, 1)], 'ins'),          # CAN GND
    ('GND', 'B', [(15, 13), (15, 12.5), (10, 12.5), (10, 12)], 'ins'),                # XCVR GND
    ('GND', 'B', [(17, 23), (17, 24), (10, 24)], 'ins'),                    # 5V IN GND
    ('5V', 'B', [(17, 21), (17, 21.5), (9.5, 21.5), (9.5, 2.5), (8, 2.5), (8, 2)], 'ins'),
    ('3V3', 'B', [(8, 3), (8, 3.5), (11.5, 3.5), (11.5, 13.5), (14, 13.5), (14, 13)], 'ins'),
    ('CTX', 'B', [(7, 17), (7.5, 17), (7.5, 16.5), (16.5, 16.5), (16.5, 13), (17, 13)], 'ins'),
    ('CRX', 'B', [(8, 18), (8.5, 18), (8.5, 15.5), (16, 15.5), (16, 13)], 'ins'),
    ('CANH', 'B', [(13, 3), (13, 1)], 'bare'),                # m3-m2-m1
    ('CANL', 'B', [(15, 3), (15, 1)], 'bare'),                # o3-o2-o1
    ('CANH', 'B', [(13, 3), (12.5, 3), (12.5, 18.5), (11, 18.5), (11, 19)], 'ins'),
    ('CANL', 'B', [(15, 3), (15, 3.5), (13.5, 3.5), (13.5, 22), (13, 22)], 'ins'),
    ('TERM', 'B', [(11, 23), (13, 23)], 'bare'),              # R3 to TERM, k23-l23-m23 (own node)
]
BRIDGES = [('GND', ('A', 18, 1), ('B', 1, 1)), ('3V3', ('A', 18, 3), ('B', 1, 3))]   # the 5.9 mm gap
LINKS = [('CANH', ('B', 13, 3)), ('CANL', ('B', 15, 3))]      # module terminal -> board

# header pins that carry a net, for labels
PINS = [
    ('A', 'i', 1, 'P1-1 GND'), ('A', 'i', 14, 'P1-27 PE9'),
    ('A', 'j', 17, 'P1-34 PB10'), ('A', 'i', 18, 'P1-35 PB11'),
    ('B', 'g', 1, 'P2-1 GND'), ('B', 'g', 2, 'P2-3 5V'), ('B', 'g', 3, 'P2-5 3V'),
    ('B', 'g', 17, 'P2-33 PD1'), ('B', 'h', 18, 'P2-36 PD0'),
]

# ---------------------------------------------------------------- drawing helpers
def draw_board(v, b, grid_labels=True):
    cfg = BOARD[b]
    v.rect(BX[0], BX[1], cfg['edge'][0], cfg['edge'][1], rx=4, fill='#f0fdf4',
           stroke='#15803d', stroke_width=1.6)
    for c in range(1, cfg['cols'] + 1):
        for r in range(1, cfg['rows'] + 1):
            x, y = v.px(RX(r), cy(b, c))
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="#fff" stroke="#a3b18a" stroke-width="0.7"/>')
    if grid_labels:
        # column letters on the front (left) edge
        for c in range(1, cfg['cols'] + 1):
            x, y = v.px(BX[0], cy(b, c))
            text(x - 4, y + 2.5, COL[c - 1], 7, '#15803d', anchor='end')
        x, y = v.px(BX[0], (cfg['edge'][0] + cfg['edge'][1]) / 2)
        w(f'<text transform="translate({x - 16:.1f},{y:.1f}) rotate(-90)" font-size="10" font-weight="700" fill="#15803d" text-anchor="middle">Board {b}</text>')

def row_labels(v, yline):
    for r in range(1, 26):
        x, _ = v.px(RX(r), 0)
        text(x, yline, str(r), 6.5, '#94a3b8' if r == 25 else '#64748b', anchor='middle', italic=r == 25)

def draw_discovery(v):
    v.rect(DISCO['x'][0], DISCO['x'][1], DISCO['y'][0], DISCO['y'][1], rx=3, fill='#eef2ff',
           fill_opacity='0.35', stroke='#4338ca', stroke_width=1.2, stroke_dasharray='7 4')

def draw_sockets(v):
    for b, col, lab in SOCKETS:
        c = ci(col)
        colr = '#0f766e' if b == 'A' else '#b45309'
        v.rect(RX(25) - 1.27, RX(1) + 1.27, cy(b, c) - 1.2, cy(b, c) + 1.2, rx=1,
               fill=colr, fill_opacity='0.22', stroke=colr, stroke_width=0.9)
        snipped(v, b, c, colr)

def snipped(v, b, c, colr):
    # row 25: no hole under it, tail cut flush, the socket body rests on the margin
    x, y = v.px(RX(25), cy(b, c))
    w(f'<line x1="{x - 2.2:.1f}" y1="{y - 2.2:.1f}" x2="{x + 2.2:.1f}" y2="{y + 2.2:.1f}" stroke="{colr}" stroke-width="1.1"/>')
    w(f'<line x1="{x - 2.2:.1f}" y1="{y + 2.2:.1f}" x2="{x + 2.2:.1f}" y2="{y - 2.2:.1f}" stroke="{colr}" stroke-width="1.1"/>')

def hp(v, b, c, r):
    X, Y = hole(b, c, r)
    return v.px(X, Y)

def pad(v, b, c, r, colr, rad=2.6):
    x, y = hp(v, b, c, r)
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{colr}"/>')

def draw_terminal(v, b, pins, entry, name, colr, top=True):
    cs = [ci(p[0]) for p in pins]
    rs = [p[1] for p in pins]
    Xs = [RX(r) for r in rs]
    Ys = [cy(b, c) for c in cs]
    if len(set(rs)) > 1:          # pins along X
        X0, X1 = min(Xs) - 2.5, max(Xs) + 2.5
        Y0, Y1 = Ys[0] - 3.8, Ys[0] + 3.8
    else:                         # pins along Y
        X0, X1 = Xs[0] - 3.8, Xs[0] + 3.8
        Y0, Y1 = min(Ys) - 2.5, max(Ys) + 2.5
    if top:
        v.rect(X0, X1, Y0, Y1, rx=1.5, fill='#dbeafe', stroke=colr, stroke_width=1.4)
        # wire-entry face
        if entry == '-Y':
            a, bb = v.px(X0, Y0), v.px(X1, Y0)
        elif entry == '+Y':
            a, bb = v.px(X0, Y1), v.px(X1, Y1)
        else:
            a, bb = v.px(X1, Y0), v.px(X1, Y1)
        w(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{bb[0]:.1f}" y2="{bb[1]:.1f}" stroke="{colr}" stroke-width="3.2"/>')
    for (col, r, lab) in pins:
        x, y = hp(v, b, ci(col), r)
        if top:
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.9" fill="#fff" stroke="{colr}" stroke-width="1.4"/>')
        else:
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="#e2e8f0" stroke="{colr}" stroke-width="1.2"/>')
    return (X0, X1, Y0, Y1)

def draw_male(v, b, pins, name, top=True):
    cs = [ci(p[0]) for p in pins]
    rs = [p[1] for p in pins]
    X0, X1 = RX(max(rs)) - 1.27, RX(min(rs)) + 1.27
    Y0 = cy(b, min(cs)) - 1.27
    Y1 = cy(b, max(cs)) + 1.27
    if top:
        v.rect(X0, X1, Y0, Y1, rx=0.8, fill='#334155', stroke='#0f172a', stroke_width=0.8)
    for (col, r, lab) in pins:
        x, y = hp(v, b, ci(col), r)
        if top:
            w(f'<rect x="{x - 1.6:.1f}" y="{y - 1.6:.1f}" width="3.2" height="3.2" fill="#fbbf24"/>')
        else:
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#e2e8f0" stroke="#334155" stroke-width="1.1"/>')
    return (X0, X1, Y0, Y1)

def draw_res(v, b, a, c, lab, top=True):
    xa, ya = hp(v, b, ci(a[0]), a[1])
    xb, yb = hp(v, b, ci(c[0]), c[1])
    if top:
        w(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#94a3b8" stroke-width="1.4"/>')
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        horiz = abs(xb - xa) > abs(yb - ya)
        bw, bh = (26, 9) if horiz else (9, 26)
        w(f'<rect x="{mx - bw / 2:.1f}" y="{my - bh / 2:.1f}" width="{bw}" height="{bh}" rx="3" fill="#bfdbfe" stroke="#1e40af" stroke-width="1"/>')
    for x, y in ((xa, ya), (xb, yb)):
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{"#fff" if top else "#e2e8f0"}" stroke="#1e40af" stroke-width="1.1"/>')

def draw_cap(v, b, minus, plus, lab, top=True, board_hole=None):
    hf = board_hole or (lambda cc, rr: hp(v, b, ci(cc), rr))
    xm, ym = hf(*minus)
    xp, yp = hf(*plus)
    if top:
        mx, my = (xm + xp) / 2, (ym + yp) / 2
        r = 5.0 * v.s
        w(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r:.1f}" fill="#fef9c3" stroke="#a16207" stroke-width="1.4"/>')
        # stripe on the minus side
        dx, dy = xm - mx, ym - my
        n = (dx * dx + dy * dy) ** 0.5 or 1
        ux, uy = dx / n, dy / n
        cxs, cys = mx + ux * r * 0.72, my + uy * r * 0.72
        w(f'<circle cx="{cxs:.1f}" cy="{cys:.1f}" r="{r * 0.2:.1f}" fill="#a16207" fill-opacity="0.35"/>')
        text(xp - ux * 7, yp - uy * 7 + 3, '+', 9, '#a16207', '700', anchor='middle')
    for x, y in ((xm, ym), (xp, yp)):
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="{"#fff" if top else "#e2e8f0"}" stroke="#a16207" stroke-width="1.2"/>')

def draw_wire(v, net, b, pts, kind, hfun=None):
    hfun = hfun or (lambda c, r: hp(v, b, c, r))
    xy = [hfun(c, r) for c, r in pts]
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in xy)
    colr = NET[net]
    if kind == 'bare':
        w(f'<polyline points="{d}" fill="none" stroke="{colr}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>')
        w(f'<polyline points="{d}" fill="none" stroke="#e5e7eb" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        w(f'<polyline points="{d}" fill="none" stroke="{colr}" stroke-width="{2.6 if kind == "pwr" else 1.8}" stroke-linecap="round" stroke-linejoin="round"/>')
    for (c, r), (x, y) in ((pts[0], xy[0]), (pts[-1], xy[-1])):
        if float(c).is_integer() and float(r).is_integer():
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{colr}" stroke="#fff" stroke-width="0.6"/>')

def draw_fix(v, b, col, row, lab=None):
    x, y = hp(v, b, col, row)
    r = 2.9 * v.s
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#f1f5f9" fill-opacity="0.7" stroke="#64748b" stroke-width="1" stroke-dasharray="3 2"/>')
    w(f'<line x1="{x - 4:.1f}" y1="{y:.1f}" x2="{x + 4:.1f}" y2="{y:.1f}" stroke="#64748b" stroke-width="0.9"/>')
    w(f'<line x1="{x:.1f}" y1="{y - 4:.1f}" x2="{x:.1f}" y2="{y + 4:.1f}" stroke="#64748b" stroke-width="0.9"/>')
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.6 * v.s:.1f}" fill="none" stroke="#0f172a" stroke-width="1.3"/>')
    if lab:
        text(x - 1.9 * v.s - 1, y - 1.9 * v.s, lab, 7.5, '#0f172a', '700', anchor='end', halo=True)

def label(v, X, Y, t, colr, size=8, anchor='middle', dy=0, weight='700'):
    x, y = v.px(X, Y)
    text(x, y + dy, t, size, colr, weight, anchor=anchor, halo=True)

# ---------------------------------------------------------------- the carrier views
def carrier_view(v, top):
    draw_board(v, 'A')
    draw_board(v, 'B')
    if top:
        draw_sockets(v)
    # module envelope and assumed outline
    if top:
        v.rect(RX(17) - 1.2, RX(3) - 1.3, cy('B', 11) - 1.0, cy('B', 18) + 1.4, rx=2, fill='none',
               stroke='#047857', stroke_width=1, stroke_dasharray='4 3')
        # assumed 25 x 18 module, header at its front edge on row 13, terminal at the rear
        mx0 = RX(13) - 1.5
        v.rect(mx0, mx0 + 25, 60.85, 78.85, rx=2, fill='#ecfdf5', fill_opacity='0.85',
               stroke='#047857', stroke_width=1.4)
        v.rect(mx0 + 25 - 7.5, mx0 + 25, 63.0, 74.0, rx=1, fill='#dbeafe', stroke='#047857', stroke_width=1)
        label(v, mx0 + 10, 70.3, 'SN65HVD230', '#047857', 8)
        label(v, mx0 + 10, 70.3, 'face up, H/L at rear', '#047857', 7, dy=10, weight=None)
        label(v, mx0 + 21.2, 76.9, 'H L', '#1d4ed8', 7, weight='700')
    # sockets pads (solder side shows them as pads)
    if not top:
        for b, col, lab in SOCKETS:
            colr = "#0f766e" if b == "A" else "#b45309"
            for r in range(1, 25):
                x, y = hp(v, b, ci(col), r)
                w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.9" fill="#e2e8f0" stroke="{colr}" stroke-width="1"/>')
            snipped(v, b, ci(col), colr)
    boxes = {}
    for b, pins, entry, name, colr in TERMS:
        boxes[name] = draw_terminal(v, b, pins, entry, name, colr, top)
    for b, pins, name in MALE:
        boxes[name] = draw_male(v, b, pins, name, top)
    for b, a, c, lab in RES:
        draw_res(v, b, a, c, lab, top)
    for b, m, p, lab in CAPS:
        draw_cap(v, b, m, p, lab, top)
    b, pins = XCVR_SOCKET
    X0, X1 = RX(13) - 1.27, RX(13) + 1.27
    if top:
        v.rect(X0, X1, cy(b, ci('n')) - 1.27, cy(b, ci('q')) + 1.27, rx=0.8, fill='#111827',
               fill_opacity='0.85', stroke='#047857', stroke_width=1)
    for col, r, lab in pins:
        x, y = hp(v, b, ci(col), r)
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.2 if top else 3.1}" fill="{"#fff" if top else "#e2e8f0"}" stroke="#047857" stroke-width="1.1"/>')
    for b, c, r, lab, _ in FIX:
        draw_fix(v, b, c, r, lab)
    if top:
        draw_discovery(v)
    return boxes

def carrier_labels_top(v, boxes):
    # Discovery
    label(v, -15, 13.0, 'STM32F4DISCOVERY above', '#4338ca', 10)
    label(v, -15, 13.0, 'plugs into the four 1x25 sockets', '#4338ca', 8, dy=13, weight=None)
    label(v, RX(25), -3.4, 'row 25: no hole', '#0f766e', 6.5, anchor='start', weight=None)
    label(v, 16, 26.5, 'CN1 ST-LINK', '#4338ca', 8, weight=None)
    label(v, 16, 26.5, 'overhangs the boards', '#4338ca', 7, dy=11, weight=None)
    label(v, 16, 26.5, '28 mm to the rear', '#4338ca', 7, dy=21, weight=None)
    # sockets
    label(v, RX(24) - 2.2, cy('A', 9) + 1.3, 'P1', '#0f766e', 9, anchor='end')
    label(v, RX(24) - 2.2, cy('B', 8) + 1.3, 'P2', '#b45309', 9, anchor='end')
    # terminals and headers
    X0, X1, Y0, Y1 = boxes['6V IN']
    label(v, (X0 + X1) / 2, Y0 - 1.2, '6V IN', '#d97706', 8)
    label(v, RX(1) + 2.2, cy('A', 9) + 0.9, 'pin 1', '#0f766e', 7, anchor='start')
    label(v, RX(1) + 2.2, cy('B', 7) + 0.9, 'pin 1', '#b45309', 7, anchor='start')
    X0, X1, Y0, Y1 = boxes['SERVO']
    label(v, (X0 + X1) / 2, Y0 - 1.6, 'SERVO', '#334155', 7.5)
    X0, X1, Y0, Y1 = boxes['I2C-B']
    label(v, (X0 + X1) / 2, Y0 - 1.6, 'I2C-B', '#7c3aed', 7.5)
    X0, X1, Y0, Y1 = boxes['I2C-A']
    label(v, (X0 + X1) / 2, Y0 - 1.6, 'I2C-A', '#7c3aed', 7.5)
    X0, X1, Y0, Y1 = boxes['CAN']
    label(v, X1 + 1.2, (Y0 + Y1) / 2, 'CAN', '#1d4ed8', 8, anchor='start')
    label(v, X1 + 1.2, (Y0 + Y1) / 2, 'H L GND', '#1d4ed8', 6.5, anchor='start', dy=10, weight=None)
    X0, X1, Y0, Y1 = boxes['5V IN']
    label(v, (X0 + X1) / 2, Y1 + 3.6, '5V IN', '#dc2626', 8)
    X0, X1, Y0, Y1 = boxes['TERM']
    label(v, X0 - 0.8, Y0 + 5.2, 'TERM', '#1d4ed8', 7.5, anchor='end')
    label(v, RX(8), -17.8, 'C2 470µF', '#a16207', 7)
    x, y = v.px(RX(10), cy('A', 8))
    text(x, y - 7, 'R4 1k', 7, '#1e40af', '700', anchor='middle', halo=True)
    label(v, RX(23) - 2.2, cy('B', 11) + 0.9, 'R3 120R', '#1e40af', 7, anchor='end')
    label(v, RX(15.5), 64.5, 'module', '#047857', 6.5, weight=None)
    label(v, RX(15.5), 64.5, 'envelope', '#047857', 6.5, weight=None, dy=8)
    label(v, RX(15.5), 64.5, 'rows 3-17', '#047857', 6.5, weight=None, dy=16)

PIN_LAB = {  # (board, col, row): (text, level, anchor) - B's in the gap, A's over A's inner columns
    ('B', 'g', 17): ('P2-33 PD1', 1, 'start'), ('B', 'h', 18): ('P2-36 PD0', 0, 'end'),
    ('A', 'i', 14): ('P1-27 PE9', 0, 'start'),
    ('A', 'j', 17): ('P1-34 PB10', 1, 'start'), ('A', 'i', 18): ('P1-35 PB11', 0, 'end'),
}
# rows 1-3 carry the bridges, so their pins are called out beyond the rear edge instead
END_LAB = [('B', 'g', ['g1  P2-1 GND', 'g2  P2-3 5V', 'g3  P2-5 3V'], (1, 2, 3)),
           ('A', 'i', ['i1  P1-1 GND', 'j1  P1-2 GND'], (1,))]

def carrier_labels_bottom(v):
    _, yb = v.px(0, BOARD['B']['edge'][0])      # B's inner edge (lower in this view)
    _, ya = v.px(0, cy('A', 12))                # A's inner columns, clear of every wire
    for (b, col, r), (t, lvl, anc) in PIN_LAB.items():
        x, y = hp(v, b, ci(col), r)
        colr = '#0f766e' if b == 'A' else '#b45309'
        ty = yb + 12 + 11 * lvl if b == 'B' else ya - 11 * lvl
        w(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ty - (3 if b == "B" else -3):.1f}" stroke="{colr}" stroke-width="0.8"/>')
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="none" stroke="{colr}" stroke-width="1.3"/>')
        text(x + (3 if anc == 'start' else -3), ty + 3, t, 7, colr, '700', anchor=anc, halo=True)
    xe, _ = v.px(BX[1], 0)
    for b, col, lines, rows in END_LAB:
        colr = '#0f766e' if b == 'A' else '#b45309'
        for r in rows:
            x, y = hp(v, b, ci(col), r)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="none" stroke="{colr}" stroke-width="1.3"/>')
        x, y = hp(v, b, ci(col), 1)
        w(f'<line x1="{x + 4.2:.1f}" y1="{y:.1f}" x2="{xe + 6:.1f}" y2="{y:.1f}" stroke="{colr}" stroke-width="0.8"/>')
        y0 = y - (len(lines) - 1) * 5.5 + 2.5
        for i, t in enumerate(lines):
            text(xe + 9, y0 + i * 11, t, 7, colr, '700', halo=True)

def draw_bridges(v):
    # the one unsupported span of each bridge: A r -> B a, 12.7 mm across the 5.9 mm gap
    for net, (ba, ca, ra), (bb, cb, rb) in BRIDGES:
        xa, ya = hp(v, ba, ca, ra)
        xb, yb = hp(v, bb, cb, rb)
        colr = NET[net]
        for sw, sc in ((4.2, colr), (1.3, '#e5e7eb')):
            w(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>')
    xe, _ = v.px(BX[1], 0)
    _, yg = v.px(0, (BOARD['A']['edge'][1] + BOARD['B']['edge'][0]) / 2)
    text(xe + 9, yg - 2, 'GND bridge, row 1', 7, NET['GND'], '700', halo=True)
    text(xe + 9, yg + 8, '3V3 bridge, row 3', 7, NET['3V3'], '700', halo=True)

def draw_links(v):
    for net, (b, c, r) in LINKS:
        x, y = hp(v, b, c, r)
        colr = NET[net]
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="none" stroke="{colr}" stroke-width="1.4"/>')

# ---------------------------------------------------------------- board C
# Rows 1-24 run across the vehicle (row 1 at the vehicle's right), columns a-j run
# front to rear. The USB-C socket for the FRDM's J1 is tied down at the row-1 end, opening
# out; the two terminals sit at the row-24 end. Both face the plate edges.
C_COLS, C_ROWS = 10, 24
C_EDGE_X, C_EDGE_Y = (-5.79, 58.42 + 5.79), (-3.57, 22.86 + 3.57)

def c_hole(col, row):
    return (row - 1) * P, (col - 1) * P

C_TERMS = [   # pins, entry (+X, the row-24 end), name, note
    ([('a', 24, '+5V'), ('c', 24, 'GND')], '+X', 'IN 5V', 'Bauer via SW2'),
    ([('g', 24, '+5V'), ('i', 24, 'GND')], '+X', 'TO STM32', 'to B 5V IN'),
]
C_RES = [(('g', 8), ('g', 12), 'R1 10k'), (('i', 8), ('i', 12), 'R2 10k')]

# The KUOQIY 6-wire USB-C female socket (BOM 5.1), lying on its side with its flange flush
# at the row-1 edge. The flange is 16.7 x 10.3 and the body 12.0 x 5.3, centred on it, so the
# body rides 2.5 mm off the board and clears the pan head of the e4 screw beneath it.
C_SOCKET = dict(y=11.43, flange=(-5.79, -3.79), flange_w=16.7, body=(-3.79, 10.21), body_w=12.0,
                flange_h=10.3, body_h=5.3)
# pigtail wire -> landing hole, cut to about 20 mm: (label, colour, col, row, exit Y on the body)
C_PIGTAIL = [('V', '#dc2626', 'a', 7, 7.2), ('G', '#111827', 'c', 7, 9.0),
             ('CC1', '#16a34a', 'g', 7, 13.8), ('CC2', '#eab308', 'i', 7, 15.6)]
C_CUT = [('D-', '#e5e7eb', 10.8), ('D+', '#1e3a8a', 12.2)]  # cut short, each insulated alone
C_TIES = [2, 6]              # zip ties at these rows, through 3 mm holes drilled at b and i
C_FIX = [(5, 4, 'C1 fix', '(99.24, 38.76)'), (5, 21, 'C2 fix', '(99.24, 81.76)')]
C_WIRES = [
    ('5V', [(1, 1), (1, 24)], 'bare'),                        # 5 V spine, column a
    ('GND', [(3, 1), (3, 24)], 'bare'),                       # GND spine, column c
    ('5V', [(7, 24), (7, 23.5), (1, 23.5), (1, 24)], 'pwr'),  # TO STM32 +
    ('GND', [(9, 24), (9, 24.5), (3, 24.5), (3, 24)], 'pwr'), # TO STM32 -
    ('CC', [(7, 7), (7, 8)], 'bare'),                         # CC1 landing g7 to R1, g8
    ('CC', [(9, 7), (9, 8)], 'bare'),                         # CC2 landing i7 to R2, i8
    ('5V', [(7, 12), (9, 12)], 'bare'),                       # R1 / R2 tops
    ('5V', [(7, 12), (7, 14.5), (1.5, 14.5), (1.5, 15), (1, 15)], 'ins'),   # tops to the 5 V spine
]

def draw_socket(v, top, hf):
    sk, yc = C_SOCKET, C_SOCKET['y']
    tie = lambda r: [(ci('b'), r), (ci('i'), r)]
    for r in C_TIES:                                  # the 3 mm holes, both sides
        for c, rr in tie(r):
            x, y = hf(c, rr)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.5 * v.s:.1f}" fill="#334155" stroke="#0f172a" stroke-width="0.8"/>')
    if top:
        v.rect(sk['body'][0], sk['body'][1], yc - sk['body_w'] / 2, yc + sk['body_w'] / 2, rx=2,
               fill='#1f2937', stroke='#0f172a', stroke_width=1.2)
        v.rect(sk['flange'][0], sk['flange'][1], yc - sk['flange_w'] / 2, yc + sk['flange_w'] / 2, rx=1.5,
               fill='#111827', stroke='#0f172a', stroke_width=1.2)
        for lab, colr, col, row, ye in C_PIGTAIL:
            a_, m_, b_ = v.px(sk['body'][1], ye), v.px(sk['body'][1] + 2.2, ye), hf(ci(col), row)
            w(f'<polyline points="{a_[0]:.1f},{a_[1]:.1f} {m_[0]:.1f},{m_[1]:.1f} {b_[0]:.1f},{b_[1]:.1f}" fill="none" stroke="{colr}" stroke-width="2.4" stroke-linecap="round"/>')
            w(f'<circle cx="{b_[0]:.1f}" cy="{b_[1]:.1f}" r="2.6" fill="{colr}" stroke="#fff" stroke-width="0.6"/>')
        for lab, colr, ye in C_CUT:
            a_, b_ = v.px(sk['body'][1], ye), v.px(sk['body'][1] + 1.6, ye)
            w(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="{colr}" stroke-width="2.4"/>')
            w(f'<rect x="{b_[0]:.1f}" y="{b_[1] - 2:.1f}" width="6" height="4" rx="1" fill="#475569"/>')
        for r in C_TIES:
            (xa, ya), (xb, yb) = [hf(c, rr) for c, rr in tie(r)]
            w(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#e5e7eb" stroke-width="{2.5 * v.s:.1f}" stroke-opacity="0.9"/>')
            w(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="2 2"/>')
        lx, ly = v.px(C_EDGE_X[0] - 3.2, yc)
        text(lx, ly - 12, 'USB-C SOCKET', 8, '#1e40af', '700', anchor='end')
        text(lx, ly - 2, 'opening out, C-to-C', 6.5, '#64748b', anchor='end')
        text(lx, ly + 7, 'cable to FRDM J1', 6.5, '#64748b', anchor='end')
        text(lx, ly + 18, 'zip ties at rows 2, 6', 6.5, '#64748b', anchor='end')
        text(lx, ly + 27, 'D−/D+ cut, insulated', 6.5, '#64748b', anchor='end')
        x, y = hf(5, 4)                               # the e4 screw, under the body
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.25 * v.s:.1f}" fill="none" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="3 2"/>')
    else:
        for lab, colr, col, row, ye in C_PIGTAIL:
            x, y = hf(ci(col), row)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="#e2e8f0" stroke="{colr}" stroke-width="1.6"/>')
        for r in C_TIES:
            (xa, ya), (xb, yb) = [hf(c, rr) for c, rr in tie(r)]
            w(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#cbd5e1" stroke-width="{2.5 * v.s:.1f}" stroke-opacity="0.8"/>')


def board_c(v, top):
    hf = lambda c, r: v.px(*c_hole(c, r))
    v.rect(C_EDGE_X[0], C_EDGE_X[1], C_EDGE_Y[0], C_EDGE_Y[1], rx=4, fill='#f0fdf4', stroke='#15803d', stroke_width=1.6)
    for c in range(1, C_COLS + 1):
        for r in range(1, C_ROWS + 1):
            x, y = hf(c, r)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="#fff" stroke="#a3b18a" stroke-width="0.7"/>')
    for c in range(1, C_COLS + 1):
        x, y = v.px(C_EDGE_X[0], (c - 1) * P)
        text(x - 4, y + 2.5, COL[c - 1], 7, '#15803d', anchor='end')
    for r in range(1, C_ROWS + 1):
        x, y = v.px((r - 1) * P, C_EDGE_Y[1] if v.flip else C_EDGE_Y[0])
        text(x, y - 3, str(r), 6.5, '#64748b', anchor='middle')
    for col, row, lab, ch in C_FIX:
        x, y = hf(col, row)
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.9 * v.s:.1f}" fill="#f1f5f9" fill-opacity="0.7" stroke="#64748b" stroke-width="1" stroke-dasharray="3 2"/>')
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.6 * v.s:.1f}" fill="none" stroke="#0f172a" stroke-width="1.3"/>')
    for pins, entry, name, note in C_TERMS:
        cs = [ci(p_[0]) for p_ in pins]
        Xc = (pins[0][1] - 1) * P
        Y0, Y1 = (min(cs) - 1) * P - 2.54, (max(cs) - 1) * P + 2.54
        if top:
            v.rect(Xc - 3.8, Xc + 3.8, Y0, Y1, rx=1.5, fill='#dbeafe', stroke='#1e40af', stroke_width=1.4)
            Xe = Xc - 3.8 if entry == '-X' else Xc + 3.8
            a_, b_ = v.px(Xe, Y0), v.px(Xe, Y1)
            w(f'<line x1="{a_[0]:.1f}" y1="{a_[1]:.1f}" x2="{b_[0]:.1f}" y2="{b_[1]:.1f}" stroke="#1e40af" stroke-width="3.2"/>')
            lx, ly = v.px(C_EDGE_X[0] - 3.2 if entry == '-X' else C_EDGE_X[1] + 1.2, (Y0 + Y1) / 2)
            anc = 'end' if entry == '-X' else 'start'
            text(lx, ly - 1, name, 8, '#1e40af', '700', anchor=anc)
            text(lx, ly + 9, note, 6.5, '#64748b', anchor=anc)
        for col, r, lab in pins:
            x, y = hf(ci(col), r)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.9 if top else 3.4}" fill="{"#fff" if top else "#e2e8f0"}" stroke="#1e40af" stroke-width="1.3"/>')
            if top:
                text(x + (9 if entry == '-X' else -9), y + 2.5, lab, 5.8, '#1e40af', '700',
                     anchor='start' if entry == '-X' else 'end', halo=True)
    draw_socket(v, top, hf)
    for a_, c_, lab in C_RES:
        xa, ya = hf(ci(a_[0]), a_[1])
        xb, yb = hf(ci(c_[0]), c_[1])
        if top:
            w(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#94a3b8" stroke-width="1.4"/>')
            mx, my = (xa + xb) / 2, (ya + yb) / 2
            w(f'<rect x="{mx - 13:.1f}" y="{my - 4.5:.1f}" width="26" height="9" rx="3" fill="#bfdbfe" stroke="#1e40af" stroke-width="1"/>')
            text(mx, my - 7, lab, 6.5, '#1e40af', '700', anchor='middle', halo=True)
        for x, y in ((xa, ya), (xb, yb)):
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{"#fff" if top else "#e2e8f0"}" stroke="#1e40af" stroke-width="1.1"/>')
    draw_cap(v, 'C', ('c', 12), ('a', 12), 'C1', top, board_hole=lambda cc, rr: hf(ci(cc), rr))
    if top:
        x, y = hf(ci('b'), 12)
        text(x, y + 3, 'C1', 8, '#a16207', '700', anchor='middle')
        x, y = hf(ci('e'), 12)
        text(x + 4, y + 3, '470µF', 6.5, '#a16207', '700', anchor='start', halo=True)
        _, yb = v.px(0, C_EDGE_Y[1])
        for col, row, lab, ch in C_FIX:                # below the board, clear of the socket
            x, y = hf(col, row)
            w(f'<line x1="{x:.1f}" y1="{y + 2.9 * v.s:.1f}" x2="{x:.1f}" y2="{yb + 4:.1f}" stroke="#64748b" stroke-width="0.7" stroke-dasharray="2 2"/>')
            text(x, yb + 13, f'{ch} · e{row}', 6.5, '#0f172a', '700', anchor='middle', halo=True)
    else:
        for net, pts, kind in C_WIRES:
            draw_wire(v, net, 'C', pts, kind, hfun=hf)
        x, y = hf(1.5, 17)
        text(x, y + 3, '5 V spine, col a', 7, '#dc2626', '700', anchor='middle', halo=True)
        x, y = hf(3.5, 17)
        text(x + 2, y + 16, 'GND spine, col c', 7, '#111827', '700', anchor='middle', halo=True)

# ---------------------------------------------------------------- sheet
if __name__ == "__main__":
    OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stm32-carrier.svg')
    W, H = 1720, 1300
    w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">')
    w(f'<rect width="{W}" height="{H}" fill="#fbfaf8"/>')
    text(40, 30, 'NEXUS - STM32 carrier and 5 V split board: soldering and wiring', 18, '#1a1a1a', '700')
    text(40, 49, 'Kit perfboards (BOM 5.11), 2.54 grid · Boards A and B, both 5×7 cm (18 × 24 holes), under P1 and P2, 5.9 mm apart · Board C 3×7 cm (10 × 24), the 5 V split · MEC-08 / MEC-15 / HW-19', 10.5, '#666')
    text(40, 66, 'Hole names: board + column letter + ROW NUMBER. On A and B the row number is the header row, so row n carries pins 2n-1 and 2n; row 25 (pins 49/50, GND) has no hole. P1 odd pins sit OUTBOARD (col i), P2 odd pins sit INBOARD (col g) - UM1472 Fig. 10.', 9.5, '#b45309')
    text(40, 80, 'Parts on the component side, every wire on the solder side. Bare tinned links only where drawn bare; everything else is insulated, soldered at both ends, so crossings are fine. Nothing on the Discovery footprint stands taller than a resistor.', 9.5, '#b45309')

    # views
    VX1, VX2, VY = 70, 590, 150
    vt = View(VX1, VY, XMIN, YMIN, YMAX, flip=False)
    vb = View(VX2, VY, XMIN, YMIN, YMAX, flip=True)
    text(VX1 - 40, 108, 'A + B  COMPONENT SIDE  (from above, front LEFT)', 12, '#1a1a1a', '700')
    text(VX1 - 40, 123, 'P1 on the vehicle right (top), P2 on the vehicle left (bottom) - chassis-layout convention', 8.5, '#64748b')
    text(VX2 - 30, 108, 'A + B  SOLDER SIDE  (turned over about the long axis)', 12, '#1a1a1a', '700')
    text(VX2 - 30, 123, 'front still LEFT, so P2 is now on TOP and every column reads upside down', 8.5, '#64748b')
    row_labels(vt, VY - 6)
    row_labels(vb, VY - 6)
    _, yb0 = vt.px(0, YMIN)
    text(vt.px(RX(1), 0)[0] + 16, VY - 6, '◀ header row  (rear ▶)', 6.5, '#64748b')

    boxes = carrier_view(vt, True)
    carrier_labels_top(vt, boxes)
    carrier_view(vb, False)
    for net, b, pts, kind in WIRES:
        draw_wire(vb, net, b, pts, kind)
    draw_bridges(vb)
    draw_links(vb)
    carrier_labels_bottom(vb)
    # a few solder-side callouts
    x, y = hp(vb, 'A', 5.5, 10)
    text(x, y + 3, 'GND spine, col e', 7, '#111827', '700', anchor='middle', halo=True)
    x, y = hp(vb, 'A', 0.5, 8)
    text(x, y + 3, '6 V spine, col a', 7, '#d97706', '700', anchor='middle', halo=True)
    x, y = hp(vb, 'B', 9.5, 11)
    text(x, y + 3, 'GND spine, col j', 7, '#111827', '700', anchor='middle', halo=True)
    x, y = hp(vb, 'B', 18, 5)
    text(x, y + 3, 'module H / L links in at m3, o3', 6.8, '#1d4ed8', '700', anchor='middle', halo=True)

    # front/rear footers under the views
    for v in (vt, vb):
        x0, y0 = v.px(XMIN, YMAX if not v.flip else YMIN)
        x1, _ = v.px(XMAX, 0)
        text((x0 + x1) / 2, y0 + 22, 'front ◀  boards 70 mm + Discovery overhang = 98 mm  ▶ rear (fascia)', 8.5, '#64748b', anchor='middle')
        text((x0 + x1) / 2, y0 + 34, 'overall width 106 mm · A1 B1 A2 B2: ⌀3.2 holes onto existing plate-2 holes, 10 mm M2.5 standoffs', 8.5, '#64748b', anchor='middle')

    # board C views
    CY = 760
    text(VX1 - 30, CY - 42, 'C  5 V SPLIT BOARD  (component side)', 12, '#1a1a1a', '700')
    text(VX1 - 30, CY - 27, 'across the plate-2 waist, x 85.5-115.5: row 1 at the vehicle right, column a to the front · socket opening faces the vehicle right', 8.5, '#64748b')
    text(VX2 - 30, CY - 42, 'C  SOLDER SIDE  (turned over about the long axis)', 12, '#1a1a1a', '700')
    text(VX2 - 30, CY - 27, 'spines in bare tinned 18 AWG, TO STM32 in 18 AWG (thick), the CC network in thin wire', 8.5, '#64748b')
    vc_t = View(VX1 + 70, CY, C_EDGE_X[0], C_EDGE_Y[0], C_EDGE_Y[1], flip=False, scale=4.6)
    vc_b = View(VX2 + 70, CY, C_EDGE_X[0], C_EDGE_Y[0], C_EDGE_Y[1], flip=True, scale=4.6)
    board_c(vc_t, True)
    board_c(vc_b, False)
    text(VX1 - 30, CY + 165, 'Socket first: meter CC1 and CC2 to V and to G, all four open - a socket with its own Rd (5.1k) or Rp cannot be the source.', 8.4, '#b45309')
    text(VX1 - 30, CY + 179, 'Fit the e4 pan-head screw before the socket: the body rides 2.5 mm up on its flange, over the head. Ties through 3 mm holes at b2 / i2 and b6 / i6, the second one over the pigtail.', 8.4, '#b45309')

    # ---------------------------------------------------------------- right column
    RX0 = 1130
    def table(y, title, head, rows, colx, rowh=19, sizes=(8.4, 7.9)):
        text(RX0, y, title, 12, '#1a1a1a', '700')
        w(f'<line x1="{RX0}" y1="{y + 8}" x2="{W - 40}" y2="{y + 8}" stroke="#e2e8f0"/>')
        y += 16
        w(f'<rect x="{RX0}" y="{y}" width="{W - 40 - RX0}" height="{rowh}" fill="#f1f5f9" stroke="#cbd5e1"/>')
        for i, h in enumerate(head):
            text(RX0 + colx[i], y + 13, h, 8.5, '#334155', '700')
        y += rowh
        for k, row in enumerate(rows):
            colr = row[0]
            w(f'<rect x="{RX0}" y="{y}" width="{W - 40 - RX0}" height="{rowh}" fill="{"#ffffff" if k % 2 == 0 else "#f8fafc"}" stroke="#e2e8f0"/>')
            if colr:
                w(f'<rect x="{RX0 + 3}" y="{y + 5}" width="4" height="{rowh - 10}" fill="{colr}"/>')
            for i, cell in enumerate(row[1:]):
                text(RX0 + colx[i], y + 13, cell, sizes[0] if i == 0 else sizes[1],
                     '#1e293b' if i == 0 else '#475569', '700' if i == 0 else None)
            y += rowh
        return y

    net_rows = [
        (NET['5V'], '5 V', 'C IN 5V', 'C TO STM32 → B 5V IN (q21) → P2-3 / P2-4 (g2 = h2)'),
        (NET['5V'], '5 V FRDM', 'C IN 5V', 'socket red V (a7) · C1 + (a12) · R1 / R2 tops (g12 = i12 → a15)'),
        (NET['GND'], 'GND', 'C IN GND', 'C spine c → B 5V IN GND → spine j → P2-1/2 · CAN GND · XCVR GND'),
        (NET['GND'], 'GND (A)', 'B g1', 'bare row 1: B a1 → A r1 → j1 = i1 (P1-2, P1-1) · spine e → 6V IN, C2, SERVO, I2C'),
        (NET['3V3'], '3.3 V', 'P2-5 / P2-6', 'XCVR 3V3 (n13) · bare row 3: B a3 → A r3 → k3, never j3 · k3 → I2C-A VCC (c21)'),
        (NET['6V'], 'Servo 6 V', 'A 6V IN +', 'C2 + (c10) · SERVO + (c13) - touches nothing else'),
        (NET['PWM'], 'Servo PWM', 'P1-27 PE9', 'R4 1k (h12-h8) → SERVO SIG (c14)'),
        (NET['SCL'], 'I²C2 SCL', 'P1-34 PB10', 'I2C-B (c17) → I2C-A (c22)'),
        (NET['SDA'], 'I²C2 SDA', 'P1-35 PB11', 'I2C-B (c18) → I2C-A (c23)'),
        (NET['CTX'], 'CAN1_TX', 'P2-33 PD1', 'XCVR CTX (q13) - straight, not crossed'),
        (NET['CRX'], 'CAN1_RX', 'P2-36 PD0', 'XCVR CRX (p13)'),
        (NET['CANH'], 'CAN_H', 'module H', 'link → m3 → CAN H (m1) · R3 120R → TERM'),
        (NET['CANL'], 'CAN_L', 'module L', 'link → o3 → CAN L (o1) · TERM'),
        (NET['CC'], 'USB-C CC', 'C socket', 'green CC1 (g7) → R1 10k → 5 V · yellow CC2 (i7) → R2 10k → 5 V (source Rp, HW-02)'),
    ]
    y = table(100, 'NETLIST', ['Net', 'From', 'To'], net_rows, [12, 96, 190])

    ext_rows = [
        (None, 'C IN 5V', 'Bauer 50 W via SW2, 18 AWG pair (HW-17)'),
        (None, 'C TO STM32', '18 AWG pair to B 5V IN'),
        (None, 'C USB-C', 'socket on C, pigtail soldered: red a7, black c7, green g7, yellow i7 · C-to-C data cable to FRDM J1'),
        (None, 'C D+ / D−', 'white and blue cut short, each insulated on its own - never twisted together'),
        (None, 'A 6V IN', 'UBEC 6 V out, 18 AWG pair (HW-14)'),
        (None, 'A SERVO', 'servo plug: signal to row 14 (rear), brown/black to row 12'),
        (None, 'A I2C-A', 'INA226 GND, VCC, SCL, SDA - F-F leads, signal only'),
        (None, 'A I2C-B', 'motor module SCL / SDA / GND - never its 5 V pin'),
        (None, 'B CAN', 'twisted H, L + GND to DE-9 stub and FRDM P12 (HW-09, HW-18)'),
        (None, 'B TERM', 'jumper ON = this end terminated (120 Ω), OFF = open'),
    ]
    y = table(y + 26, 'WHAT PLUGS IN WHERE', ['Connector', 'Cable'], ext_rows, [12, 96])

    parts = [
        (None, 'Board A', '5×7 board · 2 × 1×25 female · 1 × 2p terminal · 1×3 + 1×3 + 1×4 male · C2 470µF · R4 1k'),
        (None, 'Board B', '5×7 board · 2 × 1×25 + 1 × 1×4 female · 3p + 2p terminal · 1×2 male + jumper cap · R3 120Ω'),
        (None, 'Board C', '3×7 board · 2 × 2p terminal · USB-C socket (5.1), 2 zip ties · C1 470µF · R1, R2 10k'),
        (None, 'From stock', 'caps: 2 of the 5 in 3.14 · resistors: 3.21 · module: 4.1 · headers, terminals: 5.11'),
        (None, 'Not in BOM', 'thin copper hook-up wire, 22-26 AWG, and bare tinned copper for the spines and bridges - not the CCA Dupont leads (5.7)'),
    ]
    y = table(y + 26, 'PARTS', ['Board', 'Fitted'], parts, [12, 82])

    fix_rows = [
        (None, 'A1', 'A g14, on grid', 'plate 2 M3 hole (148.18, 23.76), ⌀3.18'),
        (None, 'B1', 'B d14, on grid', 'plate 2 M2.5 hole (148.2, 72.2), ⌀2.71 - 0.18 mm'),
        (None, 'A2', 'A between c5 / d6', 'plate 2 M2.5 hole (169.88, 14.24) - mark from the plate'),
        (None, 'B2', 'B between o5 / o6', 'plate 2 M2.5 hole (169.88, 100.24) - under the module'),
        (None, 'C e4', 'C e4, on grid', 'plate 2 M3 hole (99.24, 38.76), ⌀3.18'),
        (None, 'C e21', 'C e21, on grid', 'plate 2 M3 hole (99.24, 81.76) - 43.00 = 17 rows + 0.18'),
    ]
    y = table(y + 26, 'FIXINGS  (MEC-15)', ['Fix', 'Board hole', 'Chassis hole'], fix_rows, [12, 62, 170])
    text(RX0, y + 16, 'All six: ⌀3.2 in the board, M2.5 × 10 standoff, M2.5 screws, washer in the ⌀3.18 holes.', 8.4, '#475569')
    text(RX0, y + 29, 'Header row 1 at chassis x 181.20 · A outboard edge y 5.11 · B outboard edge y 110.99 · gap y 55.11-60.99.', 8.4, '#475569')

    # ---------------------------------------------------------------- checks and notes (bottom band)
    NY = 985
    text(40, NY, 'CHECK BEFORE THE IRON IS HOT', 12, '#1a1a1a', '700')
    w(f'<line x1="40" y1="{NY + 8}" x2="{RX0 - 30}" y2="{NY + 8}" stroke="#e2e8f0"/>')
    checks = [
        '1  Count the holes: A and B need 18 × 24, C 10 × 24. The drawing assumes the usual kit counts; a board one row short moves everything.',
        '2  Cut four 1×25 strips from the 40-pin female headers and snip the 25th tail of each flush with the body. Dry-fit them on the Discovery,',
        '    boards A and B under them: pins on A i/j and B g/h, rows 1-24, and row 25 resting on the board margin with no hole under it.',
        '3  Solder the sockets WITH THE DISCOVERY PLUGGED IN - it is the only thing that sets the 53.34 mm between A and B. Tack two corners, check, finish.',
        '4  Measure the SN65HVD230 module: outline, pin order, and CANH-CANL unpowered. ~120 Ω means it carries its own terminator - remove it,',
        '    so TERM alone decides. Pin order drawn is the BOM\'s (3V3, GND, CRX, CTX): wire the socket to what the module actually prints.',
        '5  The kit terminals may be 5.0 mm, not 5.08: the 3p CAN block spans 10.0 vs 10.16 mm of holes. Push it in; do not drill.',
        '6  Before the Discovery goes back in: 5 V to GND not shorted · 6 V rail isolated from 5 V and 3V3 · 5 V on g2/h2 only · nothing on g4 (PH0) · A j3 (P1-4 VDD) not on 3V3.',
        '7  Fixings: drill A1, B1, C e4 and C e21 on the grid first. Screw A and B down with the Discovery in, then mark A2 and B2 from under the',
        '    plate through its holes, lift the carrier and drill them. No standoff may touch a bare spine: check each one before the screw goes in.',
    ]
    yy = NY + 26
    for c in checks:
        text(40, yy, c, 9, '#475569')
        yy += 15

    notes = [
        ('Why two 5×7 boards', [
            'The kit\'s 7×9 (24 × 30) takes all 100 pins, but the Discovery',
            'covers it, so no terminal or cap would have anywhere to go. Two 5×7s',
            'leave them outboard and meet 5.9 mm apart: each bridge is bare wire',
            'soldered along its row, 12.7 mm unsupported. Row 25 is GND only.',
        ]),
        ('What moved off the WAGOs', [
            'Both 470 µF caps and every resistor are now on a board. C2 sits at',
            'the servo header, where the stall current is. C1, R1 and R2 are on',
            'board C, which is the 5 V split: the FRDM\'s amps never cross the',
            'STM32 carrier, and the Rp pair sits beside the pigtail it serves.',
        ]),
        ('Grounds and supplies', [
            'The carrier\'s one ground lead is B 5V IN GND, back through C to the',
            '(−) WAGO (HW-06). The 6 V servo rail reaches C2 and SERVO only',
            '(HW-11). 3V3 comes from P2-5/6, never P1 VDD (JP1): 100 mA ceiling,',
            'the transceiver and INA226 logic only. R4 guards PE9 if the servo',
            'plug goes on one pin off.',
        ]),
    ]
    nx = 40
    ny = yy + 18
    for t, lines in notes:
        text(nx, ny, t, 9.3, '#1e293b', '700')
        for i, l in enumerate(lines):
            text(nx, ny + 14 + i * 12.5, l, 8.8, '#475569')
        nx += 350

    w(f'<line x1="40" y1="{H - 48}" x2="{W - 40}" y2="{H - 48}" stroke="#e2e8f0"/>')
    text(40, H - 32, 'Geometry: UM1472 Fig. 10 (board 66 × 97, outer rows 53.34 apart, 6.33 in from each edge, first row 33.82 from the CN1 edge) · Pins: UM1472 Table 5 and the P1/P2 schematic · P2-3/4 = 5V, P2-5/6 = 3V, P2-7 = PH0', 8.4, '#94a3b8')
    text(40, H - 18, 'Decisions: MEC-08 (carrier) · MEC-15 (kit boards) · HW-19 (5 V split board, selectable termination) · HW-06 · HW-09 · HW-11 · HW-18 · SVG is the master - PDFs are generated once the design is frozen.', 8.4, '#94a3b8')
    w('</svg>')

    open(OUT, 'w').write('\n'.join(out) + '\n')
