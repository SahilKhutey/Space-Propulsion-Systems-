from fastapi import APIRouter, HTTPException
from ..app.schemas.simulation import ThermalRequest, ThermalResult
from thermal_engine import ThermalEngine

router = APIRouter()
engine = ThermalEngine()


@router.post("/compute", response_model=ThermalResult)
async def compute_thermal(payload: ThermalRequest):
    try:
        res = engine.compute(payload.model_dump())
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
