import os
import subprocess

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
        dur_str = result.stdout.strip()
        if not dur_str:
            raise ValueError("Durasi tidak ditemukan.")
        return int(float(dur_str))
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
        if os.path.exists(thumb_path):
            return thumb_path
        else:
            print("⚠️ Thumbnail tidak ditemukan setelah ffmpeg dijalankan.")
            return None
    except Exception as e:
        print(f"❌ Gagal mengambil thumbnail: {e}")
        return None
