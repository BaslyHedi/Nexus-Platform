#!/usr/bin/env python3
"""Check that every drawing in hardware/renders/ and system/renders/ is what its script writes (the scripts are the source, never the SVG).

    python3 tools/check-drawings.py        # exits 1 and names the first differing line of each drawing that has drifted

Each script in hardware/scripts/ or system/scripts/ takes the name of its SVG: chassis-layout.py -> chassis-layout.svg, and so on. A drawing that was
edited by hand shows up here; put the change in the script and run it.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DRAWINGS = [('hardware', 'chassis-layout'), ('hardware', 'wiring-schematic'), ('hardware', 'stm32-carrier'),
            ('system', 'Nexus-Platform-Logical-Architecture')]

bad = 0
with tempfile.TemporaryDirectory() as tmp:
    for folder, name in DRAWINGS:
        SCRIPTS = os.path.join(HERE, '..', folder, 'scripts')
        RENDERS = os.path.join(HERE, '..', folder, 'renders')
        out = os.path.join(tmp, name + '.svg')
        r = subprocess.run([sys.executable, '-B', os.path.join(SCRIPTS, name + '.py'), out], capture_output=True, text=True)
        if r.returncode:
            print(f'FAIL  {name}.py did not run:\n{r.stderr}')
            bad += 1
            continue
        mine = open(out, encoding='utf-8').read().split('\n')
        committed = open(os.path.join(RENDERS, name + '.svg'), encoding='utf-8').read().split('\n')
        if mine == committed:
            print(f'ok    {name}.svg')
            continue
        bad += 1
        n = next((i for i, (a, b) in enumerate(zip(mine, committed)) if a != b), min(len(mine), len(committed)))
        print(f'DRIFT {name}.svg differs from {name}.py at line {n + 1} ({len(mine)} lines generated, {len(committed)} committed)')
        print('      script   :', (mine[n] if n < len(mine) else '<end>')[:150])
        print('      committed:', (committed[n] if n < len(committed) else '<end>')[:150])
sys.exit(1 if bad else 0)
