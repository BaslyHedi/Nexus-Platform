#!/usr/bin/env python3
"""Rebuild the whole-vehicle mock-up from Hiwonder's chassis + the current fascia.

    python3 make-assembly.py

Reads  : chassis-3deck-fascia.obj  (Hiwonder's .3dm export + our duplicated deck 3)
         fascia-lower.stl, fascia-upper.stl  (current panels, local z 0..52)
Writes : chassis-3deck-fascia.obj  (chassis untouched, fascia groups replaced)
         assembly.stl              (the same thing as one mesh, for renders)

The chassis geometry is never regenerated here - only the FASCIA_* groups are
dropped and rebuilt, so the file stays in step with fascia.scad. Deck tops are
D1T/D2T in fascia.scad; keep the two in sync if the stack ever changes.

Deck 3 is not Hiwonder's: the .3dm is the single-plate version, and the DECK3f_*
groups are our own copy of deck 2. They were built on the assumption that both
gaps are 50 mm. The real upper gap measured 40 mm (2026-09-20), so the plate is
dropped 10 mm here and its four standoffs are shortened to 40 mm about their
bases. Fix the source CAD and this becomes unnecessary.
"""
SO_U = 40.0          # upper standoff, measured
D2T, D3B_OLD = 81.12, 131.12
import re, struct, sys, os

OBJ = "chassis-3deck-fascia.obj"
PANELS = [("FASCIA_LOWER", "fascia-lower.stl", 29.12), ("FASCIA_UPPER", "fascia-upper.stl", 81.12)]

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def read_stl(path, dz):
    d = open(path, "rb").read()
    if d[:5] == b"solid" and b"facet" in d[:400]:
        v = [tuple(map(float, m.groups()))
             for m in re.finditer(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", d)]
    else:
        n = struct.unpack("<I", d[80:84])[0]
        v = []
        for i in range(n):
            f = struct.unpack("<12f", d[84 + i * 50:84 + i * 50 + 48])
            v += [f[3:6], f[6:9], f[9:12]]
    return [(x, y, z + dz) for x, y, z in v]


def deck3_index_sets(lines):
    """Vertex indices used by our duplicated deck 3, split plate vs standoff.

    Those groups carry only faces; their vertices live elsewhere in the file, so
    they have to be found through the faces rather than by position.
    """
    plate, pillar, name = set(), set(), ""
    for line in lines:
        if line.startswith("g "):
            name = line[2:].strip()
        elif line.startswith("f ") and name.startswith("DECK3f"):
            tgt = pillar if "铜色" in name else plate
            for t in line.split()[1:]:
                tgt.add(int(t.split("/")[0]))
    return plate, pillar


def main():
    lines = open(OBJ).readlines()
    plate3, pillar3 = deck3_index_sets(lines)

    keep, verts, dropped = [], [], 0
    cur_kept = True
    vi = 0
    for line in lines:
        if line.startswith("v "):
            vi += 1
            if vi in plate3 or vi in pillar3:
                x, y, z = (float(t) for t in line.split()[1:4])
                if vi in pillar3:                      # shorten about its base
                    z = D2T + (z - D2T) * (SO_U / (D3B_OLD - D2T))
                else:                                  # drop the plate
                    z -= (D3B_OLD - D2T) - SO_U
                line = "v %.4f %.4f %.4f\n" % (x, y, z)
            verts.append(line)
            keep.append(line)
        elif line.startswith("g "):
            cur_kept = not line[2:].strip().startswith("FASCIA")
            dropped += 0 if cur_kept else 1
            if cur_kept:
                keep.append(line)
        elif line.startswith(("f ", "vn ", "vt ")):
            if cur_kept or not line.startswith("f "):
                keep.append(line)
        else:
            keep.append(line)

    base = len(verts)
    out = keep[:]
    tris = []
    for name, stl, dz in PANELS:
        v = read_stl(stl, dz)
        out.append(f"g {name}\n")
        for p in v:
            out.append("v %.4f %.4f %.4f\n" % p)
        for i in range(0, len(v), 3):
            out.append("f %d %d %d\n" % (base + i + 1, base + i + 2, base + i + 3))
        base += len(v)
        tris.append((name, len(v) // 3))

    open(OBJ, "w").writelines(out)
    print(f"{OBJ}: dropped {dropped} old fascia group(s), added " +
          ", ".join(f"{n} ({t} tris)" for n, t in tris))

    # flat STL of everything, for renders
    V, F = [], []
    for line in out:
        if line.startswith("v "):
            V.append(tuple(map(float, line.split()[1:4])))
        elif line.startswith("f "):
            idx = [int(t.split("/")[0]) for t in line.split()[1:]]
            for k in range(1, len(idx) - 1):
                F.append((idx[0], idx[k], idx[k + 1]))
    with open("assembly.stl", "wb") as f:
        f.write(b"\0" * 80 + struct.pack("<I", len(F)))
        for a, b, c in F:
            f.write(struct.pack("<12fH", 0, 0, 0, *V[a - 1], *V[b - 1], *V[c - 1], 0))
    print(f"assembly.stl: {len(F)} triangles")


if __name__ == "__main__":
    sys.exit(main())
