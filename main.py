import os
import time
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from utility.video_utils import download_m3u8_video
from utility.status_format import format_status

app = Client("m3u8_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.text)
async def handle_message(client, message):
    url = message.text.strip()

    if not url.endswith(".m3u8"):
        await message.reply("❗ Harap masukkan link .m3u8 yang valid.")
        return

    os.makedirs("downloads", exist_ok=True)
    output_path = f"downloads/{message.from_user.id}.mp4"
    status_msg = await message.reply_text("⏳ Mengunduh dimulai...")

    # ⬇️ PROSES DOWNLOAD
    success = await download_m3u8_video(url, output_path, status_msg, client)

    if not success:
        await client.send_message(
            chat_id=message.chat.id,
            text="❌ Unduhan gagal. Coba lagi dengan link yang valid."
        )
        return

    # ⬆️ PROSES UPLOAD DENGAN PROGRES
    upload_start_time = time.time()

    async def progress_callback(current, total):
        elapsed = time.time() - upload_start_time
        status_text = format_status("📤 Mengunggah", output_path, current, total, elapsed)
        status_text = status_text[:4000]  # Telegram limit
        try:
            await client.edit_message_text(
                chat_id=status_msg.chat.id,
                message_id=status_msg.id,
                text=status_text
            )
        except Exception as e:
            print(f"Gagal update status upload: {e}")

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=output_path,
            caption="✅ Unggahan selesai!",
            progress=progress_callback
        )
        await status_msg.delete()
    except Exception as e:
        await client.send_message(
            chat_id=message.chat.id,
            text=f"⚠️ Gagal mengirim file: {e}"
        )

app.run()
