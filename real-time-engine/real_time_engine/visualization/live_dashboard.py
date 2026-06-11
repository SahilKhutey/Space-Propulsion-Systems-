class LiveDashboardHook:
    def get_dashboard_metrics(self, state_dict: dict) -> dict:
        return {
            "power_solar_w": state_dict["POWER_SOLAR"] if "POWER_SOLAR" in state_dict else 0.0,
            "power_load_w": state_dict["POWER_LOAD"] if "POWER_LOAD" in state_dict else 0.0,
            "battery_soc": state_dict["battery_soc"],
            "max_thermal_k": state_dict["max_temp_k"]
        }
