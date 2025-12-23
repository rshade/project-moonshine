import numpy as np
from moonshine.thermo import Distiller
from moonshine.designs import Dimensions

def test_gravity_pressure():
    distiller = Distiller(mix_ratio=0.60)
    rho = distiller.rho_mix # kg/m3
    g = 9.81 # m/s2
    h = Dimensions.TOWER_V1["max_height_mm"] / 1000.0 # meters (0.4m)
    
    # Hydrostatic Pressure P = rho * g * h
    pressure_pa = rho * g * h
    pressure_bar = pressure_pa / 100_000
    pressure_psi = pressure_pa * 0.000145038
    
    print(f"--- Gravity Head Calculation (Tower V1) ---")
    print(f"Fluid Density: {rho:.2f} kg/m3")
    print(f"Head Height: {h:.2f} m")
    print(f"Pressure Generated: {pressure_pa:.2f} Pa")
    print(f"Pressure (Bar): {pressure_bar:.4f} bar")
    print(f"Pressure (PSI): {pressure_psi:.4f} psi")
    
    # Engineering Judgment:
    # A Tesla turbine typically requires 0.5 to 2.0 bar to overcome bearing stiction 
    # and drive a cooling fan. 0.03 bar is likely insufficient for self-starting.
    threshold_bar = 0.1 # Minimum for ultra-low friction bearings
    passed = pressure_bar > threshold_bar
    
    print(f"Result: {'PASS' if passed else 'FAIL'} (Threshold: {threshold_bar} bar)")

if __name__ == "__main__":
    test_gravity_pressure()
