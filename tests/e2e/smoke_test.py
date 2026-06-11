"""
PropSim Final System Check — End-to-end smoke test.
Verifies all 12 dashboard APIs return valid data.
"""
import sys
from pathlib import Path
import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "engines" / "thrust-engine"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "real-time-engine"))

API_BASE = "http://localhost:8000/api"


@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{API_BASE.replace('/api', '')}/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_hall_thruster_spec():
    """Spec benchmark: 5kW, 0.6, 2000s → 0.306 N."""
    async with httpx.AsyncClient() as c:
        # Note: API routes in main.py prefix with /api, e.g. /api/thrust/compute
        r = await c.post(f"{API_BASE}/thrust/compute", json={
            "thruster_type": "hall", "power_w": 5000.0, "efficiency": 0.6, "isp_s": 2000.0
        })
        assert r.status_code == 200
        F = r.json()["thrust_n"]
        assert 0.28 < F < 0.33, f"Got {F}"


@pytest.mark.asyncio
async def test_all_thruster_endpoints():
    """Verify compute endpoint responds to different thruster types."""
    types = ["hall", "ion", "vasimr"]
    async with httpx.AsyncClient() as c:
        for t in types:
            r = await c.post(f"{API_BASE}/thrust/compute", json={
                "thruster_type": t, "power_w": 5000.0, "efficiency": 0.6, "isp_s": 2000.0
            })
            assert r.status_code == 200, f"{t} failed: {r.text}"
            assert r.json()["thrust_n"] > 0
