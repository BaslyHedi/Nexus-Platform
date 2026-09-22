# 2.3 - LD-1501MG steering servo · and the drive motors

Captured from the ThinkRobotics listing for the Hiwonder Ackerman metal chassis
(`ThinkRobotics-Chassis-Motor-Servo-Specs.pdf` in this folder).

## LD-1501MG steering servo

| Parameter | Value |
|---|---|
| **Working voltage** | **6–8.4 V** - *not* a 5 V part |
| Stall torque | 13 kg·cm @ 6 V · 15 @ 6.5 V · **17 @ 7.4 V** |
| Speed | 0.16 s/60° @ 7.4 V |
| Rotation | 0–180°, 0.3° precision |
| Control | PWM, 500–2500 µs |
| Weight | 61 g |

**Design consequence:** this servo can never sit on a 5 V logic rail. It is fed either by
the Hiwonder driver's own BEC or by a dedicated 6–7.4 V supply. This is what makes the
two 5 V rails purely logic rails.

## Encoder gear motors (×4)

| Parameter | Value |
|---|---|
| Rated voltage | 12 V |
| Rated power | ~8.3 W each (≈2.8 A total across four, rated) |
| Gear ratio | 1:90 (the Hiwonder docs describe a 1:30 "520" motor - **variant-dependent, confirm on arrival**) |
| Speed | 110 rpm no-load · 85 rpm rated |
| Stall torque | 15 kg·cm |
| Shaft | 6 mm D-shaft |
| Encoder | AB dual-phase, 11 magnetic poles |
| Connector | PH2.0-6PIN |
