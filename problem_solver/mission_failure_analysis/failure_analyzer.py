from ..schemas import MissionFailure, Anomaly

class MissionFailureAnalyzer:
    def __init__(self):
        pass
        
    def analyze(self, history: list[dict], anomalies: list[Anomaly]) -> MissionFailure:
        if not anomalies:
            return MissionFailure(
                failed=False,
                reason="All subsystems operated within nominal safety envelopes.",
                limiting_subsystem="None",
                fails_first="None"
            )
            
        # Find critical anomalies
        critical_anom = [a for a in anomalies if a.severity in ["critical", "high"]]
        if not critical_anom:
            return MissionFailure(
                failed=False,
                reason="Minor warnings detected, but mission completed successfully.",
                limiting_subsystem="None",
                fails_first="None"
            )
            
        # Sort anomalies by timestamp to find what failed first
        sorted_anom = sorted(anomalies, key=lambda a: a.timestamp)
        first_failure = sorted_anom[0]
        
        # Primary reason for failure is the first critical or high anomaly
        primary_crit = [a for a in sorted_anom if a.severity in ["critical", "high"]]
        fail_reason = primary_crit[0].message if primary_crit else sorted_anom[0].message
        limiting_sub = primary_crit[0].anomaly_type if primary_crit else sorted_anom[0].anomaly_type
        fails_first = f"{first_failure.anomaly_type} Subsystem ({first_failure.message})"
        
        return MissionFailure(
            failed=True,
            reason=fail_reason,
            limiting_subsystem=limiting_sub,
            fails_first=fails_first
        )
