from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utility.video_utils import get_available_qualities, download_video
import os
import uuid

# Simpan URL sementara berdasarkan user
user_m3u8_links = {}

async def handle_m3u8_link(message: types.Message):
    url = message.text.strip()
    user_id = message.from_user.id

    await message.answer("🔍 Mengecek resolusi yang tersedia...")

    qualities = get_available_qualities(url)
    if not qualities:
        await message.answer("❌ Tidak ditemukan resolusi untuk URL tersebut.")
        return

    # Simpan url ke memory user
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

    await callback_query.message.answer(f"📥 Mengunduh video dengan resolusi {resolution}...")

    # Buat path file unik
    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("downloads", filename)

    video_path = download_video(url, resolution=resolution, output_path=output_path)
    if video_path:
        await callback_query.message.answer_document(open(video_path, 'rb'))
        os.remove(video_path)  # hapus setelah kirim
    else:
        await callback_query.message.answer("❌ Gagal mengunduh video.")

def register_download(dp: Dispatcher):
    dp.register_message_handler(handle_m3u8_link, lambda msg: msg.text and msg.text.endswith(".m3u8"))
    dp.register_callback_query_handler(handle_resolution_callback, lambda c: c.data.startswith("res_"))
