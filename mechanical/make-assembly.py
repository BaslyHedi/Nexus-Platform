#!/usr/bin/env python3
"""Rebuild the whole-vehicle mock-up from Hiwonder's chassis + the current fascia.

    python3 make-assembly.py

Reads  : chassis-3deck-fascia.obj  (Hiwonder's .3dm export + our duplicated deck 3)
         fascia-lower.stl, fascia-upper.stl  (current panels, local z 0..52)
         plate1/*.stl              (plate 1 stand-ins and wire runs, from plate1.py)
Writes : chassis-3deck-fascia.obj  (chassis untouched, fascia and plate 1 groups replaced)
         chassis-3deck-fascia.mtl  (colours, for any viewer that reads OBJ materials)
         assembly.stl              (the same thing as one mesh, for renders)

The chassis geometry is never regenerated here - only the FASCIA_* and P1_* groups
are dropped and rebuilt, so the file stays in step with fascia.scad and plate1.py.
Every group gets a material: the chassis ones from the colour word Hiwonder's CAD
put in each object name, ours from plate1.MATERIALS. Deck tops are
D1T/D2T in fascia.scad; keep the two in sync if the stack ever changes.

Deck 3 is not Hiwonder's: the .3dm is the single-plate version, and the DECK3f_*
groups are our own copy of deck 2. They were built on the assumption that both
gaps are 50 mm. The real upper gap measured 40 mm (2026-09-20), so the plate is
dropped here to sit on 40 mm standoffs, and its four standoffs are shortened
about their bases. Fix the source CAD and this becomes unnecessary.

The seed is rewritten in place, so the adjustment is computed from where deck 3
is NOW, not applied as a fixed offset: re-running is a no-op for the deck. (It
used to subtract 10 mm on every run, so each run sank deck 3 another 10 mm.)
"""
SO_U = 40.0          # upper standoff, measured
D2T = 81.12
import re, struct, sys, os

OBJ = "chassis-3deck-fascia.obj"
MTL = "chassis-3deck-fascia.mtl"
PANELS = [("FASCIA_LOWER", "fascia-lower.stl", 29.12), ("FASCIA_UPPER", "fascia-upper.stl", 81.12)]

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
sys.dont_write_bytecode = True
import plate1  # noqa: E402

# Hiwonder's object names end in a colour word; the plates are anodised black
# sheet, drawn dark grey here so black wires stay visible against them.
CHASSIS_MATS = [("黑色钣金", "chassis_plate", (0.30, 0.32, 0.36, 1)),
                ("黑色螺丝", "chassis_black_screw", (0.15, 0.15, 0.15, 1)),
                ("螺丝", "chassis_screw", (0.62, 0.62, 0.64, 1)),
                ("铜色", "chassis_brass", (0.78, 0.55, 0.22, 1)),
                ("银色", "chassis_silver", (0.72, 0.72, 0.75, 1)),
                ("白色", "chassis_white", (0.95, 0.95, 0.95, 1)),
                ("红色", "chassis_red", (0.80, 0.10, 0.10, 1)),
                ("黑色", "chassis_black", (0.14, 0.14, 0.14, 1))]
EXTRA_MATS = {"fascia": (0.62, 0.66, 0.70, 1), "chassis_default": (0.30, 0.32, 0.36, 1)}


def chassis_mat(group):
    if group.startswith("FASCIA"):
        return "fascia"
    for word, mat, _ in CHASSIS_MATS:
        if word in group:
            return mat
    return "chassis_default"


def write_mtl():
    mats = {m: c for _, m, c in CHASSIS_MATS}
    mats.update(EXTRA_MATS)
    mats.update(plate1.MATERIALS)
    with open(MTL, "w") as f:
        for name, (r, g, b, a) in mats.items():
            f.write(f"newmtl {name}\nKd {r:.3f} {g:.3f} {b:.3f}\nKa 0 0 0\nKs 0.1 0.1 0.1\nd {a:.2f}\n\n")


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


def compact(lines):
    """Drop every vertex no face uses, and renumber the faces.

    Groups this script replaces carry their own vertices, and dropping a group's
    faces used to leave those vertices behind: the seed grew by the whole fascia
    on every run, and had collected about a million orphans by 2026-09-28.
    """
    used = set()
    for line in lines:
        if line.startswith("f "):
            used.update(int(t.split("/")[0]) for t in line.split()[1:])
    new, vi, nv = {}, 0, 0
    for line in lines:
        if line.startswith("v "):
            vi += 1
            if vi in used:
                nv += 1
                new[vi] = nv
    res, vi = [], 0
    for line in lines:
        if line.startswith("v "):
            vi += 1
            if vi in new:
                res.append(line)
        elif line.startswith("f "):
            res.append("f " + " ".join(str(new[int(t.split("/")[0])]) for t in line.split()[1:]) + "\n")
        else:
            res.append(line)
    return res


def main():
    lines = open(OBJ).readlines()
    plate3, pillar3 = deck3_index_sets(lines)

    # where deck 3 sits now: plate underside and standoff top, above plate 2
    vz, vi = {}, 0
    for line in lines:
        if line.startswith("v "):
            vi += 1
            if vi in plate3 or vi in pillar3:
                vz[vi] = float(line.split()[3])
    plate_bot = min(vz[i] for i in plate3)
    pillar_top = max(vz[i] for i in pillar3)
    drop = plate_bot - (D2T + SO_U)             # 0 once the seed is right
    scale = SO_U / (pillar_top - D2T)           # 1 once the seed is right

    keep, verts, dropped = [], [], 0
    cur_kept = True
    vi = 0
    for line in lines:
        if line.startswith("v "):
            vi += 1
            if vi in plate3 or vi in pillar3:
                x, y, z = (float(t) for t in line.split()[1:4])
                if vi in pillar3:                      # shorten about its base
                    z = D2T + (z - D2T) * scale
                else:                                  # drop the plate
                    z -= drop
                line = "v %.4f %.4f %.4f\n" % (x, y, z)
            verts.append(line)
            keep.append(line)
        elif line.startswith(("mtllib", "usemtl")):
            continue                                   # re-added below
        elif line.startswith("g "):
            gname = line[2:].strip()
            cur_kept = not gname.startswith(("FASCIA", "P1_"))
            dropped += 0 if cur_kept else 1
            if cur_kept:
                keep.append(line)
                keep.append(f"usemtl {chassis_mat(gname)}\n")
        elif line.startswith(("f ", "vn ", "vt ")):
            if cur_kept or not line.startswith("f "):
                keep.append(line)
        else:
            keep.append(line)

    base = len(verts)
    out = [f"mtllib {MTL}\n"] + keep
    tris = []
    plate1.PARTS.clear()
    plate1.build()
    groups = [(n, s, dz, "fascia") for n, s, dz in PANELS]
    groups += [("P1_" + n, os.path.join("plate1", n + ".stl"), 0.0, m) for n, m, _ in plate1.PARTS]
    for name, stl, dz, mat in groups:
        v = read_stl(stl, dz)
        out.append(f"g {name}\n")
        out.append(f"usemtl {mat}\n")
        for p in v:
            out.append("v %.4f %.4f %.4f\n" % p)
        for i in range(0, len(v), 3):
            out.append("f %d %d %d\n" % (base + i + 1, base + i + 2, base + i + 3))
        base += len(v)
        tris.append((name, len(v) // 3))

    out = compact(out)
    open(OBJ, "w").writelines(out)
    write_mtl()
    print(f"{OBJ}: dropped {dropped} old fascia / plate 1 group(s), added {len(tris)} groups, "
          f"{sum(t for _, t in tris)} tris; {MTL} written")

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
