import os
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from utility.video_utils import download_m3u8_video

# Inisialisasi bot
app = Client("m3u8_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Event ketika user mengirimkan pesan
@app.on_message(filters.private & filters.text)
async def handle_message(client, message):
    url = message.text.strip()

    # Validasi dasar link
    if not url.endswith(".m3u8"):
        await message.reply("❗ Harap masukkan link .m3u8 yang valid.")
        return

    # Siapkan jalur output dan pastikan folder ada
    os.makedirs("downloads", exist_ok=True)
    output_path = f"downloads/{message.from_user.id}.mp4"

    # Kirim status awal
    status_msg = await message.reply("⏳ Mengunduh dimulai...")

    # Jalankan unduhan
    success = await download_m3u8_video(url, output_path, status_msg, client)

    # Setelah selesai, kirim hasil atau error
    if success:
        try:
            await client.send_document(
                chat_id=message.chat.id,
                document=output_path,
                caption="✅ Unduhan selesai!"
            )
        except Exception as e:
            await client.send_message(
                chat_id=message.chat.id,
                text=f"⚠️ Gagal mengirim file: {e}"
            )
    else:
        await client.send_message(
            chat_id=message.chat.id,
            text="❌ Unduhan gagal. Pastikan link valid dan coba lagi."
        )

# Jalankan bot
app.run()
