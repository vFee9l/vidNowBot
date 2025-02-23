from pyrogram import Client, filters
import yt_dlp
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# 🔹 Handle /start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    welcome_text = """
👋 **Welcome to the Video Downloader Bot!** 📥

📌 **How to Use:**
1️⃣ Send a **YouTube, TikTok, Instagram, or Twitter** video link.  
2️⃣ The bot will **download** and send the video back to you. 🎥  

💡 **Commands:**
- `/start` → Show this welcome message.
- `/help` → Get instructions on how to use the bot.

🚀 **Enjoy downloading!**
    """
    message.reply_text(welcome_text)

# 🔹 Handle /help command
@app.on_message(filters.command("help"))
def help_command(client, message):
    help_text = """
🛠 **How to Use the Bot:**

1️⃣ **Send a video link** from:
   - **YouTube**
   - **TikTok**
   - **Instagram**
   - **Twitter (X)**

2️⃣ The bot will **download** and **send the video** back to you! 📩  

🚀 **Commands:**
- `/start` → Welcome message
- `/help` → Show this guide

✅ **Example:**
Just send a link like this:  
🔗 `https://www.youtube.com/watch?v=abc123`

Enjoy! 😊
    """
    message.reply_text(help_text)

# 🔹 Handle video links
@app.on_message(filters.private & filters.text)
def handle_message(client, message):
    url = message.text
    platforms = {
        "youtube.com": "YouTube",
        "youtu.be": "YouTube",
        "tiktok.com": "TikTok",
        "instagram.com": "Instagram",
        "twitter.com": "Twitter",
        "x.com": "Twitter"
    }
    platform = next((p for k, p in platforms.items() if k in url), None)

    if not platform:
        return message.reply_text("❌ Unsupported link. Please send a valid video link.")

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
