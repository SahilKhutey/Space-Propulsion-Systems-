import os
import time
import subprocess
import sys
from playwright.sync_api import sync_playwright

MONOREPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_and_capture():
    screenshot_dir = os.path.join(MONOREPO_ROOT, "assets", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    print("1. Starting backend services...")
    # Start the backend simulation_service FastAPI app
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "services.simulation_service.app.main"],
        cwd=MONOREPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("2. Starting frontend dev server...")
    # Start the Vite React app
    frontend_proc = subprocess.Popen(
        "npm run dev",
        shell=True,
        cwd=os.path.join(MONOREPO_ROOT, "apps", "web"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Give them 8 seconds to fully start up and bind ports
    print("Waiting 8 seconds for services to initialize...")
    time.sleep(8.0)

    routes = {
        "01_home": "http://localhost:5173/#/",
        "02_mission": "http://localhost:5173/#/mission",
        "03_propulsion": "http://localhost:5173/#/propulsion",
        "04_thermal": "http://localhost:5173/#/thermal",
        "05_power": "http://localhost:5173/#/power",
        "06_orbit": "http://localhost:5173/#/orbit",
        "07_realtime": "http://localhost:5173/#/realtime",
        "08_digitaltwin": "http://localhost:5173/#/digitaltwin",
        "09_ai": "http://localhost:5173/#/ai",
        "10_sim": "http://localhost:5173/#/sim",
        "11_reports": "http://localhost:5173/#/reports",
        "12_settings": "http://localhost:5173/#/settings"
    }

    try:
        with sync_playwright() as p:
            print("Launching chromium...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1600, "height": 1000},
                color_scheme="dark"
            )
            page = context.new_page()

            for name, url in routes.items():
                print(f"Navigating to {name} dashboard: {url}")
                try:
                    page.goto(url, wait_until="networkidle", timeout=12000)
                except Exception as e:
                    print(f"Timeout or error loading {url}: {e}. Retrying simple load...")
                    try:
                        page.goto(url, timeout=10000)
                    except Exception:
                        pass
                
                # Wait for graphs and animations to render
                time.sleep(4.0)
                
                output_path = os.path.join(screenshot_dir, f"{name}_dashboard.png")
                page.screenshot(path=output_path, full_page=False)
                print(f"Captured screenshot: {output_path}")

            browser.close()
    finally:
        print("Stopping servers...")
        try:
            backend_proc.terminate()
            backend_proc.wait(timeout=2)
        except Exception:
            pass
        
        try:
            # For Vite shell process on Windows, we need to kill task tree
            subprocess.run(f"taskkill /F /T /PID {frontend_proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        
        print("Done!")

if __name__ == "__main__":
    run_and_capture()
