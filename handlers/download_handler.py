import os
import uuid
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.video_utils import get_available_qualities, download_video
from handlers.upload_handler import upload_video

# Simpan URL sementara berdasarkan user
user_m3u8_links = {}

async def handle_m3u8_link(message: types.Message):
    url = message.text.strip()
    user_id = message.from_user.id

    # 🔍 Status pesan awal
    status_msg = await message.answer("🔍 Mengecek resolusi yang tersedia...")

    qualities = get_available_qualities(url)

    # 🚮 Hapus status pesan
    await status_msg.delete()

    if not qualities:
        # Jika tidak ditemukan resolusi, tetap gunakan URL asli
        await message.answer("⚠️ Tidak ditemukan resolusi untuk URL tersebut. Menggunakan URL asli.")
        user_m3u8_links[user_id] = url
        await process_video_download(message, url)
        return

    # Simpan url ke memori user
    user_m3u8_links[user_id] = url

    # Buat tombol untuk pilih resolusi
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(text=res, callback_data=f"res_{res}")
        for res in sorted(qualities.keys(), reverse=True)
    ]
    keyboard.add(*buttons)

    await message.answer("🎞 Pilih resolusi yang ingin kamu unduh:", reply_markup=keyboard)

async def handle_resolution_callback(callback_query: CallbackQuery):
    resolution = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    url = user_m3u8_links.get(user_id)

    if not url:
        await callback_query.message.answer("❌ Link tidak ditemukan.")
        return

    # ⏳ Status sementara
    status_msg = await callback_query.message.answer(f"📥 Mengunduh video dengan resolusi {resolution}...")

    # Path file sementara
    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("downloads", filename)

    video_path = download_video(url, resolution=resolution, output_path=output_path)

    # 🚮 Hapus status loading
    await status_msg.delete()

    if video_path:
        await upload_video(callback_query.message, output_path, filename)
        os.remove(video_path)
    else:
        await callback_query.message.answer("❌ Gagal mengunduh video.")

# 🪄 Fallback jika tidak ditemukan resolusi (langsung unduh default)
async def process_video_download(message: types.Message, url: str):
    status_msg = await message.answer("📥 Mengunduh video dari URL...")

    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("downloads", filename)

    video_path = download_video(url, output_path=output_path)
    await status_msg.delete()

    if video_path:
        await upload_video(message, output_path, filename)
        os.remove(video_path)
    else:
        await message.answer("❌ Gagal mengunduh video.")

def register_download(dp: Dispatcher):
    dp.register_message_handler(handle_m3u8_link, lambda msg: msg.text and msg.text.endswith(".m3u8"))
    dp.register_callback_query_handler(handle_resolution_callback, lambda c: c.data.startswith("res_"))
