from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler  # Tambahkan ini

# Fungsi yang menangani perintah /start
async def start(_, message: Message):
    await message.reply_text("👋 Halo! Kirimkan link m3u8 dan saya akan unduh videonya untukmu.")

# Handler yang siap ditambahkan ke app
start_handler = MessageHandler(start, filters.command("start"))
