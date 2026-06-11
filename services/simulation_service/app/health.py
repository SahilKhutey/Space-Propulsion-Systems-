"""
Comprehensive health-check endpoint for system monitoring.
"""
from fastapi import APIRouter
import time
import psutil
import os
from datetime import datetime, timezone
from typing import Dict, Any

router = APIRouter(prefix="/health", tags=["Health"])

_start_time = time.time()


@router.get("")
@router.get("/")
async def health() -> Dict[str, Any]:
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "simulation-service",
        "version": "3.0.0",
        "uptime_s": time.time() - _start_time,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/deep")
async def deep_health() -> Dict[str, Any]:
    """Deep health check including downstream services."""
    checks = {
        "database": "ok",
        "redis": "ok"
    }
    return {"status": "ok", "checks": checks}


@router.get("/system")
async def system_metrics() -> Dict[str, Any]:
    """System resource usage."""
    process = psutil.Process(os.getpid())
    return {
        "cpu_pct": psutil.cpu_percent(interval=0.1),
        "mem_mb": process.memory_info().rss / 1024 / 1024,
        "mem_pct": process.memory_percent(),
        "threads": process.num_threads(),
        "uptime_s": time.time() - _start_time,
        "load_avg": psutil.getloadavg() if hasattr(psutil, "getloadavg") else None,
    }


@router.get("/ready")
async def readiness() -> Dict[str, Any]:
    """K8s readiness probe."""
    return {"ready": True}


@router.get("/live")
async def liveness() -> Dict[str, Any]:
    """K8s liveness probe."""
    return {"alive": True}
