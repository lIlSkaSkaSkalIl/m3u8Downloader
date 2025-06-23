import os
import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message

from utility.video_utils import download_m3u8
from utils.progress import make_progress_callback
from utils.video_meta import get_video_duration, get_thumbnail
from utils.status import update_status
from handlers.upload_handler import upload_video

m3u8_handler = filters.text & ~filters.command("start")

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
        flood_lock[0] = True
        await asyncio.sleep(1)  # Biarkan Telegram menyelesaikan update terakhir
    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunduh: `{e}`")
        return

    # ⏳ Transisi status secara dinamis
    await update_status(client, status_msg, "🔧 Memproses video...")
    await update_status(client, status_msg, "⏱️ Mengambil durasi video...")
    duration = get_video_duration(output_path)

    await update_status(client, status_msg, "📷 Mengambil thumbnail video...")
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    thumb = get_thumbnail(output_path, thumb_path)

    await update_status(client, status_msg, "📤 Mengunggah ke Telegram...")

    await upload_video(client, message, status_msg, output_path, filename, flood_lock, duration, thumb)
