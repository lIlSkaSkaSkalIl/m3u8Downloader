import asyncio
import subprocess
import os
import uuid
import time
from utility.status_format import format_status

# === Download M3U8 Video ===
async def download_m3u8_video(url, output_path, status_msg):
    try:
        tmp_path = f"{output_path}.tmp"
        start = time.time()

        # Jalankan streamlink dengan output ke file
        cmd = [
            "streamlink", url, "best",
            "-o", tmp_path,
            "--force"
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            if process.stdout.at_eof():
                break

            await asyncio.sleep(5)
            elapsed = time.time() - start
            try:
                await status_msg.edit(format_status("📥 Mengunduh", output_path, 0, 0, elapsed))
            except: pass

        await process.communicate()

        if not os.path.exists(tmp_path):
            return False

        # Remux agar metadata valid dan thumbnail muncul
        remux_cmd = [
            "ffmpeg", "-y", "-i", tmp_path,
            "-c", "copy", "-movflags", "+faststart",
            output_path
        ]
        subprocess.run(remux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(tmp_path)
        return os.path.exists(output_path)

    except Exception as e:
        print(f"[ERROR download_m3u8_video] {e}")
        return False

# === Ekstrak Metadata: durasi dan thumbnail ===
def extract_metadata(file_path):
    try:
        # Ambil durasi video
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration = int(float(result.stdout.decode().strip()))

        # Buat thumbnail
        thumb_path = f"{uuid.uuid4().hex}_thumb.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", "00:00:01", "-i", file_path,
             "-vframes", "1", "-q:v", "2", thumb_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if os.path.exists(thumb_path):
            return duration, thumb_path
        else:
            return duration, None

    except Exception as e:
        print(f"[ERROR extract_metadata] {e}")
        return 0, None
