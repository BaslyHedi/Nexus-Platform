#!/usr/bin/env python3
"""Check the requirements in requirements/ and generate their traceability views, from one parse of the files.

    python3 tools/check-requirements.py            # exits 1 on any problem, and when a generated file is stale
    python3 tools/check-requirements.py --write    # regenerates requirements/TRACE.md and requirements/renders/traceability.svg

What it checks, against system/method.md, requirements/README.md (format) and requirements/rules.md (writing):
  the files     one per system-of-interest or element, named by an ID that the drawings define; the block format and fields
  the links     Derived-from one level up and allocated from there; Allocated-to one level down, inside the parent; each plain
                allocation has a child, an as-is one has none; Integration lists exactly the children
  the trace     Function names a function on the logical drawing whose component exists by the requirement's phase; the
                element is listed against that function in the allocation table of system/physical-architecture.md; Need
                on level 0; tests and decisions that exist; a phase never later than a parent's, nor earlier than the element's
  the rules     an EARS pattern, "shall", and the mechanical GtWR rules (R7, R8, R9, R10, R16, R17, R21, R24, R32), no em-dash

What it writes: TRACE.md (needs, tests, derivation, function allocation as tables) and traceability.svg, the graphical view:
the systems in three columns by level, each in its colour from the drawings (SYSTEMS), its requirements listed inside, and
one link per derivation, coloured by the parent system; an as-is allocation is a dashed link to the element it passes to.
Elements and functions are read from the drawings themselves (system/scripts/*.py), so the drawings stay their single source.
"""
import glob, importlib.util, os, re, sys
from collections import defaultdict
sys.dont_write_bytecode = True

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WRITE = '--write' in sys.argv[1:]
REQ = os.path.join(ROOT, 'requirements')
SCRIPTS = os.path.join(ROOT, 'system', 'scripts')
TRACE_MD = os.path.join(REQ, 'TRACE.md')
TRACE_SVG = os.path.join(REQ, 'renders', 'traceability.svg')
errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


def read(p):
    return open(p, encoding='utf-8').read()


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), os.path.join(SCRIPTS, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ the drawings: elements, functions, phases, colours
LOGICAL = load('Nexus-Platform-Logical-Architecture')
SYSTEMS, system_colour, MONO = LOGICAL.SYSTEMS, LOGICAL.system_colour, LOGICAL.MONO
GROUP = re.compile(r'<g id="(Nexus-[A-Za-z]+-[0-9-]+)">(.*?)</g>', re.S)
functions, component_phase = {}, {}
for cid, body in GROUP.findall(LOGICAL.build()):
    component_phase[cid] = int(re.search(r'>PHASE (\d)<', body).group(1))
    for n in re.findall(r'font-size="8" font-weight="700"[^>]*>(\d+)</text>', body):
        functions[f'{cid}-F{int(n):02d}'] = cid
elements = {'Nexus-Vehicle': ('NEXUS vehicle', 1), 'Nexus-Enabling': ('Enabling system', 1)}
for name in ('Nexus-Platform-Physical-Architecture', 'Nexus-Physical-01-Local-View', 'Nexus-Physical-02-Local-View'):
    for eid, body in GROUP.findall(load(name).build()):
        title = re.search(r'font-size="13" font-weight="700" fill="#111827">(.*?)</text>', body).group(1)
        elements[eid] = (title.replace('&amp;', '&'), int(re.search(r'>PHASE (\d)<', body).group(1)))


def level(sid):
    return 0 if sid in ('Nexus-Vehicle', 'Nexus-Enabling') else 2 if re.fullmatch(r'Nexus-Physical-\d\d-\d\d', sid) else 1


def parent_system(sid):
    return None if level(sid) == 0 else 'Nexus-Vehicle' if level(sid) == 1 else sid[:17]


tests = set(re.findall(r'\*\*(T\d\.\d)\*\*', read(os.path.join(ROOT, 'system', 'phases.md'))))
decisions = set()
for f in glob.glob(os.path.join(ROOT, 'decisions', '*.md')):
    decisions |= set(re.findall(r'^## ([A-Z]+-\d+) ', read(f), re.M))
alloc_table = {}
for line in read(os.path.join(ROOT, 'system', 'physical-architecture.md')).split('\n'):
    m = re.match(r'^\| `(Nexus-Logical-\d{3}-F\d{2})`.*\|([^|]*)\|\s*$', line)
    if m:
        alloc_table[m.group(1)] = set(re.findall(r'\b(\d\d)\b', m.group(2)))

# ------------------------------------------------------------------ the requirement files
FIELDS = ['Need', 'Function', 'Derived-from', 'Allocated-to', 'Phase', 'Verification', 'Realised-by', 'Decisions']
reqs, files = {}, {}
for path in sorted(glob.glob(os.path.join(REQ, 'Nexus-*.md'))):
    sid = os.path.basename(path)[:-3]
    text = read(path)
    m = re.match(r'# (\S+) - (.+)\n', text)
    if not m or m.group(1) != sid:
        err(f'{sid}.md', 'the first line is not "# <ID> - <name>"')
    if sid not in elements:
        err(f'{sid}.md', 'no drawing defines this system or element')
        continue
    files[sid] = m.group(2) if m else sid
    if '—' in text:
        err(f'{sid}.md', 'contains an em-dash')
    for block in re.split(r'^### ', text, flags=re.M)[1:]:
        rid = block.split('\n', 1)[0].strip()
        where = f'{sid}.md {rid}'
        if not re.fullmatch(re.escape(sid) + r'-R\d{3}', rid):
            err(where, f'the ID is not {sid}-Rnnn')
            continue
        if rid in reqs:
            err(where, 'duplicate ID')
            continue
        st = re.search(r'\*\*Statement\.\*\* (.+)', block)
        q = dict(id=rid, soi=sid, level=level(sid), text=st.group(1).strip() if st else '', f={})
        for k, v in re.findall(r'^- ([A-Za-z-]+): (.*)$', block, re.M):
            if k not in FIELDS:
                err(where, f'unknown field {k}')
            q['f'][k] = v.strip()
        reqs[rid] = q

ids = lambda v: [] if v in (None, '', '-') else [x.strip() for x in v.split(',')]
for q in reqs.values():
    f, where = q['f'], f'{q["soi"]}.md {q["id"]}'
    q['up'] = ids(f.get('Derived-from'))
    q['alloc'] = ids(f.get('Allocated-to'))
    q['asis'] = [a[:-8] for a in q['alloc'] if a.endswith(' (as-is)')]
    q['der'] = [a for a in q['alloc'] if not a.endswith(' (as-is)')]
    q['fn'] = ids(f.get('Function'))
    q['kids'] = []
for q in reqs.values():
    for p in q['up']:
        if p in reqs:
            reqs[p]['kids'].append(q['id'])

# ------------------------------------------------------------------ checks
VAGUE = r'\b(some|adequate|sufficient|reasonable|fast|robust|flexible|user-friendly|appropriate|about|etc|minimi[sz]e|maximi[sz]e)\b'
ESCAPE = r'\b(where possible|as appropriate|if necessary|as far as possible|including but not limited to)\b'
for q in reqs.values():
    f, where, sid, t = q['f'], f'{q["soi"]}.md {q["id"]}', q['soi'], q['text']
    enabling = sid == 'Nexus-Enabling'
    # format
    for k in ['Phase', 'Verification'] + ([] if enabling else ['Function', 'Allocated-to']) + (['Need'] if q['level'] == 0 else ['Derived-from']):
        if k not in f:
            err(where, f'missing {k}')
    if enabling and (q['up'] or q['alloc']):
        err(where, 'the enabling system derives from nothing and allocates to nothing')
    try:
        q['phase'] = int(f.get('Phase', ''))
        assert 1 <= q['phase'] <= 5
    except (ValueError, AssertionError):
        err(where, 'Phase is not 1 to 5')
        q['phase'] = 9
    if q['phase'] < elements[sid][1]:
        err(where, f'phase {q["phase"]} is before {sid} exists (phase {elements[sid][1]})')
    # links up
    for p in q['up']:
        if p not in reqs:
            err(where, f'Derived-from {p} does not exist')
            continue
        r = reqs[p]
        if r['soi'] != parent_system(sid) and not (q['level'] == 1 and r['soi'] == 'Nexus-Vehicle'):
            err(where, f'Derived-from {p} is not in the parent of {sid}')
        if sid not in r['der']:
            err(where, f'{p} does not allocate to {sid} (as-is allocations have no children)')
    # links down
    for a in q['asis'] + q['der']:
        if a not in elements:
            err(where, f'Allocated-to {a} is not an element')
        elif level(a) != q['level'] + 1 or parent_system(a) != (sid if q['level'] == 1 else 'Nexus-Vehicle'):
            err(where, f'Allocated-to {a} is not an element of {sid}')
        elif a not in files:
            err(where, f'Allocated-to {a} has no requirements file')
    for a in q['der']:
        if not any(reqs[c]['soi'] == a for c in q['kids']):
            err(where, f'allocated to {a}, which holds no requirement derived from it')
    for a in q['asis']:
        if any(reqs[c]['soi'] == a for c in q['kids']):
            err(where, f'allocated as-is to {a}, which still derives a requirement from it')
    leaf = not q['der']
    if leaf and f.get('Realised-by') is None:
        err(where, 'nothing is derived below it, so it needs Realised-by')
    if not leaf and 'Realised-by' in f:
        err(where, 'requirements are derived below it, so it has no Realised-by')
    for rb in ids(f.get('Realised-by')):
        if rb not in ('HW', 'SW', 'SYS'):
            err(where, f'Realised-by {rb} is not HW, SW or SYS')
    # verification
    v = f.get('Verification', '')
    method, _, ref = v.partition(' ')
    if method not in ('Test', 'Inspection', 'Analysis', 'Demo', 'Integration') or not ref:
        err(where, 'Verification is "<Test|Inspection|Analysis|Demo|Integration> <reference>"')
    if method == 'Integration':
        if leaf:
            err(where, 'Integration needs children to integrate')
        elif set(ids(ref)) != set(q['kids']):
            err(where, f'Integration lists {", ".join(sorted(set(ids(ref)) ^ set(q["kids"])))} differently from its children')
    for tref in re.findall(r'\bT\d\.\d\b', v + ' ' + f.get('Need', '')):
        if tref not in tests:
            err(where, f'unknown test {tref}')
    for d in ids(f.get('Decisions')):
        if d not in decisions:
            err(where, f'unknown decision {d}')
    # trace across
    for fn in q['fn']:
        if fn not in functions:
            err(where, f'Function {fn} is not on the logical drawing')
            continue
        if component_phase[functions[fn]] > q['phase']:
            err(where, f'{fn} belongs to a component that starts in phase {component_phase[functions[fn]]}')
        if fn not in alloc_table:
            err(where, f'{fn} has no row in the allocation table')
        elif q['level'] > 0 and sid[15:17] not in alloc_table[fn]:
            err(where, f'the allocation table does not list element {sid[15:17]} against {fn}')
    # writing rules
    if t.count(' shall ') != 1:
        err(where, 'one "shall" per statement (R18)')
    if t.startswith('If ') and ', then ' not in t:
        err(where, 'an unwanted-behaviour statement reads "If <trigger>, then <subject> shall …" (EARS)')
    if re.match(r'(When|While|Where) ', t) and not re.match(r'(When|While|Where) [^,]+, ', t):
        err(where, 'a conditional statement puts a comma after its condition (EARS)')
    for pat, rule in [(VAGUE, 'R7 vague term'), (ESCAPE, 'R8/R9 escape or open clause'), (r'\bbe (able|capable) (to|of)\b', 'R10 superfluous infinitive'),
                      (r'[()]', 'R21 parentheses'), (r'\b(all|any|both)\b', 'R32 use "each"'), (r'\b(it|its|they|them|their)\b', 'R24 pronoun'),
                      (r'\b(should|will|must)\b', '"shall" only'), (r'\bnot\b(?<!shall not)', 'R16 "not"')]:
        hit = re.search(pat, t, re.I)
        if hit and not (rule.startswith('R32') and 'both nodes' in t) and not (rule.startswith('R16') and 'shall not' in t):
            err(where, f'{rule}: "{hit.group(0)}"')
    if re.search(r'(?<!kbit)/(?!s\b)', t):
        err(where, 'R17 oblique "/"')

for q in reqs.values():
    for p in q['up']:
        if p in reqs and q.get('phase', 9) > reqs[p].get('phase', 9):
            err(f'{q["soi"]}.md {q["id"]}', f'phase {q["phase"]} is later than its parent {p} (phase {reqs[p]["phase"]})')

# ------------------------------------------------------------------ TRACE.md
def short(t, n=90):
    return t if len(t) <= n else t[:n - 1].rstrip() + '…'


order = sorted(files, key=lambda s: (level(s), s != 'Nexus-Vehicle', s))
by_soi = defaultdict(list)
for q in sorted(reqs.values(), key=lambda q: q['id']):
    by_soi[q['soi']].append(q)
md = ['# Traceability', '', 'Generated by [`../tools/check-requirements.py`](../tools/check-requirements.py) from the requirement files; '
      'do not edit. The graphical view is [renders/traceability.svg](renders/traceability.svg).', '',
      f'{len(reqs)} requirements in {len(files)} files: ' + ', '.join(f'{sum(1 for q in reqs.values() if q["level"] == l)} at level {l}' for l in (0, 1, 2)) + '.', '',
      '## Needs', '', '| Need | Requirements |', '|---|---|']
needs = defaultdict(list)
for q in reqs.values():
    for n in [x.strip() for x in q['f'].get('Need', '').split(',') if x.strip()]:
        needs[n].append(q['id'])
for n in sorted(needs):
    md.append(f'| {n} | {", ".join(sorted(needs[n]))} |')
md += ['', '## Tests', '', 'Each phase test and the requirements it verifies directly.', '', '| Test | Requirements |', '|---|---|']
by_test = defaultdict(list)
for q in reqs.values():
    if not q['f'].get('Verification', '').startswith('Integration'):
        for tref in re.findall(r'\bT\d\.\d\b', q['f'].get('Verification', '')):
            by_test[tref].append(q['id'])
for tref in sorted(tests):
    md.append(f'| {tref} | {", ".join(sorted(by_test[tref])) or "none"} |')
md += ['', '## Function allocation', '', 'Which systems hold requirements on each function, from the `Function` fields.', '',
       '| Function | Systems |', '|---|---|']
fn_sys = defaultdict(set)
for q in reqs.values():
    for fn in q['fn']:
        fn_sys[fn].add(q['soi'].replace('Nexus-Physical-', ''))
for fn in sorted(fn_sys):
    md.append(f'| `{fn}` | {", ".join(sorted(fn_sys[fn]))} |')
md += ['', '## Derivation', '']


def tree(rid, depth):
    q = reqs[rid]
    asis = f' *(as-is to {", ".join(q["asis"])})*' if q['asis'] else ''
    md.append(f'{"  " * depth}- **{rid}**: {short(q["text"])}{asis}')
    for c in sorted(q['kids']):
        tree(c, depth + 1)


for q in by_soi['Nexus-Vehicle']:
    tree(q['id'], 0)
md.append('')
md = '\n'.join(md) + '\n'

# ------------------------------------------------------------------ traceability.svg
COLW, GAP, X0, Y0, ROWH, HEAD, PAD, BOXGAP = 560, 230, 40, 150, 15, 40, 10, 22
cols = {l: [s for s in order if level(s) == l] for l in (0, 1, 2)}
row_y, box = {}, {}


def place(col):
    y = Y0
    for sid in col:
        h = HEAD + ROWH * len(by_soi[sid]) + PAD
        box[sid] = (X0 + level(sid) * (COLW + GAP), y, h)
        for i, q in enumerate(by_soi[sid]):
            row_y[q['id']] = y + HEAD + ROWH * i + ROWH / 2 + 2
        y += h + BOXGAP
    return y


def barycentre(sid):
    ys = [row_y[p] for q in by_soi[sid] for p in q['up'] if p in row_y]
    ys += [row_y[r['id']] for r in reqs.values() for a in r['asis'] if a == sid and r['id'] in row_y]
    return sum(ys) / len(ys) if ys else 1e9


bottom = place(cols[0])
cols[1].sort(key=lambda s: (barycentre(s), s))
bottom = max(bottom, place(cols[1]))
cols[2].sort(key=lambda s: (parent_system(s), barycentre(s), s))
bottom = max(bottom, place(cols[2]))
W, H = X0 * 2 + 3 * COLW + 2 * GAP, int(bottom + 90)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">',
       f'<rect width="{W}" height="{H}" fill="#fbfaf8"/>',
       '<text x="40" y="44" font-size="24" font-weight="700" fill="#1a1a1a">Nexus Platform Requirements Traceability</text>',
       '<text x="40" y="68" font-size="12" fill="#555">Generated by tools/check-requirements.py from requirements/ · each box is a system or element, '
       'in its colour from the drawings · each line is a derivation, from the parent requirement to the child, in the colour of the parent system · '
       'a dashed line passes a requirement as-is to an element · hover a row for its full statement</text>']
for l, title in [(0, 'LEVEL 0 · SYSTEM-OF-INTEREST AND ENABLING SYSTEM'), (1, 'LEVEL 1 · SYSTEM ELEMENTS OF THE VEHICLE'), (2, 'LEVEL 2 · ELEMENTS OF THE NODES')]:
    svg.append(f'<text x="{X0 + l * (COLW + GAP)}" y="{Y0 - 22}" font-size="10" font-weight="700" fill="#6b7280" letter-spacing="1">{title}</text>')
links = []
for q in sorted(reqs.values(), key=lambda q: q['id']):
    stroke = system_colour(q['soi'])[0]
    x1 = box[q['soi']][0] + COLW
    for c in sorted(q['kids']):
        x2, y1, y2 = box[reqs[c]['soi']][0], row_y[q['id']], row_y[c]
        links.append(f'<path d="M{x1},{y1:.1f} C{x1 + GAP / 2},{y1:.1f} {x2 - GAP / 2},{y2:.1f} {x2},{y2:.1f}" fill="none" stroke="{stroke}" stroke-width="1" stroke-opacity="0.55"/>')
    for a in q['asis']:
        if a in box:
            x2, y1, y2 = box[a][0], row_y[q['id']], box[a][1] + 20
            links.append(f'<path d="M{x1},{y1:.1f} C{x1 + GAP / 2},{y1:.1f} {x2 - GAP / 2},{y2:.1f} {x2},{y2:.1f}" fill="none" stroke="{stroke}" stroke-width="1.2" stroke-dasharray="5 3" stroke-opacity="0.8"/>')
svg += links
for sid in order:
    x, y, h = box[sid]
    stroke, fill = system_colour(sid)
    within = {0: 'the system-of-interest' if sid == 'Nexus-Vehicle' else 'beside the vehicle', 1: 'in Nexus-Vehicle', 2: f'in {parent_system(sid)}'}[level(sid)]
    svg += [f'<g id="{sid}">',
            f'<rect x="{x}" y="{y}" width="{COLW}" height="{h}" rx="4" fill="#ffffff" stroke="{stroke}" stroke-width="1.6"/>',
            f'<path d="M{x},{y + 4} a4,4 0 0 1 4,-4 h{COLW - 8} a4,4 0 0 1 4,4 v{HEAD - 8} h-{COLW} z" fill="{fill}"/>',
            f'<text x="{x + 10}" y="{y + 14}" font-size="9.5" font-weight="700" fill="{stroke}" font-family="{MONO}">{sid}</text>',
            f'<text x="{x + COLW - 10}" y="{y + 14}" font-size="9" fill="{stroke}" text-anchor="end">{within} · {len(by_soi[sid])} requirements</text>',
            f'<text x="{x + 10}" y="{y + 29}" font-size="12.5" font-weight="700" fill="#111827">{esc(files[sid])}</text>']
    for q in by_soi[sid]:
        ry = row_y[q['id']]
        tag = ' · as-is' if q['asis'] else ''
        svg += [f'<g><title>{esc(q["id"] + ": " + q["text"])}</title>',
                f'<text x="{x + 10}" y="{ry + 3.5:.1f}" font-size="9" font-weight="700" fill="{stroke}" font-family="{MONO}">{q["id"][-4:]}</text>',
                f'<text x="{x + 48}" y="{ry + 3.5:.1f}" font-size="9.5" fill="#374151">{esc(short(q["text"], 92 - len(tag)))}'
                f'{f"<tspan font-weight=\"700\" fill=\"{stroke}\">{tag}</tspan>" if tag else ""}</text></g>']
    svg.append('</g>')
ly = H - 40
svg.append(f'<text x="40" y="{ly}" font-size="10" font-weight="700" fill="#1a1a1a">SYSTEMS</text>')
x = 110
for sid in SYSTEMS:
    if sid in files:
        stroke, fill = SYSTEMS[sid]
        label = sid.replace('Nexus-Physical-', '')
        svg += [f'<rect x="{x}" y="{ly - 11}" width="16" height="14" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>',
                f'<text x="{x + 21}" y="{ly}" font-size="9" font-weight="700" fill="{stroke}" font-family="{MONO}">{label}</text>']
        x += 30 + 6 * len(label)
svg.append(f'<text x="{x + 10}" y="{ly}" font-size="10" fill="#374151">elements inside a node take the colour of the node · '
           'solid line: derived · dashed line: allocated as-is</text>')
svg = '\n'.join(svg + ['</svg>']) + '\n'

# ------------------------------------------------------------------ write or compare
if not errors:
    for path, content in [(TRACE_MD, md), (TRACE_SVG, svg)]:
        rel = os.path.relpath(path, ROOT)
        if WRITE:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8').write(content)
        elif not os.path.exists(path) or read(path) != content:
            err(rel, 'is not what the requirements generate; run with --write')
for e in errors:
    print('FAIL ', e)
if not errors:
    print(f'ok    {len(reqs)} requirements in {len(files)} files' + ('; TRACE.md and traceability.svg written' if WRITE else ''))
sys.exit(1 if errors else 0)
