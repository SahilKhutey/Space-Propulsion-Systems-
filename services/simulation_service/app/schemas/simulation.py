from pydantic import BaseModel, Field
from typing import Literal


class ThermalRequest(BaseModel):
    power_dissipation_w: float = Field(..., gt=0, le=50000)
    ambient_temp_k: float = Field(3.0, ge=0)
    component_area_m2: float = Field(0.1, gt=0, le=100)
    emissivity: float = Field(0.85, gt=0, le=1.0)
    radiator_area_m2: float = Field(0.5, gt=0, le=200)
    radiator_emissivity: float = Field(0.85, gt=0, le=1.0)
    solar_irradiance_w_m2: float = Field(1361.0, ge=0)
    absorptivity: float = Field(0.3, ge=0, le=1.0)
    time_hours: float = Field(24.0, gt=0, le=8760)
    time_step_s: float = Field(60.0, gt=0)


class ThermalNodeResult(BaseModel):
    component: str
    min_temp_k: float
    max_temp_k: float
    steady_state_k: float
    time_series_t: list[float]
    time_series_temp_k: list[float]


class ThermalResult(BaseModel):
    steady_state_k: float
    min_temp_k: float
    max_temp_k: float
    radiator_required_m2: float
    heat_rejected_w: float
    time_series: list[ThermalNodeResult]
    warnings: list[str] = []
    safe: bool = True


class PowerRequest(BaseModel):
    solar_array_area_m2: float = Field(..., gt=0, le=1000)
    solar_efficiency: float = Field(0.30, gt=0, le=0.5)
    distance_au: float = Field(1.0, gt=0, le=50)
    battery_capacity_wh: float = Field(..., gt=0)
    eclipse_duration_min: float = Field(35.0, ge=0, le=120)
    orbit_period_min: float = Field(90.0, gt=0, le=1440)
    thruster_power_w: float = Field(..., gt=0)
    thruster_duty_cycle: float = Field(0.25, ge=0, le=1.0)


class PowerResult(BaseModel):
    solar_power_w: float
    average_power_w: float
    eclipse_loss_wh: float
    thruster_energy_per_orbit_wh: float
    battery_margin: float
    feasible: bool
    notes: list[str] = []


class TradeStudyRequest(BaseModel):
    payload_mass_kg: float = Field(..., gt=0)
    delta_v_ms: float = Field(..., gt=0)
    mission_duration_years: float = Field(5.0, gt=0)
    power_budget_w: float | None = Field(None, gt=0)
    candidates: list[str] = [
        "chemical_bipropellant", "hall_thruster",
        "ion_thruster", "VASIMR"
    ]


class TradeStudyCandidate(BaseModel):
    thruster_type: str
    isp_s: float
    thrust_n: float
    propellant_mass_kg: float
    total_mass_kg: float
    power_w: float
    efficiency: float
    transfer_time_days: float
    score: float


class TradeStudyResult(BaseModel):
    mission_summary: dict
    candidates: list[TradeStudyCandidate]
    winner: str
    rationale: str
