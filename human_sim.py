import random
import asyncio
from playwright.async_api import Page, Locator

async def human_type(page: Page, selector: str, text: str, delay_range=(70, 160)):
    try:
        element: Locator = page.locator(selector).first
        await element.focus()
        
        for char in text:
            await element.press_sequentially(char, delay=random.randint(*delay_range))
            if random.random() < 0.12:
                await asyncio.sleep(random.uniform(0.4, 1.1))
        
        await asyncio.sleep(random.uniform(0.5, 1.3))
    except Exception as e:
        print(f"Typing error on {selector}: {e}")

async def human_click(page: Page, selector: str):
    try:
        element: Locator = page.locator(selector).first
        box = await element.bounding_box()
        
        if not box:
            print(f"Could not get bounding box for {selector}")
            await element.click(force=True)
            return
        
        center_x = box['x'] + box['width'] / 2
        center_y = box['y'] + box['height'] / 2
        
        # curved mouse path
        await page.mouse.move(
            center_x + random.uniform(-60, 60),
            center_y + random.uniform(-40, 40),
            steps=random.randint(18, 35)
        )
        await asyncio.sleep(random.uniform(0.18, 0.55))
        
        await page.mouse.move(center_x, center_y, steps=random.randint(12, 22))
        await asyncio.sleep(random.uniform(0.12, 0.38))
        
        await element.click(delay=random.randint(50, 110))
    except Exception as e:
        print(f"Click error on {selector}: {e}")
