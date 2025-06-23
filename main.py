from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

from handlers import m3u8_handler  # Pastikan ini terpasang

app = Client("m3u8-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    print("🚀 Bot m3u8-only siap dijalankan!")
    app.run()
