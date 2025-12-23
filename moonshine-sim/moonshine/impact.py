from dataclasses import dataclass
from typing import Dict

@dataclass
class Feedstock:
    name: str
    water_intensity_l_per_l: float  # Liters of water per Liter of ethanol
    carbon_intensity_kg_per_l: float # kg CO2e per Liter of ethanol
    avg_price_usd_per_l: float       # Market price estimate
    typical_yield_l_per_hectare: float
    water_scarcity_index: float      # 1.0 = baseline, >1.0 = high stress region

# Source Data (Estimated/Average values for simulation)
# References: GREET model, various LCA studies.
FEEDSTOCKS = {
    "CORN": Feedstock(
        name="Corn (Maize)",
        water_intensity_l_per_l=10.0, 
        carbon_intensity_kg_per_l=1.2, 
        avg_price_usd_per_l=0.50,
        typical_yield_l_per_hectare=3800,
        water_scarcity_index=1.2 # US Midwest/General
    ),
    "SUGAR_BEET": Feedstock(
        name="Sugar Beet",
        water_intensity_l_per_l=5.0,
        carbon_intensity_kg_per_l=0.9,
        avg_price_usd_per_l=0.65,
        typical_yield_l_per_hectare=6000,
        water_scarcity_index=1.5 # often grown in areas needing irrigation
    ),
    "SUGARCANE": Feedstock(
        name="Sugarcane",
        water_intensity_l_per_l=4.0,
        carbon_intensity_kg_per_l=0.5,
        avg_price_usd_per_l=0.45,
        typical_yield_l_per_hectare=7000,
        water_scarcity_index=2.0 # High stress in some tropical regions
    ),
    "POTATO": Feedstock(
        name="Potato",
        water_intensity_l_per_l=12.0,
        carbon_intensity_kg_per_l=1.5,
        avg_price_usd_per_l=0.80,
        typical_yield_l_per_hectare=2500,
        water_scarcity_index=1.1
    ),
    "CELLULOSIC": Feedstock(
        name="Cellulosic (Waste/Switchgrass)",
        water_intensity_l_per_l=2.0,
        carbon_intensity_kg_per_l=0.2,
        avg_price_usd_per_l=1.20,
        typical_yield_l_per_hectare=2000,
        water_scarcity_index=1.0 # Baseline
    )
}

class Logistics:
    # kg CO2 per Liter per km
    EMISSIONS_TRUCK = 0.0001  
    EMISSIONS_RAIL = 0.00003
    EMISSIONS_SHIP = 0.00001

    @staticmethod
    def calculate_transport_impact(volume_l: float, distance_km: float, mode: str = "TRUCK"):
        if mode == "TRUCK":
            factor = Logistics.EMISSIONS_TRUCK
        elif mode == "RAIL":
            factor = Logistics.EMISSIONS_RAIL
        elif mode == "SHIP":
            factor = Logistics.EMISSIONS_SHIP
        else:
            factor = Logistics.EMISSIONS_TRUCK
            
        return volume_l * distance_km * factor

class ImpactAnalyzer:
    def __init__(self, volume_l: float):
        self.volume_l = volume_l

    def analyze_source(self, feedstock_key: str, distance_km: float, mode: str = "TRUCK"):
        feedstock = FEEDSTOCKS.get(feedstock_key)
        if not feedstock:
            raise ValueError(f"Unknown feedstock: {feedstock_key}")
            
        production_carbon = feedstock.carbon_intensity_kg_per_l * self.volume_l
        transport_carbon = Logistics.calculate_transport_impact(self.volume_l, distance_km, mode)
        total_carbon = production_carbon + transport_carbon
        
        total_water = feedstock.water_intensity_l_per_l * self.volume_l
        weighted_water = total_water * feedstock.water_scarcity_index
        total_cost = feedstock.avg_price_usd_per_l * self.volume_l
        
        return {
            "feedstock": feedstock.name,
            "total_carbon_kg": total_carbon,
            "transport_carbon_kg": transport_carbon,
            "production_carbon_kg": production_carbon,
            "total_water_l": total_water,
            "weighted_water_l": weighted_water,
            "total_cost_usd": total_cost,
            "carbon_per_l": total_carbon / self.volume_l
        }

    def find_carbon_breakeven_distance(self, feedstock_a: str, feedstock_b: str, mode_a: str = "TRUCK", mode_b: str = "TRUCK"):
        """
        Finds the distance for feedstock_b that makes it equivalent in carbon to feedstock_a at 0km.
        """
        fa = FEEDSTOCKS[feedstock_a]
        fb = FEEDSTOCKS[feedstock_b]
        
        diff_production = fa.carbon_intensity_kg_per_l - fb.carbon_intensity_kg_per_l
        
        if diff_production <= 0:
            return 0.0 # Feedstock B is already worse or equal at production level
            
        factor_b = getattr(Logistics, f"EMISSIONS_{mode_b}")
        return diff_production / factor_b

    def find_water_breakeven_delta(self, feedstock_a: str, feedstock_b: str):
        """
        Compares water usage. Since shipping doesn't (usually) consume fresh water 
        in the same way farming does, this is a simpler direct comparison.
        """
        fa = FEEDSTOCKS[feedstock_a]
        fb = FEEDSTOCKS[feedstock_b]
        return fa.water_intensity_l_per_l - fb.water_intensity_l_per_l
