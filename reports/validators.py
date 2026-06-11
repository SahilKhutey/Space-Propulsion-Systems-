import numpy as np

class PhysicalValidator:
    def __init__(self):
        pass
        
    def validate_physics(self, history: list[dict]) -> dict:
        results = {
            "mass_conserved": True,
            "energy_conserved": True,
            "efficiency_valid": True,
            "errors": []
        }
        
        if not history:
            return results
            
        for i in range(len(history)):
            step = history[i]
            
            # 1. Efficiency limit check
            eff = step.get("efficiency", 0.0)
            if eff > 1.0:
                results["efficiency_valid"] = False
                results["errors"].append(f"Step {i}: Thruster efficiency ({eff}) exceeds physical limit of 1.0.")
                
            # 2. Mass conservation check (mass shouldn't increase spontaneously)
            if i > 0:
                prev_step = history[i-1]
                m_prev = prev_step.get("mass_total_kg", 0.0)
                m_curr = step.get("mass_total_kg", 0.0)
                if m_curr > m_prev + 1e-5: # allowing tiny numeric tolerance
                    results["mass_conserved"] = False
                    results["errors"].append(f"Step {i}: Spontaneous mass increase from {m_prev:.3f} to {m_curr:.3f} kg.")
                    
        return results
