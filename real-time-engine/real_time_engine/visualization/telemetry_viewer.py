class TelemetryViewer:
    def format_telemetry(self, raw_telemetry: dict) -> dict:
        return {"sc_time_s": raw_telemetry.get("time", 0.0), "telemetry_aligned": True}
