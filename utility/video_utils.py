import subprocess
import os
import time
import asyncio

async def download_m3u8(url, output_path, progress_callback=None):
    print(f"[FFMPEG] 🚀 Memulai proses download dari URL:\n{url}")

    process = None
    try:
        start_time = time.time()

        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",           # Overwrite tanpa konfirmasi
                "-i", url,      # Input M3U8
                "-c", "copy",   # Copy langsung tanpa re-encoding
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        total_time = 15  # estimasi waktu proses dalam detik
        interval = 1     # interval update (detik)
        current = 0

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break

            if progress_callback and os.path.exists(output_path):
                size = os.path.getsize(output_path)
                elapsed = max((time.time() - start_time), 1)
                estimated_total = max(size, size * (total_time / elapsed))
                await progress_callback(size, estimated_total)

            await asyncio.sleep(interval)

        process.wait()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            raise FileNotFoundError(f"File tidak ditemukan: {output_path}")

        size = os.path.getsize(output_path)
        if size < 1024:
            raise Exception("Ukuran file terlalu kecil, kemungkinan file kosong atau gagal.")

    except Exception as e:
        print(f"[FFMPEG] ❌ Error saat mengunduh: {e}")
        raise

    finally:
        if process and process.poll() is None:
            process.kill()
