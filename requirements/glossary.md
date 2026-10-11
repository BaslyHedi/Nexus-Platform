# Glossary

The terms the requirements use, defined once (GtWR R4, R36). Systems engineering terms (system-of-interest, system
element, enabling system, allocation) are defined in [`../system/method.md`](../system/method.md) and not repeated here.
A term in a requirement means exactly what this file says.

## Vehicle level: the black-box terms

| Term | Meaning |
|---|---|
| **Component** | Any part fitted to the vehicle |
| **Computing**, **computing power** | Whatever in the vehicle runs software, and the supply that powers it. At element level: the STM32 node and the FRDM node on the logic branch |
| **Control software** | The software of the vehicle's real-time control. At element level: the application on the STM32 node |
| **Debug probe** | A tool that programs or halts a processor through its debug interface, such as an ST-LINK |
| **Diagnostic port** | The vehicle's external CAN connection, a male DE-9 on the rear fascia (HW-18) |
| **Drive**, **drive power** | What moves the vehicle (the rear-wheel drive and the steering), and the supply that powers it. At element level: the drive branch |
| **Drive command** | A request to move the rear wheels or the steering. Phase 1 sends none |
| **External tool** | Software on a PC connected to the diagnostic port, part of the enabling system |
| **Internal communication** | The messages exchanged between parts of the vehicle. At element level: the traffic on the CAN bus |
| **On-board software** | All software the vehicle runs |
| **On-board storage** | Storage inside the vehicle that holds software: the flash of the STM32 node and the SD card of the FRDM node |
| **Operator** | The person who uses the vehicle at its rear fascia; later also through the remote station |
| **Power switches** | SW1 (DRIVE) and SW2 (LOGIC) on the rear fascia (HW-08, MEC-06) |
| **Program** | One piece of on-board software that runs on its own: the bootloader, the FBL-Updater, the application, each program on the FRDM node |
| **Service ports** | The ports for maintenance and debugging: the diagnostic port, the ST-LINK USB port, the FRDM console port |
| **Software is alive** | The on-board software publishes its heartbeats on the diagnostic port |
| **Software update**, **update** | Replacing the control software through the update mechanism |
| **State of the software update** | One of: update idle, update receiving, update mechanism being replaced, application running |
| **Update mechanism** | The software that installs control software. At element level: the bootloader of the STM32 node |

## Element level

| Term | Meaning |
|---|---|
| **Application region** | The part of the STM32 flash that holds the application, fixed by the memory map of the STM32 node |
| **Bootloader**, **FBL** | The flash bootloader of the STM32 node, software element `Nexus-Physical-01-04` |
| **Bootloader region** | The part of the STM32 flash that holds the bootloader, fixed by the same memory map |
| **CAN matrix** | The definition of the bus: bit rate, node IDs, Cyphal subjects and services, and rates. Released by tag in `Nexus-CAN-Utils` |
| **Configuration table** | The table in `Nexus-Enabling.md` that names the repository and build target implementing each software element |
| **Drive branch** | The circuit SW1 switches: the motor driver and the steering UBEC (HW-08, HW-14) |
| **FBL-Updater** | Software element `Nexus-Physical-01-05`: an image whose only job is to rewrite the bootloader region. Built from the same repository as the bootloader |
| **Heartbeat** | The periodic Cyphal message by which a node announces that it runs (SW-01) |
| **Image** | A program in the binary form that is written to flash or to the SD card |
| **Logic branch** | The circuit SW2 switches: the 5 V converter, which feeds both nodes (HW-08, HW-17) |
| **Memory map** | The division of the STM32 flash into the bootloader region and the application region, a design artefact of the STM32 node, fixed by SW-04 |
| **Node** | A computer on the CAN bus: the STM32 node (`Nexus-Physical-01`) or the FRDM node (`Nexus-Physical-02`). A PC on the diagnostic port is a further node |
| **Node info** | The Cyphal service through which a node reports its name and version (SW-01) |
| **Pack voltage** | The voltage of the 3S battery, 11.1 V nominal |
| **Software element** | A system element made of software, handed over to the team that implements it |
