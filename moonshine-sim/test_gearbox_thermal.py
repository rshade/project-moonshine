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

    def calculate_active_cooling(k_shaft, k_gears, h_air=50, fin_area=0.01):
        """
        Simulates an "Active Thermal Break" where the gearbox has fins and is in the airflow.
        We treat the gearbox as a thermal node between the Turbine and the Fan.
        
        Q_in (from Turbine) = (T_hot - T_gearbox) / R_shaft_in
        Q_out_air (to Air)  = h_air * fin_area * (T_gearbox - T_air)
        Q_leak (to Fan)     = (T_gearbox - T_cold) / R_shaft_out
        
        We solve for T_gearbox where Q_in = Q_out_air + Q_leak
        """
        # Resistances
        # Assume gearbox is at 1/3 distance from turbine
        dist_to_gearbox = 0.05 # 5cm
        dist_to_fan = 0.10     # 10cm remaining
        
        r_shaft_in = dist_to_gearbox / (k_shaft * shaft_area)
        r_shaft_out = dist_to_fan / (k_shaft * shaft_area)
        
        # Add gear resistance to the input side (heat must cross gears to enter housing?)
        # Or assume gears are the "node". Let's assume gears are the node.
        gear_length_m = 0.01
        r_gears = gear_length_m / (k_gears * shaft_area)
        r_in_total = r_shaft_in + r_gears
        
        # Convection Resistance (1 / hA)
        r_convection = 1 / (h_air * fin_area)
        
        # Solve for T_gearbox (Node analysis)
        # (T_h - T_g)/R_in = (T_g - T_air)/R_conv + (T_g - T_c)/R_out
        # T_h/R_in + T_air/R_conv + T_c/R_out = T_g * (1/R_in + 1/R_conv + 1/R_out)
        
        t_air = 25 # Assuming intake air temp
        
        conductance_sum = (1/r_in_total) + (1/r_convection) + (1/r_shaft_out)
        weighted_temps = (temp_hot/r_in_total) + (t_air/r_convection) + (temp_cold/r_shaft_out)
        
        t_gearbox = weighted_temps / conductance_sum
        
        # Calculate leakage to fan
        q_leak = (t_gearbox - temp_cold) / r_shaft_out
        
        return q_leak, t_gearbox

    # Active Cooling Parameters
    # h_air ~ 50-100 W/m^2K for forced air
    # fin_area ~ 10cm x 10cm effective surface area = 0.01 m^2
    active_leak, active_temp = calculate_active_cooling(k_values["Stainless Steel"], k_values["Zirconia (ZrO2)"])

    results = {
        "Baseline (All Stainless)": calculate_leakage(k_values["Stainless Steel"]),
        "Si3N4 Gears (Strength focus)": calculate_leakage(k_values["Stainless Steel"], k_values["Silicon Nitride (Si3N4)"]),
        "ZrO2 Gears (Thermal Break focus)": calculate_leakage(k_values["Stainless Steel"], k_values["Zirconia (ZrO2)"]),
        "Full Thermal Break (Invar + ZrO2)": calculate_leakage(k_values["Invar (Low Expansion)"], k_values["Zirconia (ZrO2)"]),
        "Active Cooling (Fins + Airflow)": active_leak
    }
    
    print(f"--- Gearbox Thermal Leakage Simulation ({temp_hot}°C -> {temp_cold}°C) ---")
    for scenario, watts in results.items():
        print(f"{scenario:35}: {watts:.4f} Watts")
        
    print(f"\nActive Cooling Node Temp: {active_temp:.2f}°C")
        
    print("\n--- Analysis ---")
    reduction = (1 - (results["ZrO2 Gears (Thermal Break focus)"] / results["Baseline (All Stainless)"])) * 100
    active_reduction = (1 - (active_leak / results["Baseline (All Stainless)"])) * 100
    print(f"Zirconia gears reduce shaft heat creep by {reduction:.1f}%")
    print(f"Adding Fins + Airflow reduces it by {active_reduction:.1f}% (The 'Active Break')")

if __name__ == "__main__":
    simulate_gearbox_heat_transfer()
