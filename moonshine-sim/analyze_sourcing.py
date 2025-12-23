from moonshine.impact import ImpactAnalyzer, FEEDSTOCKS
from moonshine.thermo import Distiller

def run_sourcing_comparison():
    # Volume for a single rack unit fill (estimated 5 Liters)
    fill_volume_l = 5.0
    
    scenarios = [
        {"name": "Local Corn (Truck 100km)", "key": "CORN", "dist": 100, "mode": "TRUCK"},
        {"name": "Distant Sugar Beet (Rail 1000km)", "key": "SUGAR_BEET", "dist": 1000, "mode": "RAIL"},
        {"name": "Imported Sugarcane (Ship 8000km + Truck 200km)", "key": "SUGARCANE", "dist": 8200, "mode": "SHIP"},
        {"name": "Local Cellulosic (Truck 50km)", "key": "CELLULOSIC", "dist": 50, "mode": "TRUCK"},
        {"name": "Regional Potato (Truck 500km)", "key": "POTATO", "dist": 500, "mode": "TRUCK"},
    ]
    
    analyzer = ImpactAnalyzer(volume_l=fill_volume_l)
    still = Distiller(mix_ratio=0.60) # Target project mix
    flash_point = still.get_flash_point()
    
    print(f"--- Sourcing Impact Analysis ({fill_volume_l}L Fill) ---")
    print(f"Safety Note: 60/40 Mix Flash Point approx {flash_point:.1f} °C")
    print("-" * 85)
    print(f"{'Scenario':<40} | {'CO2(kg)':<8} | {'Water(L)':<8} | {'W-Water(L)':<10} | {'Cost($)':<8}")
    print("-" * 85)
    
    results = []
    for s in scenarios:
        res = analyzer.analyze_source(s["key"], s["dist"], s["mode"])
        print(f"{s['name']:<40} | {res['total_carbon_kg']:<8.2f} | {res['total_water_l']:<8.1f} | {res['weighted_water_l']:<10.1f} | {res['total_cost_usd']:<8.2f}")
        results.append((s['name'], res))

    # Identify bests
    best_carbon = min(results, key=lambda x: x[1]['total_carbon_kg'])
    best_water = min(results, key=lambda x: x[1]['weighted_water_l'])
    best_cost = min(results, key=lambda x: x[1]['total_cost_usd'])
    
    print("-" * 85)
    print(f"Best for Carbon: {best_carbon[0]} ({best_carbon[1]['total_carbon_kg']:.2f} kg)")
    print(f"Best for Water:  {best_water[0]} ({best_water[1]['weighted_water_l']:.1f} Weighted L)")
    print(f"Best for Cost:   {best_cost[0]} (${best_cost[1]['total_cost_usd']:.2f})")
    
    print("\n--- Break-even Analysis (Carbon) ---")
    be_km = analyzer.find_carbon_breakeven_distance("CORN", "SUGAR_BEET", mode_b="RAIL")
    print(f"Local Corn vs Distant Sugar Beet (Rail): Sugar Beet is better up to {be_km:.0f} km")
    
    be_km_truck = analyzer.find_carbon_breakeven_distance("CORN", "SUGAR_BEET", mode_b="TRUCK")
    print(f"Local Corn vs Distant Sugar Beet (Truck): Sugar Beet is better up to {be_km_truck:.0f} km")

    be_km_cane = analyzer.find_carbon_breakeven_distance("CORN", "SUGARCANE", mode_b="SHIP")
    print(f"Local Corn vs Imported Sugarcane (Ship): Sugarcane is better up to {be_km_cane:.0f} km")

if __name__ == "__main__":
    run_sourcing_comparison()
