from fastapi import APIRouter
from .thrust import router as thrust_router
from .thermal import router as thermal_router
from .power import router as power_router
from .mission import router as mission_router
from .orbit import router as orbit_router
from .optimization import router as optimization_router

api_router = APIRouter()

api_router.include_router(thrust_router, prefix="/thrust", tags=["thrust"])
api_router.include_router(thermal_router, prefix="/thermal", tags=["thermal"])
api_router.include_router(power_router, prefix="/power", tags=["power"])
api_router.include_router(mission_router, prefix="/mission", tags=["mission"])
api_router.include_router(orbit_router, prefix="/orbit", tags=["orbit"])
api_router.include_router(optimization_router, prefix="/optimization", tags=["optimization"])
