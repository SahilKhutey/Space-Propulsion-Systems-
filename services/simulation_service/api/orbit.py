from fastapi import APIRouter, HTTPException
from orbit_engine import OrbitEngine

router = APIRouter()
engine = OrbitEngine()


@router.get("/orbit")
async def get_orbit_points(altitude: float, num_points: int = 120):
    try:
        points = engine.generate_orbit_points(altitude, num_points)
        return {"points": points}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transfer")
async def get_transfer_points(start_alt: float, target_alt: float, num_points: int = 100):
    try:
        paths = engine.generate_hohmann_transfer_points(start_alt, target_alt, num_points)
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/plume")
async def get_plume_geometry(thrust_n: float, power_w: float):
    try:
        plume = engine.generate_plume_geometry(thrust_n, power_w)
        return plume
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
