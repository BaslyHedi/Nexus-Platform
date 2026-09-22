# 3.4a - Bauer Electronics DC-DC 12 V → 5 V, 10 A / 50 W (Wire)

No manufacturer datasheet is published for this part; the listing is the only source.
Captured 2026-09-12 from Amazon.de, €19.99.

| Parameter | Value |
|---|---|
| Input | 8–36 V DC |
| Output | 5 V, 10 A, 50 W |
| Connection | tinned flying leads (the "Wire" variant - **not** the Type-C or USB variants) |
| Protection | over-voltage, **reverse polarity**, short circuit, overload, over-temperature |
| Construction | epoxy potted, IP68, finned aluminium body |
| Fuse | none built in - external branch fuse required |

**Role:** compute rail, feeds the FRDM-IMX91S. 10 A chosen over 5 A so a Raspberry Pi 5
(~2.7 A at the input) can join this rail later without a second purchase.

**To measure on arrival:** actual body dimensions (listing gives none), and output ripple
under a real load step.
