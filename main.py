from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

from utils.state import user_state
from utility.video_utils import download_m3u8_video
from utility.status_format import format_status
import os, time

app = Client("m3u8-only-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("m3u8") & filters.private)
async def m3u8_step_one(client, message: Message):
    await message.reply_text(
        "🎬 Silakan kirimkan link `.m3u8` Anda.\n\nContoh:\n`https://example.com/video/stream.m3u8`"
    )
    user_state[message.from_user.id] = "awaiting_m3u8_link"

@app.on_message(filters.text & filters.private)
async def fallback_handler(client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_state.get(user_id) == "awaiting_m3u8_link":
        if not text.startswith("http") or ".m3u8" not in text:
            await message.reply_text("❌ Link tidak valid. Pastikan itu adalah link `.m3u8`.")
            return

        await message.reply_text("⏳ Sedang mendownload video...")
        output_file = f"{user_id}_m3u8.mp4"
        status_msg = await message.reply_text("📥 Mulai mengunduh...")

        success = await download_m3u8_video(text, output_file, status_msg)
        if not success or not os.path.exists(output_file):
            await status_msg.edit("❌ Gagal mendownload video.")
        else:
            await status_msg.edit("✅ Berhasil! Mengunggah ke Telegram...")

            # Setup upload progress tracking
            upload_progress.start_time = time.time()
            upload_progress.last_update = 0
            upload_progress.filename = output_file
            upload_progress.status_msg = status_msg

            await client.send_video(
                chat_id=message.chat.id,
                video=output_file,
                caption="✅ Video berhasil diunggah 🎬",
                supports_streaming=True,
                progress=upload_progress
            )
            os.remove(output_file)

        user_state.pop(user_id, None)

# Fungsi progress upload
async def upload_progress(current, total):
    now = time.time()
    elapsed = now - upload_progress.start_time
    if now - upload_progress.last_update > 5 or current == total:
        try:
            await upload_progress.status_msg.edit(
                format_status("📤 Mengunggah", upload_progress.filename, current, total, elapsed)
            )
            upload_progress.last_update = now
        except:
            pass

if __name__ == "__main__":
    print("✅ Bot siap berjalan!")
    app.run()
