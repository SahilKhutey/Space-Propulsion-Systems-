from pydantic import BaseModel, Field, field_validator
from typing import Literal


class HallThrusterInput(BaseModel):
    thruster_type: Literal["hall_thruster"] = "hall_thruster"
    power_w: float = Field(..., gt=0, le=200000, description="Input power [W]")
    efficiency: float = Field(..., gt=0, le=1.0, description="Thrust efficiency")
    isp_s: float = Field(..., gt=0, le=20000, description="Specific impulse [s]")
    mass_flow_kg_s: float | None = Field(None, ge=0, description="Optional mass flow")

    @field_validator("efficiency")
    @classmethod
    def eff_range(cls, v):
        if not 0.1 <= v <= 0.85:
            raise ValueError("Hall thruster efficiency realistic range: 0.1-0.85")
        return v


class IonThrusterInput(BaseModel):
    thruster_type: Literal["ion_thruster"] = "ion_thruster"
    power_w: float = Field(..., gt=0, le=50000)
    efficiency: float = Field(..., gt=0, le=0.85)
    isp_s: float = Field(..., gt=0, le=15000)


class ChemicalThrusterInput(BaseModel):
    thruster_type: Literal["chemical"] = "chemical"
    propellant: Literal["bipropellant", "monopropellant", "LOX_LH2", "LOX_methane", "solid"]
    mass_flow_kg_s: float = Field(..., gt=0, le=2000)
    isp_s: float = Field(..., gt=0, le=550)
    chamber_pressure_pa: float = Field(7e6, gt=0)
    nozzle_area_ratio: float = Field(40, gt=1)


class VASIMRInput(BaseModel):
    thruster_type: Literal["VASIMR"] = "VASIMR"
    power_w: float = Field(..., gt=0, le=10_000_000)
    efficiency: float = Field(..., gt=0, le=0.9)
    isp_s: float = Field(..., gt=0, le=50000)


class NTRInput(BaseModel):
    thruster_type: Literal["NTR"] = "NTR"
    power_w: float = Field(..., gt=0, le=2_000_000)
    efficiency: float = Field(..., gt=0, le=0.8)
    isp_s: float = Field(..., gt=0, le=1200)
    mass_flow_kg_s: float = Field(..., gt=0, le=50)


class MPDInput(BaseModel):
    thruster_type: Literal["MPD"] = "MPD"
    power_w: float = Field(..., gt=0, le=5_000_000)
    efficiency: float = Field(..., gt=0, le=0.7)
    isp_s: float = Field(..., gt=0, le=10000)


class PulsedPlasmaInput(BaseModel):
    thruster_type: Literal["PPT"] = "PPT"
    power_w: float = Field(..., gt=0, le=5000)
    efficiency: float = Field(..., gt=0, le=0.4)
    isp_s: float = Field(..., gt=0, le=3000)


class ArcjetInput(BaseModel):
    thruster_type: Literal["arcjet"] = "arcjet"
    power_w: float = Field(..., gt=0, le=100000)
    efficiency: float = Field(..., gt=0, le=0.5)
    isp_s: float = Field(..., gt=0, le=2000)


class ResistojetInput(BaseModel):
    thruster_type: Literal["resistojet"] = "resistojet"
    power_w: float = Field(..., gt=0, le=2000)
    efficiency: float = Field(..., gt=0, le=0.4)
    isp_s: float = Field(..., gt=0, le=500)


ThrusterDesignRequest = (
    HallThrusterInput | IonThrusterInput | ChemicalThrusterInput
    | VASIMRInput | NTRInput | MPDInput | PulsedPlasmaInput
    | ArcjetInput | ResistojetInput
)


class ThrusterPerformanceResult(BaseModel):
    thruster_type: str
    thrust_n: float
    isp_s: float
    exhaust_velocity_ms: float
    power_w: float
    efficiency: float
    mass_flow_kg_s: float
    specific_power_w_per_n: float
    notes: str = ""
