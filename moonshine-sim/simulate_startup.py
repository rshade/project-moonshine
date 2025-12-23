import numpy as np
from moonshine.thermo import Distiller

def simulate_startup(tdp_watts=350, fluid_volume_ml=500, ambient_temp=20, max_chip_temp=95):
    """
    Simulates the 'Cold Start' phase where heat is applied but the fan is not yet spinning.
    """
    still = Distiller(mix_ratio=0.60)
    
    # Specific Heat Capacities (J/g*K)
    cp_water = 4.18
    cp_ethanol = 2.44
    cp_mix = (0.6 * cp_ethanol) + (0.4 * cp_water)
    
    # Mass of fluid
    rho_mix_g_ml = still.rho_mix / 1000 # kg/m3 to g/ml is 1:1
    mass_fluid_g = fluid_volume_ml * rho_mix_g_ml
    
    # Heat Capacity of the system (J/K)
    # Adding a placeholder 500g of copper for the cold plate/condenser
    mass_copper_g = 500
    cp_copper = 0.385
    system_heat_capacity = (mass_fluid_g * cp_mix) + (mass_copper_g * cp_copper)
    
    boiling_point = still.get_boiling_point()
    
    print(f"--- Cold Start Simulation ({tdp_watts}W) ---")
    print(f"Fluid Volume: {fluid_volume_ml}ml | Ambient: {ambient_temp}°C")
    print(f"Boiling Point: {boiling_point:.2f}°C")
    print("-" * 50)
    
    current_temp = ambient_temp
    time_seconds = 0
    dt = 1 # 1 second steps
    
    boil_time = None
    meltdown_time = None
    
    # Simulation loop
    for s in range(3600): # Max 1 hour
        # Heat added: Q = P * t
        energy_added_joules = tdp_watts * dt
        delta_t = energy_added_joules / system_heat_capacity
        current_temp += delta_t
        time_seconds += dt
        
        # Chip temp is slightly higher than fluid temp (assumed 5 degree gradient)
        chip_temp = current_temp + 5
        
        if current_temp >= boiling_point and boil_time is None:
            boil_time = time_seconds
            print(f"Minute {time_seconds/60:.1f}: Phase Change Starts (Vapor Production Begins)")
            
        if chip_temp >= max_chip_temp and meltdown_time is None:
            meltdown_time = time_seconds
            print(f"Minute {time_seconds/60:.1f}: ⚠️ CHIP OVERHEAT ({chip_temp:.1f}°C)")
            
        if boil_time and meltdown_time:
            break

    if boil_time and meltdown_time:
        margin = meltdown_time - boil_time
        if margin > 0:
            print(f"--- SUCCESS ---")
            print(f"The system has a {margin} second 'Vapor Buffer' to spin up the fan.")
        else:
            print(f"--- FAILURE ---")
            print(f"The chip overheated {abs(margin)} seconds BEFORE boiling started.")

if __name__ == "__main__":
    simulate_startup(tdp_watts=350, fluid_volume_ml=500)
    print("\n")
    simulate_startup(tdp_watts=1000, fluid_volume_ml=500) # Stress test
