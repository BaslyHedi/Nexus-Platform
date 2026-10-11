#!/usr/bin/env python3
"""Check the requirements in requirements/ and generate their traceability views, from one parse of the files.

    python3 tools/check-requirements.py            # exits 1 on any problem, and when a generated file is stale
    python3 tools/check-requirements.py --write    # regenerates requirements/TRACE.md and requirements/renders/traceability.html

What it checks, against system/method.md, requirements/README.md (format) and requirements/rules.md (writing):
  the files     one per system-of-interest or element, named by an ID that the drawings define, in the folder of its level
                (level-0, level-1, level-2/<node>); the block format and fields
  the links     Derived-from one level up and allocated from there; Allocated-to one level down, inside the parent; each plain
                allocation has a child, an as-is one has none; Integration lists exactly the children
  the trace     Function names a function on the logical drawing whose component exists by the requirement's phase; the
                element is listed against that function in the allocation table of system/physical-architecture.md; Need
                on level 0; tests and decisions that exist; a phase never later than a parent's, nor earlier than the element's
  the rules     an EARS pattern, "shall", and the mechanical GtWR rules (R7, R8, R9, R10, R16, R17, R21, R24, R32), no em-dash

What it writes: TRACE.md (needs, tests, derivation, function allocation as tables) and renders/traceability.html, built from
tools/traceability-template.html: the systems as cards in three columns by level, each in its colour from the drawings
(SYSTEMS), its requirements as bubbles, and a line for each derivation and each as-is allocation. Cards fold and unfold one
by one, by column or all at once; a bubble opens its lineage and its fields; light, dark and automatic themes.
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
TRACE_HTML = os.path.join(REQ, 'renders', 'traceability.html')
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
def expected_path(sid):
    """Where a system's file belongs: one folder per level, and level 2 grouped by the node it is inside."""
    return os.path.join({0: 'level-0', 1: 'level-1', 2: os.path.join('level-2', sid[:17])}[level(sid)], sid + '.md')


for path in sorted(glob.glob(os.path.join(REQ, '**', 'Nexus-*.md'), recursive=True)):
    sid = os.path.basename(path)[:-3]
    text = read(path)
    if os.path.relpath(path, REQ) != expected_path(sid):
        err(os.path.relpath(path, REQ), f'belongs in requirements/{expected_path(sid)}')
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
      'do not edit. The interactive view is [renders/traceability.html](renders/traceability.html).', '',
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

# ------------------------------------------------------------------ traceability.html
import json


def first_parent_index(sid):
    """Where a system's parents sit in their own list, so that cards line up with what they derive from."""
    idx = [by_soi[reqs[p]['soi']].index(reqs[p]) for q in by_soi[sid] for p in q['up'] if p in reqs]
    idx += [by_soi[r['soi']].index(r) for r in reqs.values() for a in r['asis'] if a == sid]
    return min(idx) if idx else 999


lvl1 = sorted([s for s in files if level(s) == 1], key=lambda s: (first_parent_index(s), s))
nodes = [s for s in lvl1 if any(parent_system(x) == s for x in files)]
columns = [
    {'title': 'Level 0 · system-of-interest and enabling system', 'groups': [{'label': '', 'systems': [s for s in ('Nexus-Vehicle', 'Nexus-Enabling') if s in files]}]},
    {'title': 'Level 1 · system elements of the vehicle', 'groups': [{'label': '', 'systems': lvl1}]},
    {'title': 'Level 2 · elements of the nodes', 'groups': [
        {'label': f'Inside {n} · {files[n]}', 'systems': sorted([s for s in files if parent_system(s) == n], key=lambda s: (first_parent_index(s), s))}
        for n in nodes]},
]
systems = {}
for sid in files:
    within = {0: 'system-of-interest' if sid == 'Nexus-Vehicle' else 'enabling system, beside the vehicle',
              1: 'element of Nexus-Vehicle', 2: f'element of {parent_system(sid)}'}[level(sid)]
    systems[sid] = {'name': files[sid], 'colour': system_colour(sid)[0], 'within': within, 'reqs': [q['id'] for q in by_soi[sid]]}
data = {'columns': columns, 'systems': systems, 'reqs': {q['id']: {
    'soi': q['soi'], 'text': q['text'], 'up': q['up'], 'kids': sorted(q['kids']), 'der': q['der'], 'asis': q['asis'], 'fn': q['fn'],
    'need': q['f'].get('Need', ''), 'phase': q['f'].get('Phase', ''), 'ver': q['f'].get('Verification', ''),
    'real': q['f'].get('Realised-by', ''), 'dec': q['f'].get('Decisions', '')} for q in reqs.values()}}
counts = ', '.join(f'{sum(1 for q in reqs.values() if q["level"] == l)} at level {l}' for l in (0, 1, 2))
html = read(os.path.join(ROOT, 'tools', 'traceability-template.html'))
html = html.replace('%%SUB%%', f'Generated by tools/check-requirements.py from requirements/; do not edit · {len(reqs)} requirements in '
                    f'{len(files)} files: {counts} · each card is a system in its colour from the drawings, each bubble one of its requirements')
html = html.replace('%%DATA%%', json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))

# ------------------------------------------------------------------ write or compare
if not errors:
    for path, content in [(TRACE_MD, md), (TRACE_HTML, html)]:
        rel = os.path.relpath(path, ROOT)
        if WRITE:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8').write(content)
        elif not os.path.exists(path) or read(path) != content:
            err(rel, 'is not what the requirements generate; run with --write')
for e in errors:
    print('FAIL ', e)
if not errors:
    print(f'ok    {len(reqs)} requirements in {len(files)} files' + ('; TRACE.md and traceability.html written' if WRITE else ''))
sys.exit(1 if errors else 0)
