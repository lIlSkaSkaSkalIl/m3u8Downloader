import subprocess
import time
import asyncio
import os
import streamlink
import ffmpeg
from utility.status_format import format_status

async def download_m3u8_video(url, output, status_msg):
    try:
        streams = streamlink.streams(url)
        if "best" not in streams:
            return False
        stream = streams["best"]

        with open(output, "wb") as f:
            start = time.time()
            downloaded = 0
            for chunk in stream.open():
                f.write(chunk)
                downloaded += len(chunk)

                elapsed = time.time() - start
                if elapsed > 1:
                    await status_msg.edit(format_status("📥 Mengunduh", output, downloaded, 0, elapsed))
                    await asyncio.sleep(5)

        return os.path.exists(output)
    except Exception as e:
        print(f"[ERR] {e}")
        return False

def extract_metadata(path):
    try:
        probe = ffmpeg.probe(path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        duration = int(float(video_stream['duration']))
        thumbnail_path = f"{path}_thumb.jpg"

        (
            ffmpeg.input(path, ss=1)
            .output(thumbnail_path, vframes=1)
            .run(quiet=True, overwrite_output=True)
        )
        return duration, thumbnail_path if os.path.exists(thumbnail_path) else None
    except Exception as e:
        print(f"[META ERR] {e}")
        return 0, None
