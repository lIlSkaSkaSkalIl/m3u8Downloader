import os
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram.errors import FloodWait

from utility.video_utils import download_m3u8
from utility.status_format import format_status
from handlers.upload_handler import upload_video
from utils.progress import make_progress_callback

DOWNLOAD_DIR = "downloads"

async def handle_m3u8(client, message: Message):
    url = message.text.strip()
    status_msg = await message.reply_text("🔍 Memproses link...")

    filename = f"{int(time.time())}.mp4"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    start_time = time.time()
    flood_lock = [False]
    last_dl_update = [0]

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

    await status_msg.edit_text("📤 Mengunggah ke Telegram...")
    await upload_video(client, message, status_msg, output_path, filename, flood_lock)

# Handler siap dipasang di app
m3u8_handler = MessageHandler(handle_m3u8, filters.text & ~filters.command("start"))
