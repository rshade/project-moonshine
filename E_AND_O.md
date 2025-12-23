# E_AND_O.md - Errors and Omissions (Design Flaws)

This document tracks identified mechanical and thermodynamic flaws in the Project Moonshine design. Each item must be addressed or mitigated to reach a production-ready state.

## 1. The "Azeotrope" Fallacy (Chemical Instability) - [UNDER EVALUATION]
* **The Flaw:** The documentation claims a 60/40 ethanol/water mix is an azeotrope. It is actually a zeotropic mixture.
* **The Consequence:** During boiling, ethanol vaporizes preferentially. The remaining liquid becomes water-rich, raising the boiling point.

### Option A: Forced Circulation (Mechanical Pump) - [STATUS: BASELINE PASS]
* **Description:** Use a small DC pump to keep the fluid mixed and moving.
* **Pros:** Reliable, simple to control, prevents localized "hot spots" and fractionation.
* **Cons:** Introduces a parasitic electrical load (~10W); adds a mechanical failure point.
* **Evaluation Tests:
    1. `NET_ENERGY_SURPLUS`: **PASS** (~40.5W surplus @ 350W TDP).
    2. `THERMAL_STABILITY`: **PASS** (Pumped mixing prevents glide issues).
    3. `STARTUP_RELIABILITY`: **TBD** (Requires hardware testing of priming).

### Option B: Pumpless Ejector Cycle (Vapor-Jet) - [STATUS: PENDING SIMULATION]
* **Description:** Use a Venturi-style ejector nozzle powered by a small "bleed" of high-pressure vapor to pull liquid through the loop.
* **Pros:** No moving parts, zero electrical parasitic load.
* **Cons:** Complexity of geometry; risk of clogging.
* **Evaluation Tests:
    1. `EJECTOR_MOTIVE_PRESSURE`: **TODO** (Calculate if 350W TDP provides enough delta-P).
    2. `THERMAL_STABILITY`: **TODO**.
    3. `STARTUP_RELIABILITY`: **TODO**.

### Option C: Passive Thermosyphon (Gravity-Fed) - [STATUS: FAIL (PHYSICS LIMIT)]
* **Description:** Rely on density differences and gravity (requires vertical orientation).
* **Pros:** Simplest possible design.
* **Cons:** Height constraints; low static pressure.
* **Evaluation Tests:
    1. `GRAVITY_HEAD_PRESSURE`: **FAIL** (Generated 0.034 bar; requires > 0.1 bar for Tesla Turbine).
    2. `THERMAL_STABILITY`: **FAIL** (Likely to stall without forced circulation).
    3. `STARTUP_RELIABILITY`: **FAIL** (Static friction overcomes gravity head).


## 2. Thermal Expansion & Tesla Turbine Clearances
* **The Flaw:** The "Axial Condensing Tunnel" uses a single central shaft connecting a hot turbine (~82°C) to a cool fan.
* **The Consequence:** Tesla turbines require extremely tight disc spacing (0.1mm - 0.5mm). Differential thermal expansion between the hot turbine end and cold fan end will cause the shaft to grow unevenly, leading to disc-rub or housing interference.
* **Proposed Mitigations:**
    1. **Ceramic Bearings:** Use Si3N4 (Silicon Nitride) bearings to handle high RPMs with minimal friction and zero thermal expansion issues.
    2. **Thermal Break Shaft:** Replace the solid metal shaft with a high-strength, low-thermal-conductivity composite or use a decoupled "Split-Shaft" design.
    3. **Ceramic Gearing:** Use ceramic gears in the speed increaser/transmission to prevent heat-related gear lash changes.

## 3. The Sealing Nightmare (Dynamic Leakage)
* **The Flaw:** High-speed rotating shaft carrying volatile, flammable fluid.
* **The Consequence:** Standard lip seals fail at the RPMs required for Tesla turbines. Micro-leaks lead to loss of vacuum/pressure and the venting of flammable ethanol vapor into the server rack.

## 4. Starting Torque vs. Thermal Inertia
* **The Flaw:** Tesla turbines have very low starting torque and require high-velocity vapor to overcome static friction.
* **The Consequence:** On server startup, fluid may boil and build pressure (the "thumper" effect) before the turbine has enough torque to start the cooling fan, leading to a potential pressure spike or thermal runaway.

## 5. Parasitic Heat Soak (The Shaft Bridge)
* **The Flaw:** The central drive shaft acts as a massive thermal bridge.
* **The Consequence:** Heat conducts directly from the 80°C turbine into the generator and fan bearings. Most COTS bearings and magnets are not rated for these temperatures, leading to premature failure.
* **Proposed Mitigations:**
    1. **Ceramic Transmission:** Introduce a gearbox/transmission that acts as a thermal isolator.
    2. **Zirconia (ZrO2) Isolators:** Use zirconia spacers between the turbine assembly and the rest of the stack to block conductive paths.

