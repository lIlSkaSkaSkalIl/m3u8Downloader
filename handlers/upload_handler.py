import os
from aiogram import types
from aiogram.types import InputFile
from utils.video_meta import get_video_duration, get_thumbnail

def is_valid_thumbnail(path: str) -> bool:
    """Validasi thumbnail: ada, ukuran masuk akal, dan berekstensi .jpg"""
    return (
        path
        and os.path.exists(path)
        and os.path.getsize(path) > 10 * 1024  # minimal 10 KB
        and path.lower().endswith(".jpg")
    )

async def upload_video(message: types.Message, output_path, filename, duration=None, thumb=None):
    try:
        # 🎞️ Hitung durasi jika belum ada
        if duration is None:
            duration = get_video_duration(output_path)

        # 📸 Buat thumbnail jika belum ada
        if thumb is None:
            thumb_path = f"{output_path}.jpg"
            thumb = get_thumbnail(output_path, thumb_path)

        # ✅ Validasi thumbnail dan kirim log ke Telegram
        if not is_valid_thumbnail(thumb):
            await message.answer("⚠️ Thumbnail tidak valid atau gagal dibuat.")
            thumb = None
        else:
            await message.answer(f"🖼️ Thumbnail berhasil dibuat: `{os.path.basename(thumb)}`", parse_mode="Markdown")
            # Kirim thumbnail sebagai foto (untuk debug visual)
            await message.answer_photo(InputFile(thumb), caption="📷 Ini thumbnail-nya")

        await message.answer_video(
            video=InputFile(output_path),
            duration=duration,
            thumb=InputFile(thumb) if thumb else None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode="Markdown"
        )

        # 🧹 Bersihkan thumbnail setelah kirim
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.answer(f"❌ Gagal mengunggah: `{e}`", parse_mode="Markdown")
