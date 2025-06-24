import os
from aiogram import types
from aiogram.types import InputFile
from utils.video_meta import get_video_duration, get_thumbnail

def is_valid_thumbnail(path: str) -> bool:
    """Validasi thumbnail: ada, ukuran masuk akal, dan berekstensi .jpg"""
    return (
        path
        and os.path.exists(path)
        and os.path.getsize(path) > 5 * 1024  # minimal 5 KB
        and path.lower().endswith(".jpg")
    )

async def upload_video(message: types.Message, output_path, filename, duration=None, thumb=None):
    try:
        # 🎞️ Hitung durasi jika belum diberikan
        if duration is None:
            duration = get_video_duration(output_path)

        # 📸 Buat thumbnail jika belum tersedia
        if thumb is None:
            thumb_path = f"{output_path}.jpg"
            thumb = get_thumbnail(output_path, thumb_path)

        # 🧪 Validasi & debug thumbnail (log internal)
        if thumb and is_valid_thumbnail(thumb):
            print(f"🖼️ Thumbnail valid → {thumb} ({os.path.getsize(thumb) // 1024} KB)")
        else:
            print("⚠️ Thumbnail tidak valid atau terlalu kecil.")
            thumb = None  # Jangan dikirim

        # 🚀 Kirim video ke user
        await message.answer_video(
            video=InputFile(output_path),
            duration=duration,
            thumb=InputFile(thumb) if thumb else None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode="Markdown"
        )

        # 🧹 Hapus thumbnail jika ada
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.answer(f"❌ Gagal mengunggah: `{e}`", parse_mode="Markdown")
