class DesignAlternativeComparer:
    def __init__(self):
        pass
        
    def compare_thrusters(self, payload_mass_kg: float, delta_v_ms: float) -> dict:
        # Compare Hall vs Ion thrusters
        from core.mathematics.mission_design.tsiolkovsky import propellant_for_dv
        
        # Hall Thruster
        m_prop_hall = propellant_for_dv(delta_v_ms, 2000.0, payload_mass_kg)
        # Ion Thruster
        m_prop_ion = propellant_for_dv(delta_v_ms, 3500.0, payload_mass_kg)
        
        savings = m_prop_hall - m_prop_ion
        return {
            "hall_thruster": {
                "isp_s": 2000.0,
                "propellant_needed_kg": m_prop_hall,
                "total_mass_kg": payload_mass_kg + m_prop_hall
            },
            "ion_thruster": {
                "isp_s": 3500.0,
                "propellant_needed_kg": m_prop_ion,
                "total_mass_kg": payload_mass_kg + m_prop_ion
            },
            "propellant_savings_kg": savings,
            "best_option": "ion_thruster" if savings > 0 else "hall_thruster"
        }
