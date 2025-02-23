import os
from pyrogram import Client, filters
import yt_dlp

# Get API credentials from environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Initialize bot
app = Client("video_downloader_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to download video
def download_video(url):
    options = {'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s', 'quiet': True}
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.on_message(filters.private & filters.text)
def handle_message(client, message):
    url = message.text
    platforms = {"youtube.com": "YouTube", "tiktok.com": "TikTok", "instagram.com": "Instagram", "twitter.com": "Twitter"}
    platform = next((p for k, p in platforms.items() if k in url), None)

    if not platform:
        return message.reply_text("❌ Unsupported link.")

    message.reply_text(f"🔄 Downloading from {platform}...")

    try:
        file_path = download_video(url)
        message.reply_text("✅ Download complete! Uploading...")
        message.reply_video(file_path)
        os.remove(file_path)
    except Exception as e:
        message.reply_text(f"❌ Download failed: {e}")

# Run bot
app.run()
