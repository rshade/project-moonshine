import numpy as np

def simulate_gearbox_heat_transfer(temp_hot=80, temp_cold=25):
    """
    Simulates heat leakage from the turbine to the fan through the drivetrain.
    Baseline: Stainless Steel shaft and gears.
    Option A: Stainless shaft + Silicon Nitride gears.
    Option B: Stainless shaft + Zirconia gears.
    Option C: Invar/Composite shaft + Zirconia gears.
    """
    
    # Material Conductivity (W/m*K)
    k_values = {
        "Stainless Steel": 16.0,
        "Silicon Nitride (Si3N4)": 30.0,
        "Zirconia (ZrO2)": 2.5,
        "Invar (Low Expansion)": 13.0,
        "G10 Garolite (Housing)": 0.3
    }
    
    # Dimensions
    shaft_length_m = 0.15 # 15cm
    shaft_radius_m = 0.004 # 4mm
    shaft_area = np.pi * (shaft_radius_m**2)
    
    delta_t = temp_hot - temp_cold
    
    def calculate_leakage(k_shaft, k_gears=None):
        # Simplified: Heat flows through the shaft. 
        # If we have gears, they act as a series resistance.
        # R_total = L1/(k1*A) + L2/(k2*A) ...
        
        r_shaft = shaft_length_m / (k_shaft * shaft_area)
        
        if k_gears:
            # Gear contact area is small, but for simulation let's assume 
            # a 5mm 'gear zone' where the material changes.
            gear_length_m = 0.01 # 10mm of gear interface
            r_shaft_reduced = (shaft_length_m - gear_length_m) / (k_shaft * shaft_area)
            r_gears = gear_length_m / (k_gears * shaft_area)
            r_total = r_shaft_reduced + r_gears
        else:
            r_total = r_shaft
            
        watts = delta_t / r_total
        return watts

    results = {
        "Baseline (All Stainless)": calculate_leakage(k_values["Stainless Steel"]),
        "Si3N4 Gears (Strength focus)": calculate_leakage(k_values["Stainless Steel"], k_values["Silicon Nitride (Si3N4)"]),
        "ZrO2 Gears (Thermal Break focus)": calculate_leakage(k_values["Stainless Steel"], k_values["Zirconia (ZrO2)"]),
        "Full Thermal Break (Invar + ZrO2)": calculate_leakage(k_values["Invar (Low Expansion)"], k_values["Zirconia (ZrO2)"])
    }
    
    print(f"--- Gearbox Thermal Leakage Simulation ({temp_hot}°C -> {temp_cold}°C) ---")
    for scenario, watts in results.items():
        print(f"{scenario:35}: {watts:.4f} Watts")
        
    print("\n--- Analysis ---")
    reduction = (1 - (results["ZrO2 Gears (Thermal Break focus)"] / results["Baseline (All Stainless)"])) * 100
    print(f"Zirconia gears reduce shaft heat creep by {reduction:.1f}%")

if __name__ == "__main__":
    simulate_gearbox_heat_transfer()
