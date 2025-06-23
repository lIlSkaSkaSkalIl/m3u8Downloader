from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

from utils.state import user_state
from utility.video_utils import download_m3u8_video, extract_metadata
import os

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

        await message.reply_chat_action("upload_video")
        status_msg = await message.reply_text("⏳ Memulai download...")
        output_file = f"{user_id}_m3u8.mp4"

        success = await download_m3u8_video(text, output_file, status_msg)
        if not success or not os.path.exists(output_file):
            await status_msg.edit("❌ Gagal mendownload video.")
        else:
            metadata = extract_metadata(output_file)
            duration = metadata.get("duration") if metadata else 0
            width = metadata.get("width") if metadata else None
            height = metadata.get("height") if metadata else None

            await status_msg.edit("✅ Berhasil! Mengirim ke Telegram...")
            await client.send_video(
                chat_id=message.chat.id,
                video=output_file,
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                caption="🎉 Video berhasil dikirim!",
            )
            os.remove(output_file)

        # Hapus status & jejak
        await status_msg.delete()
        user_state.pop(user_id, None)

if __name__ == "__main__":
    print("✅ Bot siap berjalan!")
    app.run()
