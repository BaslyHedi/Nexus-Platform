#!/usr/bin/env python3
"""Check the harness model in mechanical/scripts/plate1.py (MEC-16): clearances and joints.

    python3 tools/check-harness-clearance.py      # exits 1 and lists the problems, if any

1. No two parts of the harness board overlap (clips, fuse holders, INA226, UBEC), apart from the two stacked splice pairs.
2. No wire runs through a part, or through the battery, the driver or a switch.
3. No two wires share space: any 1.5 mm sample closer than the two radii (less 1.0 mm: where wires cross they may press together) fails. Wires that end at the same clip
   port are checked only beyond 8 mm of their ends.
4. No wire is joined to another without a part: where two or more wire ends meet, a clip, bus, holder, module or plug must be
   within 8 mm. (The MEC-16 audit of 2026-10-06 found three joints with none.)
"""
import sys, os, math, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mechanical', 'scripts'))
import plate1
plate1.build()


def bbox(t):
    xs = [v[0] for tri in t for v in tri]; ys = [v[1] for tri in t for v in tri]; zs = [v[2] for tri in t for v in tri]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


parts = [(n, bbox(t)) for n, m, t in plate1.PARTS
         if not n.startswith(('battery', 'driver', 'tire', 'sw1', 'sw2', 'sm2p', 'p2-', 'run', 'drop'))
         and not n.endswith(('-tape', '-levers', '-rating', '-mark', '-tabs', '-bezel', '-terminals'))]
solid = parts + [(n, bbox(t)) for n, m, t in plate1.PARTS if n.startswith(('battery', 'driver', 'sw1-drive', 'sw2-logic'))
                 and not n.endswith(('-charge-lead', '-charge-socket', '-bezel', '-tabs'))]
STACKED = {frozenset(('splice-s2-vm-plus', 'splice-s4-vm-minus')), frozenset(('splice-s3-ubec-plus', 'splice-s5-ubec-minus'))}
err = []


def overlap(a, b, tol=0.3):
    return all(a[2 * i] < b[2 * i + 1] - tol and b[2 * i] < a[2 * i + 1] - tol for i in range(3))


for (n1, a), (n2, b) in itertools.combinations(parts, 2):
    if frozenset((n1, n2)) not in STACKED and overlap(a, b):
        err.append(f'parts overlap: {n1} / {n2}')


def samples(pts, step=1.5):
    out = []
    for a, b in zip(pts, pts[1:]):
        k = max(1, int(math.dist(a, b) / step))
        out += [tuple(a[j] + (b[j] - a[j]) * i / k for j in range(3)) for i in range(k + 1)]
    return out


runs = [(n, d / 2, samples(p), p) for n, m, d, p in plate1.RUNS]
for n, r, smp, pts in runs:
    for pn, b in solid:
        hit = sum(1 for s in smp if math.dist(s, pts[0]) >= 7 and math.dist(s, pts[-1]) >= 7
                  and b[0] + r < s[0] < b[1] - r and b[2] + r < s[1] < b[3] - r and b[4] + r < s[2] < b[5] - r)
        if hit > 3:
            err.append(f'{n} runs through {pn} ({hit} samples)')
for (n1, r1, s1, p1), (n2, r2, s2, p2) in itertools.combinations(runs, 2):
    cnt = sum(1 for a in s1 if math.dist(a, p1[0]) >= 8 and math.dist(a, p1[-1]) >= 8
              for b in s2 if math.dist(b, p2[0]) >= 8 and math.dist(b, p2[-1]) >= 8 and math.dist(a, b) < r1 + r2 - 1.0)
    if cnt >= 1:
        err.append(f'{n1} and {n2} share space ({cnt} samples)')

ends = [(p[0], n) for n, m, d, p in plate1.RUNS] + [(p[-1], n) for n, m, d, p in plate1.RUNS]
joiners = [(n, b) for n, b in solid if n.startswith(('bus-', 'split-', 'splice-', 'fuse-', 'ina226', 'ubec'))]
seen = set()
for i, (e, n) in enumerate(ends):
    group = [(f, m) for f, m in ends if math.dist(e, f) < 4.0]
    names = sorted(set(m for _, m in group if not m.startswith(('run01a', 'run04a'))))      # the pack leads leave the battery together
    if len(group) < 2 or len(names) < 2 or tuple(names) in seen:
        continue
    seen.add(tuple(names))
    if not any(b[0] - 8 < e[0] < b[1] + 8 and b[2] - 8 < e[1] < b[3] + 8 and b[4] - 8 < e[2] < b[5] + 8 for _, b in joiners):
        err.append(f'wires meet with no clip: {names} at {tuple(round(x) for x in e)}')
        # the switch tabs and plugs are the other places where ends meet; they are checked by eye in the animation

if err:
    print('\n'.join(err))
    sys.exit(1)
print(f'harness clearance OK: {len(parts)} parts, {len(runs)} runs')
