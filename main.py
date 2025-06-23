from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Import hanya handler m3u8
from handlers import m3u8_handler

app = Client("m3u8-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    print("🚀 Bot m3u8 siap dijalankan!")
    app.run()
