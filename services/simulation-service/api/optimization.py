from fastapi import APIRouter, HTTPException
from typing import Literal
from ..app.schemas.simulation import TradeStudyRequest, TradeStudyResult
from optimization_engine import OptimizationEngine

router = APIRouter()
engine = OptimizationEngine()


@router.post("/study", response_model=TradeStudyResult)
async def run_trade_study(payload: TradeStudyRequest):
    try:
        res = engine.run_trade_study(payload.model_dump())
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def run_optimization(
    thruster_type: str,
    target: Literal["thrust", "isp", "efficiency"],
    power_limit_w: float = 10000.0,
    mass_flow_limit_kg_s: float = 100e-6
):
    try:
        res = engine.optimize_thruster(
            thruster_type=thruster_type,
            target=target,
            power_limit_w=power_limit_w,
            mass_flow_limit_kg_s=mass_flow_limit_kg_s
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
