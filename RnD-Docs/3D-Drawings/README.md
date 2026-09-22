# 3D drawings - rear fascia and the chassis it mounts to

Everything the rear fascia is built from. The **why** lives in the design decisions
([`../../Architecture/Design-Decisions/README.md`](../../Architecture/Design-Decisions/README.md));
this folder owns the geometry, and the table below says which file is which.

| File | Size | What it is |
|---|---|---|
| [`fascia.scad`](fascia.scad) | 18 kB | **Source of truth for both panels.** Every dimension, and why, in comments. Edit only here |
| [`fascia-lower.stl`](fascia-lower.stl) | 1.3 MB | Print file - lower panel, 124.2 × 18.9 × **52** mm, 20.5 cm³ (~26 g in PETG) |
| [`fascia-upper.stl`](fascia-upper.stl) | 1.9 MB | Print file - upper panel, 124.2 × 18.9 × **42** mm, 17.5 cm³ (~22 g in PETG) |
| `Ackermann Chassis (Single Layer).3dm` | 186 MB | **Hiwonder's own CAD**, untouched. Every chassis number in the project is measured from this, not from photos - see [`../Datasheets/2.1-Hiwonder-Ackermann-Chassis/SPECS.md`](../Datasheets/2.1-Hiwonder-Ackermann-Chassis/SPECS.md). It is the **single-plate** version |
| `chassis-3deck-fascia.obj` | 65 MB | Whole-vehicle mock-up: Hiwonder's chassis + our deck 3 + the current panels. **Generated** |
| `assembly.stl` | 69 MB | The same assembly as one mesh, for renders. **Generated** |
| [`make-assembly.py`](make-assembly.py) | 5 kB | Rebuilds both of the above from the current STLs. Run it after any fascia change |

## Building

```bash
openscad -D 'PART="lower"' -o fascia-lower.stl fascia.scad
openscad -D 'PART="upper"' -o fascia-upper.stl fascia.scad
python3 make-assembly.py
```

`PART` also takes `both` / `exploded` / `blank` for previews, `fit` to see the panels
against the rear chassis, and **`clash`**, which intersects both panels with the plates and
standoffs. That one is the gate:

```bash
openscad -D 'PART="clash"' -o /tmp/clash.stl fascia.scad   # must be zero volume
```

Zero volume - a few hundred triangles of coincident face - is a pass; those are the pad faces
lying on the plates, which is the clamp. Real volume is an interference. It has caught a live
bug once already (MEC-07), so run it before every print.

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
| **MEC-05** | The three debug ports, aperture sizes, the Mini-B screw slot |
| **MEC-06** | DRIVE / LOGIC legends |
| **MEC-07** | The fixing: four pads per panel, six M3, captive nuts |
| **MEC-09** | The measured gaps, and the panels being different parts |

## Caveats worth knowing before you trust this geometry

- **Deck 3 is ours, not Hiwonder's.** The `.3dm` is the single-plate version; deck 3 in the
  `.obj` is a copy of deck 2, dropped to the measured 40 mm gap by `make-assembly.py`. Fixing
  the source CAD would make that patch unnecessary.
- **Two apertures are still nominal** - the USB-C and Mini-B moulded bosses. Try the parts,
  file if tight (MEC-05).
- **Switch depth with terminals fitted is unverified** and it is tight against the motors,
  about 8 mm (MEC-02, MEC-07).
