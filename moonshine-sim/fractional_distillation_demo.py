import numpy as np

def get_boiling_point(ethanol_frac):
    """
    Rough approximation of Ethanol-Water boiling point curve at 1 atm.
    """
    x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    y = [100.0, 92.7, 87.7, 84.4, 82.5, 81.3, 80.5, 79.8, 79.1, 78.5, 78.4]
    return np.interp(ethanol_frac, x, y)

def simulate_evaporation(initial_volume_ml=1000, initial_mix=0.60, steps=100):
    vol_liquid = initial_volume_ml
    mix_liquid = initial_mix
    
    print(f"{'Step':<5} | {'Vol (mL)':<10} | {'Mix (%)':<10} | {'BP (°C)':<10}")
    print("-" * 45)
    
    for i in range(steps):
        bp = get_boiling_point(mix_liquid)
        
        if i % 10 == 0:
            print(f"{i:<5} | {vol_liquid:<10.1f} | {mix_liquid*100:<10.1f} | {bp:<10.2f}")
        
        # VLE approximation
        alpha = 3.0 
        mix_vapor = (alpha * mix_liquid) / (1 + (alpha - 1) * mix_liquid)
        
        dv = vol_liquid * 0.01
        total_ethanol = vol_liquid * mix_liquid
        vapor_ethanol = dv * mix_vapor
        
        vol_liquid -= dv
        if vol_liquid <= 0: break
        mix_liquid = (total_ethanol - vapor_ethanol) / vol_liquid
        if mix_liquid < 0: mix_liquid = 0

if __name__ == "__main__":
    simulate_evaporation()