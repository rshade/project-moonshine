import numpy as np

class Distiller:
    """
    The Core Physics Engine for Project Moonshine.
    Calculates thermodynamic performance of the Rankine Cycle.
    """
    
    def __init__(self, mix_ratio=0.60):
        self.mix_ratio = mix_ratio
        # Latent Heat (kJ/kg) approx
        self.h_vap_ethanol = 841
        self.h_vap_water = 2260
        self.rho_ethanol = 789
        self.rho_water = 997
        
        # Weighted Average
        self.h_vap_mix = (mix_ratio * self.h_vap_ethanol) + ((1-mix_ratio) * self.h_vap_water)
        self.rho_mix = (mix_ratio * self.rho_ethanol) + ((1-mix_ratio) * self.rho_water)

    def get_boiling_point(self):
        """
        Returns boiling point in Celsius for the current mix_ratio at 1 atm.
        Accounts for zeotropic 'Glide'.
        """
        x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        y = [100.0, 92.7, 87.7, 84.4, 82.5, 81.3, 80.5, 79.8, 79.1, 78.5, 78.4]
        return np.interp(self.mix_ratio, x, y)

    def get_flash_point(self):
        """
        Estimates the flash point in Celsius.
        Data based on standard Ethanol/Water flash point curves.
        """
        # x: Ethanol volume fraction, y: Flash point (C)
        x = [0.05, 0.10, 0.20, 0.30, 0.40, 0.60, 0.80, 0.96, 1.0]
        y = [62, 49, 36, 29, 26, 22, 19, 17, 13]
        if self.mix_ratio < 0.01:
            return 100 # Effectively non-flammable
        return np.interp(self.mix_ratio, x, y)

    def analyze_node(self, tdp_watts, turbine_efficiency=0.15):
        h_vap_joules = self.h_vap_mix * 1000
        mass_flow_rate = tdp_watts / h_vap_joules # kg/s
        
        vol_flow_rate_m3 = mass_flow_rate / self.rho_mix
        vol_flow_rate_ml_min = vol_flow_rate_m3 * 1e6 * 60
        
        recovered_power = tdp_watts * turbine_efficiency
        bp = self.get_boiling_point()
        
        return {
            "mass_flow_kg_s": mass_flow_rate,
            "vol_flow_ml_min": vol_flow_rate_ml_min,
            "recovered_power_w": recovered_power,
            "boiling_point_c": bp
        }

    def simulate_drift(self, leak_rate_vol_pct_per_day, days):
        """
        Simulates 'Boiling Point Drift' due to fractional distillation.
        Assumes any vapor leak is 85% ethanol (azeotrope-ish) while the 
        bulk liquid is 60%. This causes the liquid to become water-heavy.
        """
        current_mix = self.mix_ratio
        for _ in range(int(days)):
            # Loss of ethanol is faster than loss of water in a vapor leak
            # This is a simplified model of preferential evaporation
            ethanol_loss_factor = 1.5 
            loss = (leak_rate_vol_pct_per_day / 100.0)
            current_mix -= (loss * current_mix * ethanol_loss_factor)
            current_mix = max(0.0, current_mix)
            
        new_bp = np.interp(current_mix, 
                           [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                           [100.0, 92.7, 87.7, 84.4, 82.5, 81.3, 80.5, 79.8, 79.1, 78.5, 78.4])
        
        return {
            "new_mix_ratio": current_mix,
            "new_boiling_point_c": new_bp,
            "requires_flush": new_bp > 85.0 # Maintenance trigger
        }

if __name__ == "__main__":
    still = Distiller(mix_ratio=0.60)
    data = still.analyze_node(tdp_watts=350)
    print(f"Boiling Point: {data['boiling_point_c']:.2f} °C")
    print(f"Required Flow: {data['vol_flow_ml_min']:.2f} mL/min")
    print(f"Recovered Power: {data['recovered_power_w']:.2f} W")