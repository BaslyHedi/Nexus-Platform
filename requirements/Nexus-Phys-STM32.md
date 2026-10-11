# Nexus-Phys-STM32 - STM32 node: real-time MCU

Physical, level 2. Requirements follow [../system/method.md](../system/method.md).

- **Purpose and boundary.** The STM32F4DISCOVERY (MB997B) on its perfboard carrier, with the CAN transceiver and the LEDs, and the software it runs from its flash: the FBL, the FBL-Updater and the app.
- **Interfaces.** [Nexus-Phys-CAN](Nexus-Phys-CAN.md); 5 V from [Nexus-Phys-PWR](Nexus-Phys-PWR.md); I2C and PWM prepared for [Nexus-Phys-DRV](Nexus-Phys-DRV.md); the on-board ST-LINK to an external PC.
- **Allocated functions.** The MCU side of 504, 503 F04, 401 F01 and the prepared side of 201 and 202.
- **Modes.** FBL idle; FBL receiving; FBL-Updater running; app running.

## Requirements

### Nexus-Phys-STM32-R001

**Statement.** The node shall reach the bus through an SN65HVD230 transceiver on CAN1, PD0 receive and PD1 transmit.

- Derived-from: Nexus-SubSys-401-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection The transceiver is wired to PD0 and PD1
- Realised-by: HW
- Decisions: HW-09

### Nexus-Phys-STM32-R002

**Statement.** The node shall publish a heartbeat at the rate set in the CAN matrix.

- Derived-from: Nexus-SubSys-401-R002
- Allocated-to: Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-App-R001

### Nexus-Phys-STM32-R003

**Statement.** The node shall show on an LED that it receives the FRDM's heartbeat.

- Derived-from: Nexus-SubSys-401-R002
- Allocated-to: Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-App-R002

### Nexus-Phys-STM32-R004

**Statement.** The node shall accept an image over the bus on request, program it into the application region and start it, with no debug probe.

- Derived-from: Nexus-SubSys-504-R001
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R001, Nexus-STM32-FBL-R002 and Nexus-STM32-App-R005

### Nexus-Phys-STM32-R005

**Statement.** The flash shall keep the FBL region apart from the application region, so that an image running from the application region can rewrite the FBL region.

- Derived-from: Nexus-SubSys-504-R004
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-FBL-Updater
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R003 and Nexus-STM32-FBL-Updater-R001

### Nexus-Phys-STM32-R006

**Statement.** The node shall verify an image's CRC before it starts it.

- Derived-from: Nexus-SubSys-504-R002
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R004

### Nexus-Phys-STM32-R007

**Statement.** The node shall remain reachable for a new download after an interrupted download, a failed verification or an absent image.

- Derived-from: Nexus-SubSys-504-R003
- Allocated-to: Nexus-STM32-FBL
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R005

### Nexus-Phys-STM32-R008

**Statement.** The on-board ST-LINK shall give SWD access, reachable from the fascia, and stays the recovery path for the first FBL.

- Derived-from: Nexus-SubSys-503-R002
- Allocated-to: -
- Phase: 1
- Verification: Inspection The ST-LINK is reached from the fascia USB port
- Realised-by: HW
- Decisions: MEC-05

### Nexus-Phys-STM32-R009

**Statement.** The four on-board LEDs shall show a pattern distinct for each state: FBL idle, FBL receiving, FBL-Updater running, app running.

- Derived-from: Nexus-SubSys-503-R004
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-FBL-Updater, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R006, Nexus-STM32-FBL-Updater-R002 and Nexus-STM32-App-R003

### Nexus-Phys-STM32-R010

**Statement.** The node shall bring out I2C on PB10 and PB11 to the motor module.

- Derived-from: Nexus-SubSys-201-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection PB10 and PB11 reach the motor module header
- Realised-by: HW
- Decisions: HW-10

### Nexus-Phys-STM32-R011

**Statement.** The node shall bring out the servo PWM on PE9 through a 1 kohm series resistor.

- Derived-from: Nexus-SubSys-202-R001
- Allocated-to: -
- Phase: 1
- Verification: Inspection PE9 reaches the servo header through R4
- Realised-by: HW
- Decisions: HW-19, HW-21

### Nexus-Phys-STM32-R012

**Statement.** The node shall report its software version in its node info.

- Derived-from: Nexus-SubSys-504-R001
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R007 and Nexus-STM32-App-R004

### Nexus-Phys-STM32-R013

**Statement.** The FBL-Updater shall be an image the FBL downloads and starts exactly like an application.

- Derived-from: Nexus-SubSys-504-R004
- Allocated-to: Nexus-STM32-FBL (as-is), Nexus-STM32-FBL-Updater
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-Updater-R003

### Nexus-Phys-STM32-R014

**Statement.** Every software item of the node shall have its own repository with CI building it from a clean clone.

- Derived-from: Nexus-SubSys-504-R006
- Allocated-to: Nexus-STM32-FBL, Nexus-STM32-FBL-Updater, Nexus-STM32-App
- Phase: 1
- Verification: Integration Nexus-STM32-FBL-R008, Nexus-STM32-FBL-Updater-R004 and Nexus-STM32-App-R006
