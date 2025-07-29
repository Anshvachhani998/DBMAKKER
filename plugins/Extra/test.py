from pyrogram import Client, filters
from pyrogram.types import Message
from playwright.async_api import async_playwright
import re

# Custom function to sniff video link
async def sniff_vahaflix_video(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        )

        # OPTIONAL: Add cookies here if needed
        # await context.add_cookies([
        #     {"name": "_ga", "value": "xxx", "domain": "h5.vahaflix.com", "path": "/"},
        # ])

        page = await context.new_page()
        video_url = None

        async def handle_response(response):
            nonlocal video_url
            if (
                ("vod-qcloud.com" in response.url) and
                (".mp4" in response.url or ".m3u8" in response.url)
            ):
                video_url = response.url

        page.on("response", handle_response)

        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_timeout(8000)  # Let the video load
        except Exception as e:
            print(f"Error loading page: {e}")

        await browser.close()
        return video_url

# Pyrogram handler
@Client.on_message(filters.command("dl") & filters.private)
async def vahaflix_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Please provide a Vahaflix link.\nUsage: `/dl <link>`", quote=True)

    link = message.command[1]
    if not re.match(r"https?://", link):
        return await message.reply("⚠️ Invalid URL. Please provide a proper link.", quote=True)

    msg = await message.reply("⏳ Scraping video link from Vahaflix...", quote=True)
    video_url = await sniff_vahaflix_video(link)

    if video_url:
        await msg.edit(f"✅ Video URL Found:\n`{video_url}`")
    else:
        await msg.edit("❌ Unable to find MP4/M3U8 video URL.\nIt may be DRM protected or expired.")

