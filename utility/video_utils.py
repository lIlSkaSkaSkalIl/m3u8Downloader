import subprocess
import asyncio
import time
import os
import json
from utility.status_format import format_status

def extract_metadata(path):
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return None

        info = json.loads(result.stdout)
        duration = float(info["format"].get("duration", 0))
        streams = info.get("streams", [])
        width = height = None
        for stream in streams:
            if stream.get("codec_type") == "video":
                width = stream.get("width")
                height = stream.get("height")
                break
        return {
            "duration": int(duration),
            "width": width,
            "height": height
        }
    except Exception as e:
        print("[Metadata Error]", e)
        return None

def build_progress_bar(percent: int, length: int = 25) -> str:
    filled = int(length * percent / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}]"

async def download_m3u8_video(url, output_path, status_msg):
    try:
        cmd = [
            "streamlink", url, "best",
            "-o", output_path
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        start_time = time.time()
        last_update = 0

        while True:
            line = await process.stderr.readline()
            if not line:
                break
            elapsed = time.time() - start_time

            # Estimasi dummy progres berdasarkan waktu (jika tidak ada parsing)
            if time.time() - last_update > 5:
                try:
                    progress_text = format_status("📥 Mengunduh", output_path, 0, 0, elapsed)
                    await status_msg.edit(progress_text + "\n" + build_progress_bar(50))
                    last_update = time.time()
                except:
                    pass

        await process.wait()
        return os.path.exists(output_path)

    except Exception as e:
        print(f"[ERROR] {e}")
        return False
