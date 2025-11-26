# NOTE: Customize selectors according to vendor dashboard.
import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv
load_dotenv()

VENDOR_URL = os.getenv("VENDOR_URL")
USERNAME = os.getenv("VENDOR_USER")
PASSWORD = os.getenv("VENDOR_PASS")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/shared/downloads")

async def run():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await page.goto(VENDOR_URL)
        # TODO: replace selectors below with actual vendor selectors
        await page.fill("input[name='Email']", USERNAME)
        await page.fill("input[name='Password']", PASSWORD)
        await page.click("button[name='Masuk']")
        await page.wait_for_load_state('networkidle')
        # Example: navigate to report page and click export
        # await page.click("a[href='/reports']")
        # await page.click("button#export")
        # download = await page.wait_for_event("download")
        # await download.save_as(os.path.join(DOWNLOAD_FOLDER, download.suggested_filename))
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())