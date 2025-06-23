import subprocess
import asyncio
import time
from utility.status_format import format_status
import os
import re

async def download_m3u8_video(url, output, status_msg):
    try:
        start = time.time()
        temp_file = "temp_streamlink_output.mp4"

        cmd = [
            "streamlink", url, "best",
            "-o", temp_file
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        progress_text = ""
        last_update = 0

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            elapsed = time.time() - start
            now = time.time()

            # Contoh parsing: "Downloading fragment 15..." → jadi progres simbolik
            if "fragment" in line.lower():
                match = re.search(r'fragment\s+(\d+)', line, re.IGNORECASE)
                if match:
                    frag_num = int(match.group(1))
                    progress_text = f"📥 Mengunduh Fragmen #{frag_num}"

            # Update status tiap 5 detik
            if now - last_update > 5:
                try:
                    await status_msg.edit(
                        f"{progress_text}\n\n" +
                        format_status("📥 Mengunduh", output, 0, 0, elapsed)
                    )
                    last_update = now
                except:
                    pass

            await asyncio.sleep(0.2)

        if process.returncode != 0 or not os.path.exists(temp_file):
            return False

        # Remux video untuk metadata/thumbnail
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
