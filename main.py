import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import subprocess
import time

# Konfigurasi API Telegram
API_ID = int(os.getenv("API_ID") or input("Masukkan API_ID: "))
API_HASH = os.getenv("API_HASH") or input("Masukkan API_HASH: ")
BOT_TOKEN = os.getenv("BOT_TOKEN") or input("Masukkan BOT_TOKEN: ")

app = Client("m3u8_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# State memory user
user_state = {}

# Fungsi untuk status progres
def format_status(phase: str, filename: str, done: int, total: int, elapsed: float) -> str:
    speed = done / elapsed if elapsed > 0 else 0
    return (
        f"**{phase}...**\n"
        f"📄 File: `{filename}`\n"
        f"🚀 Kecepatan: `{speed / 1024:.2f} KB/s`\n"
        f"⏱️ Waktu: `{int(elapsed)}s`"
    )

# Fungsi download m3u8 + remux
async def download_m3u8_video(url, output, status_msg):
    try:
        start = time.time()
        temp_file = "temp_raw.mp4"

        # Unduh m3u8
        cmd = [
            "ffmpeg", "-i", url,
            "-c", "copy", "-bsf:a", "aac_adtstoasc",
            "-y", temp_file
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while process.poll() is None:
            elapsed = time.time() - start
            try:
                await status_msg.edit(format_status("📥 Mengunduh", output, 0, 0, elapsed))
            except:
                pass
            await asyncio.sleep(5)

        if process.returncode != 0 or not os.path.exists(temp_file):
            return False

        # Remux ulang agar metadata & thumbnail terbaca Telegram
        remux_cmd = [
            "ffmpeg", "-i", temp_file,
            "-c", "copy", "-map", "0", "-movflags", "+faststart",
            "-y", output
        ]
        subprocess.run(remux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(temp_file)

        return os.path.exists(output)

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

# Command /m3u8
@app.on_message(filters.command("m3u8") & filters.private)
async def step_1(client, message: Message):
    user_state[message.from_user.id] = "awaiting_m3u8"
    await message.reply_text("🎬 Kirimkan link `.m3u8` Anda untuk didownload:")

# Proses teks masuk
@app.on_message(filters.text & filters.private)
async def step_2(client, message: Message):
    uid = message.from_user.id
    if user_state.get(uid) != "awaiting_m3u8":
        return

    user_state.pop(uid, None)  # Hapus state agar tidak dobel
    link = message.text.strip()

    if not link.startswith("http") or ".m3u8" not in link:
        return await message.reply("❌ Link tidak valid, pastikan itu file `.m3u8`.")

    msg = await message.reply("📥 Mengunduh video...")
    filename = f"{uid}_video.mp4"

    success = await download_m3u8_video(link, filename, msg)

    if not success or not os.path.exists(filename):
        return await msg.edit("❌ Gagal mengunduh video.")

    await msg.edit("✅ Selesai! Mengirim video ke Telegram...")
    await client.send_video(message.chat.id, video=filename, caption="🎉 Selesai!", supports_streaming=True)
    os.remove(filename)

if __name__ == "__main__":
    print("✅ Bot m3u8-only siap dijalankan!")
    app.run()
