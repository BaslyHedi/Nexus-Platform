# Mechanical - rear fascia and the chassis it mounts to

Everything the rear fascia is built from. The **why** lives in the design decisions
([`../decisions/README.md`](../decisions/README.md));
this folder owns the geometry, and the table below says which file is which.

| File | Size | What it is |
|---|---|---|
| [`fascia.scad`](fascia.scad) | 18 kB | **Source of truth for both panels.** Every dimension, and why, in comments. Edit only here |
| [`fascia-lower.stl`](fascia-lower.stl) | 1.3 MB | Print file - lower panel, 124.2 × 18.9 × **52** mm, 19.6 cm³ (~25 g in PETG) |
| [`fascia-upper.stl`](fascia-upper.stl) | 2.2 MB | Print file - upper panel, 124.2 × 18.9 × **42** mm, 16.7 cm³ (~21 g in PETG) |
| **Hiwonder** · *Ackermann Chassis (Single Layer)* `.3dm` | 186 MB | Hiwonder's own CAD, untouched. **Not in the repository** - it is theirs, not ours to redistribute, and it has to be fetched by hand on a fresh clone. Every chassis number in the project is measured from this, not from photos - see [`../bom/parts/2.1-Hiwonder-Ackermann-Chassis/SPECS.md`](../bom/parts/2.1-Hiwonder-Ackermann-Chassis/SPECS.md). It is the **single-plate** version |
| `chassis-3deck-fascia.obj` | 65 MB | Whole-vehicle mock-up: Hiwonder's chassis + our deck 3 + the current panels. **Untracked, and a seed rather than output** - `make-assembly.py` reads it and rewrites it in place, so it cannot be rebuilt from this repository alone. It began as a Rhino export of the `.3dm`. Keep a local backup |
| `assembly.stl` | 69 MB | The same assembly as one mesh, for renders. **Generated and untracked** - delete it and re-run |
| [`plate1.py`](plate1.py) | 20 kB | **Plate 1 stand-ins for an eye review** (MEC-16): every component and every wire run as its own STL in `plate1/`, at the assumed sizes. Not for building from |
| `plate1/*.stl`, `plate1/states/`, `chassis-3deck-fascia.mtl` | 1 MB | **Generated and untracked** - the parts; the two wires that cross between the decks in the `raised` and `open` positions (plate 2 lowering, 60 mm up, or hinged over like a book); and the colours. Re-run the two scripts |
| [`animate-assembly.py`](animate-assembly.py) | 8 kB | **Assembly animation** of the harness-board sandwich, in MEC-16's build order: parts onto the upturned plate 2, wires run by run, the flip, the lowering, the plugs, plate 3. `blender -b -P animate-assembly.py` writes `assembly-animation.mp4` (72 s, 720p, untracked; the timeline is in seconds at the top of the script); `-- --preview` renders a quick quarter-size version |
| [`make-assembly.py`](make-assembly.py) | 8 kB | Rebuilds the assembly from the current STLs, fascia and plate 1, coloured through the `.mtl`. Run it after any fascia or plate 1 change |

## Building

```bash
openscad -D 'PART="lower"' -o fascia-lower.stl fascia.scad
openscad -D 'PART="upper"' -o fascia-upper.stl fascia.scad
python3 plate1.py
python3 make-assembly.py
```

Open `chassis-3deck-fascia.obj` in a viewer that reads OBJ materials (Blender, MeshLab, f3d) to see
the colours; the `.mtl` sits beside it. Plate 1's parts are the `P1_*` groups, one per component and
one per wire run, numbered as in the run table on the chassis layout drawing. Wire colours: red
unswitched +, orange switched +, black ground, teal the servo's 6 V.

`PART` also takes `both` / `exploded` / `blank` for previews, `fit` to see the panels
against the rear chassis, and **`clash`**, which intersects both panels with the plates and
standoffs. That one is the gate:

```bash
openscad -D 'PART="clash"' -o /tmp/clash.stl fascia.scad   # must be zero volume
```

Zero volume - a few hundred triangles of coincident face - is a pass; those are the pad faces
lying on the plates, which is the clamp. Real volume is an interference. It has caught a live
bug once already (MEC-07), so run it before every print.

`PART="portclash"` is the second gate. It checks rough stand-ins of the three upper-panel
connectors against the panel, the rear chassis and each other, and must also
render zero volume (MEC-13):

```bash
openscad -D 'PART="portclash"' -o /tmp/portclash.stl fascia.scad   # must be zero volume
```

## Print settings

PETG, 0.2 mm layers, ≥40 % infill, 4 walls, flat on the rear face, no supports.
Material choice and the reasoning behind it: **MEC-02**.

## Two panels, two heights

The gaps were measured on the built kit as **50 mm (lower)** and **40 mm (upper)** - the kit
ships two standoff lengths. So the panels are different parts and are **not** interchangeable
(**MEC-09**, which retires MEC-03). Mark each one on the inside face as it comes off the printer.

## What each decision owns

| | |
|---|---|
| **MEC-02** | The fascia exists at all, material, what each gap carries |
| **HW-18** | DE-9 as the CAN debug port, pinout |
| **MEC-03** | The split into two panels - its *interchangeable* half is retired by MEC-09 |
| **MEC-04** | Vents |
| **MEC-05** | The three debug ports and which board each reaches. Positions and apertures superseded by MEC-13 |
| **MEC-06** | DRIVE / LOGIC legends |
| **MEC-07** | The fixing: four pads per panel, six M3, captive nuts |
| **MEC-09** | The measured gaps, and the panels being different parts |
| **MEC-13** | The ports mounted from behind in pockets, in two horizontal rows; the USB-C grip limit; the upper panel's vents |
| **MEC-14** | The switch holes (⌀22.4) and what the switch drawing settles |

## Caveats worth knowing before you trust this geometry

- **Deck 3 is ours, not Hiwonder's.** The `.3dm` is the single-plate version; deck 3 in the
  `.obj` is a copy of deck 2, dropped to the measured 40 mm gap by `make-assembly.py`. Fixing
  the source CAD would make that patch unnecessary.
- **Some port geometry is read off photos** - the USB-C body width and flange depth, the Mini-B
  screw pitch and body. None of it is critical any more: the nearest body is 6 mm from a standoff,
  and the Mini-B's slotted hole takes any pitch from 27 to 30 (MEC-13).
- **The switch harness depth is unverified.** The bare switch is 25 mm deep and clears the motors by
  about 8 mm, but the plug-on socket harness adds to that (MEC-14). It affects the wiring, not the
  print.
