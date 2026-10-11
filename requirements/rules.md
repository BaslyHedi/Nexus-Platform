# Requirement rules

What a good requirement is in NEXUS, at every level. This file owns the **content** rules. The method, levels and relations
are in [`../system/method.md`](../system/method.md); the block format and its fields are in [README.md](README.md).

**The rules are the state of the art, adopted whole.** Section 1 takes three references as they are. Sections 2 to 5 are
NEXUS's own application of them to each level, and every rule there cites the reference it applies. NEXUS claims
conformance with none of the references; it uses their content as its rule set.

| Reference | What it gives | Source used here |
|---|---|---|
| **INCOSE Guide to Writing Requirements**, version 4, INCOSE-TP-2010-006-04 (2023), "GtWR" | 15 quality characteristics, **C1 to C15**: nine for a single statement, six for a set. 42 rules, **R1 to R42**, in 14 categories | The INCOSE v4 summary sheet and overview, and a public digest of the 42 rules; the full guide is sold by INCOSE |
| **ISO/IEC/IEEE 29148:2018**, *Systems and software engineering: Life cycle processes: Requirements engineering* | The same characteristics, and a statement built from **condition, subject, action, object, constraint of action** | Public summaries; the standard is paywalled |
| **EARS**, the Easy Approach to Requirements Syntax (A. Mavin et al., Rolls-Royce, RE'09, 2009) | Five sentence patterns with fixed keywords and a fixed clause order | The published description of the patterns |

## 1. Every requirement

### Quality characteristics (GtWR C1 to C15, ISO 29148)

| | Characteristic | In NEXUS |
|---|---|---|
| C1 | **Necessary** | It traces up: to a parent requirement, or at the system level to a phase-plan item (`Need`). Without it the parent or the need has a gap |
| C2 | **Appropriate** | Its intent and detail match the level of the entity it is about. Sections 2 to 5 say what that means per level |
| C3 | **Unambiguous** | It has one reading for every reader |
| C4 | **Complete** | It stands on its own, without its heading or its neighbours |
| C5 | **Singular** | One capability, characteristic, constraint or quality |
| C6 | **Feasible** | It can be met with the hardware and the decisions of its phase |
| C7 | **Verifiable** | It can be shown to be met: `Verification` names the method and the pass criterion |
| C8 | **Correct** | It is a faithful statement of its source: the parent, the phase plan, the decision it cites |
| C9 | **Conforming** | It follows a pattern below and the block format of [README.md](README.md) |
| C10 | **Complete** (set) | Every goal, deliverable and test of the phase is covered at the system level; every derived allocation has its children |
| C11 | **Consistent** (set) | No conflict, no overlap, the same terms and units throughout |
| C12 | **Feasible** (set) | The phase can meet all of them together |
| C13 | **Comprehensible** (set) | What is required at a level is clear without reading the levels below |
| C14 | **Able to be validated** (set) | Meeting the set achieves the phase goal |
| C15 | **Correct** (set) | The set represents the needs and the parent requirements it comes from |

### Sentence patterns (EARS; GtWR R1; ISO 29148)

Every statement follows one of the EARS patterns. The clauses always come in this order: precondition (`While`), trigger
(`When` or `If`), subject, `shall`, response. This is ISO 29148's *condition, subject, action, object, constraint of action*
with fixed keywords.

| Pattern | Template | NEXUS example |
|---|---|---|
| **Ubiquitous**, always active | The *subject* shall *response*. | The bus shall be classic CAN at 500 kbit/s. |
| **Event-driven** | When *trigger*, the *subject* shall *response*. | When a software-update request arrives, the bootloader shall pull the image by Cyphal file transfer. |
| **State-driven** | While *precondition*, the *subject* shall *response*. | While the bootloader receives an image, the node shall show the receiving pattern on its LEDs. |
| **Unwanted behaviour** | If *trigger*, then the *subject* shall *response*. | If a download is interrupted, then the bootloader shall remain reachable for a new download. |
| **Optional feature** | Where *feature is included*, the *subject* shall *response*. | Where the Pi 5 is fitted, the vehicle shall … (Phase 4) |
| **Complex** | While *precondition*, when *trigger*, the *subject* shall *response*. | While the drive switch is on, when no command has been received, the rear drive shall hold the wheels still. |

### The 42 rules (GtWR R1 to R42)

All 42 apply. Where NEXUS sharpens one, the note says how.

| Category | Rules | NEXUS note |
|---|---|---|
| **Accuracy** | R1 structured statements; R2 active voice; R3 subject and verb appropriate to the entity; R4 defined terms; R5 "the", not "a"; R6 common units; R7 no vague terms; R8 no escape clauses; R9 no open-ended clauses | R1: the EARS patterns above. R4: product terms are defined in [glossary.md](glossary.md), systems engineering terms in the method. R6: SI units. R7: none of *some, adequate, sufficient, reasonable, fast, robust, user-friendly*. R8: none of *where possible, as appropriate, if necessary*. R9: no *including but not limited to*, no *etc.* |
| **Concision** | R10 no superfluous infinitives; R11 a separate clause for each condition | R10: no *be able to*, *be capable of* |
| **Non-ambiguity** | R12 grammar; R13 spelling; R14 punctuation; R15 defined logical expressions; R16 avoid "not"; R17 no oblique "/" | R14: no em-dashes, as everywhere in the project. R16: *shall not* is allowed for a prohibition |
| **Singularity** | R18 one thought per sentence; R19 no combinators (*and, or, then, unless*) joining clauses; R20 no purpose phrases; R21 no parentheses with subordinate text; R22 enumerate sets instead of group nouns; R23 refer to diagrams, models or ICDs for complex behaviour | R20: the reason goes in a decision, cited in `Decisions`. R22: a list is allowed when it defines one property, such as the four states one LED pattern must tell apart. R23: cite the drawing, the BOM item or the CAN matrix |
| **Completeness** | R24 no pronouns; R25 no reliance on headings | |
| **Realism** | R26 no unachievable absolutes (*100 %*, *always*) | |
| **Conditions** | R27 explicit conditions; R28 explicit logic for multiple conditions | Through the EARS keywords |
| **Uniqueness** | R29 classify by aspect; R30 express each requirement once | R30: a value is stated once, by the element that owns it, and cited elsewhere |
| **Abstraction** | R31 solution-free unless there is a reason to constrain the design | The reason is a decision, cited in `Decisions`. Sections 2 to 5 say where technology may enter |
| **Quantifiers** | R32 *each*, not *all*, *any* or *both* | |
| **Tolerance** | R33 values with a range | Where a value matters to verification |
| **Quantification** | R34 measurable performance; R35 explicit temporal dependencies | R34: a value defined elsewhere is cited by its controlled source ("the rate set in the CAN matrix", a tagged release). No *TBD* |
| **Uniformity of language** | R36 consistent terms and units; R37 consistent acronyms; R38 abbreviations defined; R39 a project style guide; R40 consistent decimal format | R39: this file is the style guide |
| **Modularity** | R41 group related requirements; R42 a defined structure for sets | R42: one file per system-of-interest, element or item, in the format of [README.md](README.md) |

## 2. The vehicle: system requirements

1. **The subject is the vehicle** (R2, R3): "The vehicle shall …".
2. **Black box** (C2, R31). The statement names only the vehicle, its **actors** (operator, charger, environment, a PC at
   the diagnostic port, and later the remote station) and its **external interfaces** (the power switches, the charge
   input, the diagnostic CAN port, the debug ports). It never names an element, an internal bus, a board or a software element.
3. **Observable from outside** (C7). It can be verified on the closed vehicle, through its external interfaces.
4. **External interface properties are vehicle level** (C2). The connector and bit rate of the diagnostic port are what a
   PC must match, so they may be stated here. Internal values may not.
5. **A limit only where the stakeholder needs one** (C2, R34). "Stops within 0.5 m" belongs here. A test's own pass
   criteria, such as a duration, an error count or a number of cycles, stay in the test in [phases.md](../system/phases.md).
6. **Solution-free** (R31), except for what the platform decided as a stakeholder choice: the decisions in the project's
   `CLAUDE.md`, such as Ackermann steering and the 3S battery.
7. **Traced to its need** (C1, C15): `Need` names the phase-plan item, a goal, deliverable or test.
8. **Traced to its functions**: `Function` names the logical functions it concerns.
9. **Verified by system verification**: a phase test, or a demonstration or inspection of the whole vehicle.

## 3. The enabling system, beside the vehicle

1. **The subject is the enabling item** (R3): "Each repository", "The Linux image build", "The USB-CAN adapter".
2. **Not derived from the vehicle** (C1): `Need` names the phase-plan item, typically a deliverable.
3. **No vehicle behaviour** (C2): what the vehicle does belongs in the vehicle file, even when a tool performs the test.
4. **Realised mostly by `SYS`**: a procedure or convention, verified by inspecting the CI runs, tags and builds.

## 4. Subsystems

1. **The subject is the element** (R3): "The node", "The bus", "The element", or a named part of it ("SW1").
2. **Only what adds to the parent** (C1, R30): a split, an interface, a value, a physical property, or a constraint from a
   decision. A requirement that would repeat its parent is not written; the parent is allocated **as-is**.
3. **Technology enters here** (C2, R31): parts, pins, values and protocols, each with the decision that fixed it.
4. **One requirement, one element** (C5): a requirement two elements share is split into one for each, plus an interface
   requirement on what connects them.
5. **An interface value is stated once** (R30), by the element that owns the interface (the bus for CAN, the power element
   for a supply), and the elements on either side cite it.
6. **Cite, do not copy** (R23, R30): wiring and placement owned by a drawing, the BOM or a decision are cited, never restated.
7. **The function traced is allocated to the element** in [physical-architecture.md](../system/physical-architecture.md). A
   derived requirement may bring in a supporting function its parent does not name; the table then lists it.
8. **Hardware ends here**: a requirement realised in hardware is a leaf with `Realised-by: HW`.

## 5. Components

1. **The subject is the element** (R3): "The Discovery board", "The carrier", "The bootloader", "The Linux image".
2. **Elements, never repositories** (C2): a statement names the element, not the repository or the build target that
   implements it. Which repository implements which software element is the configuration table of the enabling system.
3. **A bought hardware element** states what the node relies on from the part: a pin left free, a supply it accepts, a
   feature it has. It is verified by **analysis** against the vendor documentation, or by a test. Its internals are not decomposed.
4. **A hardware element designed here** (the carrier boards) states what its drawing must satisfy, and is verified by
   **inspection** against the drawing, or by a measurement.
5. **A software element** states behaviour at its boundary, as the node sees it: on the bus, on the LEDs, in the memory
   regions, at the console. No internal design (modules, algorithms, libraries) unless a decision has fixed it, such as Cyphal (SW-01).
6. **Hand-over**: nothing below a software element is written here. Its team derives the software requirements from these
   and cites their IDs.
7. **No repository obligations** (C2): CI, tags and builds belong to the enabling system.

**Checked by the tool.** `tools/check-requirements.py` enforces the EARS clause forms, one "shall" per statement, and R7, R8,
R9, R10, R16, R17, R21, R24 and R32. The other rules need a reader.

## Before committing a requirement

- Which EARS pattern is it, and is its subject the entity of its file (R1, R3)?
- Does its detail fit its level (C2, sections 2 to 5)?
- Does it trace up (`Need` or `Derived-from`) and across (`Function`) (C1)?
- One thought, no combinator, no parentheses, no vague term or escape clause (R7, R8, R18, R19, R21)?
- Does it say something its parent did not, or should the parent be allocated as-is (R30)?
- Is there a verification with a pass criterion (C7)?
