# Mechanical - the parts we make, the chassis model, and its renders

Everything we build and model mechanically: the rear fascia, the proposed carrier tray, the
plate-1 stand-ins and the whole-vehicle model. The **why** lives in the design decisions
([`../decisions/README.md`](../decisions/README.md)); this folder owns the geometry.

| Folder | Holds |
|---|---|
| [`cad/`](cad/) | Models and the files made from them: OpenSCAD sources, the print STLs, the drilling template, and (untracked) the whole-vehicle model and its parts |
| [`scripts/`](scripts/) | The Python and Blender scripts that build the model and animate it |
| `renders/` | Videos and stills. **Generated and untracked** - re-run the scripts |

The scripts find everything relative to themselves, so they run from any directory.

| File | Size | What it is |
|---|---|---|
| [`cad/fascia.scad`](cad/fascia.scad) | 18 kB | **Source of truth for both panels.** Every dimension, and why, in comments. Edit only here |
| [`cad/fascia-lower.stl`](cad/fascia-lower.stl) | 1.3 MB | Print file - lower panel, 124.2 × 18.9 × **52** mm, 19.6 cm³ (~25 g in PETG) |
| [`cad/fascia-upper.stl`](cad/fascia-upper.stl) | 2.2 MB | Print file - upper panel, 124.2 × 18.9 × **42** mm, 16.7 cm³ (~21 g in PETG) |
| [`cad/carrier-tray.scad`](cad/carrier-tray.scad) | 11 kB | ***Proposed* carrier tray** (MEC-17): one plate under boards A, B and C and the Bauer converter, in two steps - the boards placed on the tray in its own frame, then the tray placed on plate 2 by one `PLACE` offset. It copies the plate-2 holes under it and bolts down at six of them with nut pockets; the Bauer is screwed to it through its own two holes. `PART="tray"` → [`cad/carrier-tray.stl`](cad/carrier-tray.stl) to print; `PART="template"` → a 1:1 SVG with a 50 mm check bar (the hand-cut fallback); `PART="step1"` / `"step2"` → the two placement views in `renders/`. Output is mirrored once from the layout frame into the real world |
| [`cad/compute-tray.scad`](cad/compute-tray.scad) | 5 kB | ***Proposed* compute tray** (MEC-18): one plate on plate 3 under the FRDM (at its MEC-11 place) and the Raspberry Pi 5 ahead of it, turned so its ports face the nose. FRDM fixed by its own four screws from below; Pi on four bosses with captive nuts; the pad bolted down at four M3 holes. `PART="tray"` -> [`cad/compute-tray.stl`](cad/compute-tray.stl) to print; `PART="plan"` -> a ghosted preview |
| [`cad/carrier-tray-hand-template.pdf`](cad/carrier-tray-hand-template.pdf) | 61 kB | **Print-ready template for the hand-made tray** (MEC-17): A4 landscape, 1:1, print at 100 % and check the 100 mm bar. Written from `scripts/carrier-tray-hand.py`; regenerate it when the script changes |
| **Hiwonder** · *Ackermann Chassis (Single Layer)* `.3dm` | 186 MB | Hiwonder's own CAD, untouched. **Not in the repository** - it is theirs, not ours to redistribute, and it has to be fetched by hand on a fresh clone. Every chassis number in the project is measured from this, not from photos - see [`../bom/parts/2.1-Hiwonder-Ackermann-Chassis/SPECS.md`](../bom/parts/2.1-Hiwonder-Ackermann-Chassis/SPECS.md). It is the **single-plate** version |
| `cad/chassis-3deck-fascia.obj` | 65 MB | Whole-vehicle mock-up: Hiwonder's chassis + our deck 3 + the current panels. **Untracked, and a seed rather than output** - `make-assembly.py` reads it and rewrites it in place, so it cannot be rebuilt from this repository alone. It began as a Rhino export of the `.3dm`. Keep a local backup |
| `cad/assembly.stl` | 69 MB | The same assembly as one mesh, for renders. **Generated and untracked** - delete it and re-run |
| `cad/plate1/*.stl`, `cad/plate1/states/`, `cad/chassis-3deck-fascia.mtl` | 1 MB | **Generated and untracked** - the plate 1 parts; the two wires that cross between the decks in the `raised` and `open` positions (plate 2 lowering, 60 mm up, or hinged over like a book); and the colours. Re-run the two scripts |
| [`scripts/plate1.py`](scripts/plate1.py) | 20 kB | **Plate 1 stand-ins for an eye review** (MEC-16): every component and every wire run as its own STL in `cad/plate1/`, at the assumed sizes, plus the four tires the CAD leaves off (about 68 x 30, estimated from a photo). Not for building from |
| [`scripts/make-assembly.py`](scripts/make-assembly.py) | 8 kB | Rebuilds the assembly in `cad/` from the current STLs, fascia and plate 1, coloured through the `.mtl`. Run it after any fascia or plate 1 change |
| [`scripts/animate-assembly.py`](scripts/animate-assembly.py) | 10 kB | **Assembly animation** of the harness-board sandwich, in MEC-16's build order: parts onto the upturned plate 2, wires run by run, the flip, the lowering, the plugs, plate 3. `blender -b -P scripts/animate-assembly.py` writes `renders/assembly-animation.mp4` (36 s at double speed, 720p; the timeline is in seconds at the top of the script); `-- --preview` renders a quick quarter-size version |
| [`scripts/animate-tray.py`](scripts/animate-tray.py) | 30 kB | **Tray assembly animation** (MEC-17): the carrier built on the tray at the bench, then the tray set on plate 2, screwed from below, and plate 2 lowered onto its standoffs; the Discovery plugs on last. Plate 2 is the survey's own outline and holes, the tray is `cad/carrier-tray.stl`, the boards are the as-built carrier through `carrier_model.py`, the Bauer is from the seller's drawing; the harness parts and the Discovery are stand-ins. `blender -b -P scripts/animate-tray.py` writes `renders/tray-assembly.mp4` (50 s); `-- --preview` renders a quick half-size version; `-- --still 30` writes one PNG |
| [`scripts/carrier_model.py`](scripts/carrier_model.py) | 18 kB | The finished carrier (boards A, B, C and the Discovery mock) as Blender objects, read from `hardware/scripts/stm32-carrier.py`. Used by `animate-tray.py`; `animate-carrier.py` still builds the same geometry step by step |
| [`scripts/carrier-tray-hand.py`](scripts/carrier-tray-hand.py) | 7 kB | **The hand-made tray's template** (MEC-17): a 1:1 A4 SVG (print at 100 %) with the all-right-angle cut line, true-size holes, the boards and the Bauer in outline, and the hole table, for a 4 mm sheet. Checks that no hole is too near an edge or another hole. `python3 scripts/carrier-tray-hand.py` -> `renders/carrier-tray-hand-template.svg` |
| [`scripts/animate-carrier.py`](scripts/animate-carrier.py) | 33 kB | **Carrier assembly animation** (MEC-15, HW-19), in the drawing's build order: sockets with the Discovery as the jig, the parts, the solder side run by run, the bridge, the module and standoffs, then board C. Built entirely from [`../hardware/scripts/stm32-carrier.py`](../hardware/scripts/stm32-carrier.py), so it cannot drift from the drawing. The Discovery is a **mock**: outline and headers from UM1472, everything on it placed by eye. `blender -b -P scripts/animate-carrier.py` writes `renders/carrier-animation.mp4` (47 s at double speed, 720p); `-- --preview` renders a quick half-size version, `-- --still 40` one frame at 40 s |

## Building

```bash
cd cad
openscad -D 'PART="lower"' -o fascia-lower.stl fascia.scad
openscad -D 'PART="upper"' -o fascia-upper.stl fascia.scad
openscad -D 'PART="tray"'     -o carrier-tray.stl          carrier-tray.scad
openscad -D 'PART="tray"'     -o compute-tray.stl          compute-tray.scad
openscad -D 'PART="step1"' --camera=0,0,0,0,0,0,300 --projection=o --autocenter --viewall -o ../renders/tray-step1.png carrier-tray.scad   # and step2
cd ..
python3 scripts/plate1.py
python3 scripts/make-assembly.py
blender -b -P scripts/animate-assembly.py
blender -b -P scripts/animate-carrier.py
```

Open `chassis-3deck-fascia.obj` in a viewer that reads OBJ materials (Blender, MeshLab, f3d) to see
the colours; the `.mtl` sits beside it. Plate 1's parts are the `P1_*` groups, one per component and
one per wire run, numbered as in the run table on the chassis layout drawing. Wire colours: red
unswitched +, orange switched +, black ground, teal the servo's 6 V.

`PART` also takes `both` / `exploded` / `blank` for previews, `fit` to see the panels
against the rear chassis, and **`clash`**, which intersects both panels with the plates and
standoffs. That one is the gate:

```bash
openscad -D 'PART="clash"' -o /tmp/clash.stl cad/fascia.scad   # must be zero volume
```

Zero volume - a few hundred triangles of coincident face - is a pass; those are the pad faces
lying on the plates, which is the clamp. Real volume is an interference. It has caught a live
bug once already (MEC-07), so run it before every print.

`PART="portclash"` is the second gate. It checks rough stand-ins of the three upper-panel
connectors against the panel, the rear chassis and each other, and must also
render zero volume (MEC-13):

```bash
openscad -D 'PART="portclash"' -o /tmp/portclash.stl cad/fascia.scad   # must be zero volume
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
| **MEC-18** | *Proposed:* the compute tray on plate 3 - FRDM and Raspberry Pi 5 |

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
