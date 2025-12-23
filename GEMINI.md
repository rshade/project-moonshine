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
    * **Safety:** Higher flash point than pure ethanol. **Constraint:** We strictly use a ~60/40 mix to minimize flammability and prevent explosive vapor risks; 95%+ concentrations are rejected for safety.
    * **Thermodynamics:** High latent heat capacity from the water content; low boiling point from the alcohol.
* **"The Bourbon Glaze" Risk:** This is our term for the accumulation of impurities (like copper oxides) over time. While the name is campy, **actual bourbon is strictly forbidden** as sugars/tannins would foul the cold plates. Requires a "Wash Cycle" maintenance protocol.

## ⚙️ Mechanical Constraints
* **Turbine Type:** Tesla Turbine (Bladeless). Preferred for its ability to handle "wet vapor" (mixed phase) without damage.
* **Generator:** Permanent Magnet Micro-Generator.
* **Gearing:**
    * **Speed Increaser:** Turbine (Low Torque/High RPM) -> Fan (High Speed/Air Volume).
    * **Variable Gearing:** Users change gears based on climate (e.g., larger fan gear for Texas heat, smaller for Alaska).

## 🛡️ Safety & "The Happy Hour Protocol"
* **Leak Detection:** Standard hydrocarbon sensors.
* **Failure Mode:** If the loop ruptures, the fluid evaporates quickly. It is flammable but not toxic.
* **"Happy Hour":** A tongue-in-cheek reference to the fact that the working fluid components (pure ethanol and distilled water) are food-grade, making clean-up less hazardous than glycol or refrigerant leaks. Still, don't drink the "Wash."

## 🧪 Architecture Evaluation Framework (AEF)

To ensure design decisions are grounded in physics, Project Moonshine employs a structured evaluation framework for all proposed hardware tracks.

### The Methodology

1.  **Candidate Architectures:** New designs are defined as "Options" with specific constraints (e.g., parasitic load, mechanical complexity).

2.  **Physics-Based Validation:** Every option must pass a battery of automated tests within the `moonshine-sim` environment.

3.  **Metric-Driven Evaluation:** Designs are scored against Net Energy Surplus, Thermal Stability, and Mechanical Reliability.

### Standard Test Structs

All simulations must output a standard result struct to maintain consistency across the project:

*   **Result (Boolean):** Pass/Fail against a defined physical threshold.

*   **Data (Object):** Raw physics values (e.g., Delta-P, Watts, kg/s).

*   **Narrative (String):** Engineering justification for the result.

## 📓 Discovery & Pivot Log

* **Pivot 1: Sourcing vs. Distance (Dec 2025)**
    * *Insight:* Local isn't always greener. Logistics (shipping) is so efficient that it often pays to "import" high-yield sugarcane ethanol rather than use local corn. 
    * *Action:* Integrated `ImpactAnalyzer` into the AEF.
* **Pivot 2: The Purity Imperative**
    * *Insight:* Industrial denaturants (methanol/gasoline) are "poisons" to our seals and thermal stability. 
    * *Action:* Moved to a "Food Grade / Pure Only" sourcing mandate in the roadmap.
* **Pivot 3: The Drift Trigger**
    * *Insight:* Preferential evaporation of ethanol means the system "stiffens" (boiling point rises) over time.
    * *Action:* Established "The Wash" flushing protocol based on BP drift thresholds.
    * *Research Goal:* Define triggers (e.g., hours of operation, conductivity change, or color shift) for replacing the 60/40 mix and cleaning the "Bourbon Glaze" (precipitated oxides).
* **Pivot 4: The Race to RPM (Dec 2025)**
    * *Insight:* At high TDP (1000W), we only have ~15 seconds from the first bubble of vapor to chip overheat. This is likely not enough time to overcome turbine stiction and spin the fan to full RPM.
    * *Action:* Added "Hybrid Starter Motor" discovery to the roadmap.
## 📝 Design History Log

* **Iteration 5:** "The Evaluation Pivot" - Introduced the AEF to allow for parallel development and simulation of multiple thermodynamic cycles.
