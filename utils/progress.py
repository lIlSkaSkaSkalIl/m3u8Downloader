import time
from pyrogram.errors import FloodWait
from utility.status_format import format_status
from math import floor

def make_progress_callback(client, status_msg, label, output_path, start_time, last_update_ref):
    async def progress_callback(current, total):
        now = time.time()
        if now - last_update_ref[0] < 10:
            return
        last_update_ref[0] = now
        elapsed = floor(now - start_time)
        text = format_status(label, output_path, current, total, elapsed)[:4000]

        try:
            await client.edit_message_text(
                chat_id=status_msg.chat.id,
                message_id=status_msg.id,
                text=text
            )
            print(f"[PROGRESS] ✅ Status diperbarui ({label}): {current}/{total}")
        except FloodWait as e:
            print(f"[PROGRESS] 🚫 FloodWait {e.value}s")
        except Exception as e:
            print(f"[PROGRESS] ❌ Gagal update: {e}")
    return progress_callback
