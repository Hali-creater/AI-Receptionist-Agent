import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://localhost:8501", wait_until="networkidle")

            chat_input = page.locator('[data-testid="stChatInputTextArea"]')
            await chat_input.wait_for(state="visible", timeout=15000)

            # Use fill and press for a more robust interaction
            test_message = "Hello, this is the final verification attempt."
            await chat_input.fill(test_message)
            await page.keyboard.press("Enter")

            # The most reliable check: wait for the submitted text to be visible in the DOM.
            await expect(page.locator(f"text='{test_message}'")).to_be_visible(timeout=20000)
            print("User message text confirmed visible on page.")

            # Now that we know the user message is there, the bubble class must also be there.
            # Let's also confirm the assistant has replied.
            await expect(page.locator(".assistant-bubble").last).to_be_visible(timeout=20000)
            print("Assistant reply confirmed visible on page.")

            await page.screenshot(path="screenshot.png")
            print("Screenshot captured successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            html_content = await page.content()
            with open("debug.html", "w") as f:
                f.write(html_content)
            print("Saved page HTML to debug.html for inspection.")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
