from aiogram import Bot, Dispatcher, executor
from config import API_TOKEN
from handlers.command_handler import register_commands
from handlers.download_handler import register_download
from handlers.upload_handler import register_upload

# Inisialisasi bot dan dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Registrasi handler
register_commands(dp)
register_download(dp)
register_upload(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
