#!/usr/bin/env python3
"""Plate outline from Hiwonder's CAD export - the first step of the chassis layout drawing (MEC-10, 2026-09-20).

    python3 extract-plate-outline.py [plate.json]       # default: ./plate.json

Reads ../../../mechanical/cad/chassis-3deck-fascia.obj (the chassis groups are Hiwonder's, untouched), takes the faces of the
black sheet-metal plate (group obj30) lying at z 29.1, and writes the silhouette as a simplified polygon of (x, y) in the CAD's own
millimetres. The plan drawings then place it at 1.7 px/mm. Recovered from the 2026-09-20 session that made it; the group name and the
z level are the CAD's, and they have not been checked against a newer export.
"""
import json, math, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, "..", "..", "..", "mechanical", "cad", "chassis-3deck-fascia.obj")
OUT = sys.argv[1] if len(sys.argv) > 1 else "plate.json"
GROUP, Z, STEP, TOL = 'obj30_黑色钣金', 29.1, 0.5, 0.2

V, F, cur = [], [], None
for line in open(OBJ, encoding='utf-8'):
    if line.startswith('v '):
        V.append(tuple(map(float, line.split()[1:4])))
    elif line.startswith('g '):
        cur = line[2:].strip()
    elif line.startswith('f ') and cur == GROUP:
        F.append([int(t.split('/')[0]) - 1 for t in line.split()[1:]])

E = Counter()
key = lambda i: (round(V[i][0], 3), round(V[i][1], 3))
for f in F:
    if all(abs(V[i][2] - Z) < 0.1 for i in f):
        for a, b in zip(f, f[1:] + f[:1]):
            E[tuple(sorted([key(a), key(b)]))] += 1
seg = [e for e, c in E.items() if c == 1]                 # boundary edges only

ys = [p[1] for e in seg for p in e]
y0, y1 = min(ys), max(ys)
prof, y = [], y0 + 0.02
while y < y1:                                             # leftmost and rightmost x at each y: the silhouette
    xs = [ax + (bx - ax) * (y - ay) / (by - ay) for (ax, ay), (bx, by) in seg if (ay - y) * (by - y) < 0]
    if xs:
        prof.append((min(xs), max(xs), y))
    y += STEP
poly = [(p[0], p[2]) for p in prof] + [(p[1], p[2]) for p in prof][::-1]


def dp(pts, tol=TOL):                                     # Douglas-Peucker
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    idx = dmax = 0
    for i, p in enumerate(pts[1:-1], 1):
        d = abs(dx * (p[1] - a[1]) - dy * (p[0] - a[0])) / L if L else math.hypot(p[0] - a[0], p[1] - a[1])
        if d > dmax:
            idx, dmax = i, d
    return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol) if dmax > tol else [a, b]


S = dp(poly)
json.dump(S, open(OUT, 'w'))
xs, ys = [p[0] for p in S], [p[1] for p in S]
print('%d -> %d points; x %.2f..%.2f, y %.2f..%.2f -> %s' % (len(poly), len(S), min(xs), max(xs), min(ys), max(ys), OUT))
