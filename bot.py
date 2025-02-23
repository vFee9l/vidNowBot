import os
from pyrogram import Client, filters
import yt_dlp

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("video_downloader_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("👋 Welcome! Send a video link to download.")

@app.on_message(filters.text)
def download_video(client, message):
    url = message.text
    message.reply_text("Downloading...")
    
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            file_path = ydl.extract_info(url, download=True)['url']
        
        message.reply_text("✅ Download complete! Uploading...")
        message.reply_video(file_path)
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")

app.run()
