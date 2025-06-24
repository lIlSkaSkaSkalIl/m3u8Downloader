import os
import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.progress import make_progress_callback
from utils.video_meta import get_video_duration, get_thumbnail, get_video_info
from utils.status import update_status
from handlers.upload_handler import upload_video


# Fungsi utama penanganan M3U8
async def handle_m3u8(client, message: Message, url: str = None, previewed: bool = False):
    if url is None:
        url = message.text.strip()

    if not previewed:
        status_msg = await message.reply_text("🔎 Mengambil info video...")
        info = get_video_info(url)

        if not info:
            await status_msg.edit_text("❌ Tidak bisa mengambil info video. Langsung mulai unduhan...")
        else:
            caption = (
                "🔎 <b>Preview Metadata:</b>\n"
                f"▫️ Resolusi: <code>{info['width']}x{info['height']}</code>\n"
                f"▫️ Durasi: <code>{info['duration']} detik</code>\n"
                f"▫️ Codec: <code>{info['codec']}</code>\n\n"
                "Ingin melanjutkan unduhan?"
            )

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Lanjut Unduh", callback_data=f"dl:{url}")],
                [InlineKeyboardButton("❌ Batal", callback_data="cancel")]
            ])

            await status_msg.edit_text(caption, reply_markup=buttons, parse_mode="html")
            return

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
        await asyncio.sleep(1)  # Tunggu agar status edit sinkron
    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunduh: <code>{e}</code>", parse_mode="html")
        return

    await update_status(client, status_msg, "🔧 Memproses video...")
    await update_status(client, status_msg, "⏱️ Mengambil durasi video...")
    duration = get_video_duration(output_path)

    await update_status(client, status_msg, "📷 Mengambil thumbnail video...")
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    thumb = get_thumbnail(output_path, thumb_path)

    await update_status(client, status_msg, "📤 Mengunggah ke Telegram...")
    await upload_video(client, message, status_msg, output_path, filename, flood_lock, duration, thumb)


# Handler pesan teks biasa (selain /start)
async def m3u8_text_handler(client, message: Message):
    await handle_m3u8(client, message, previewed=False)


# Handler yang didaftarkan di main.py
m3u8_handler = MessageHandler(
    m3u8_text_handler,
    filters.text & ~filters.command("start")
    )
