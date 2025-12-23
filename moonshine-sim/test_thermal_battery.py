import numpy as np

def simulate_thermal_battery(target_runtime_minutes=5, turbine_load_watts=50):
    """
    Calculates the volume of Phase Change Material (PCM) required to 
    sustain the turbine output after the heat source (chip) is turned off.
    
    Target PCM: Barium Hydroxide Octahydrate (Ba(OH)2·8H2O)
    Melting Point: 78°C
    Latent Heat: 265 kJ/kg
    Density: 2180 kg/m3
    """
    
    # PCM Properties
    pcm_name = "Barium Hydroxide Octahydrate"
    melting_point_c = 78.0
    latent_heat_j_kg = 265 * 1000 # J/kg
    density_kg_m3 = 2180
    
    # Energy Required
    # We need to supply enough heat to boil the ethanol.
    # The turbine is ~15% efficient. So to get 50W mechanical output,
    # we need ~330W of thermal input? No, we need to supply the *Latent Heat of Vaporization*
    # to the ethanol to keep the pressure up.
    
    # Let's assume the turbine needs a mass flow rate equivalent to 300W thermal input
    # to maintain minimal idle RPM.
    thermal_input_required_watts = 300 
    
    seconds = target_runtime_minutes * 60
    total_energy_joules = thermal_input_required_watts * seconds
    
    # Mass of PCM required
    # Energy = Mass * Latent_Heat
    mass_pcm_kg = total_energy_joules / latent_heat_j_kg
    
    # Volume required
    vol_pcm_m3 = mass_pcm_kg / density_kg_m3
    vol_pcm_liters = vol_pcm_m3 * 1000
    
    # Dimensions (Cylinder)
    # Assume we fit this inside a canister in the flow path.
    # If cylinder radius is 3cm (0.03m)
    radius_m = 0.03
    area_m2 = np.pi * (radius_m**2)
    length_m = vol_pcm_m3 / area_m2
    
    print(f"--- Thermal Battery Simulation ({pcm_name}) ---")
    print(f"Target Runtime: {target_runtime_minutes} minutes")
    print(f"Thermal Load: {thermal_input_required_watts} Watts (to sustain turbine)")
    print(f"Total Energy Stored: {total_energy_joules/1000:.1f} kJ")
    print("-" * 40)
    print(f"Mass Required: {mass_pcm_kg:.3f} kg")
    print(f"Volume Required: {vol_pcm_liters:.3f} Liters")
    print(f"Physical Size (r=3cm): Length = {length_m*100:.1f} cm")
    
    return {
        "mass_kg": mass_pcm_kg,
        "volume_l": vol_pcm_liters
    }

if __name__ == "__main__":
    simulate_thermal_battery()
