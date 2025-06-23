import subprocess
import asyncio
import time
from utility.status_format import format_status
import os

async def download_m3u8_video(url, output, status_msg):
    try:
        start = time.time()
        temp_file = "temp_streamlink_output.mp4"

        cmd = [
            "streamlink", url, "best",
            "-o", temp_file
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while process.poll() is None:
            line = process.stdout.readline().decode().strip()
            elapsed = time.time() - start

            # Update status setiap 5 detik
            try:
                await status_msg.edit(format_status("📥 Mengunduh", output, 0, 0, elapsed))
            except:
                pass
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
