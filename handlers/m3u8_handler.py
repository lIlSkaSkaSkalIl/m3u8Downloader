import os
from pyrogram import Client, filters
from pyrogram.types import Message
from utility.video_utils import download_m3u8_video
from utils.state import user_state

@Client.on_message(filters.command("m3u8") & filters.private)
async def step_1(client, message: Message):
    user_state[message.from_user.id] = "awaiting_m3u8"
    await message.reply_text("🎬 Kirim link `.m3u8` Anda:")

@Client.on_message(filters.text & filters.private)
async def step_2(client, message: Message):
    uid = message.from_user.id
    if user_state.get(uid) != "awaiting_m3u8":
        return  # Abaikan pesan teks jika bukan dalam state

    user_state.pop(uid, None)  # Hapus state untuk cegah duplikasi
    link = message.text.strip()

    if not link.startswith("http") or ".m3u8" not in link:
        return await message.reply("❌ Link tidak valid, pastikan itu file `.m3u8`.")

    msg = await message.reply("📥 Mendownload...")
    filename = f"{uid}_m3u8.mp4"
    success = await download_m3u8_video(link, filename, msg)

    if not success or not os.path.exists(filename):
        return await msg.edit("❌ Gagal mendownload video.")

    await msg.edit("✅ Selesai! Mengirim ke Telegram...")
    await client.send_video(message.chat.id, video=filename, supports_streaming=True)
    os.remove(filename)
