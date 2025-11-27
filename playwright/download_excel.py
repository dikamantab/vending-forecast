# NOTE: Customize selectors according to vendor dashboard.
import asyncio
import os
import re
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

# VENDOR_URL = os.getenv("VENDOR_URL")
# USERNAME = os.getenv("VENDOR_USER")
# PASSWORD = os.getenv("VENDOR_PASS")
# DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/shared/downloads")

# Save downloads to ./shared/downloads (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent
DOWNLOAD_FOLDER = PROJECT_ROOT / "shared" / "downloads"
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

async def run():
    os.makedirs("/shared/downloads", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # Step 1: Go to login
        await page.goto("https://cms.smartven.id/login")
        
        # Step 2: Fill login form (from Codegen)
        await page.get_by_role("textbox", name="*Email").fill("neltivia@gmail.com")
        await page.get_by_role("textbox", name="*Password").fill("propolitekniknegerimalang974")
        await page.get_by_role("button", name="Masuk").click()

        # Step 3: Close popup if exists (from Codegen)
        try:
            await page.get_by_role("button", name="Close this dialog").click()
        except Exception:
            print("No dialog to close.")
        
        # Step 4: Navigate to Vending Sales
        await page.get_by_role("menubar").locator("div").filter(has_text="Penjualan").click()
        await page.get_by_role("menuitem", name="Vending Sales", exact=True).click()
        await page.locator(".el-checkbox__inner").first.click()

        await page.wait_for_load_state('networkidle')
        
        # Step 5: Trigger download
        async with page.expect_download() as download_info:
            await page.locator("button").filter(has_text=re.compile(r"^Download$")).click()
        download = await download_info.value

        # Step 6: Save file
        # suggested_filename = download.suggested_filename
        # save_path = os.path.join("/shared/downloads", suggested_filename)
        # print("Resolved DOWNLOAD_FOLDER:", os.path.abspath("shared/downloads"))
        # await download.save_as(save_path)

        #  6. Save with a clean name (optional: rename)
        original_name = download.suggested_filename  # e.g., "vending-sales-26_11_2025, 16.46.19.xlsx"
        safe_name = "vending_sales_latest.xlsx"  # or keep original: safe_name = original_name
        save_path = DOWNLOAD_FOLDER / safe_name

        await download.save_as(save_path)
        print(f"✅ File saved to: {save_path.resolve()}")

        await browser.close()

        # Example: navigate to report page and click export
        # await page.click("a[href='/reports']")
        # await page.click("button#export")
        # download = await page.wait_for_event("download")
        # await download.save_as(os.path.join(DOWNLOAD_FOLDER, download.suggested_filename))
        # await browser.close()

if __name__ == "__main__":
    asyncio.run(run())