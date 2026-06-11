class ThermalMapRenderer:
    def render_heat_map(self, thermal_vector: list[float]) -> dict:
        return {f"node_{i}": temp for i, temp in enumerate(thermal_vector)}
