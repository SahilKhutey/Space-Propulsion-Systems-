import os
import time
from playwright.sync_api import sync_playwright

def capture():
    # Ensure screenshot directory exists
    screenshot_dir = r"c:\Users\User\Documents\Space Propulsion\propulsion-simulation-platform\assets\screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
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

    with sync_playwright() as p:
        # Launch browser with a high resolution viewport
        browser = p.chromium.launch(headless=True)
        # Use dark mode if preferred by the UI theme
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            color_scheme="dark"
        )
        page = context.new_page()

        for name, url in routes.items():
            print(f"Navigating to {name} dashboard: {url}")
            try:
                page.goto(url, wait_until="networkidle", timeout=10000)
            except Exception as e:
                print(f"Timeout or error loading {url}: {e}. Proceeding anyway...")
                try:
                    page.goto(url)
                except Exception:
                    pass
            
            # Wait for 3 seconds to let animation/Recharts/Cesium/three.js render completely
            time.sleep(3.0)
            
            output_path = os.path.join(screenshot_dir, f"{name}_dashboard.png")
            page.screenshot(path=output_path, full_page=False)
            print(f"Captured screenshot: {output_path}")
            
        browser.close()

if __name__ == "__main__":
    capture()
