from pyrogram import filters
from pyrogram.types import Message

start_handler = filters.command("start")

async def start(_, message: Message):
    await message.reply_text("👋 Halo! Kirimkan link m3u8 dan saya akan unduh videonya untukmu.")
