from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

async def handle_start(_, message: Message):
    await message.reply_text("👋 Halo! Kirimkan link m3u8 dan saya akan unduh videonya untukmu.")

# Handler siap dipasang di app
start_handler = MessageHandler(handle_start, filters.command("start"))
