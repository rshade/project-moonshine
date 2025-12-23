# GEMINI.md - Project Context & Engineering Memory
**DO NOT DELETE.** This file contains the engineering history, physics constraints, and design logic for Project Moonshine. AI Agents should read this first to understand the current state of the project.

## 🧠 Core Concept: The Self-Cooling Rankine Cycle
The goal is to eliminate water consumption in AI data centers by using a **Closed-Loop Organic Rankine Cycle (ORC)**.
* **Traditional Cooling:** Evaporative (consumes water) or Air (energy expensive).
* **Moonshine Cooling:** Phase-change cooling where the vapor pressure performs mechanical work (spinning the cooling fan) before condensing.
* **Fluid:** 60/40 Ethanol/Water azeotrope.
* **Boiling Point:** ~80°C-82°C.
* **Goal:** Zero Water Consumption + Parasitic Load Removal.

## 📐 The Geometry: "Axial Condensing Tunnel"
We rejected the "box and radiator" design in favor of a linear, jet-engine style layout to fit in server racks.
* **The Shaft:** A single central drive shaft runs the length of the unit.
* **The Stack:** [Turbine] --- [Generator] --- [Gearbox] --- [Fan].
* **The Condenser:** A cylinder of copper fins ("The Tube") surrounding the shaft.
* **The Airflow:** The fan pulls air *through* the center of the fin-tube (Venturi effect).
* **Thermal Isolation:** The hot condenser tube is held by "Spider Mounts" made of G10 Garolite or Zirconia to prevent heat soaking into the chassis.

## ⚗️ The Physics: 60/40 Azeotrope
* **Fluid:** 60% Ethanol / 40% Water.
* **Why?** Pure water boils too hot (100°C) for chips. Pure alcohol boils too cool (78°C) and is a fire hazard.
* **The Sweet Spot:** The mix boils at ~80°C-82°C.
    * **Safety:** Higher flash point than pure ethanol.
    * **Thermodynamics:** High latent heat capacity from the water content; low boiling point from the alcohol.
* **"The Bourbon Glaze" Risk:** If using non-pure sources (like actual bourbon), sugar/tannins will foul the cold plates. Requires a "Wash Cycle" maintenance protocol.

## ⚙️ Mechanical Constraints
* **Turbine Type:** Tesla Turbine (Bladeless). Preferred for its ability to handle "wet vapor" (mixed phase) without damage.
* **Generator:** Permanent Magnet Micro-Generator.
* **Gearing:**
    * **Speed Increaser:** Turbine (Low Torque/High RPM) -> Fan (High Speed/Air Volume).
    * **Variable Gearing:** Users change gears based on climate (e.g., larger fan gear for Texas heat, smaller for Alaska).

## 🛡️ Safety & "The Happy Hour Protocol"
* **Leak Detection:** Standard hydrocarbon sensors.
* **Failure Mode:** If the loop ruptures, the fluid evaporates quickly. It is flammable but not toxic.
* **"Happy Hour":** A tongue-in-cheek reference to the fact that the working fluid is technically food-grade (distilled spirits), making clean-up less hazardous than glycol or refrigerant leaks.

## 📝 Design History Log
* **Iteration 1:** Steam turbine. (Rejected: Temps too high).
* **Iteration 2:** Pure Alcohol ORC. (Refined: Safety concerns).
* **Iteration 3:** "The Still" - condenser added.
* **Iteration 4:** "Axial Tunnel" - Shaft runs through the condenser for compact form factor.
* **Branding:** Adopted "Moonshiner" terminology (Wash, Worm, Thumper) to make open-source hardware approachable.