import os
from pyrogram import Client, filters
from pyrogram.types import Message
from utility.video_utils import download_m3u8_video
from utils.state import user_state

@Client.on_message(filters.command("m3u8") & filters.private)
async def m3u8_step_one(client, message: Message):
    user_state[message.from_user.id] = "awaiting_m3u8_link"
    await message.reply_text(
        "🎬 Silakan kirimkan link `.m3u8` Anda.\n\nContoh:\n`https://example.com/video/stream.m3u8`"
    )

@Client.on_message(filters.text & filters.private)
async def m3u8_step_two(client, message: Message):
    user_id = message.from_user.id

    if user_state.get(user_id) != "awaiting_m3u8_link":
        return

    m3u8_url = message.text.strip()

    # Hapus state duluan untuk cegah double execution
    user_state.pop(user_id, None)

    if not m3u8_url.startswith("http") or ".m3u8" not in m3u8_url:
        return await message.reply_text("❌ Link tidak valid. Pastikan itu adalah link `.m3u8`.")

    status_msg = await message.reply_text("📥 Mulai mengunduh video...")

    output_file = f"{user_id}_m3u8.mp4"
    success = await download_m3u8_video(m3u8_url, output_file, status_msg, client)

    if not success or not os.path.exists(output_file):
        return await status_msg.edit("❌ Gagal mendownload video.")

    await status_msg.edit("✅ Video berhasil diunduh!\n📤 Mengirim ke Telegram...")
    await client.send_video(
        chat_id=message.chat.id,
        video=output_file,
        caption="🎉 Selesai!",
        supports_streaming=True
    )

    os.remove(output_file)
