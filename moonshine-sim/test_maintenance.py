from moonshine.thermo import Distiller

def run_maintenance_sim():
    initial_mix = 0.60
    still = Distiller(mix_ratio=initial_mix)
    
    print(f"--- Maintenance & Degradation Simulation ---")
    print(f"Initial State: {initial_mix*100:.1f}% Ethanol | BP: {still.get_boiling_point():.2f}°C")
    print("-" * 50)
    
    # Simulate a micro-leak of 0.1% of volume per day
    # Vapor leaks are ethanol-rich, shifting the liquid composition.
    checkpoints = [30, 90, 180, 365]
    
    for days in checkpoints:
        drift = still.simulate_drift(leak_rate_vol_pct_per_day=0.5, days=days)
        status = "OK" if not drift["requires_flush"] else "⚠️ REQUIRES FLUSH"
        
        print(f"Day {days:3}: Mix {drift['new_mix_ratio']*100:4.1f}% | BP {drift['new_boiling_point_c']:5.2f}°C | {status}")

if __name__ == "__main__":
    run_maintenance_sim()
