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
            stderr=asyncio.subprocess.STDOUT
        )

        done = 0
        total = 0
        last_update = 0

        while True:
            line = await proc.stdout.readline()
            if not line:
                break

            decoded = line.decode("utf-8").strip()

            if "Download" in decoded and "%" in decoded:
                try:
                    data = decoded.split("Download:")[-1].strip()
                    parts = data.split("/")
                    if len(parts) >= 2:
                        done_str = parts[0].strip()
                        total_str = parts[1].split("(")[0].strip()
                        done = parse_size(done_str)
                        total = parse_size(total_str)

                        now = time.time()
                        if now - last_update > 5 or done == total:
                            await status_msg.edit(
                                format_status("📥 Mengunduh", output, done, total, now - start)
                            )
                            last_update = now
                except Exception as e:
                    print("[Parse Error]", e)

        await proc.wait()
        return os.path.exists(output)

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def parse_size(size_str):
    size_str = size_str.upper().replace("MIB", "MB").replace("KIB", "KB")
    num = ''.join(c for c in size_str if (c.isdigit() or c == '.' or c == ',')).replace(',', '.')
    num = float(num)
    if "KB" in size_str:
        return int(num * 1024)
    elif "MB" in size_str:
        return int(num * 1024**2)
    elif "GB" in size_str:
        return int(num * 1024**3)
    else:
        return int(num)
