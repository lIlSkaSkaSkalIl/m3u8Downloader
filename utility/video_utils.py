import subprocess
import time
import os
from utility.status_format import format_status

async def download_m3u8_video(url: str, output: str, status_msg, client):
    try:
        start = time.time()
        cmd = [
            "ffmpeg",
            "-i", url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y",
            output
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Tunggu proses selesai sambil sesekali update
        while process.poll() is None:
            elapsed = time.time() - start
            try:
                await status_msg.edit(
                    format_status("📥 Mengunduh M3U8", output, 0, 0, elapsed)
                )
            except:
                pass
            await client.sleep(5)

        if process.returncode != 0:
            return False

        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False
