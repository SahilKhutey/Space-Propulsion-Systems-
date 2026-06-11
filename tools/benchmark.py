"""
PropSim Performance Benchmark — for the dashboards.
"""
import time
import statistics
import httpx
import asyncio

API = "http://localhost:8000"


async def bench_endpoint(client, method, url, **kwargs):
    times = []
    for _ in range(10):
        t0 = time.time()
        if method == "GET":
            r = await client.get(url, **kwargs)
        else:
            r = await client.post(url, **kwargs)
        elapsed = (time.time() - t0) * 1000
        assert r.status_code == 200
        times.append(elapsed)
    return {
        "endpoint": url.replace(API, ""),
        "mean_ms": statistics.mean(times),
        "p50_ms": statistics.median(times),
        "p95_ms": statistics.quantiles(times, n=20)[18],
        "p99_ms": statistics.quantiles(times, n=100)[98],
    }


async def main():
    async with httpx.AsyncClient(timeout=30) as c:
        endpoints = [
            ("GET",  f"{API}/health", {}),
            ("POST", f"{API}/api/thrust/compute", {"json": {"thruster_type": "hall", "power_w": 5000.0, "efficiency": 0.6, "isp_s": 2000.0}}),
            ("POST", f"{API}/api/optimization/study", {"json": {"payload_mass_kg": 1000.0, "delta_v_ms": 10000.0, "mission_duration_years": 5.0, "candidates": ["hall", "ion"]}}),
        ]
        results = []
        for m, u, kw in endpoints:
            try:
                r = await bench_endpoint(c, m, u, **kw)
                results.append(r)
            except Exception as e:
                results.append({"endpoint": u, "error": str(e)})

        print(f"\n{'Endpoint':<40} {'mean':>8} {'p50':>8} {'p95':>8} {'p99':>8}")
        print("-" * 76)
        for r in results:
            if "error" in r:
                print(f"{r['endpoint']:<40} ERROR: {r['error']}")
            else:
                print(f"{r['endpoint']:<40} {r['mean_ms']:>7.1f}ms {r['p50_ms']:>7.1f}ms "
                      f"{r['p95_ms']:>7.1f}ms {r['p99_ms']:>7.1f}ms")


if __name__ == "__main__":
    asyncio.run(main())
