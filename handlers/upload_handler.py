import os
import time
from pyrogram.errors import FloodWait
from utility.status_format import format_status
from utils.progress import make_progress_callback

async def upload_video(client, message, status_msg, output_path, filename, flood_lock, duration, thumb):
    upload_start = time.time()
    last_ul_update = [0]

    progress_callback = make_progress_callback(
        client=client,
        status_msg=status_msg,
        label="📤 Mengunggah",
        output_path=output_path,
        start_time=upload_start,
        flood_lock=flood_lock,
        last_update_ref=last_ul_update
    )

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration if duration else None,
            thumb=thumb if thumb else None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            progress=progress_callback
        )
        await status_msg.delete()

        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await status_msg.edit_text(f"❌ Gagal mengunggah: `{e}`")
