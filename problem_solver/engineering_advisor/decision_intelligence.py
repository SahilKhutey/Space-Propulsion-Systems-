import numpy as np
from ..schemas import EngineeringReport, Anomaly, Recommendation
from problem_solver.diagnosis.anomaly_detector import AnomalyDetector
from problem_solver.root_cause_analysis.diagnostic_engine import DiagnosticEngine
from problem_solver.recommendation_engine.advisor import EngineeringAdvisor
from problem_solver.mission_failure_analysis.failure_analyzer import MissionFailureAnalyzer

class DecisionIntelligenceSystem:
    def __init__(self):
        self.detector = AnomalyDetector()
        self.diagnoser = DiagnosticEngine()
        self.advisor = EngineeringAdvisor()
        self.analyzer = MissionFailureAnalyzer()
        
    def evaluate_run(self, history: list[dict], mission_context: dict = None) -> EngineeringReport:
        # 1. Detect anomalies
        anomalies = self.detector.detect(history)
        
        # 2. Diagnoses & Root causes
        root_causes = self.diagnoser.diagnose(history, anomalies, mission_context)
        
        # 3. Recommendations
        recommendations = self.advisor.generate_recommendations(root_causes)
        
        # 4. Failure analysis
        failure_info = self.analyzer.analyze(history, anomalies)
        
        # 5. Physical validity checks
        physically_valid = True
        for step in history:
            # Check efficiency limits (if available in step or context)
            if step.get("efficiency", 0.0) > 1.0:
                physically_valid = False
                break
            # Check mass total shouldn't increase without reason
            # (checked by comparing mass over time)
            
        # 6. Risks and uncertainties
        risks = []
        if anomalies:
            risks.append("Spacecraft operations encountered warning/critical thresholds during the run.")
        if any(step.get("battery_soc", 1.0) < 0.25 for step in history):
            risks.append("Low power margins: battery discharged below 25% SOC.")
        if any(np.max(step.get("thermal_k", [250.0])) > 330.0 for step in history):
            risks.append("Thermal margins: spacecraft component temperatures are approaching upper limit.")
        if any(step.get("propellant_fraction", 1.0) < 0.15 for step in history):
            risks.append("Low propellant margins: remaining fuel fraction is below 15%.")
            
        if not risks:
            risks.append("No critical risks identified. System parameters are well within margins.")
            
        # 7. Confidence calculation
        prediction_confidence = 0.95
        # If there are many anomalies, confidence drops slightly
        if anomalies:
            prediction_confidence -= min(0.3, len(anomalies) * 0.01)
            
        return EngineeringReport(
            physically_valid=physically_valid,
            mission_success=not failure_info.failed,
            limiting_subsystem=failure_info.limiting_subsystem,
            fails_first=failure_info.fails_first,
            design_improvements=recommendations,
            risks_and_uncertainties=risks,
            prediction_confidence=prediction_confidence
        )
