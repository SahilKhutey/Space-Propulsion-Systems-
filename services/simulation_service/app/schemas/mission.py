from pydantic import BaseModel, Field
from typing import Literal


class MissionRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    initial_orbit: Literal["LEO", "SSO", "MEO", "GEO", "HEO", "LUNAR"] = "LEO"
    target_orbit: Literal["LEO", "SSO", "MEO", "GEO", "HEO", "LUNAR", "MARS_TRANSFER", "ASTEROID"] = "GEO"
    payload_mass_kg: float = Field(..., gt=0, le=50000)
    thruster_type: str
    isp_s: float = Field(..., gt=0)
    efficiency: float = Field(0.5, gt=0, le=1.0)
    power_w: float = Field(..., gt=0)
    duration_years: float = Field(5.0, gt=0, le=50)
    safety_factor: float = Field(1.2, ge=1.0, le=2.0)


class MissionResult(BaseModel):
    mission_name: str
    delta_v_ms: float
    propellant_mass_kg: float
    initial_mass_kg: float
    final_mass_kg: float
    transfer_time_days: float
    power_consumed_kwh: float
    thermal_load_w: float
    success_probability: float
    notes: list[str] = []


class HohmannTransferRequest(BaseModel):
    r1_m: float = Field(..., gt=0, description="Initial orbit radius [m]")
    r2_m: float = Field(..., gt=0, description="Target orbit radius [m]")
    body: Literal["earth", "mars", "venus", "jupiter", "saturn"] = "earth"


class OrbitRaisingResult(BaseModel):
    dv1_ms: float
    dv2_ms: float
    total_dv_ms: float
    transfer_time_s: float
    transfer_time_days: float
    body: str
