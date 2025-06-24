import os
from pyrogram import Client
from pyrogram.types import CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN

from handlers.command_handler import start_handler
from handlers.download_handler import m3u8_handler, handle_m3u8

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Client("m3u8_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

app.add_handler(start_handler)
app.add_handler(m3u8_handler)

# 🔁 Callback untuk tombol interaktif
@app.on_callback_query()
async def callback_handler(client, callback: CallbackQuery):
    data = callback.data

    if data.startswith("dl:"):
        url = data[3:]
        await callback.answer()
        await handle_m3u8(client, callback.message, url=url, previewed=True)
    elif data == "cancel":
        await callback.message.edit_text("❌ Unduhan dibatalkan.")
        await callback.answer()

if __name__ == "__main__":
    print("🚀 Bot dimulai...")
    app.run()
