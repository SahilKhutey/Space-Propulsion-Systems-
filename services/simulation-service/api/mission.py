from fastapi import APIRouter, HTTPException
from ..app.schemas.mission import MissionRequest, MissionResult
from mission_engine import MissionEngine

router = APIRouter()
engine = MissionEngine()


@router.post("/compute", response_model=MissionResult)
async def compute_mission(payload: MissionRequest):
    try:
        res = engine.compute(payload.model_dump())
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
