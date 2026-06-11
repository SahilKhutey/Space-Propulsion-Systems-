from ..schemas import Recommendation, RootCause

class EngineeringAdvisor:
    def __init__(self):
        pass
        
    def generate_recommendations(self, root_causes: list[RootCause]) -> list[Recommendation]:
        recommendations = []
        for rc in root_causes:
            cause = rc.root_cause
            if cause == "Solar Array Undersized":
                recommendations.append(Recommendation(
                    title="Increase Solar Array Area",
                    description="Expand the solar array area by 40-50% to generate sufficient power at Mars distance (1.52 AU) where solar intensity drops to ~43% of Earth levels.",
                    expected_impact="Eliminates power deficit during transit, maintaining positive power margin.",
                    confidence=0.95
                ))
                recommendations.append(Recommendation(
                    title="Upgrade to High-Efficiency Solar Cells",
                    description="Upgrade the solar arrays from 30% to 35-40% multi-junction solar cells to generate more power per square meter.",
                    expected_impact="Increases power output by 15-20% without requiring larger mechanical array deployment.",
                    confidence=0.85
                ))
            elif cause == "Battery Undersized":
                recommendations.append(Recommendation(
                    title="Increase Battery Capacity",
                    description="Increase the battery capacity (e.g. from 5 kWh to 8-10 kWh) to handle shadow/eclipse periods in LEO or planet orbit.",
                    expected_impact="Maintains battery State of Charge above 20% warning threshold during worst-case eclipses.",
                    confidence=0.95
                ))
                recommendations.append(Recommendation(
                    title="Optimize Eclipse Power Profile",
                    description="Implement load-shedding during eclipse periods by turning off non-essential systems and lower thruster duty cycles.",
                    expected_impact="Reduces battery discharge rate, preventing critical depletion during eclipse.",
                    confidence=0.8
                ))
            elif cause in ["Insufficient Radiator Heat Rejection", "Overheating"]:
                recommendations.append(Recommendation(
                    title="Expand Radiator Rejection Area",
                    description="Increase the spacecraft radiator area or add deployable radiators to reject thruster waste heat more effectively.",
                    expected_impact="Reduces peak node temperature, preventing thermal runaway during continuous thruster firing.",
                    confidence=0.9
                ))
                recommendations.append(Recommendation(
                    title="Apply High-Emissivity Coating",
                    description="Use high-emissivity (e.g., silverized Teflon, ε >= 0.88) coating on thermal nodes to maximize radiative cooling.",
                    expected_impact="Increases radiative heat rejection rate by 5-10%.",
                    confidence=0.8
                ))
            elif cause == "Fuel Depleted":
                recommendations.append(Recommendation(
                    title="Increase Propellant Mass",
                    description="Increase initial propellant load (increase fuel fraction).",
                    expected_impact="Ensures sufficient propellant for the complete mission delta-v requirements.",
                    confidence=0.95
                ))
                recommendations.append(Recommendation(
                    title="Upgrade to High-Isp Thruster",
                    description="Upgrade the thruster from a Hall thruster (Isp = 2000s) to an Ion thruster (Isp = 3500s) to reduce mass flow rate.",
                    expected_impact="Reduces propellant consumption by ~40% for the same delta-v.",
                    confidence=0.9
                ))
                
        # Default recommendation if no root causes identified
        if not recommendations:
            recommendations.append(Recommendation(
                title="Perform Margin Review",
                description="Review all subsystem design margins (power, thermal, mass) for compliance.",
                expected_impact="Identifies hidden safety factor violations.",
                confidence=0.5
            ))
            
        return recommendations
