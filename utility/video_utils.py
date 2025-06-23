import subprocess
import asyncio
import time
import os
import requests
from utility.status_format import format_status

def estimate_m3u8_size(url: str, bitrate_kbps: int = 1000) -> int:
    """
    Estimasi ukuran file dari link m3u8 berdasarkan total durasi dan bitrate (kbps).
    Default bitrate 1000 kbps = 125000 bytes/s.
    """
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return 0

        m3u8_content = r.text.splitlines()
        total_duration = 0.0

        for line in m3u8_content:
            if line.startswith("#EXTINF:"):
                try:
                    duration = float(line.split(":")[1].rstrip(","))
                    total_duration += duration
                except:
                    continue

        bitrate_bytes = bitrate_kbps * 125  # 1000 kbps = 125000 bytes/s
        estimated_size = int(total_duration * bitrate_bytes)
        return estimated_size
    except:
        return 0

async def download_m3u8_video(url, output, status_msg):
    try:
        start_time = time.time()
        temp_file = "temp_streamlink_output.ts"
        estimated_total = estimate_m3u8_size(url)

        # Mulai proses streamlink
        process = subprocess.Popen(
            ["streamlink", "--default-stream", "best", "-o", temp_file, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        last_update = 0
        while process.poll() is None:
            elapsed = time.time() - start_time
            done = os.path.getsize(temp_file) if os.path.exists(temp_file) else 0

            if elapsed - last_update > 5:
                try:
                    await status_msg.edit(
                        format_status("📥 Mengunduh", output, done, estimated_total, elapsed)
                    )
                    last_update = elapsed
                except:
                    pass
            await asyncio.sleep(1)

        if not os.path.exists(temp_file):
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
