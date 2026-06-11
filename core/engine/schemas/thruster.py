from pydantic import BaseModel, Field

class HallInput(BaseModel):
    power_w: float = Field(..., gt=0)
    efficiency: float = Field(..., gt=0, le=1.0)
    isp_s: float = Field(..., gt=0)
