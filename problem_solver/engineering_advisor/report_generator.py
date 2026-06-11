from ..schemas import EngineeringReport

class EngineeringReportGenerator:
    def __init__(self):
        pass
        
    def generate_markdown(self, report: EngineeringReport) -> str:
        lines = []
        lines.append("# PROPSIM ENGINEERING DECISION INTELLIGENCE REPORT")
        lines.append("## Executive Summary")
        lines.append(f"- **Physical Validity:** {'PASS' if report.physically_valid else 'FAIL'}")
        lines.append(f"- **Mission Success:** {'SUCCESS' if report.mission_success else 'FAILED'}")
        lines.append(f"- **Limiting Subsystem:** {report.limiting_subsystem}")
        lines.append(f"- **First Failure Component:** {report.fails_first}")
        lines.append(f"- **Prediction Confidence:** {report.prediction_confidence*100:.1f}%")
        lines.append("")
        
        lines.append("## Risks and Uncertainties")
        for risk in report.risks_and_uncertainties:
            lines.append(f"- {risk}")
        lines.append("")
        
        lines.append("## Recommended Design Improvements")
        for i, rec in enumerate(report.design_improvements):
            lines.append(f"### {i+1}. {rec.title}")
            lines.append(f"- **Description:** {rec.description}")
            lines.append(f"- **Expected Impact:** {rec.expected_impact}")
            lines.append(f"- **Confidence:** {rec.confidence*100:.1f}%")
            lines.append("")
            
        return "\n".join(lines)
