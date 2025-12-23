from dataclasses import dataclass
from typing import Dict
import yaml
from pathlib import Path

@dataclass
class Feedstock:
    name: str
    water_intensity_l_per_l: float  # Liters of water per Liter of ethanol
    carbon_intensity_kg_per_l: float # kg CO2e per Liter of ethanol
    avg_price_usd_per_l: float       # Market price estimate
    typical_yield_l_per_hectare: float
    water_scarcity_index: float      # 1.0 = baseline, >1.0 = high stress region

def load_data():
    # Resolve path to data/feedstocks.yaml
    # This file is in moonshine-sim/moonshine/impact.py
    # We need to go up two levels to root, then into data/
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    yaml_path = project_root / "data" / "feedstocks.yaml"
    
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data

_YAML_DATA = load_data()

# Load Feedstocks from YAML
FEEDSTOCKS = {}
for key, val in _YAML_DATA["feedstocks"].items():
    FEEDSTOCKS[key] = Feedstock(
        name=val["name"],
        water_intensity_l_per_l=val["water_intensity_l_per_l"],
        carbon_intensity_kg_per_l=val["carbon_intensity_kg_per_l"],
        avg_price_usd_per_l=val["avg_price_usd_per_l"],
        typical_yield_l_per_hectare=val["typical_yield_l_per_hectare"],
        water_scarcity_index=val["water_scarcity_index"]
    )

class Logistics:
    # Load Logistics from YAML
    _EMISSIONS = _YAML_DATA["logistics"]["emissions_per_kg_km"]
    
    EMISSIONS_TRUCK = _EMISSIONS["TRUCK"]
    EMISSIONS_RAIL = _EMISSIONS["RAIL"]
    EMISSIONS_SHIP = _EMISSIONS["SHIP"]

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
            
        # Get emission factor dynamically based on mode
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
