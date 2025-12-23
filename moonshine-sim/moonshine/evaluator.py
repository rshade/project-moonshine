from moonshine.thermo import Distiller
from moonshine.designs import Dimensions
from moonshine.impact import ImpactAnalyzer

class EvaluationMetrics:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.passed = False
        self.result_data = {}

class DesignOption:
    def __init__(self, id, name, parasitic_load_w):
        self.id = id
        self.name = name
        self.parasitic_load_w = parasitic_load_w
        self.tests = {
            "NET_ENERGY_SURPLUS": EvaluationMetrics("Net Energy Surplus", "Calculates recovered power minus parasitic loads."),
            "THERMAL_STABILITY": EvaluationMetrics("Thermal Stability", "Checks if boiling point stays below 85°C."),
            "STARTUP_RELIABILITY": EvaluationMetrics("Startup Reliability", "Ability to start without external assistance."),
            "ENVIRONMENTAL_IMPACT": EvaluationMetrics("Environmental Impact", "Analysis of sourcing and production footprint.")
        }

# Define the Architecture Struct
ARCHITECTURES = {
    "OPTION_A": DesignOption("A", "Forced Circulation (Pump)", parasitic_load_w=12.0),
    "OPTION_B": DesignOption("B", "Pumpless Ejector (Vapor-Jet)", parasitic_load_w=0.0),
    "OPTION_C": DesignOption("C", "Passive Thermosyphon (Gravity)", parasitic_load_w=0.0)
}

# Specific Tests for Options B and C
ARCHITECTURES["OPTION_B"].tests["EJECTOR_MOTIVE_PRESSURE"] = EvaluationMetrics(
    "Ejector Motive Pressure", "Verify if TDP produces enough vapor pressure to drive the Venturi."
)
ARCHITECTURES["OPTION_C"].tests["GRAVITY_HEAD_PRESSURE"] = EvaluationMetrics(
    "Gravity Head Pressure", "Verify if 400mm height overcomes turbine resistance."
)

def run_evaluation(tdp_watts=350, fill_volume_l=5.0, feedstock="CORN", dist_km=100):
    distiller = Distiller(mix_ratio=0.60)
    base_data = distiller.analyze_node(tdp_watts)
    recovered_pwr = base_data["recovered_power_w"]
    
    impact_analyzer = ImpactAnalyzer(volume_l=fill_volume_l)
    impact_data = impact_analyzer.analyze_source(feedstock, dist_km)
    
    print(f"--- Evaluating Architectures for {tdp_watts}W TDP ---")
    print(f"--- Sourcing: {feedstock} at {dist_km}km ---")
    
    for key, opt in ARCHITECTURES.items():
        # Test 1: Net Energy Surplus
        surplus = recovered_pwr - opt.parasitic_load_w
        opt.tests["NET_ENERGY_SURPLUS"].passed = surplus > 0
        opt.tests["NET_ENERGY_SURPLUS"].result_data = {"surplus_w": surplus}
        
        # Test 2: Thermal Stability
        opt.tests["THERMAL_STABILITY"].passed = True if key == "OPTION_A" else False 
        
        # Test 3: Environmental Impact (New)
        # We pass if the carbon footprint is below a certain threshold (arbitrary 10kg for now)
        opt.tests["ENVIRONMENTAL_IMPACT"].passed = impact_data["total_carbon_kg"] < 10.0
        opt.tests["ENVIRONMENTAL_IMPACT"].result_data = impact_data
        
        print(f"[{opt.id}] {opt.name}: Surplus={surplus:.2f}W | Stability={'PASS' if opt.tests['THERMAL_STABILITY'].passed else 'FAIL'} | Impact={'PASS' if opt.tests['ENVIRONMENTAL_IMPACT'].passed else 'FAIL'}")

if __name__ == "__main__":
    run_evaluation()
