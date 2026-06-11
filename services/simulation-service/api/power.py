from fastapi import APIRouter, HTTPException
from ..app.schemas.simulation import PowerRequest, PowerResult
from power_engine import PowerEngine

router = APIRouter()
engine = PowerEngine()


@router.post("/compute", response_model=PowerResult)
async def compute_power(payload: PowerRequest):
    try:
        res = engine.compute(payload.model_dump())
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
