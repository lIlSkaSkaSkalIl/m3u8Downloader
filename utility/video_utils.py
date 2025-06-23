import subprocess
import asyncio
import time
from utility.status_format import format_status
import os

async def download_m3u8_video(url, output, status_msg):
    try:
        start = time.time()
        temp_file = "temp_raw_m3u8.mp4"

        cmd = [
            "ffmpeg", "-i", url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y", temp_file
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while process.poll() is None:
            elapsed = time.time() - start
            try:
                await status_msg.edit(format_status("📥 Mengunduh", output, 0, 0, elapsed))
            except: pass
            await asyncio.sleep(5)

        if process.returncode != 0 or not os.path.exists(temp_file):
            return False

        # Remux agar metadata dan thumbnail valid
        remux_cmd = [
            "ffmpeg", "-i", temp_file,
            "-c", "copy", "-map", "0",
            "-movflags", "+faststart",
            "-y", output
        ]
        subprocess.run(remux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(temp_file)
        return os.path.exists(output)

    except Exception as e:
        print(f"[ERROR] {e}")
        return False
