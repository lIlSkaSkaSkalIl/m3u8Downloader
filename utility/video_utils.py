import subprocess
import asyncio
import time
from utility.status_format import format_status

async def download_m3u8_video(url, output, status_msg):
    try:
        start = time.time()
        cmd = [
            "ffmpeg", "-i", url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y", output
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while process.poll() is None:
            elapsed = time.time() - start
            try:
                await status_msg.edit(format_status("📥 Mengunduh", output, 0, 0, elapsed))
            except: pass
            await asyncio.sleep(5)

        return process.returncode == 0
    except Exception as e:
        print(f"[Error] {e}")
        return False
