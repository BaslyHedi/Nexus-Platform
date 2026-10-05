#!/usr/bin/env python3
"""The FIRST chassis layout drawing, as generated on 2026-09-20 (kept for provenance only - it does NOT make today's SVG).

    python3 extract-plate-outline.py plate.json
    python3 gen-layout-2026-09-20.py [out.svg]        # reads ./plate.json

This drew the three identical plates at 1.7 px/mm from the CAD outline, with the deck stack elevation and the first component
blocks. Since 2026-09-24 `hardware/renders/chassis-layout.svg` has been edited in place, around thirty times (the measured gaps, the
hole survey, the plate 2 lower face as the harness board, the carrier, the cut table), and no generator has been kept in step with
those edits. The SVG is the source of truth; this script and its notes (old HD-nn decision numbers, a placeholder battery) only show
how the drawing started. Recovered verbatim from the session transcript apart from the two input/output paths.
"""
import json, sys
S=json.load(open('plate.json'))     # from extract-plate-outline.py
SC=1.7; X0=60.0; YMIN=-138.38; XMIN=-57.78; H=120.42*SC
def pt(x,y,top): return (X0+(y-YMIN)*SC, top+(x-XMIN)*SC)
def path(top):
    return " ".join(("M" if i==0 else "L")+"%.1f %.1f"%pt(x,y,top) for i,(x,y) in enumerate(S))+" Z"
def box(x0,y0,x1,y1,top):
    a=pt(x0,y0,top); b=pt(x1,y1,top)
    return min(a[0],b[0]),min(a[1],b[1]),abs(b[0]-a[0]),abs(b[1]-a[1])

o=[]
o.append('<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="920" viewBox="0 0 1320 920" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">')
o.append('<defs><marker id="d" markerWidth="8" markerHeight="8" refX="1" refY="3" orient="auto"><path d="M6,0 L0,3 L6,6 z" fill="#64748b"/></marker><marker id="e" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#64748b"/></marker></defs>')
o.append('<rect width="1320" height="920" fill="#fbfaf8"/>')
o.append('<text x="40" y="32" font-size="18" font-weight="700" fill="#1a1a1a">NEXUS — chassis deck layout</text>')
o.append('<text x="40" y="52" font-size="11" fill="#666">Hiwonder Ackermann advanced kit · three identical plates, outline traced from Hiwonder\'s own CAD · 1.7 px/mm · front of vehicle to the LEFT</text>')
o.append('<text x="40" y="68" font-size="11" font-weight="700" fill="#b45309">⚠ Deck spacing is NOT confirmed — the stack is drawn at the equal 50 mm gaps the CAD implies; the photos of the real kit suggest otherwise. Measure both standoffs.</text>')

decks=[(132,'UPPER DECK — plate 3','top face z 133.12 · NOT YET ALLOCATED','#94a3b8','7 4','#f8fafc'),
       (390,'MIDDLE DECK — plate 2','top face z 81.12 · NOT YET ALLOCATED','#94a3b8','7 4','#f8fafc'),
       (648,'LOWER DECK — plate 1','top face z 29.12 · DEFINED — motors already mounted','#334155','none','#ffffff')]
for top,title,sub,stroke,dash,fill in decks:
    o.append(f'<text x="60" y="{top-22}" font-size="13" font-weight="700" fill="#1a1a1a">{title}</text>')
    o.append(f'<text x="60" y="{top-8}" font-size="9.5" fill="#64748b">{sub}</text>')
    dashattr='' if dash=='none' else f' stroke-dasharray="{dash}"'
    o.append(f'<path d="{path(top)}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"{dashattr}/>')
    # rear cross-slot
    x,y,w,h=box(-34.22,121.94,39.19,127.32,top)
    o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w/2:.1f}" fill="#e2e8f0" stroke="#94a3b8" stroke-width="0.8"/>')
    for sx,sy in [(-35.61,118.46),(40.57,118.46),(-35.61,-111.05),(40.57,-111.05)]:
        cx,cy=pt(sx,sy,top)
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.4" fill="#fde68a" stroke="#a16207" stroke-width="1.2"/>')
    for fx,fy in [(-41.34,124.54),(46.30,124.54)]:
        cx,cy=pt(fx,fy,top)
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="none" stroke="#7c3aed" stroke-width="1.5"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.5" fill="#7c3aed"/>')

# ---- plate 3 / 2 notes
o.append('<text x="300" y="215" font-size="12" font-weight="700" fill="#94a3b8" text-anchor="middle">to be defined</text>')
o.append('<text x="300" y="238" font-size="9" fill="#94a3b8" text-anchor="middle">candidates: Raspberry Pi 5 (BOM 6.1, later phase) · vision / sensors · camera mast</text>')
o.append('<text x="300" y="262" font-size="8.5" fill="#7c3aed" text-anchor="middle">fascia upper panel clamps here — 2 × M3×8 driven down from the top (HD-26)</text>')
o.append('<text x="300" y="470" font-size="12" font-weight="700" fill="#94a3b8" text-anchor="middle">to be defined</text>')
o.append('<text x="300" y="493" font-size="9" fill="#94a3b8" text-anchor="middle">the obvious tenants are the compute boards and the power stage — not yet decided</text>')
o.append('<text x="300" y="517" font-size="8.5" fill="#7c3aed" text-anchor="middle">one M3×12 through this plate clamps BOTH fascia panels (HD-26)</text>')
o.append('<text x="300" y="540" font-size="8.5" fill="#b45309" text-anchor="middle">gap ABOVE carries the 3 debug ports · gap BELOW has the switch bodies</text>')

# ---- plate 1 content
top=648
x,y,w,h=box(-17.5,-119.1,22.5,-90.3,top)
o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="#fff7ed" stroke="#c2410c" stroke-width="1.4"/>')
o.append(f'<text x="{x+w/2:.1f}" y="{y+h/2-3:.1f}" font-size="8.5" font-weight="700" fill="#c2410c" text-anchor="middle">SERVO</text>')
o.append(f'<text x="{x+w/2:.1f}" y="{y+h/2+9:.1f}" font-size="7.5" fill="#c2410c" text-anchor="middle">LD-1501MG</text>')
o.append(f'<text x="{X0+8:.0f}" y="{top+H/2:.0f}" font-size="8.5" font-weight="700" fill="#475569">Ackermann</text>')
o.append(f'<text x="{X0+8:.0f}" y="{top+H/2+12:.0f}" font-size="7.8" fill="#475569">front axle</text>')
for (x0,y0,x1,y1),lab in [((-63.7,64.8,-1.1,101.7),'MOTOR L'),((6.1,64.8,68.7,101.7),'MOTOR R')]:
    bx,by,bw,bh=box(x0,y0,x1,y1,top)
    o.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="#eef2ff" stroke="#4338ca" stroke-width="1.4"/>')
    o.append(f'<text x="{bx+bw/2:.1f}" y="{by+bh/2-2:.1f}" font-size="8.5" font-weight="700" fill="#4338ca" text-anchor="middle">{lab}</text>')
    o.append(f'<text x="{bx+bw/2:.1f}" y="{by+bh/2+9:.1f}" font-size="7.5" fill="#4338ca" text-anchor="middle">JGB37-520</text>')
bx,by,bw,bh=box(-30,-30,30,40,top)
o.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="#fef2f2" stroke="#b91c1c" stroke-width="1.4" stroke-dasharray="5 3"/>')
o.append(f'<text x="{bx+bw/2:.1f}" y="{by+bh/2-4:.1f}" font-size="9" font-weight="700" fill="#b91c1c" text-anchor="middle">3S LiPo 11.1 V</text>')
o.append(f'<text x="{bx+bw/2:.1f}" y="{by+bh/2+8:.1f}" font-size="7.5" fill="#b91c1c" text-anchor="middle">PLACEHOLDER — real size still open</text>')
o.append(f'<text x="480" y="{top+H+30:.0f}" font-size="8" fill="#b45309" text-anchor="middle">motors reach to 29.8 mm from the rear edge — the switch bodies stop ~8 mm short of them</text>')

o.append(f'<line x1="60" y1="{648+H+46:.0f}" x2="518" y2="{648+H+46:.0f}" stroke="#94a3b8" stroke-width="1" marker-start="url(#d)" marker-end="url(#e)"/>')
o.append(f'<text x="289" y="{648+H+60:.0f}" font-size="9" fill="#64748b" text-anchor="middle">270 mm · widest 120.4 mm at the front axle, 84.7 mm at the waist, 97.3 mm across the rear face</text>')
o.append(f'<text x="63" y="{648+H+60:.0f}" font-size="9" fill="#64748b">◀ FRONT</text>')
o.append(f'<text x="515" y="{648+H+60:.0f}" font-size="9" fill="#64748b" text-anchor="end">REAR ▶</text>')

# ---- side elevation
o.append('<text x="600" y="110" font-size="13" font-weight="700" fill="#1a1a1a">DECK STACK — side elevation</text>')
o.append('<line x1="600" y1="118" x2="1280" y2="118" stroke="#e2e8f0"/>')
rows=[(156,'plate 3  z 131.12–133.12'),(278,'plate 2  z 79.12–81.12'),(400,'plate 1  z 27.12–29.12')]
for yy,lab in rows:
    o.append(f'<rect x="600" y="{yy}" width="300" height="4.7" fill="#cbd5e1" stroke="#94a3b8"/>')
    o.append(f'<text x="908" y="{yy+6}" font-size="9" font-weight="700" fill="#334155">{lab}</text>')
o.append('<rect x="600" y="160.7" width="300" height="117.3" fill="#fffbeb" stroke="#f59e0b" stroke-dasharray="4 3"/>')
o.append('<text x="750" y="212" font-size="8.5" fill="#92400e" text-anchor="middle">UPPER GAP — drawn 50 mm, UNVERIFIED</text>')
o.append('<text x="750" y="226" font-size="8" fill="#92400e" text-anchor="middle">photos suggest ~45 mm · fascia upper panel: USB-C · DE-9 · Mini-B</text>')
o.append('<rect x="600" y="282.7" width="300" height="117.3" fill="#fffbeb" stroke="#f59e0b" stroke-dasharray="4 3"/>')
o.append('<text x="750" y="334" font-size="8.5" fill="#92400e" text-anchor="middle">LOWER GAP — drawn 50 mm, UNVERIFIED</text>')
o.append('<text x="750" y="348" font-size="8" fill="#92400e" text-anchor="middle">photos suggest ~55 mm · fascia lower panel: DRIVE / LOGIC switches</text>')
o.append('<text x="600" y="420" font-size="8.5" fill="#64748b">below plate 1: running gear, wheels, ground clearance — nothing mounted</text>')

o.append('<text x="600" y="470" font-size="13" font-weight="700" fill="#1a1a1a">WHAT IS FIXED, AND WHAT IS NOT</text>')
o.append('<line x1="600" y1="478" x2="1280" y2="478" stroke="#e2e8f0"/>')
notes=[('#b45309','Deck spacing — the open question',[
    'The single-plate CAD gives one 50 mm standoff, and the 3-deck model simply repeats it. The photos of',
    'the built kit do not agree: the lower gap reads ~55 mm and the upper ~45 mm on a tape. Both fascia',
    'panels are cut to 52 mm tall, so this decides whether they fit at all. Measure each standoff.']),
 ('#1e293b','Plate 1 — fixed',[
    'Motors are mounted and the battery goes here: the heaviest mass low and central. Each motor reaches',
    'from the centreline out past the plate edge to its wheel, 29.8–66.7 mm forward of the rear edge.']),
 ('#1e293b','Plate 2 / 3 — open',[
    'Deliberately blank. Compute boards, power stage and the Pi 5 all want deck space; nothing is committed',
    'until the wiring and thermal picture settle.']),
 ('#1e293b','The fascia already constrains all three',[
    'Purple rings are the clamp holes (y 124.54 from centre, x −41.34 / +46.30), present on every plate.',
    'Yellow circles are the four standoffs. Plate 2\'s single M3×12 clamps both panels at once (HD-26).']),
 ('#1e293b','Keep clear of the rear on plate 1',[
    'Switch bodies protrude ~25 mm into the lower gap and the motors start 29.8 mm in, leaving about 8 mm',
    'between them — confirm with the switches in hand before printing (HD-26).']),
 ('#1e293b','Battery and servo blocks are indicative',[
    'The servo box is traced from the CAD; the battery is a placeholder until the pack is measured (BOM).'])]
yy=498
for col,head,lines in notes:
    o.append(f'<text x="600" y="{yy}" font-size="9.5" font-weight="700" fill="{col}">{head}</text>')
    yy+=14
    for ln in lines:
        o.append(f'<text x="600" y="{yy}" font-size="9" fill="#475569">{ln}</text>'); yy+=13
    yy+=6
o.append('</svg>')
out='\n'.join(o)
open(sys.argv[1] if len(sys.argv) > 1 else 'chassis-layout-2026-09-20.svg','w').write(out)
print(len(out),'bytes')