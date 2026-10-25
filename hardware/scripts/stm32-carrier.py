#!/usr/bin/env python3
"""The STM32 carrier's geometry, and the drawing made from it (MEC-15, HW-19).

    python3 stm32-carrier.py            # -> ../renders/stm32-carrier.svg

Everything above the sheet section is data and helpers with no side effects, so
../mechanical/scripts/animate-stm32-carrier.py imports it and builds the 3D assembly from the same
holes, parts and wires the drawing shows.
"""
import os
import sys

P = 2.54
S = 4.6                       # px per mm in the carrier views

# ---------------------------------------------------------------- geometry (mm)
# Carrier views: X along the vehicle (rear = +X, right), Y across (down = +Y).
# Grid row n sits at X = -(n-1)*P, row 1 at the rear: it is B's hole row n. The frame is the one the
# Discovery set (its header row n was grid row n) and the boards are still where it put them.
def RX(n):
    return -(n - 1) * P

BOARD = {
    # name: (cols, rows, Y of col 1, board Y edges, colour)
    'A': dict(cols=18, rows=24, y1=-20.32, edge=(-23.73, 26.27)),
    'B': dict(cols=18, rows=24, y1=35.56, edge=(32.15, 82.15)),
}
BX = (-64.21, 5.79)                  # a board whose hole 1 sits on grid row 1, 70 mm
# The tray (MEC-17) holds A one pitch forward of B, as the first A was built (2026-10-03): A's hole g sits on
# grid row g + 1. The new A and B (2026-10-25, for the Nucleo) go on the same tray holes, so that stays.
SHIFT = {'A': 1, 'B': 0}

# The NUCLEO-H533RE (MB1814, UM3121 Fig. 7): 70 x 82.5, ST-LINK USB-C (CN1) on the rear edge. Its two
# 2 x 19 ST morpho headers (CN7, CN10) point down. Their outer rows are 63.50 apart (25 pitches), 3.25 in
# from each long edge; row 1 is 31.70 from the CN1 edge and row 19 is 5.08 from the front edge. The
# headers are 4 pitches wider than the Discovery's P1 / P2, so each socket pair moves two columns outboard
# (A: i/j to g/h, B: g/h to i/j), and the board stays centred where the Discovery was. Header row k sits
# on grid row k + NUC_ROW0: five rows forward of the Discovery's row 1, for room behind CN1's plug.
NUC_ROWS = 19
NUC_ROW0 = 5
NUC = dict(x=(RX(1 + NUC_ROW0) - 18 * P - 5.08, RX(1 + NUC_ROW0) + 31.70), y=(-8.33, 61.67))
CN1_Y = 14.3                 # CN1, the ST-LINK USB-C, on the rear edge (UM3121 Fig. 7, +-0.3)
XMIN, XMAX = -64.21 - P, NUC['x'][1]


def NX(k):
    """X of Nucleo header row k."""
    return RX(k + NUC_ROW0)


def HX(b, g):
    """X of board b's hole row g."""
    return RX(g + SHIFT[b])


def bx(b):
    return BX[0] - SHIFT[b] * P, BX[1] - SHIFT[b] * P


def hdr_hole(b, k):
    """The board hole row under Nucleo header row k."""
    return k + NUC_ROW0 - SHIFT[b]
YMIN, YMAX = -23.73, 82.15

def cy(board, col):
    return BOARD[board]['y1'] + (col - 1) * P

COL = 'abcdefghijklmnopqr'

def ci(letter):
    return COL.index(letter) + 1

# ---------------------------------------------------------------- silkscreen names
# The geometry above indexes holes by (column, header row). The kit boards print their own
# names: letters A-X along the 70 mm side and numbers along the short side, A1 at the bottom
# left with the print readable. Every view shows each board that way up (front left), so on
# A and B header row 1 is letter X and row 24 is letter A; the numbers count up from the
# bottom of the component view.
# Board C's print is the other way round (Hedi, 2026-10-05, from the board): numbers 1-24 along the 70 mm side,
# letters A-J across the 30 mm side, A1 at the bottom left with components up and the USB-C socket on the left.
# That is how C is drawn here (row 1 on the left, column 1 at the top), so the letter counts up from the bottom
# row (column 10 = A, column 1 = J) and the number is the row.
LET = 'ABCDEFGHIJKLMNOPQRSTUVWX'


def silk(b, col, row):
    c = ci(col) if isinstance(col, str) else col
    if b in 'AB':
        return f'{LET[24 - row]}{19 - c}'
    return f'{LET[10 - c]}{row}'


def N(b, col, row):
    return f'{b}·{silk(b, col, row)}'

# ---------------------------------------------------------------- colours
NET = {
    '5V': '#dc2626', 'GND': '#111827', '3V3': '#db2777', '6V': '#d97706',
    'PWM': '#92400e', 'SCL': '#7c3aed', 'SDA': '#a855f7', 'CTX': '#0891b2',
    'CRX': '#0e7490', 'TERM': '#64748b', 'CANH': '#1d4ed8', 'CANL': '#60a5fa',
    'TERM1': '#64748b',
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
    return HX(board, row), BOARD[board]['y1'] + (col - 1) * P

# ---------------------------------------------------------------- component data
# Boards A (CN10 side) and B (CN7 side) are both 5x7 kit boards, 18 x 24; col a of A is outboard.
# Four 1x19 sockets, every tail in a hole: A's on hole rows 5-23, B's on 6-24. On each header the odd pins
# are one column and the even pins the other: CN10's even pins are its outer row, CN7's odd pins are its.
SOCKETS = [('A', 'g', 'CN10 even'), ('A', 'h', 'CN10 odd'), ('B', 'i', 'CN7 even'), ('B', 'j', 'CN7 odd')]
# The NUCLEO pins the carrier uses, by header and pin (UM3121 Table 17), and the net each one is on.
# FDCAN2 on PB12 / PB13 (AF9), I2C1 on PB6 / PB7 (AF4), TIM2_CH1 on PA0 (AF1): checked against the STM32H533
# datasheet, DS14539 Rev 3, March 2026. E5V takes the 5 V in with JP5 on [5-6]. Every CAN pin the part has is
# on CN10 and its only supply pins are on CN7, so the CAN and I2C parts sit on A and the power and the servo on B:
# one wire, 3V3, crosses between the boards.
NUC_PINS = {('CN10', 3): ('PB6', 'SCL'), ('CN10', 5): ('PB7', 'SDA'), ('CN10', 9): ('GND', 'GND'),
            ('CN10', 16): ('PB12', 'CRX'), ('CN10', 20): ('GND', 'GND'), ('CN10', 30): ('PB13', 'CTX'),
            ('CN7', 6): ('E5V', '5V'), ('CN7', 8): ('GND', 'GND'), ('CN7', 16): ('3V3', '3V3'),
            ('CN7', 19): ('GND', 'GND'), ('CN7', 20): ('GND', 'GND'), ('CN7', 22): ('GND', 'GND'),
            ('CN7', 28): ('PA0', 'PWM_MCU')}


def nuc_hole(hdr, pin):
    """(board, column, hole row) of a Nucleo morpho pin."""
    k = (pin + 1) // 2
    if hdr == 'CN10':
        return 'A', 'g' if pin % 2 == 0 else 'h', hdr_hole('A', k)
    return 'B', 'j' if pin % 2 else 'i', hdr_hole('B', k)

# screw terminals: board, [(col,row,label)], entry side ('-Y','+Y','+X'), name, colour
TERMS = [
    ('A', [('b', 19, 'H'), ('b', 21, 'L'), ('b', 23, 'GND')], '-Y', 'CAN', '#1d4ed8'),
    ('B', [('q', 8, '+6V'), ('q', 10, 'GND')], '+Y', '6V IN', '#d97706'),
    ('B', [('q', 13, '+5V'), ('q', 15, 'GND')], '+Y', '5V IN', '#dc2626'),
]
# male headers: board, [(col,row,label)], name, all with their pins across the board on one row. SERVO is a
# straight header on top. The two I2C headers are 90 degree headers fitted UNDER A, pointing forward: the plug
# lies in the 8 mm gap over the tray and its lead leaves by A's front edge, down through the tray window
# (MEC-17). Each is in the order of the module it takes, so a straight lead is right: the INA226 is VCC SDA
# SCL GND, the motor module's IIC port SCL SDA GND 5V (its 5 V, an output, lands on a pin with no wire), the
# LD-1501MG black, red, white (HW-21).
MALE = [
    ('B', [('o', 23, 'GND'), ('n', 23, '+6V'), ('m', 23, 'SIG')], 'SERVO'),
    ('A', [('j', 20, 'SCL'), ('k', 20, 'SDA'), ('l', 20, 'GND'), ('m', 20, 'NC')], 'I2C-B'),
    ('A', [('r', 20, '3V3'), ('q', 20, 'SDA'), ('p', 20, 'SCL'), ('o', 20, 'GND')], 'I2C-A'),
]
UNDER = {'I2C-B', 'I2C-A'}                   # fitted on the solder side


def header_boxes(b, pins, name):
    """A male header as 3D boxes (X0, X1, Y0, Y1, Z0, Z1, material), Z up from the board's top face (its underside
    is at -1.6). Straight on top: the spacer and the pin. 90 degrees UNDER the board: the leg comes down through the
    hole, bends and points forward (-X) inside the spacer, and the plug goes on there."""
    out = []
    for c, r, _ in pins:
        X, Y = hole(b, ci(c), r)
        if name in UNDER:
            zc = -1.6 - 1.27
            out += [(X - 3.8, X - 1.27, Y - 1.27, Y + 1.27, -1.6 - 2.54, -1.6, 'black'),
                    (X - 0.32, X + 0.32, Y - 0.32, Y + 0.32, zc - 0.32, 0.8, 'gold'),
                    (X - 9.8, X + 0.32, Y - 0.32, Y + 0.32, zc - 0.32, zc + 0.32, 'gold')]
        else:
            out += [(X - 1.27, X + 1.27, Y - 1.27, Y + 1.27, 0, 2.5, 'black'),
                    (X - 0.32, X + 0.32, Y - 0.32, Y + 0.32, -3.0, 8.5, 'gold')]
    return out


RES = [('B', ('k', 19), ('k', 23), 'R4 1k')]       # in the servo PWM; flat, under the Nucleo's edge
CAPS = [('B', ('n', 18), ('n', 20), 'C2')]         # (minus leg, plus leg)
# The SN65HVD230 module (BOM 4.1, 26.98 x 10.24) lies FLAT and, as bent (2026-10-03), FACE DOWN:
# upright it would hit plate 3. Its pins are bent 90 deg toward its component side into a 1x4
# socket on row XCVR_ROW, it points to the rear, and its screw terminal hangs under its far end.
# Face down, the header reads CTX, CRX, GND, 3V3 across the socket toward the vehicle's left.
# CAN H / L leave by the module's own 2-pin header, which points down when face down, into a
# 1x2 socket seven holes behind the 4-pin row; the screw terminal is not used. The module terminates this
# end of the bus with its own 120 ohm (HW-09), so the carrier has no terminator of its own.
XCVR_ROW = 17
XCVR_SOCKET = ('A', [('a', XCVR_ROW, 'CTX'), ('b', XCVR_ROW, 'CRX'), ('c', XCVR_ROW, 'GND'), ('d', XCVR_ROW, '3V3')])
CAN_ROW = XCVR_ROW - 7                     # 17.55 mm on the module, 17.78 on the grid
CAN_SOCKET = ('A', [('b', CAN_ROW, 'CANH'), ('c', CAN_ROW, 'CANL')])
MODULE = dict(length=26.98, width=10.24, terminal=3.74, pin_in=-0.3, canhl=17.25)
# pin_in: header face to the bent pins (negative: the bent legs stand just outside the face);
# canhl: header face to the 2-pin CANH / CANL header (BOM 4.1)


def xc(lab):
    """The printed name of the transceiver socket's pin carrying `lab` (CTX, CRX, GND, 3V3)."""
    col = next(c for c, r, l in XCVR_SOCKET[1] if l == lab)
    return silk(XCVR_SOCKET[0], col, XCVR_ROW)


def module_box():
    """(X0, X1, Y0, Y1) of the flat module, and its terminal's X start."""
    b, pins = XCVR_SOCKET
    X0 = HX(b, XCVR_ROW) - MODULE['pin_in']
    yc = cy(b, (ci(pins[0][0]) + ci(pins[-1][0])) / 2)     # the middle of the four pins
    return X0, X0 + MODULE['length'], yc - MODULE['width'] / 2, yc + MODULE['width'] / 2
# MEC-17 (2026-10-05): the three boards stand on one tray on their own four corner holes and nylon standoffs, so nothing is drilled and the
# old direct fixings F1-F6 (MEC-15) are gone. The kit boards' corner holes are CORNER_INSET in from the edges, as the tray is drawn.
CORNER_INSET = 2.5


def corner_holes(x0, x1, y0, y1):
    """The four corner holes of a board whose edges are x0..x1 (along the vehicle) and y0..y1 (across), in the drawing frame."""
    return [(x, y) for x in (x0 + CORNER_INSET, x1 - CORNER_INSET) for y in (y0 + CORNER_INSET, y1 - CORNER_INSET)]

# Wires, all insulated and all pad to pad: nothing is joined to another wire except at a pad,
# and no pad takes more than two wire ends. A net with several pins is a chain, part to part.
# Points are (column, header row) and may sit between holes, in the channels the wire runs
# along. kind: 'pwr' 18 AWG silicone copper (servo and FRDM current), 'ins' 22 AWG hook-up
# wire, 'lead' a component's own lead bent over to the next pad on the solder side.
WIRES = [
    # ---- board A, the CAN module and its terminal outboard
    ('CTX', 'A', [(7, 19), (6.5, 18.5), (1.5, 18.5), (1.5, 17.5), (1, 17)], 'ins'),          # PB13 to XCVR CTX
    ('CRX', 'A', [(7, 12), (6.5, 12.5), (2.5, 12.5), (2.5, 16.5), (2, 17)], 'ins'),          # PB12 to XCVR CRX
    ('GND', 'A', [(7, 14), (6.5, 14.5), (3.5, 14.5), (3.5, 16.5), (3, 17)], 'ins'),          # CN10-20 to XCVR GND
    ('GND', 'A', [(3, 17), (3.5, 17.5), (3.5, 22.5), (2, 23)], 'ins'),                      # XCVR GND to CAN GND
    ('CANH', 'A', [(2, 10), (1.5, 10.5), (0.5, 10.5), (0.5, 19.5), (1.5, 19.5), (2, 19)], 'ins'),   # module H to CAN H
    ('CANL', 'A', [(3, 10), (3.5, 10.5), (4.5, 10.5), (4.5, 20.5), (2.5, 20.5), (2, 21)], 'ins'),   # module L to CAN L
    # ---- board A, the two I2C headers under its front: SCL from PB6 to each, SDA from PB7 along both
    ('SCL', 'A', [(8, 6), (8.5, 5.5), (9.5, 5.5), (9.5, 19.5), (10, 20)], 'ins'),           # PB6 to I2C-B
    ('SCL', 'A', [(8, 6), (8.5, 6.5), (15.5, 6.5), (15.5, 18.5), (16, 19), (16, 20)], 'ins'),   # PB6 to I2C-A
    ('SDA', 'A', [(8, 7), (8.5, 7.5), (10.5, 7.5), (10.5, 19.5), (11, 20)], 'ins'),         # PB7 to I2C-B
    ('SDA', 'A', [(11, 20), (11.5, 19.5), (16.5, 19.5), (17, 20)], 'ins'),                  # I2C-B to I2C-A
    ('GND', 'A', [(8, 9), (8.5, 9.5), (12.5, 9.5), (12.5, 18.5), (12, 19), (12, 20)], 'ins'),   # CN10-9 to I2C-B GND
    ('GND', 'A', [(8, 9), (8.5, 8.5), (14.5, 8.5), (14.5, 18.5), (15, 19), (15, 20)], 'ins'),   # CN10-9 to I2C-A GND
    ('3V3', 'A', [(18, 20), (18.5, 19.5), (18.5, 17.5), (5.5, 17.5), (4, 17)], 'ins'),      # I2C-A VCC to XCVR 3V3
    # ---- board B: 5 V in to E5V, and the servo: 6V IN, C2, R4 and its header at the front
    ('5V', 'B', [(17, 13), (16.5, 12.5), (11.5, 12.5), (11.5, 7.5), (9.5, 7.5), (9, 8)], 'ins'),   # 5V IN + to CN7-6 E5V
    ('GND', 'B', [(17, 15), (16.5, 15.5), (9.5, 15.5), (9, 16)], 'ins'),                    # 5V IN - to CN7-22
    ('GND', 'B', [(17, 15), (18.5, 15.5), (18.5, 23.5), (15.5, 23.5), (15, 23)], 'ins'),    # 5V IN - to SERVO GND
    ('6V', 'B', [(17, 8), (16.5, 8.5), (16.5, 19.5), (14.5, 19.5), (14, 20)], 'pwr'),       # 6V IN + to C2 +
    ('6V', 'B', [(14, 20), (13.5, 20.5), (13.5, 22.5), (14, 23)], 'pwr'),                   # C2 + to SERVO +
    ('GND', 'B', [(17, 10), (17.5, 10.5), (17.5, 17.5), (14.5, 17.5), (14, 18)], 'pwr'),    # 6V IN - to C2 -
    ('GND', 'B', [(14, 18), (14.5, 18.5), (15.5, 18.5), (15.5, 22.5), (15, 23)], 'pwr'),    # C2 - to SERVO GND
    ('PWM', 'B', [(9, 19), (9.5, 19.5), (10.5, 19.5), (11, 19)], 'ins'),                    # PA0 to R4
    ('PWM', 'B', [(11, 23), (11.5, 22.5), (12.5, 22.5), (13, 23)], 'ins'),                  # R4 to SERVO SIG
]
# The one bridge: 3V3 is on CN7 (B) only, and the INA226 and the transceiver are on A. A's ground comes from
# its own CN10-9 and CN10-20, the Nucleo tying all its GNDs. A's hole row r and B's row r + 1 are the same X,
# so the bridge crossing at A row 18.5 leaves B on its row 19.5.
XWIRES = [
    ('3V3', [('B', 9, 13), ('B', 8.5, 13.5), ('B', 8.5, 19.5), ('B', 0.5, 19.5), ('A', 17.5, 18.5),
             ('A', 17.5, 19.5), ('A', 18, 20)], 'ins'),                          # CN7-16 to I2C-A VCC
]
LINKS = []                   # no links: CAN H / L reach the board through the module's 2-pin header

# ---------------------------------------------------------------- drawing helpers
def draw_board(v, b, grid_labels=True):
    cfg = BOARD[b]
    x0, x1 = bx(b)
    v.rect(x0, x1, cfg['edge'][0], cfg['edge'][1], rx=4, fill='#f0fdf4',
           stroke='#15803d', stroke_width=1.6)
    for c in range(1, cfg['cols'] + 1):
        for r in range(1, cfg['rows'] + 1):
            x, y = v.px(HX(b, r), cy(b, c))
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="#fff" stroke="#a3b18a" stroke-width="0.7"/>')
    if grid_labels:
        # column letters on the front (left) edge
        for c in range(1, cfg['cols'] + 1):
            x, y = v.px(x0, cy(b, c))
            text(x - 4, y + 2.5, str(19 - c), 7, '#15803d', anchor='end')
        # the printed letters, along whichever long edge is uppermost in this view
        ye = cfg['edge'][1] if v.flip else cfg['edge'][0]
        for r in range(1, cfg['rows'] + 1):
            x, y = v.px(HX(b, r), ye)
            text(x, y - 3, LET[24 - r], 6.5, '#15803d', '700', anchor='middle')
        x, y = v.px(x0, (cfg['edge'][0] + cfg['edge'][1]) / 2)
        w(f'<text transform="translate({x - 16:.1f},{y:.1f}) rotate(-90)" font-size="10" font-weight="700" fill="#15803d" text-anchor="middle">Board {b}</text>')

A1_RED = '#e11d48'


def a1_marker(v, corner, dx, dy, leg=6.0):
    """A red triangle in the board corner nearest printed hole A1, legs along the two edges.
    dx, dy point from the corner into the board (+1 / -1), in board millimetres."""
    X, Y = corner
    pts = [v.px(X, Y), v.px(X + dx * leg, Y), v.px(X, Y + dy * leg)]
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    w(f'<polygon points="{d}" fill="{A1_RED}" fill-opacity="0.9"/>')
    x, y = v.px(X + dx * leg * 0.3, Y + dy * leg * 0.3)
    text(x, y + 2.5, 'A1', 5.5, '#fff', '700', anchor='middle')


def board_a1(v, b, leg=6.0):
    # A and B: A1 is header row 24 (front) at column r - the front edge, high-Y side
    a1_marker(v, (bx(b)[0], BOARD[b]['edge'][1]), +1, -1, leg)


def row_labels(v, yline):
    # the Nucleo's header rows; each board prints its own letters along its edge
    for k in range(1, NUC_ROWS + 1):
        x, _ = v.px(NX(k), 0)
        text(x, yline, str(k), 6.5, '#64748b', anchor='middle')

# CN11 and CN12, the jumper parking headers on the Nucleo's underside, hang about 8.5 mm below it at the
# CN1 end, in line with the outer morpho rows (UM3121 Fig. 2). Past the boards' rear edges, over the tray.
CN11_12 = [(NUC['x'][1] - 5.6, -5.4), (NUC['x'][1] - 5.6, 58.6)]
# The Nucleo's tall parts, for the 3D mock: (side, X0, X1, Y0, Y1, height, material, what). Read off UM3121
# Fig. 7 at +-0.5 mm; heights are typical, not measured. 'top' stands on the PCB, 'under' hangs below it.
NUC_MOCK = [
    ('top', 8.6, 20.0, CN1_Y - 4.4, CN1_Y + 4.4, 3.2, 'usb', 'CN1 ST-LINK USB-C'),
    ('top', -64.4, -53.2, 34.7, 43.6, 3.2, 'usb', 'CN3 user USB-C'),
    ('top', -0.2, 10.0, 26.8, 37.2, 1.0, 'chip', 'STLINK-V3EC MCU'),
    ('top', -45.5, -33.5, 20.6, 32.6, 1.4, 'chip', 'STM32H533RE, LQFP64'),
    ('top', -7.1, 5.9, 1.3, 6.4, 8.5, 'black', 'JP5, 2 x 5, jumper on [5-6] for E5V'),
    ('top', 15.4, 17.9, 33.2, 38.3, 8.5, 'black', 'JP1 ST-LINK reset'),
    ('top', -42.2, -21.4, 49.6, 52.0, 8.5, 'black', 'CN5 ARDUINO'),
    ('top', -60.0, -44.4, 49.6, 52.0, 8.5, 'black', 'CN9 ARDUINO'),
    ('top', -38.3, -12.2, 1.3, 3.7, 8.5, 'black', 'CN6 ARDUINO'),
    ('top', -60.0, -39.5, 1.3, 3.7, 8.5, 'black', 'CN8 ARDUINO'),
    ('top', -13.1, -7.1, 32.0, 38.0, 3.5, 'btn_b', 'B1 USER'),
    ('top', -13.1, -7.1, 15.5, 21.5, 3.5, 'black', 'B2 RESET'),
    ('top', -12.0, -10.4, 8.8, 10.0, 0.6, 'led_g', 'LD2 user, PA5'),
    ('top', 14.3, 15.9, 4.4, 5.6, 0.6, 'led_g', 'LD1 COM'),
    ('top', 14.3, 15.9, -0.7, 0.5, 0.6, 'led_r', 'LD7 PWR'),
] + [('under', X - 2.5, X + 2.5, Y - 1.3, Y + 1.3, 8.5, 'black', 'CN11 / CN12 jumper park') for X, Y in CN11_12]


def draw_nucleo(v):
    v.rect(NUC['x'][0], NUC['x'][1], NUC['y'][0], NUC['y'][1], rx=3, fill='#eef2ff',
           fill_opacity='0.35', stroke='#4338ca', stroke_width=1.2, stroke_dasharray='7 4')
    v.rect(NUC['x'][1] - 7.3, NUC['x'][1] + 0.6, CN1_Y - 4.5, CN1_Y + 4.5, rx=1, fill='#cbd5e1',
           stroke='#4338ca', stroke_width=1)
    for X, Y in CN11_12:
        v.rect(X - 2.5, X + 2.5, Y - 1.3, Y + 1.3, rx=0.6, fill='none', stroke='#4338ca', stroke_width=0.9,
               stroke_dasharray='2 2')

def draw_sockets(v):
    for b, col, lab in SOCKETS:
        c = ci(col)
        colr = '#0f766e' if b == 'A' else '#b45309'
        v.rect(NX(NUC_ROWS) - 1.27, NX(1) + 1.27, cy(b, c) - 1.2, cy(b, c) + 1.2, rx=1,
               fill=colr, fill_opacity='0.22', stroke=colr, stroke_width=0.9)

def hp(v, b, c, r):
    X, Y = hole(b, c, r)
    return v.px(X, Y)

def pad(v, b, c, r, colr, rad=2.6):
    x, y = hp(v, b, c, r)
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{colr}"/>')

def draw_terminal(v, b, pins, entry, name, colr, top=True):
    cs = [ci(p[0]) for p in pins]
    rs = [p[1] for p in pins]
    Xs = [HX(b, r) for r in rs]
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

PLUG = 16.5                  # a 90 degree header's body and its Dupont plug, from the pin row forward, mm


def draw_male(v, b, pins, name, top=True):
    cs = [ci(p[0]) for p in pins]
    rs = [p[1] for p in pins]
    X0, X1 = HX(b, max(rs)) - 1.27, HX(b, min(rs)) + 1.27
    Y0 = cy(b, min(cs)) - 1.27
    Y1 = cy(b, max(cs)) + 1.27
    under = name in UNDER
    if top and not under:
        v.rect(X0, X1, Y0, Y1, rx=0.8, fill='#334155', stroke='#0f172a', stroke_width=0.8)
    if top and under:                       # seen through the board: where it is, nothing to solder here but its pins
        v.rect(X0, X1, Y0, Y1, rx=0.8, fill='none', stroke='#7c3aed', stroke_width=1, stroke_dasharray='3 2')
    if not top and under:                   # its body on the pin row, then the plug lying forward in the 8 mm gap
        v.rect(X1 - PLUG, X0, Y0 + 0.3, Y1 - 0.3, rx=1, fill='#ede9fe', fill_opacity='0.75', stroke='#7c3aed',
               stroke_width=0.9, stroke_dasharray='4 2')
        v.rect(X0 - 2.5, X1, Y0, Y1, rx=0.8, fill='#334155', stroke='#0f172a', stroke_width=0.8)
    for (col, r, lab) in pins:
        x, y = hp(v, b, ci(col), r)
        if top and not under:
            w(f'<rect x="{x - 1.6:.1f}" y="{y - 1.6:.1f}" width="3.2" height="3.2" fill="#fbbf24"/>')
        elif not top and under:
            w(f'<rect x="{x - 1.4:.1f}" y="{y - 1.4:.1f}" width="2.8" height="2.8" fill="#fbbf24"/>')
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
    if kind == 'lead':                        # a part's own lead, bent to the next pad
        w(f'<polyline points="{d}" fill="none" stroke="#64748b" stroke-width="2.4" stroke-linecap="round"/>')
        w(f'<polyline points="{d}" fill="none" stroke="#e5e7eb" stroke-width="1.0" stroke-linecap="round"/>')
        colr = '#64748b'
    else:
        w(f'<polyline points="{d}" fill="none" stroke="{colr}" stroke-width="{3.2 if kind == "pwr" else 1.8}" stroke-linecap="round" stroke-linejoin="round"/>')
    for (c, r), (x, y) in ((pts[0], xy[0]), (pts[-1], xy[-1])):
        if float(c).is_integer() and float(r).is_integer():
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{colr}" stroke="#fff" stroke-width="0.6"/>')

def draw_corner(v, x, y):
    """A corner fixing: the board hole and the 8 mm nylon standoff it carries (MEC-17)."""
    x, y = v.px(x, y)
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.9 * v.s:.1f}" fill="#f1f5f9" fill-opacity="0.7" stroke="#64748b" stroke-width="1" stroke-dasharray="3 2"/>')
    w(f'<line x1="{x - 4:.1f}" y1="{y:.1f}" x2="{x + 4:.1f}" y2="{y:.1f}" stroke="#64748b" stroke-width="0.9"/>')
    w(f'<line x1="{x:.1f}" y1="{y - 4:.1f}" x2="{x:.1f}" y2="{y + 4:.1f}" stroke="#64748b" stroke-width="0.9"/>')
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.6 * v.s:.1f}" fill="none" stroke="#0f172a" stroke-width="1.3"/>')

def label(v, X, Y, t, colr, size=8, anchor='middle', dy=0, weight='700'):
    x, y = v.px(X, Y)
    text(x, y + dy, t, size, colr, weight, anchor=anchor, halo=True)

# ---------------------------------------------------------------- the carrier views
def carrier_view(v, top):
    draw_board(v, 'A')
    draw_board(v, 'B')
    board_a1(v, 'A')
    board_a1(v, 'B')
    if top:
        draw_sockets(v)
    # module envelope and assumed outline
    if top:
        X0, X1, Y0, Y1 = module_box()
        v.rect(X0 - 1.5, X1 + 1.5, Y0 - 1.5, Y1 + 1.5, rx=2, fill='none',
               stroke='#047857', stroke_width=1, stroke_dasharray='4 3')
        v.rect(X0, X1, Y0, Y1, rx=1.5, fill='#1e3a8a', fill_opacity='0.55', stroke='#047857', stroke_width=1.4)
        v.rect(X1 - MODULE['terminal'], X1, Y0 + 0.4, Y1 - 0.4, rx=1, fill='none',
               stroke='#bfdbfe', stroke_width=1, stroke_dasharray='2 2')      # the terminal, underneath
        x, y = v.px(X0 + 7.5, (Y0 + Y1) / 2)            # plain white on the dark module, no halo
        text(x, y - 1, 'SN65HVD230', 7, '#ffffff', '700', anchor='middle')
        text(x, y + 8, 'FACE DOWN', 6, '#ffffff', anchor='middle')
        for col, r, lab in CAN_SOCKET[1]:                 # the 2-pin header, down into its socket
            X, Y = hole(CAN_SOCKET[0], ci(col), r)
            x, y = v.px(X + 2.0, Y)
            text(x, y + 2.5, lab[-1], 7, '#ffffff', '700', anchor='start')
    # sockets pads (solder side shows them as pads)
    if not top:
        for b, col, lab in SOCKETS:
            colr = "#0f766e" if b == "A" else "#b45309"
            for k in range(1, NUC_ROWS + 1):
                x, y = v.px(NX(k), cy(b, ci(col)))
                w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.9" fill="#e2e8f0" stroke="{colr}" stroke-width="1"/>')
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
    X0, X1 = HX(b, XCVR_ROW) - 1.27, HX(b, XCVR_ROW) + 1.27
    if top:
        v.rect(X0, X1, cy(b, ci(pins[0][0])) - 1.27, cy(b, ci(pins[-1][0])) + 1.27, rx=0.8, fill='#111827',
               fill_opacity='0.85', stroke='#047857', stroke_width=1)
    b2, pins2 = CAN_SOCKET
    if top:
        v.rect(HX(b2, CAN_ROW) - 1.27, HX(b2, CAN_ROW) + 1.27, cy(b2, ci(pins2[0][0])) - 1.27, cy(b2, ci(pins2[-1][0])) + 1.27,
               rx=0.8, fill='#111827', fill_opacity='0.85', stroke='#1d4ed8', stroke_width=1)
    for col, r, lab in pins + pins2:
        x, y = hp(v, b, ci(col), r)
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.2 if top else 3.1}" fill="{"#fff" if top else "#e2e8f0"}" stroke="#047857" stroke-width="1.1"/>')
    for b in ('A', 'B'):
        for x, y in corner_holes(*bx(b), *BOARD[b]['edge']):
            draw_corner(v, x, y)
    if top:
        draw_nucleo(v)
    return boxes

def carrier_labels_top(v, boxes):
    # the Nucleo
    label(v, -30, 20.0, 'NUCLEO-H533RE above', '#4338ca', 10)
    label(v, -30, 20.0, 'plugs into the four 1x19 sockets', '#4338ca', 8, dy=13, weight=None)
    label(v, 8.5, 26.5, 'CN1 ST-LINK', '#4338ca', 8, weight=None)
    label(v, 8.5, 26.5, 'USB-C, 13.2 mm', '#4338ca', 7, dy=11, weight=None)
    label(v, 8.5, 26.5, 'past the boards', '#4338ca', 7, dy=21, weight=None)
    label(v, NUC['x'][1] - 5.6, 52.5, 'CN12 under', '#4338ca', 6.5, weight=None)
    label(v, NUC['x'][1] - 5.6, 0.6, 'CN11 under', '#4338ca', 6.5, weight=None)
    # sockets
    label(v, NX(NUC_ROWS) - 2.2, cy('A', 7) + 1.3, 'CN10', '#0f766e', 9, anchor='end')
    label(v, NX(NUC_ROWS) - 2.2, cy('B', 10) + 1.3, 'CN7', '#b45309', 9, anchor='end')
    # terminals and headers
    X0, X1, Y0, Y1 = boxes['6V IN']
    label(v, (X0 + X1) / 2, Y1 + 3.6, '6V IN', '#d97706', 8)
    X0, X1, Y0, Y1 = boxes['5V IN']
    label(v, (X0 + X1) / 2, Y1 + 3.6, '5V IN', '#dc2626', 8)
    label(v, NX(1) + 2.2, cy('A', 7) + 0.9, 'pin 2', '#0f766e', 7, anchor='start')
    label(v, NX(1) + 2.2, cy('B', 10) + 0.9, 'pin 1', '#b45309', 7, anchor='start')
    b, pins, name = MALE[0]
    X0, X1, Y0, Y1 = boxes[name]
    label(v, (X0 + X1) / 2, Y1 + 3.4, name, '#334155', 7.5)
    for (col, row, _), (t, colr) in zip(pins, (('blk', '#111827'), ('red', '#dc2626'), ('wht', '#64748b'))):
        X, Y = hole(b, ci(col), row)
        label(v, X0 - 0.6, Y + 0.7, t, colr, 6, anchor='end')      # the LD-1501MG lead, HW-21
    for b, pins, name in MALE[1:]:
        X0, X1, Y0, Y1 = boxes[name]
        label(v, X0 - 0.6, (Y0 + Y1) / 2 + 0.7, name + ' under', '#7c3aed', 6.5, anchor='end')
    X0, X1, Y0, Y1 = boxes['CAN']
    label(v, (X0 + X1) / 2, Y1 + 2.8, 'CAN  H · L · GND', '#1d4ed8', 7)
    label(v, HX('B', 19), cy('B', 16) + 1.2, 'C2 470µF', '#a16207', 7, anchor='start')
    label(v, HX('B', 23) - 1.6, cy('B', 11) + 0.9, 'R4 1k', '#1e40af', 7, anchor='end')

PIN_LAB = {  # (board, col, row): (text, level, anchor) - each board's over its own inner columns
    nuc_hole('CN7', 6): ('CN7-6 E5V', 1, 'start'), nuc_hole('CN7', 8): ('CN7-8 GND', 0, 'start'),
    nuc_hole('CN7', 16): ('CN7-16 3V3', 1, 'end'), nuc_hole('CN7', 19): ('CN7-19 GND', 0, 'end'),
    nuc_hole('CN10', 3): ('CN10-3 PB6', 2, 'start'), nuc_hole('CN10', 5): ('CN10-5 PB7', 1, 'end'),
    nuc_hole('CN10', 9): ('CN10-9 GND', 0, 'start'), nuc_hole('CN10', 16): ('CN10-16 PB12', 2, 'end'),
    nuc_hole('CN10', 20): ('CN10-20 GND', 1, 'end'), nuc_hole('CN10', 30): ('CN10-30 PB13', 0, 'end'),
    nuc_hole('CN7', 28): ('CN7-28 PA0', 2, 'end'),
}
END_LAB = []

def carrier_labels_bottom(v):
    _, yb = v.px(0, cy('B', 6))                 # B's inner columns (below its sockets in this view)
    _, ya = v.px(0, cy('A', 12))                # A's inner columns (above its sockets)
    for (b, col, r), (t, lvl, anc) in PIN_LAB.items():
        x, y = hp(v, b, ci(col), r)
        colr = '#0f766e' if b == 'A' else '#b45309'
        ty = yb + 11 * lvl if b == 'B' else ya - 11 * lvl
        w(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ty - (6 if b == "B" else -3):.1f}" stroke="{colr}" stroke-width="0.8"/>')
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="none" stroke="{colr}" stroke-width="1.3"/>')
        text(x + (3 if anc == 'start' else -3), ty + 3, t, 7, colr, '700', anchor=anc, halo=True)
    xe, _ = v.px(BX[1], 0)
    for b, pins in END_LAB:
        colr = '#0f766e' if b == 'A' else '#b45309'
        for col, r, t in pins:
            x, y = hp(v, b, ci(col), r)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="none" stroke="{colr}" stroke-width="1.3"/>')
        x, y = hp(v, b, ci(pins[0][0]), 1)
        w(f'<line x1="{x + 4.2:.1f}" y1="{y:.1f}" x2="{xe + 6:.1f}" y2="{y:.1f}" stroke="{colr}" stroke-width="0.8"/>')
        y0 = y - (len(pins) - 1) * 5.5 + 2.5
        for i, (col, r, t) in enumerate(pins):
            text(xe + 9, y0 + i * 11, f'{silk(b, col, r)}  {t}', 7, colr, '700', halo=True)

def draw_bridges(v):
    """The two wires that cross the 5.9 mm gap, drawn whole."""
    for net, pts, kind in XWIRES:
        xy = [hp(v, b, c, r) for b, c, r in pts]
        d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in xy)
        w(f'<polyline points="{d}" fill="none" stroke="{NET[net]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        for x, y in (xy[0], xy[-1]):
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{NET[net]}" stroke="#fff" stroke-width="0.6"/>')
    xe, _ = v.px(BX[1], 0)
    _, yg = v.px(0, (BOARD['A']['edge'][1] + BOARD['B']['edge'][0]) / 2)
    for k, (net, pts, kind) in enumerate(XWIRES):
        (b0, c0, r0), (b1, c1, r1) = pts[0], pts[-1]
        text(xe + 9, yg - 2 + 10 * k, f'{net} bridge {N(b0, c0, r0)} → {N(b1, c1, r1)}', 7, NET[net], '700', halo=True)

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
C_RES = []   # none: the FRDM boots from VBUS and GND alone, so no source Rp is fitted (HW-02, HW-19)

# The KUOQIY 6-wire USB-C female socket (BOM 5.1), lying on its side with its flange flush
# at the row-1 edge. The flange is 16.7 x 10.3 and the body 12.0 x 5.3, centred on it, so the
# body rides 2.5 mm off the board and clears the pan head of the e4 screw beneath it.
C_SOCKET = dict(y=11.43, flange=(-5.79, -3.79), flange_w=16.7, body=(-3.79, 10.21), body_w=12.0,
                flange_h=10.3, body_h=5.3)
# pigtail wire -> landing hole, cut to about 20 mm: (label, colour, col, row, exit Y on the body)
C_PIGTAIL = [('V', '#dc2626', 'a', 7, 7.2), ('G', '#111827', 'c', 7, 9.0)]
# D-, D+, CC1 and CC2 are cut short, each insulated alone (the socket's own 5.1k Rd stays on CC; the FRDM does not use CC)
C_CUT = [('D-', '#e5e7eb', 10.8), ('D+', '#1e3a8a', 12.2), ('CC1', '#16a34a', 13.8), ('CC2', '#eab308', 15.6)]
C_TIES = [2, 6]              # zip ties at these rows, through 3 mm holes drilled at b and i
C_WIRES = [   # the FRDM's current in 18 AWG, IN 5V -> C1 -> socket on each rail
    ('5V', [(1, 24), (0.5, 23.5), (0.5, 12.5), (1, 12)], 'pwr'),              # IN 5V + to C1 +
    ('5V', [(1, 12), (1.5, 11.5), (1.5, 7.5), (1, 7)], 'pwr'),                # C1 + to socket red
    ('5V', [(1, 24), (1.5, 23.5), (6.5, 23.5), (7, 24)], 'pwr'),              # IN 5V + to TO STM32 +
    ('GND', [(3, 24), (2.5, 24.5), (2.5, 12.5), (3, 12)], 'pwr'),             # IN 5V - to C1 -
    ('GND', [(3, 12), (2.5, 11.5), (2.5, 7.5), (3, 7)], 'pwr'),               # C1 - to socket black
    ('GND', [(3, 24), (3.5, 24.5), (8.5, 24.5), (9, 24)], 'pwr'),             # IN 5V - to TO STM32 -
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
        text(lx, ly + 18, f"zip ties along {LET[C_TIES[0] - 1]}, {LET[C_TIES[1] - 1]}", 6.5, '#64748b', anchor='end')
        text(lx, ly + 27, 'D−/D+/CC1/CC2 cut, insulated', 6.5, '#64748b', anchor='end')
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
    a1_marker(v, (C_EDGE_X[0], C_EDGE_Y[1]), +1, -1)
    for c in range(1, C_COLS + 1):
        for r in range(1, C_ROWS + 1):
            x, y = hf(c, r)
            w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="#fff" stroke="#a3b18a" stroke-width="0.7"/>')
    for c in range(1, C_COLS + 1):
        x, y = v.px(C_EDGE_X[0], (c - 1) * P)
        text(x - 4, y + 2.5, str(11 - c), 7, '#15803d', anchor='end')
    for r in range(1, C_ROWS + 1):
        x, y = v.px((r - 1) * P, C_EDGE_Y[1] if v.flip else C_EDGE_Y[0])
        text(x, y - 3, LET[r - 1], 7, '#15803d', '700', anchor='middle')
    for X, Y in corner_holes(C_EDGE_X[0], C_EDGE_X[1], C_EDGE_Y[0], C_EDGE_Y[1]):
        draw_corner(v, X, Y)
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
        text(v.px((C_EDGE_X[0] + C_EDGE_X[1]) / 2, 0)[0], yb + 13, 'four corner holes: M2.5 screw into an 8 mm nylon standoff, from below (MEC-17)', 6.5, '#0f172a', '700', anchor='middle', halo=True)
    else:
        for net, pts, kind in C_WIRES:
            draw_wire(v, net, 'C', pts, kind, hfun=hf)

def orientation_inset(y0):
    """Which board goes under which header: the Nucleo from above, A and B beneath it."""
    text(RX0, y0, 'ORIENTATION - where A and B sit under the Nucleo', 12, '#1a1a1a', '700')
    w(f'<line x1="{RX0}" y1="{y0 + 8}" x2="{W - 40}" y2="{y0 + 8}" stroke="#e2e8f0"/>')
    v = View(RX0 + 42, y0 + 32, XMIN, YMIN, YMAX, flip=False, scale=1.55)
    for b in ('A', 'B'):
        v.rect(*bx(b), BOARD[b]['edge'][0], BOARD[b]['edge'][1], rx=2, fill='#dcfce7',
               stroke='#15803d', stroke_width=1.2)
        board_a1(v, b, leg=9.0)
        # the label goes on the strip of each board outboard of the Nucleo
        yl = (BOARD[b]['edge'][0] + NUC['y'][0]) / 2 if b == 'A' else (NUC['y'][1] + BOARD[b]['edge'][1]) / 2
        x, y = v.px(-15, yl)
        text(x, y + 4, f'board {b}', 10, '#15803d', '700', anchor='middle')
    v.rect(NUC['x'][0], NUC['x'][1], NUC['y'][0], NUC['y'][1], rx=2, fill='none',
           stroke='#4338ca', stroke_width=1.4, stroke_dasharray='5 3')
    x, y = v.px(-28, 29.2)
    text(x, y + 3, 'Nucleo, above', 7.5, '#4338ca', '700', anchor='middle')
    for b, cols, pin1, lab in (('A', ('g', 'h'), 'h', 'CN10'), ('B', ('i', 'j'), 'j', 'CN7')):
        ya, yb = cy(b, ci(cols[0])), cy(b, ci(cols[1]))
        v.rect(NX(NUC_ROWS) - 1.27, NX(1) + 1.27, min(ya, yb) - 1.27, max(ya, yb) + 1.27, fill='#1f2937')
        x, y = v.px(NX(1), cy(b, ci(pin1)))            # pin 1 (odd pins' column), at the CN1 end
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="#fbbf24"/>')
        x, y = v.px(NX(10), max(ya, yb) + (5.5 if b == 'A' else 4.8))
        text(x, y, lab, 8, '#4338ca', '700', anchor='middle', halo=True)
    v.rect(NUC['x'][1] - 7.3, NUC['x'][1] + 0.6, CN1_Y - 4.5, CN1_Y + 4.5, rx=1, fill='#94a3b8', stroke='#334155', stroke_width=0.8)
    x, y = v.px(NUC['x'][1] - 3, CN1_Y)
    text(x - 9, y + 3, 'CN1', 7, '#334155', '700', anchor='end', halo=True)
    x0, ya_ = v.px(XMIN, YMIN)
    x1, yb_ = v.px(XMAX, YMAX)
    text((x0 + x1) / 2, ya_ - 5, 'vehicle RIGHT', 7, '#64748b', anchor='middle')
    text((x0 + x1) / 2, yb_ + 11, 'vehicle LEFT', 7, '#64748b', anchor='middle')
    text(x0 - 4, (ya_ + yb_) / 2, 'FRONT', 7, '#64748b', '700', anchor='end')
    text(x1 + 4, (ya_ + yb_) / 2, 'REAR', 7, '#64748b', '700', anchor='start')
    tx = x1 + 40
    lines = [
        ('Nucleo from above, components up, as in every view.', True),
        ('CN1, the ST-LINK USB-C, points to the REAR (fascia).', False),
        ('CN10 is the header on the vehicle RIGHT: board A goes under it.', False),
        ('CN7 is the header on the vehicle LEFT: board B goes under it.', False),
        ('Both have pin 1 (yellow) at the CN1 end, in their vehicle-LEFT column.', False),
        ('', False),
        ('Red triangle = the corner at printed hole A1.', True),
        ('On A and on B: the FRONT corner on the vehicle-LEFT edge.', False),
        ('Mark that corner on both faces with a pen before soldering:', False),
        ('both boards then read the same way up, print legible.', False),
    ]
    for i, (t, bold) in enumerate(lines):
        text(tx, y0 + 34 + i * 12.5, t, 8.2, '#1e293b' if bold else '#475569', '700' if bold else None)


# ---------------------------------------------------------------- sheet
if __name__ == "__main__":
    OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders', 'stm32-carrier.svg')
    W, H = 1720, 1400
    w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">')
    w(f'<rect width="{W}" height="{H}" fill="#fbfaf8"/>')
    text(40, 30, 'NEXUS - STM32 carrier and 5 V split board: soldering and wiring', 18, '#1a1a1a', '700')
    text(40, 49, 'Kit perfboards (BOM 5.11), 2.54 grid · Boards A and B, both 5×7 cm (18 × 24 holes), under CN10 and CN7 of the NUCLEO-H533RE, 5.9 mm apart · Board C 3×7 cm (10 × 24), the 5 V split · MEC-08 / MEC-15 / HW-19', 10.5, '#666')
    def col_range(b, c):           # the holes a socket column's soldered tails occupy
        hs = [hdr_hole(b, k) for k in range(1, NUC_ROWS + 1)]
        return f"{b}·{silk(b, c, max(hs))}-{silk(b, c, min(hs))}"
    text(40, 66, 'Hole names: board·hole, as PRINTED on the kit board - letters A-X along the 70 mm side, numbers across (1-18 on A and B, 1-10 on C), A1 bottom-left with the print readable, as every view shows it.', 9.5, '#b45309')
    text(40, 80, f"Nucleo header row k sits on B's hole row k + 5 and A's k + 4 (A one pitch ahead, the tray) · CN10 even pins {col_range('A', 'g')}, odd {col_range('A', 'h')[2:]} · CN7 even {col_range('B', 'i')}, odd {col_range('B', 'j')[2:]} · fixings: four corner holes per board (MEC-17).", 9.5, '#b45309')
    text(40, 93, 'Wires on the solder side, ALL INSULATED, PAD TO PAD: they meet only at pads, two wire ends per pad at most. Thick 18 AWG (3.11), thin 22 AWG, grey = a part lead bent over.', 9.5, '#b45309')

    # views
    VX1, VX2, VY = 70, 590, 150
    vt = View(VX1, VY, XMIN, YMIN, YMAX, flip=False)
    vb = View(VX2, VY, XMIN, YMIN, YMAX, flip=True)
    text(VX1 - 40, 108, 'A + B  COMPONENT SIDE  (from above, front LEFT)', 12, '#1a1a1a', '700')
    text(VX1 - 40, 123, 'CN10 on the vehicle right (top), CN7 on the vehicle left (bottom) - chassis-layout convention', 8.5, '#64748b')
    text(VX2 - 30, 108, 'A + B  SOLDER SIDE  (turned over about the long axis)', 12, '#1a1a1a', '700')
    text(VX2 - 30, 123, 'front still LEFT, so CN7 is now on TOP and every column reads upside down', 8.5, '#64748b')
    row_labels(vt, VY - 15)
    row_labels(vb, VY - 15)
    _, yb0 = vt.px(0, YMIN)
    text(vt.px(RX(1), 0)[0] + 16, VY - 15, '◀ Nucleo header row  (rear ▶)', 6.5, '#64748b')

    boxes = carrier_view(vt, True)
    carrier_labels_top(vt, boxes)
    carrier_view(vb, False)
    for net, b, pts, kind in WIRES:
        draw_wire(vb, net, b, pts, kind)
    draw_bridges(vb)
    draw_links(vb)
    carrier_labels_bottom(vb)
    # a few solder-side callouts

    # front/rear footers under the views
    for v in (vt, vb):
        x0, y0 = v.px(XMIN, YMAX if not v.flip else YMIN)
        x1, _ = v.px(XMAX, 0)
        text((x0 + x1) / 2, y0 + 22, f'front ◀  A sits one pitch ahead of B (the tray) · A front to Nucleo rear {NUC["x"][1] - bx("A")[0]:.1f} mm  ▶ rear (fascia)', 8.5, '#64748b', anchor='middle')
        text((x0 + x1) / 2, y0 + 34, 'overall width 106 mm · four corner holes per board, 8 mm nylon M2.5 standoffs, onto the carrier tray (MEC-17)', 8.5, '#64748b', anchor='middle')

    # board C views
    CY = 760
    text(VX1 - 30, CY - 42, 'C  5 V SPLIT BOARD  (component side)', 12, '#1a1a1a', '700')
    text(VX1 - 30, CY - 27, 'across the plate-2 waist, x 85.5-115.5: letter A at the vehicle right, 10 to the front · socket opening faces the vehicle right', 8.5, '#64748b')
    text(VX2 - 30, CY - 42, 'C  SOLDER SIDE  (turned over about the long axis)', 12, '#1a1a1a', '700')
    text(VX2 - 30, CY - 27, 'the FRDM current in 18 AWG (thick), each rail a chain IN 5V → C1 → socket', 8.5, '#64748b')
    vc_t = View(VX1 + 70, CY, C_EDGE_X[0], C_EDGE_Y[0], C_EDGE_Y[1], flip=False, scale=4.6)
    vc_b = View(VX2 + 70, CY, C_EDGE_X[0], C_EDGE_Y[0], C_EDGE_Y[1], flip=True, scale=4.6)
    board_c(vc_t, True)
    board_c(vc_b, False)
    text(VX1 - 30, CY + 165, 'The socket carries its own 5.1k Rd on CC1 and CC2 (4.98k measured, 2026-10-07). Its CC wires are cut short and insulated: the FRDM boots on VBUS and GND alone.', 8.4, '#b45309')
    text(VX1 - 30, CY + 179, f"The USB-C body rides 2.5 mm up on its flange. Ties through 3 mm holes at {silk('C', 'b', 2)} / {silk('C', 'i', 2)} and {silk('C', 'b', 6)} / {silk('C', 'i', 6)}, the second one over the pigtail.", 8.4, '#b45309')

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

    def pins_of(name):
        return {l: c for c, r, l in next(ps for b, ps, n in MALE if n == name)}, next((b, ps[0][1]) for b, ps, n in MALE if n == name)

    def mpin(name, lab):
        cols, (b, row) = pins_of(name)
        return silk(b, cols[lab], row)
    can = {l: (c, r) for c, r, l in next(ps for b, ps, e, n, c_ in TERMS if n == 'CAN')}
    net_rows = [
        (NET['5V'], '5 V', 'C TO STM32', f"B 5V IN ({N('B', 'q', 13)}) → CN7-6 E5V ({silk(*nuc_hole('CN7', 6))}), JP5 on [5-6]"),
        (NET['5V'], '5 V FRDM', 'C IN 5V', f"{N('C', 'a', 24)} → C1 + ({silk('C', 'a', 12)}) → socket red ({silk('C', 'a', 7)}), 18 AWG"),
        (NET['GND'], 'GND FRDM', 'C IN GND', f"{N('C', 'c', 24)} → C1 − ({silk('C', 'c', 12)}) → socket black ({silk('C', 'c', 7)}), 18 AWG"),
        (NET['GND'], 'GND STM32', 'C IN GND', f"TO STM32 − → B 5V IN − ({N('B', 'q', 15)}) → CN7-22 ({silk(*nuc_hole('CN7', 22))}) · → SERVO GND ({mpin('SERVO', 'GND')})"),
        (NET['GND'], 'Servo GND', 'B 6V IN −', f"{N('B', 'q', 10)} → C2 − ({silk('B', 'n', 18)}) → SERVO GND ({mpin('SERVO', 'GND')}), 18 AWG"),
        (NET['GND'], 'GND (A)', f"CN10-9 {N(*nuc_hole('CN10', 9))}", f"→ I2C-B GND ({N('A', *pins_of('I2C-B')[0]['GND'], 20)}) · → I2C-A GND ({silk('A', pins_of('I2C-A')[0]['GND'], 20)})"),
        (NET['GND'], 'GND CAN', f"CN10-20 {N(*nuc_hole('CN10', 20))}", f"→ XCVR GND ({xc('GND')}) → CAN GND ({silk('A', *can['GND'])})"),
        (NET['3V3'], '3.3 V', f"CN7-16 {N(*nuc_hole('CN7', 16))}", f"→ bridge → I2C-A VCC ({N('A', pins_of('I2C-A')[0]['3V3'], 20)}) → XCVR 3V3 ({xc('3V3')})"),
        (NET['6V'], 'Servo 6 V', 'B 6V IN +', f"{N('B', 'q', 8)} → C2 + ({silk('B', 'n', 20)}) → SERVO + ({mpin('SERVO', '+6V')}), 18 AWG"),
        (NET['PWM'], 'TIM2_CH1', 'CN7-28 PA0', f"R4 1k ({N('B', 'k', 19)}-{silk('B', 'k', 23)}) → SERVO SIG ({mpin('SERVO', 'SIG')})"),
        (NET['SCL'], 'I²C1 SCL', 'CN10-3 PB6', f"→ I2C-B ({N('A', pins_of('I2C-B')[0]['SCL'], 20)}) · → I2C-A ({silk('A', pins_of('I2C-A')[0]['SCL'], 20)})"),
        (NET['SDA'], 'I²C1 SDA', 'CN10-5 PB7', f"→ I2C-B ({N('A', pins_of('I2C-B')[0]['SDA'], 20)}) → I2C-A ({silk('A', pins_of('I2C-A')[0]['SDA'], 20)})"),
        (NET['CTX'], 'FDCAN2_TX', 'CN10-30 PB13', f"XCVR CTX ({N('A', *[(c, r) for c, r, l in XCVR_SOCKET[1] if l == 'CTX'][0])}) - straight, not crossed"),
        (NET['CRX'], 'FDCAN2_RX', 'CN10-16 PB12', f"XCVR CRX ({N('A', *[(c, r) for c, r, l in XCVR_SOCKET[1] if l == 'CRX'][0])})"),
        (NET['CANH'], 'CAN_H', 'module H pin', f"socket {N('A', *CAN_SOCKET[1][0][:2])} → CAN H ({silk('A', *can['H'])})"),
        (NET['CANL'], 'CAN_L', 'module L pin', f"socket {N('A', *CAN_SOCKET[1][1][:2])} → CAN L ({silk('A', *can['L'])}) · 120 Ω on the module (HW-09)"),
    ]
    y = table(100, 'NETLIST', ['Net', 'From', 'To'], net_rows, [12, 96, 190])

    ext_rows = [
        (None, 'C IN 5V', 'Bauer 50 W via SW2, 18 AWG pair (HW-17)'),
        (None, 'C TO STM32', '18 AWG pair to B 5V IN'),
        (None, 'C USB-C', f"socket on C, pigtail soldered: red {silk('C', 'a', 7)}, black {silk('C', 'c', 7)} · C-to-C data cable to FRDM J1"),
        (None, 'C D+ / D−', 'white, blue, green and yellow (D−, D+, CC1, CC2) cut short, each insulated on its own - never twisted together'),
        (None, 'B 6V IN', 'UBEC 6 V out, 18 AWG pair (HW-14)'),
        (None, 'B SERVO', f"straight header on top, across B: LD-1501MG black {N('B', *[(c, r) for c, r, l in MALE[0][1] if l == 'GND'][0])}, red, white inboard (HW-21)"),
        (None, 'A I2C-A', 'under A, pointing forward: INA226 VCC, SDA, SCL, GND - its own order, a straight 4-way lead'),
        (None, 'A I2C-B', 'under A, pointing forward: motor module SCL, SDA, GND, 5V - its own order; pin 4 has no wire'),
        (None, 'I2C leads', 'plugged before the boards go on the tray; they leave A\'s front edge in the 8 mm gap and drop through the window'),
        (None, 'A CAN', 'twisted H, L + GND to DE-9 stub and FRDM J7 (HW-09, HW-18); the module\'s 120 Ω terminates this end'),
        (None, 'CN1', 'ST-LINK USB-C: a 90° USB-C plug to the fascia Mini-B extension (5.10); a straight plug meets the FRDM USB-C port body'),
    ]
    y = table(y + 26, 'WHAT PLUGS IN WHERE', ['Connector', 'Cable'], ext_rows, [12, 96])

    parts = [
        (None, 'Board A', '5×7 board · 2 × 1×19 + 1 × 1×4 + 1 × 1×2 female · 3p terminal · 2 × 1×4 90° male, under · the SN65HVD230 module'),
        (None, 'Board B', '5×7 board · 2 × 1×19 female · 2 × 2p terminal · 1×3 male · C2 470µF · R4 1k'),
        (None, 'Board C', '3×7 board · 2 × 2p terminal · USB-C socket (5.1), 2 zip ties · C1 470µF'),
        (None, 'From stock', 'caps: 2 of the 5 in 3.14 · resistors: 3.21 · module: 4.1 · headers, terminals: 5.11'),
        (None, 'Wire', '22 AWG insulated copper hook-up wire (not in BOM) · 18 AWG silicone copper (3.11) for the thick runs · not the CCA Dupont leads (5.7)'),
    ]
    y = table(y + 26, 'PARTS', ['Board', 'Fitted'], parts, [12, 82])

    fix_rows = [
        (None, 'A', 'four corner holes', '2.5 mm in from each edge · M2.5 screw into an 8 mm nylon standoff'),
        (None, 'B', 'four corner holes', 'same · the holes under the module stay free of wires'),
        (None, 'C', 'four corner holes', 'same · the USB-C body lies between the two on its side'),
    ]
    y = table(y + 26, 'FIXINGS  (MEC-17)', ['Board', 'Hole', 'Fixing'], fix_rows, [12, 62, 170])
    text(RX0, y + 16, 'Nothing is drilled. The tray (MEC-17) takes the boards from below; only the tray is screwed to plate 2, by six M2.5 screws (T1-T6).', 8.4, '#475569')
    text(RX0, y + 29, f'A·X.. at chassis x 181.20, B·X.. at x 183.74 · Nucleo row 1 at x {183.74 + NX(1):.2f}, its outline x {183.74 + NUC["x"][0]:.1f}-{183.74 + NUC["x"][1]:.1f} · A y 5.11, B y 110.99.', 8.4, '#475569')
    orientation_inset(y + 58)

    # ---------------------------------------------------------------- checks and notes (bottom band)
    NY = 985
    text(40, NY, 'CHECK BEFORE THE IRON IS HOT', 12, '#1a1a1a', '700')
    w(f'<line x1="40" y1="{NY + 8}" x2="{RX0 - 30}" y2="{NY + 8}" stroke="#e2e8f0"/>')
    checks = [
        '1  Count the holes: A and B need 18 × 24, C 10 × 24. The drawing assumes the usual kit counts; a board one row short moves everything.',
        '2  New A and B, two fresh 5×7 boards. Cut four 1×19 strips from the 40-pin female headers and dry-fit them on the Nucleo, A and B',
        f"    screwed to the tray under it: {col_range('A', 'g')} / {col_range('A', 'h')[2:]} and {col_range('B', 'i')} / {col_range('B', 'j')[2:]}. Nothing else goes in the columns under the Nucleo.",
        '3  Solder the sockets WITH THE NUCLEO PLUGGED IN and A and B screwed to the tray: it sets the 63.50 mm between the rows. Tack two corners, check, finish.',
        f"4  SN65HVD230 FACE DOWN on A, as bent: sockets {N('A', XCVR_SOCKET[1][0][0], XCVR_ROW)}-{silk('A', XCVR_SOCKET[1][-1][0], XCVR_ROW)} = {', '.join(l for _, _, l in XCVR_SOCKET[1])}, and",
        f"    {N('A', CAN_SOCKET[1][0][0], CAN_ROW)} / {silk('A', CAN_SOCKET[1][1][0], CAN_ROW)} = CANH / CANL, 7 holes behind. Its screw terminal is unused. CANH-CANL unpowered must read ~120 Ω: keep its terminator (HW-09).",
        '5  The kit terminals may be 5.0 mm, not 5.08: the 3p CAN block spans 10.0 vs 10.16 mm of holes. Push it in; do not drill.',
        f"6  Before the Nucleo goes in: 5 V to GND not shorted · 6 V isolated from 5 V and 3V3 · 5 V on {N(*nuc_hole('CN7', 6))} (E5V) only, nothing on {silk(*nuc_hole('CN7', 18))} (5V) or {silk(*nuc_hole('CN7', 5))} (VDD) · JP5 on [5-6].",
        '7  Fixings: nothing is drilled. Fit an 8 mm nylon standoff with a screw in each corner hole of A, B and C; the tray (MEC-17) takes the',
        '    boards from below. No wire may pass under a standoff, nor in front of an I2C header under A, where its plug lies (violet).',
        '8  The two I2C headers are 90° headers fitted from UNDER A, soldered on top, pins pointing forward. Plug both leads before A goes on the tray.',
    ]
    yy = NY + 26
    for c in checks:
        text(40, yy, c, 9, '#475569')
        yy += 15

    notes = [
        ('Why A and B split this way', [
            'New boards on the same tray holes (MEC-17). Every CAN pin is on',
            'CN10 and every supply pin on CN7, so A takes CAN and I2C and B the',
            'power and the servo (PA0): one wire crosses, 3V3. Each header is',
            'in its module\'s order: a straight lead is right.',
        ]),
        ('What moved off the WAGOs', [
            'Both 470 µF caps and every resistor are now on a board. C2 sits at',
            'the servo header, where the stall current is. C1 is on board C,',
            'which is the 5 V split: the FRDM\'s amps never cross the STM32',
            'carrier. No Rp is fitted: the FRDM boots on plain 5 V (HW-02).',
        ]),
        ('Grounds and supplies', [
            'The carrier\'s one ground lead is B 5V IN GND, back through C to the',
            '(−) WAGO (HW-06). The 6 V servo rail reaches C2 and SERVO only',
            '(HW-11). 3V3 comes from CN7-16, the Nucleo\'s own regulator, never',
            'CN7-5 VDD. 5 V enters on E5V, so the ST-LINK USB alone does not',
            'power the MCU: LOGIC on first, then the USB. R4 guards PA0.',
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
    text(40, H - 32, 'Geometry: UM3121 Fig. 7 (board 70 × 82.5, outer rows 63.50 apart, 3.25 in from each edge, row 1 31.70 from the CN1 edge) · Pins: UM3121 Table 17 · AFs: DS14539 Rev 3 (PB12 / PB13 AF9, PB6 / PB7 AF4, PA8 AF1)', 8.4, '#94a3b8')
    text(40, H - 18, 'Decisions: MEC-08 (carrier) · MEC-15 (kit boards) · HW-19 (5 V split board, selectable termination) · HW-06 · HW-09 · HW-11 · HW-18 · SVG is the master - PDFs are generated once the design is frozen.', 8.4, '#94a3b8')
    w('</svg>')

    open(OUT, 'w').write('\n'.join(out) + '\n')
