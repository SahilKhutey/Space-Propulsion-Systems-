import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from real_time_engine import SpacecraftConfig, StateManager, MissionLoop
from problem_solver.engineering_advisor.decision_intelligence import DecisionIntelligenceSystem

@pytest.mark.e2e
class TestEndToEndMissionReasoning:
    """End-to-End test for the integrated Problem-Solving and Validation framework."""

    def test_mars_transfer_battery_depletion_rca(self):
        # 1. Setup a Mars Transfer simulation configuration
        # Dry mass 500kg, battery capacity 5000 Wh, solar efficiency 30%, array 10m2
        cfg = SpacecraftConfig(
            name="MarsExplorer", dry_mass_kg=500, initial_propellant_kg=500,
            solar_array_area_m2=10.0, solar_efficiency=0.30,
            battery_capacity_wh=5000.0, base_load_w=5000.0
        )
        sm = StateManager(cfg)
        
        # Position far out (simulate deep space Mars transfer at 1.5 AU)
        # Position vector size: 1.5 AU
        sm.spacecraft.state.position = np.array([1.5 * 1.496e11, 0.0, 0.0])
        # Solar generation at 1.5 AU with 10m2 and 30% eff:
        # P_solar = 0.3 * 10 * 1361 * (1/1.5)^2 ≈ 1814 W
        
        loop = MissionLoop(sm, dt=60.0)
        
        # Force a heavy load that exceeds solar generation and drains the battery
        sm.spacecraft.state.thruster_on = False
        
        # Simulate until battery is completely depleted
        loop.run(150) # 150 steps * 60s = 9000s (2.5 hours)
        
        # Verify battery is depleted
        assert sm.spacecraft.state.battery_energy == 0.0
        
        # 2. Run the Decision Intelligence reasoning system
        dis = DecisionIntelligenceSystem()
        report = dis.evaluate_run(sm.get_history())
        
        # 3. Assert on the 7 Decision Intelligence questions
        assert report.physically_valid is True
        assert report.mission_success is False
        assert report.limiting_subsystem == "Power"
        assert "Power Subsystem" in report.fails_first
        
        # Verify recommended fixes contain design upgrades
        improvements = [rec.title for rec in report.design_improvements]
        assert any("Solar Array" in title or "Battery" in title for title in improvements)
        
        # Verify risks are identified
        assert len(report.risks_and_uncertainties) > 0
        assert report.prediction_confidence > 0.5
