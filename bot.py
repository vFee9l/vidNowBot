from pyrogram import Client, filters
import yt_dlp
import os

# Replace with your API credentials
api_id = 20534294  # Your API ID
api_hash = "8099087ad1f0ee68c3f391a04032a2b0"  # Your API Hash
bot_token = "7841644976:AAEY6Tqc4meRKSnbsGwbkKRgd6Y8z5yFFEA"  # Your Bot Token

# Initialize the bot
app = Client("video_downloader_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to download video
def download_video(url):
    output_path = "downloads/%(title)s.%(ext)s"
    options = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# Handle messages
@app.on_message(filters.private & filters.text)
def handle_message(client, message):
    url = message.text

    # Identify platform
    if "youtube.com" in url or "youtu.be" in url:
        platform = "YouTube"
    elif "tiktok.com" in url:
        platform = "TikTok"
    elif "instagram.com" in url:
        platform = "Instagram"
    elif "twitter.com" in url or "x.com" in url:
        platform = "Twitter"
    else:
        message.reply_text("❌ الرابط لا يدعم")
        return

    message.reply_text(f"🔄 جاري تنزيل الفيديو {platform}...")

    try:
        file_path = download_video(url)
        message.reply_text("✅ تم التنزيل!...")

        # Send the video
        message.reply_video(file_path)

        # Delete the video after sending
        os.remove(file_path)
    except Exception as e:
        message.reply_text(f"❌ في مشكلة \nError: {str(e)}")

# Run the bot
app.run()
