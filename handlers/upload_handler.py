import os
from aiogram import types
from aiogram.types import InputFile
from utils.video_meta import get_video_duration, get_thumbnail

def is_valid_thumbnail(path: str) -> bool:
    """Validasi thumbnail: ada, ukuran masuk akal (>2KB), dan berekstensi .jpg"""
    return (
        path
        and os.path.exists(path)
        and os.path.getsize(path) > 2 * 1024  # lebih longgar: minimal 2 KB
        and path.lower().endswith(".jpg")
    )

async def upload_video(message: types.Message, output_path, filename, duration=None, thumb=None):
    try:
        # 🎞️ Hitung durasi jika tidak tersedia
        if duration is None:
            duration = get_video_duration(output_path)

        # 📸 Buat thumbnail jika belum disediakan
        if thumb is None:
            thumb_path = f"{output_path}.jpg"
            thumb = get_thumbnail(output_path, thumb_path)

        # 🔍 Debug thumbnail di Telegram
        if os.path.exists(thumb):
            size = os.path.getsize(thumb)
            await message.answer(
                f"🧪 Debug Thumbnail:\nPath: `{thumb}`\nUkuran: `{size / 1024:.1f} KB`",
                parse_mode="Markdown"
            )
        else:
            await message.answer("❌ File thumbnail tidak ditemukan saat dicek ulang.")

        # ✅ Validasi thumbnail
        if not is_valid_thumbnail(thumb):
            await message.answer("⚠️ Thumbnail tidak valid atau gagal dibuat.")
            thumb = None
        else:
            await message.answer(
                f"🖼️ Thumbnail valid: `{os.path.basename(thumb)}`",
                parse_mode="Markdown"
            )
            await message.answer_photo(InputFile(thumb), caption="📷 Ini thumbnail-nya")

        # 🚀 Upload video
        try:
            await message.answer_video(
                video=InputFile(output_path),
                duration=duration,
                thumb=InputFile(thumb) if thumb else None,
                caption=f"✅ Selesai!\nNama file: `{filename}`",
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer(f"⚠️ Video berhasil, tapi thumbnail gagal: `{e}`", parse_mode="Markdown")
            # Fallback tanpa thumbnail
            await message.answer_video(
                video=InputFile(output_path),
                duration=duration,
                caption=f"✅ Selesai tanpa thumbnail.\nNama file: `{filename}`",
                parse_mode="Markdown"
            )

        # 🧹 Bersihkan thumbnail jika ada
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.answer(f"❌ Gagal mengunggah: `{e}`", parse_mode="Markdown")
