import os
import time
import asyncio
import re
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.progress import make_progress_callback
from utils.video_meta import get_video_duration, get_thumbnail, get_video_info
from utils.status import update_status
from handlers.upload_handler import upload_video


# Fungsi escape untuk MarkdownV2
def escape_md(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(rf"([{re.escape(escape_chars)}])", r"\\\1", str(text))


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
                "🔎 *Preview Metadata:*\n"
                f"▫️ Resolusi: `{escape_md(info['width'])}x{escape_md(info['height'])}`\n"
                f"▫️ Durasi: `{escape_md(info['duration'])} detik`\n"
                f"▫️ Codec: `{escape_md(info['codec'])}`\n\n"
                "Ingin melanjutkan unduhan?"
            )

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Lanjut Unduh", callback_data=f"dl:{url}")],
                [InlineKeyboardButton("❌ Batal", callback_data="cancel")]
            ])

            await status_msg.edit_text(
                escape_md(caption),
                reply_markup=buttons,
                parse_mode="MarkdownV2"
            )
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
        await asyncio.sleep(1)
    except Exception as e:
        await status_msg.edit_text(
            f"❌ Gagal mengunduh:\n`{escape_md(str(e))}`",
            parse_mode="MarkdownV2"
        )
        return

    await update_status(client, status_msg, "🔧 Memproses video...")
    await update_status(client, status_msg, "⏱️ Mengambil durasi video...")
    duration = get_video_duration(output_path)

    await update_status(client, status_msg, "📷 Mengambil thumbnail video...")
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    thumb = get_thumbnail(output_path, thumb_path)

    await update_status(client, status_msg, "📤 Mengunggah ke Telegram...")
    await upload_video(client, message, status_msg, output_path, filename, flood_lock, duration, thumb)


# Handler pesan teks
async def m3u8_text_handler(client, message: Message):
    await handle_m3u8(client, message, previewed=False)


# Handler final untuk didaftarkan di main.py
m3u8_handler = MessageHandler(
    m3u8_text_handler,
    filters.text & ~filters.command("start")
            )
