import unittest
from moonshine.thermo import Distiller

class TestDistillerPhysics(unittest.TestCase):
    def test_h100_flow_rate(self):
        still = Distiller(mix_ratio=0.60)
        # Test with 350W load
        _, flow_rate, power = still.analyze_node(tdp_watts=350)
        
        # Expect flow roughly 15mL/min
        self.assertTrue(10 < flow_rate < 20, f"Flow rate {flow_rate} outside expected range")
        self.assertGreater(power, 0)

if __name__ == '__main__':
    unittest.main()