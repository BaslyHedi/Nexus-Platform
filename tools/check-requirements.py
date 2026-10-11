#!/usr/bin/env python3
"""Check the requirements in requirements/ against the method in system/method.md, and keep requirements/TRACE.md in step.

    python3 tools/check-requirements.py            # exits 1 on any problem, and on a stale TRACE.md
    python3 tools/check-requirements.py --write    # regenerates TRACE.md after a clean check
    python3 tools/check-requirements.py --root DIR # check another tree laid out like this repository (used to test the checker)

The rules are listed at the end of requirements/README.md. This script is the only place that knows the block format.
"""
import glob, os, re, sys

ARGS = sys.argv[1:]
ROOT = os.path.abspath(ARGS[ARGS.index('--root') + 1]) if '--root' in ARGS else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WRITE = '--write' in ARGS
REQ = os.path.join(ROOT, 'requirements')

errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


def read(p):
    return open(p, encoding='utf-8').read()


# --- registry
sois = {}
reg = read(os.path.join(REQ, 'README.md')).split('## Systems of interest', 1)[1].split('\n## ', 1)[0]
for row in re.findall(r'^\|\s*([A-Z][A-Z0-9]*)\s*\|\s*([^|]+?)\s*\|\s*(\w+)\s*\|\s*(\d)\s*\|', reg, re.M):
    code, name, kind, level = row
    if code in sois:
        err('README.md', f'SoI {code} listed twice')
    if kind not in ('Vehicle', 'Logical', 'Physical', 'Component'):
        err('README.md', f'SoI {code}: unknown kind {kind}')
    sois[code] = dict(name=name, kind=kind, level=int(level))

# --- known tests and decisions
tests = set(re.findall(r'\*\*(T\d\.\d)\*\*', read(os.path.join(ROOT, 'system', 'phases.md'))))
decisions = set()
for f in glob.glob(os.path.join(ROOT, 'decisions', '*.md')):
    decisions |= set(re.findall(r'^## ([A-Z]+-\d+) ', read(f), re.M))

# --- parse the SoI files
FIELDS = {'Derived-from', 'Allocated-to', 'Phase', 'Verification', 'Realised-by', 'Decisions'}
reqs = {}
for code in sois:
    path = os.path.join(REQ, code + '.md')
    if not os.path.exists(path):
        err('README.md', f'SoI {code} has no {code}.md')
        continue
    text = read(path)
    if '—' in text:
        err(f'{code}.md', 'contains an em-dash')
    for block in re.split(r'^### ', text, flags=re.M)[1:]:
        rid = block.split('\n', 1)[0].strip()
        where = f'{code}.md {rid}'
        if not re.fullmatch(r'[A-Z][A-Z0-9]*-R\d{3}', rid):
            err(where, 'ID is not <CODE>-Rnnn')
            continue
        if rid.rsplit('-R', 1)[0] != code:
            err(where, f'ID does not belong in the file of {code}')
        if rid in reqs:
            err(where, 'duplicate ID')
            continue
        m = re.search(r'\*\*Statement\.\*\*\s*(.+)', block)
        r = dict(id=rid, soi=code, level=sois[code]['level'], statement=m.group(1).strip() if m else '', f={})
        if not m or ' shall ' not in ' ' + r['statement'] + ' ':
            err(where, 'no Statement containing "shall"')
        for k, v in re.findall(r'^- ([A-Za-z-]+):\s*(.*)$', block, re.M):
            if k not in FIELDS:
                err(where, f'unknown field {k}')
            r['f'][k] = v.strip()
        reqs[rid] = r


def ids(v):
    return [] if v in ('', '-') else [x.strip() for x in v.split(',')]


for r in reqs.values():
    where = f'{r["soi"]}.md {r["id"]}'
    f = r['f']
    for k in ('Derived-from', 'Allocated-to', 'Phase'):
        if k not in f:
            err(where, f'missing {k}')
    r['up'], r['down'] = ids(f.get('Derived-from', '-')), ids(f.get('Allocated-to', '-'))
    leaf = not r['down']
    if r['level'] == 0 and r['up']:
        err(where, 'a level 0 requirement derives from nothing')
    if r['level'] > 0 and not r['up']:
        err(where, 'derives from nothing')
    for p in r['up']:
        if p not in reqs:
            err(where, f'Derived-from {p} does not exist')
        elif reqs[p]['level'] != r['level'] - 1:
            err(where, f'Derived-from {p} is not one level up')
        elif r['soi'] not in ids(reqs[p]['f'].get('Allocated-to', '-')):
            err(where, f'{p} does not allocate to {r["soi"]}')
    for c in r['down']:
        if c not in sois:
            err(where, f'Allocated-to {c} is not a SoI')
        elif sois[c]['level'] != r['level'] + 1:
            err(where, f'Allocated-to {c} is not one level down')
        elif not any(x['soi'] == c and r['id'] in ids(x['f'].get('Derived-from', '-')) for x in reqs.values()):
            err(where, f'allocated to {c} but {c} has no requirement derived from it')
    try:
        ph = int(f.get('Phase', ''))
        if not 1 <= ph <= 5:
            raise ValueError
        r['phase'] = ph
    except ValueError:
        err(where, 'Phase is not 1 to 5')
    if leaf:
        if f.get('Realised-by') not in ('HW', 'SW', 'SYS'):
            err(where, 'a leaf needs Realised-by HW, SW or SYS')
    elif 'Realised-by' in f:
        err(where, 'only a leaf has Realised-by')
    if (leaf or r['level'] == 0) and 'Verification' not in f:
        err(where, 'needs Verification')
    if 'Verification' in f:
        method, _, ref = f['Verification'].partition(' ')
        if method not in ('Test', 'Inspection', 'Analysis', 'Demo') or not ref:
            err(where, 'Verification is "<Test|Inspection|Analysis|Demo> <reference>"')
        for t in re.findall(r'\bT\d\.\d\b', ref):
            if t not in tests:
                err(where, f'unknown test {t}')
    for d in ids(f.get('Decisions', '-')):
        if d not in decisions:
            err(where, f'unknown decision {d}')
for r in reqs.values():
    for p in r['up']:
        if p in reqs and 'phase' in r and 'phase' in reqs[p] and r['phase'] > reqs[p]['phase']:
            err(f'{r["soi"]}.md {r["id"]}', f'phase {r["phase"]} is later than {p} (phase {reqs[p]["phase"]})')

# --- TRACE.md
kids = {}
for r in reqs.values():
    for p in r.get('up', []):
        kids.setdefault(p, []).append(r['id'])


def tree(rid, depth, out):
    r = reqs[rid]
    out.append(f'{"  " * depth}- **{rid}** (phase {r.get("phase", "?")}): {r["statement"]}')
    for c in sorted(kids.get(rid, [])):
        tree(c, depth + 1, out)


trace = ['# Trace', '', 'Generated by [`../tools/check-requirements.py`](../tools/check-requirements.py) from the requirements. Do not edit.',
         '', '## Derivation', '']
roots = sorted(r['id'] for r in reqs.values() if r['level'] == 0)
for rid in roots:
    tree(rid, 0, trace)
if not roots:
    trace.append('No requirements yet.')
cols = sorted({c for r in reqs.values() for c in r.get('down', [])})
trace += ['', '## Allocation', '']
if cols:
    trace += ['| Requirement | ' + ' | '.join(cols) + ' |', '|---|' + '---|' * len(cols)]
    for r in sorted(reqs.values(), key=lambda x: x['id']):
        if r.get('down'):
            trace.append(f'| {r["id"]} | ' + ' | '.join('x' if c in r['down'] else '' for c in cols) + ' |')
else:
    trace.append('Nothing allocated yet.')
trace += ['', '## Leaves', '']
leaves = sorted(r for r in reqs.values() if not r.get('down'))
trace += [f'- {r["soi"]}: {r["id"]} ({r["f"].get("Realised-by", "?")}, {r["f"].get("Verification", "?")})' for r in leaves] or ['None yet.']
trace = '\n'.join(trace) + '\n'

tp = os.path.join(REQ, 'TRACE.md')
if not errors:
    if WRITE:
        open(tp, 'w', encoding='utf-8').write(trace)
    elif not os.path.exists(tp) or read(tp) != trace:
        err('TRACE.md', 'is not what the requirements generate; run with --write')

for e in errors:
    print('FAIL ', e)
if not errors:
    print(f'ok    {len(reqs)} requirements in {len(sois)} systems of interest')
sys.exit(1 if errors else 0)
