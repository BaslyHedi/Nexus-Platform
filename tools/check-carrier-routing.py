#!/usr/bin/env python3
"""Check the STM32 carrier's routing in hardware/scripts/stm32-carrier.py (MEC-15, 2026-09-30).

    python3 tools/check-carrier-routing.py        # exits 1 and lists the problems, if any

The build uses insulated wire, so the rules are: every wire ends on a pad of its own net;
wires meet only at pads, two wire ends per pad at most; nothing runs along another wire,
under a standoff, or over another net's joint. Every net must come out whole and no two
nets may touch, counting the Nucleo's own ties between its duplicate header pins and
the C-to-B supply pair.
"""
import sys
sys.dont_write_bytecode = True             # a stale cached module once hid a real overlap
import importlib.util as u, math, itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = u.spec_from_file_location('carrier', os.path.join(HERE, '..', 'hardware', 'scripts', 'stm32-carrier.py'))
C = u.module_from_spec(s); s.loader.exec_module(C)
ci = C.ci

# ---- what each pad is, by part pin (A/B/C, col, row) -> net
PAD = {}
def put(b, col, row, net):
    PAD[(b, ci(col) if isinstance(col, str) else col, row)] = net
for hdr in ('CN10', 'CN7'):                   # the four 1x19 sockets: every morpho pin has a hole
    for pin in range(1, 2 * C.NUC_ROWS + 1):
        b, col, row = C.nuc_hole(hdr, pin)
        put(b, col, row, f'{hdr}-{pin}')
NUC = {f'{h}-{p}': net for (h, p), (_, net) in C.NUC_PINS.items()}
for k, v in list(PAD.items()):
    PAD[k] = NUC.get(v, v)
for col, row, net in [('c', 1, '6V'), ('c', 3, 'GND'), ('c', 8, 'GND'), ('c', 10, '6V'), ('c', 12, 'GND'),
                      ('c', 13, '6V'), ('c', 14, 'PWM_SRV'), ('c', 16, 'GND'), ('c', 17, 'SCL'), ('c', 18, 'SDA'),
                      ('c', 20, 'GND'), ('c', 21, '3V3'), ('c', 22, 'SCL'), ('c', 23, 'SDA'),
                      ('e', 12, 'PWM_SRV'), ('e', 16, 'PWM_MCU')]:
    put('A', col, row, net)
for col, row, net in [('m', 1, 'CANH'), ('o', 1, 'CANL'), ('q', 1, 'GND'), ('q', 21, '5V'), ('q', 23, 'GND'),
                      ('m', 22, 'CANL'), ('m', 23, 'TERM'), ('k', 19, 'CANH'), ('k', 23, 'TERM1'), ('k', 24, 'TERM1'), ('o', 24, 'TERM')]:
    put('B', col, row, net)
for col, row, net in C.XCVR_SOCKET[1] + C.CAN_SOCKET[1]:   # the module's two sockets
    put('B', col, row, net)
for col, row, net in [('a', 24, '5V'), ('c', 24, 'GND'), ('g', 24, '5V'), ('i', 24, 'GND'), ('a', 12, '5V'),
                      ('c', 12, 'GND'), ('a', 7, '5V'), ('c', 7, 'GND')]:
    put('C', col, row, net)
# conductors that arrive from the component side and count as a wire end at their pad
ENTRY = {('C', 1, 7): 'pigtail red', ('C', 3, 7): 'pigtail black'}
WIRE_NET = {'PWM': ('PWM_MCU', 'PWM_SRV')}
R = {'ins': 0.3, 'pwr': 0.39, 'lead': 0.12}         # wire radius, in pitches
STANDOFF = 2.89 / 2.54            # a 5 mm hex nylon standoff: corner radius
STANDOFF_FLAT = 2.5 / 2.54        # ... and flat radius
# the standoffs now stand on each board's four corner holes (MEC-17), so a wire may not run under any of them. A corner hole is
# off the grid; it is given as a fractional (column, header row) so the same distance test applies.
FIX = {'A': [], 'B': [], 'C': []}
for b in 'AB':
    cfg = C.BOARD[b]
    for X, Y in C.corner_holes(*C.bx(b), *cfg['edge']):
        FIX[b].append(((Y - cfg['y1']) / C.P + 1, 1 - C.SHIFT[b] - X / C.P))
for X, Y in C.corner_holes(C.C_EDGE_X[0], C.C_EDGE_X[1], C.C_EDGE_Y[0], C.C_EDGE_Y[1]):
    FIX['C'].append((Y / C.P + 1, X / C.P + 1))

wires = [(n, [(b, c, r) for c, r in pts], k) for n, b, pts, k in C.WIRES]
wires += [(n, pts, k) for n, pts, k in C.XWIRES]
wires += [(n, [('C', c, r) for c, r in pts], k) for n, pts, k in C.C_WIRES]

err = []
def whole(p):
    return float(p[1]).is_integer() and float(p[2]).is_integer()

# 1. ends on pads of the wire's own net; pads' net agree
ends = {}
for i, (net, pts, kind) in enumerate(wires):
    for p in (pts[0], pts[-1]):
        if not whole(p):
            err.append(f'wire {i} {net}: end {p} is not a hole')
            continue
        pad = (p[0], int(p[1]), int(p[2]))
        pn = PAD.get(pad)
        ok = WIRE_NET.get(net, (net,))
        if pn not in ok:
            err.append(f'wire {i} {net}: end {C.N(*pad)} is {pn}')
        ends.setdefault(pad, []).append(i)
for pad, ws in ends.items():
    n = len([w for w in ws if wires[w][2] != 'lead']) + (1 if pad in ENTRY else 0)
    if n > 2:
        err.append(f'{C.N(*pad)}: {n} wire ends')

# 2. connectivity, with the Nucleo tying its same-named pins and the C-to-B pair
parent = {}
def f(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        x = parent[x]
    return x
def join(a, b):
    parent[f(a)] = f(b)
for net, pts, kind in wires:
    a, b = pts[0], pts[-1]
    join((a[0], int(a[1]), int(a[2])), (b[0], int(b[1]), int(b[2])))
disco = {}
for k, v in PAD.items():
    if k[0] in 'AB' and ((k[0] == 'A' and k[1] in (7, 8)) or (k[0] == 'B' and k[1] in (9, 10))):
        disco.setdefault(v, []).append(k)
for v, ks in disco.items():
    for k in ks[1:]:
        join(ks[0], k)
join(('C', 7, 24), ('B', 17, 21)); join(('C', 9, 24), ('B', 17, 23))       # TO STM32 -> 5V IN
groups = {}
for k, v in PAD.items():
    groups.setdefault(f(k), set()).add(v)
for g, nets in groups.items():
    real = {n for n in nets if not n.startswith('CN')}
    if len(real) > 1:
        err.append(f'short: {sorted(real)}')
bynet = {}
for k, v in PAD.items():
    if not v.startswith('CN'):
        bynet.setdefault(v, set()).add(f(k))
for v, gs in bynet.items():
    if len(gs) > 1:
        miss = [C.N(*k) for k, n in PAD.items() if n == v]
        err.append(f'{v} is in {len(gs)} pieces: {miss}')

# 3. geometry: standoffs, overlaps, lying over another net's joint
def seg_pt(a, b, p):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    dx, dy = bx - ax, by - ay
    t = 0 if dx == dy == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(ax + t * dx - p[0], ay + t * dy - p[1])
def segs(pts):
    for a, b in zip(pts, pts[1:]):
        if a[0] == b[0]:
            yield a[0], (a[1], a[2]), (b[1], b[2])
used = set(ends) | set(ENTRY) | set(PAD)
for i, (net, pts, kind) in enumerate(wires):
    for bd, a, b in segs(pts):
        for fx in FIX[bd]:
            d = seg_pt(a, b, fx)
            if d < STANDOFF + R[kind]:
                # a wire's own end sits on a pad and leaves flat to the board, so there the standoff is its hex FLAT (5.0 across), not its corner
                is_end = min(math.hypot(e[0] - fx[0], e[1] - fx[1]) for e in ((pts[0][1], pts[0][2]), (pts[-1][1], pts[-1][2]))) <= d + 1e-6
                if is_end and d >= STANDOFF_FLAT + R[kind] - 0.05:
                    continue
                err.append(f'wire {i} {net}: {d * 2.54:.2f} mm from a standoff centre on {bd}')
        for pad in used:
            if pad[0] != bd or (bd, *map(int, a)) == pad and whole((bd, *a)):
                continue
            if pad in ((pts[0][0], int(pts[0][1]), int(pts[0][2])), (pts[-1][0], int(pts[-1][1]), int(pts[-1][2]))):
                continue
            if seg_pt(a, b, pad[1:]) < 0.3 and PAD.get(pad) is not None and kind != 'lead':
                err.append(f'wire {i} {net}: lies over {C.N(*pad)} ({PAD.get(pad)})')
S = [(i, bd, a, b) for i, (n, pts, k) in enumerate(wires) for bd, a, b in segs(pts)]
for (i, bi, a1, b1), (j, bj, a2, b2) in itertools.combinations(S, 2):
    if i == j or bi != bj:
        continue
    v1 = (b1[0] - a1[0], b1[1] - a1[1]); v2 = (b2[0] - a2[0], b2[1] - a2[1])
    if abs(v1[0] * v2[1] - v1[1] * v2[0]) > 1e-9:
        continue                               # not parallel: a crossing at most
    L = math.hypot(*v1)
    if L == 0 or seg_pt(a1, b1, a2) > 0.15 and seg_pt(a1, b1, b2) > 0.15 and seg_pt(a2, b2, a1) > 0.15:
        continue
    t = sorted(((p[0] - a1[0]) * v1[0] + (p[1] - a1[1]) * v1[1]) / L for p in (a2, b2))
    if min(L, t[1]) - max(0, t[0]) > 0.05:
        err.append(f"overlap: wire {i} {wires[i][0]} {a1}-{b1} and wire {j} {wires[j][0]} {a2}-{b2} on {bi}")
print('\n'.join(err) if err else 'routing OK')
print(len(wires), 'wires,', sum(1 for w in wires if w[2] == 'pwr'), 'in 18 AWG,',
      sum(1 for w in wires if w[2] == 'lead'), 'bent leads')
sys.exit(1 if err else 0)
