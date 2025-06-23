import asyncio
import subprocess
import os
import time
from utility.status_format import format_status

async def download_m3u8_video(url: str, output_path: str, status_msg, client) -> bool:
    start_time = time.time()

    cmd = [
        "ffmpeg", "-i", url,
        "-c", "copy", "-bsf:a", "aac_adtstoasc",
        "-movflags", "+faststart",
        "-loglevel", "error",
        output_path
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    last_update = time.time()
    while True:
        if process.returncode is not None:
            break
        now = time.time()
        if now - last_update >= 5:
            elapsed = now - start_time
            size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
            status_text = format_status("📥 Mengunduh", output_path, size, 0, elapsed)
            try:
                await status_msg.edit(status_text)
            except:
                pass
            last_update = now
        await asyncio.sleep(1)

    await process.wait()
    return os.path.exists(output_path)