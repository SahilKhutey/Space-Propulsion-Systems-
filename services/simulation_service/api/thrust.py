from fastapi import APIRouter, HTTPException
from ..app.schemas.thruster import ThrusterDesignRequest, ThrusterPerformanceResult
from thrust_engine import ThrustEngine

router = APIRouter()
engine = ThrustEngine()


@router.post("/compute", response_model=ThrusterPerformanceResult)
async def compute_thrust(payload: ThrusterDesignRequest):
    try:
        res = engine.compute(payload.thruster_type, payload.model_dump())
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")
