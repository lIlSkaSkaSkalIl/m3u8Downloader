import subprocess
import asyncio
import time
import os
from utility.status_format import format_status

async def download_m3u8_video(url, output, status_msg, client=None):
    try:
        start = time.time()
        proc = await asyncio.create_subprocess_exec(
            "streamlink", url, "best", "-o", output,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        progress = 0
        last_update = 0

        while True:
            line = await proc.stderr.readline()
            if not line:
                break
            decoded = line.decode("utf-8")

            if "Download" in decoded and "%" in decoded:
                # Contoh parsing: Download: 12.34 MiB / 120.56 MiB (10%), ...
                parts = decoded.split("Download:")[-1].strip()
                if "/" in parts:
                    try:
                        downloaded_str, total_str = parts.split("/")[:2]
                        downloaded = parse_size(downloaded_str.strip())
                        total = parse_size(total_str.strip().split(" ")[0])
                        now = time.time()
                        if now - last_update > 5:
                            await status_msg.edit(
                                format_status("📥 Mengunduh", output, downloaded, total, now - start)
                            )
                            last_update = now
                    except:
                        pass

        await proc.wait()
        return os.path.exists(output)

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def parse_size(size_str):
    """Ubah string seperti '10.5 MiB' jadi bytes."""
    size_str = size_str.upper().replace("MIB", "MB").replace("KIB", "KB")
    num, unit = size_str.split()
    num = float(num)
    if unit == "KB":
        return int(num * 1024)
    elif unit == "MB":
        return int(num * 1024 ** 2)
    elif unit == "GB":
        return int(num * 1024 ** 3)
    else:
        return int(num)

def extract_metadata(path: str):
    """Ambil thumbnail & durasi dari video."""
    try:
        thumb_path = "thumbnail.jpg"
        subprocess.run([
            "ffmpeg", "-i", path,
            "-ss", "00:00:02.000", "-vframes", "1",
            "-vf", "scale=320:-1",
            "-y", thumb_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result = subprocess.run(
            ["ffprobe", "-i", path, "-show_entries", "format=duration",
             "-v", "quiet", "-of", "csv=p=0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        duration = int(float(result.stdout.strip()))
        return duration, thumb_path
    except Exception as e:
        print(f"[Metadata ERROR] {e}")
        return 0, None
