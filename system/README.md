# System Definition

What NEXUS must **do**, decomposed top-down. This is the logical view - it names functions and
the sub-systems that own them, not the boards that run them. Hardware allocation comes later
and lives in [`../hardware/`](../hardware/README.md), with the reasoning in
[`../decisions/`](../decisions/README.md).

Each drawing exists as an `.svg` (editable source) and a `.pdf` (for reading and printing) -
regenerate the PDF from the SVG after any edit.

| Drawing | Owns |
|---|---|
| [Nexus-Platform-System-Layout](Nexus-Platform-System-Layout.svg) | The sub-system decomposition - every `Nexus-SubSys-DNN` ID, its name, phase and key flows |

The layout owns the list of sub-systems. Do not restate it here; link to it.

## IDs

| Level | Format | Example |
|---|---|---|
| Sub-system | `Nexus-SubSys-DNN` - D = functional domain (1–5), NN = sub-system in it | `Nexus-SubSys-203` |
| Function | `Nexus-SubSys-DNN-Fnn` | `Nexus-SubSys-203-F02` |

IDs are never reused. A retired sub-system keeps its number.

## Workflow

1. **System layout** - settle the decomposition. *← current step, Draft A*
2. **One drawing per sub-system** - `Nexus-SubSys-DNN-<Name>.svg` / `.pdf`, showing the
   functions it realises and its interfaces to other sub-systems.
3. **Requirements per function**, traced to the `-Fnn` IDs.
