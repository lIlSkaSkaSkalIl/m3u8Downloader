import os
import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.progress import make_progress_callback
from utils.video_meta import get_video_duration, get_thumbnail
from handlers.upload_handler import upload_video

async def handle_m3u8(client, message: Message):
    print("[BOT] 🔗 Menerima link M3U8:", message.text)

    url = message.text.strip()
    status_msg = await message.reply_text("📥 Mengunduh...")

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
        await asyncio.sleep(1)
        print("[BOT] ✅ Unduhan selesai:", output_path)
    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunduh: `{e}`")
        print("[BOT] ❌ Gagal mengunduh:", e)
        return

    # Ambil metadata untuk keperluan upload
    duration = get_video_duration(output_path)
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    thumb = get_thumbnail(output_path, thumb_path)

    # Langsung lanjutkan ke upload (progres upload akan tampil otomatis)
    # ... (kode sebelumnya tetap)

    # Upload video (ubah argumen flood_lock jadi `_`)
    await upload_video(client, message, status_msg, output_path, filename, _, duration, thumb)
    
# MessageHandler utama (selain /start)
m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
)
