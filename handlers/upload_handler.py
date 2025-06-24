import os

async def upload_video(client, message, output_path, filename, duration, thumb):
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration if duration else None,
            thumb=thumb if thumb else None,
            caption=f"✅ Selesai!\nNama file: `{filename}`"
        )

        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.reply_text(f"❌ Gagal mengunggah: `{e}`")
