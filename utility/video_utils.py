import subprocess
import os
import asyncio

async def download_m3u8(url, output_path, progress_callback=None):
    print(f"[FFMPEG] 🚀 Memulai proses download dari URL:\n{url}")

    try:
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-i", url,
                "-c", "copy",
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break
            await asyncio.sleep(0.5)

        process.wait()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            raise FileNotFoundError("File tidak ditemukan setelah unduhan.")

        size = os.path.getsize(output_path)
        if size < 1024:
            raise Exception("Ukuran file terlalu kecil, kemungkinan gagal.")

    except Exception as e:
        raise
