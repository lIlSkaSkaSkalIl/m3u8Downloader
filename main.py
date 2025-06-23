import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from config import API_ID, API_HASH, BOT_TOKEN
from utility.video_utils import download_m3u8
from utility.status_format import format_status

app = Client("m3u8_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("👋 Halo! Kirimkan link m3u8 dan saya akan unduh videonya untukmu.")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_message(client: Client, message: Message):
    url = message.text.strip()
    status_msg = await message.reply_text("🔍 Memproses link...")

    filename = f"{int(time.time())}.mp4"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    start_time = time.time()
    last_dl_update = [0]
    flood_lock = [False]

    async def progress_callback(current, total):
        now = time.time()
        if now - last_dl_update[0] < 30 or flood_lock[0]:
            return
        last_dl_update[0] = now
        elapsed = now - start_time
        text = format_status("📥 Mengunduh", output_path, current, total, elapsed)[:4000]

        try:
            await client.edit_message_text(
                chat_id=status_msg.chat.id,
                message_id=status_msg.id,
                text=text
            )
        except FloodWait as e:
            print(f"[DL] 🚫 FloodWait {e.value}s, menonaktifkan update.")
            flood_lock[0] = True
        except Exception as e:
            print(f"[DL] ❌ Gagal update: {e}")

    try:
        await download_m3u8(url, output_path, progress_callback)
    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunduh: `{e}`")
        return

    await status_msg.edit_text("📤 Mengunggah ke Telegram...")

    upload_start = time.time()
    last_ul_update = [0]

    async def upload_progress(current, total):
        now = time.time()
        if now - last_ul_update[0] < 30 or flood_lock[0]:
            return
        last_ul_update[0] = now
        elapsed = now - upload_start
        text = format_status("📤 Mengunggah", output_path, current, total, elapsed)[:4000]

        try:
            await client.edit_message_text(
                chat_id=status_msg.chat.id,
                message_id=status_msg.id,
                text=text
            )
        except FloodWait as e:
            print(f"[UL] 🚫 FloodWait {e.value}s, menonaktifkan update.")
            flood_lock[0] = True
        except Exception as e:
            print(f"[UL] ❌ Gagal update: {e}")

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            progress=upload_progress
        )
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunggah: `{e}`")
if __name__ == "__main__":
    print("🚀 Bot dimulai...")
    app.run()
