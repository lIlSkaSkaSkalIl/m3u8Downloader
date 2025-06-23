import os
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler  # Tambahkan ini

from utility.video_utils import download_m3u8
from utils.progress import make_progress_callback
from utils.video_meta import get_video_duration, get_thumbnail
from handlers.upload_handler import upload_video

# Fungsi handler utama
async def handle_m3u8(client, message: Message):
    url = message.text.strip()
    status_msg = await message.reply_text("🔍 Memproses link...")

    filename = f"{int(time.time())}.mp4"
    output_path = os.path.join("downloads", filename)

    start_time = time.time()
    last_dl_update = [0]
    flood_lock = [False]

    progress_callback = make_progress_callback(
        client=client,
        status_msg=status_msg,
        label="📥 Mengunduh",
        output_path=output_path,
        start_time=start_time,
        flood_lock=flood_lock,
        last_update_ref=last_dl_update
    )

    try:
        await download_m3u8(url, output_path, progress_callback)
    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunduh: `{e}`")
        return

    await status_msg.edit_text("🔧 Memproses video...")

    await status_msg.edit_text("⏱️ Mengambil durasi video...")
    duration = get_video_duration(output_path)

    await status_msg.edit_text("📷 Mengambil thumbnail video...")
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    thumb = get_thumbnail(output_path, thumb_path)

    await status_msg.edit_text("📤 Mengunggah ke Telegram...")
    await upload_video(client, message, status_msg, output_path, filename, flood_lock, duration, thumb)

# Ini yang harus dipanggil di main.py
m3u8_handler = MessageHandler(handle_m3u8, filters.text & ~filters.command("start"))
