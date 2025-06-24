import os
from aiogram import types
from aiogram.types import InputFile

async def upload_video(message: types.Message, output_path, filename, duration=None, thumb=None):
    try:
        video = InputFile(output_path)

        await message.answer_video(
            video=video,
            duration=duration if duration else None,
            thumbnail=thumb if thumb else None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode="Markdown"
        )

        # Hapus thumbnail jika ada
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.answer(f"❌ Gagal mengunggah: `{e}`", parse_mode="Markdown")
