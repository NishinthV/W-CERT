"""Capture wcert_poster.html as a high-res A2 PNG using Playwright with embedded images."""
from playwright.sync_api import sync_playwright
import base64
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_DIR = r"C:\Users\nishi\.gemini\antigravity\brain\dafb135a-b8d8-4926-96b3-324ce76c1b9a"
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "POSTER.png")

# Read images and convert to base64
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

brain_b64 = img_to_b64(os.path.join(BRAIN_DIR, "poster_ai_brain_1777832266141.png"))
shield_b64 = img_to_b64(os.path.join(BRAIN_DIR, "poster_centerpiece_1777832249817.png"))

# Read HTML and replace file:// URLs with base64
html_path = os.path.join(SCRIPT_DIR, "wcert_poster.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace(
    "file:///C:/Users/nishi/.gemini/antigravity/brain/dafb135a-b8d8-4926-96b3-324ce76c1b9a/poster_ai_brain_1777832266141.png",
    f"data:image/png;base64,{brain_b64}"
)
html = html.replace(
    "file:///C:/Users/nishi/.gemini/antigravity/brain/dafb135a-b8d8-4926-96b3-324ce76c1b9a/poster_centerpiece_1777832249817.png",
    f"data:image/png;base64,{shield_b64}"
)

# A2 at 150 DPI = 2480 x 3508
WIDTH = 2480
HEIGHT = 3508

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
    page.set_content(html, wait_until="networkidle")
    page.wait_for_timeout(5000)
    page.screenshot(path=OUTPUT_PATH, full_page=False, type="png")
    browser.close()
    print(f"Saved A2 poster to: {OUTPUT_PATH}")
    print(f"Dimensions: {WIDTH}x{HEIGHT} (A2 at 150 DPI)")
    print(f"Size: {os.path.getsize(OUTPUT_PATH)} bytes")
