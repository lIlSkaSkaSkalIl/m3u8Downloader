import os
from aiogram import types
from aiogram.types import InputFile
from utils.video_meta import get_video_duration, get_thumbnail  # ✅ import fungsi meta

async def upload_video(message: types.Message, output_path, filename, duration=None, thumb=None):
    try:
        # 🎞️ Hitung durasi jika tidak diberikan
        if duration is None:
            duration = get_video_duration(output_path)

        # 📸 Ambil thumbnail jika belum tersedia
        if thumb is None:
            thumb_path = f"{output_path}.jpg"
            thumb = get_thumbnail(output_path, thumb_path)

        video = InputFile(output_path)

        await message.answer_video(
            video=video,
            duration=duration,
            thumb=thumb if thumb else None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode="Markdown"
        )

        # Hapus thumbnail setelah upload (jika ada)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.answer(f"❌ Gagal mengunggah: `{e}`", parse_mode="Markdown")
