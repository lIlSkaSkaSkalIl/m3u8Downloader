import subprocess
import os
import json

def get_video_duration(path: str) -> int:
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return int(float(result.stdout.strip()))
    except Exception as e:
        print(f"❌ Gagal mengambil durasi: {e}")
        return 0

def get_thumbnail(path: str, thumb_path: str) -> str:
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", path,
                "-ss", "00:00:01.000", "-vframes", "1",
                thumb_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return thumb_path if os.path.exists(thumb_path) else None
    except Exception as e:
        print(f"❌ Gagal mengambil thumbnail: {e}")
        return None

def get_video_info(url: str) -> dict:
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration,codec_name",
                "-of", "json",
                "-i", url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        data = json.loads(result.stdout)
        stream = data["streams"][0] if "streams" in data and data["streams"] else {}

        return {
            "duration": int(float(stream.get("duration", 0))),
            "width": stream.get("width"),
            "height": stream.get("height"),
            "codec": stream.get("codec_name")
        }

    except Exception as e:
        print(f"❌ Gagal mengambil info video: {e}")
        return {}
