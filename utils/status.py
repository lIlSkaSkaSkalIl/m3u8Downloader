import asyncio
from pyrogram.errors import FloodWait

async def update_status(client, status_msg, text, delay: float = 0.5):
    """
    Update status pesan secara aman dan fleksibel.

    Args:
        client: Client Pyrogram
        status_msg: Objek pesan status (Message)
        text: Teks status yang ingin ditampilkan
        delay: Delay opsional sebelum update (default: 0.5 detik)
    """
    try:
        await asyncio.sleep(delay)
        await client.edit_message_text(
            chat_id=status_msg.chat.id,
            message_id=status_msg.id,
            text=text
        )
    except FloodWait as e:
        print(f"[STATUS] 🚫 FloodWait {e.value}s saat update status.")
        await asyncio.sleep(e.value)
    except Exception as e:
        print(f"[STATUS] ❌ Gagal memperbarui status: {e}")
