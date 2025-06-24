from aiogram import types
from aiogram.dispatcher import Dispatcher

# Fungsi untuk menangani perintah /start
async def start_command(message: types.Message):
    await message.reply("👋 Halo! Kirimkan link m3u8 dan saya akan unduh videonya untukmu.")

# Fungsi untuk registrasi handler
def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
