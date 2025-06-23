import subprocess
import os

async def download_m3u8(url, output_path, progress_callback=None):
    print(f"[FFMPEG] 🚀 Memulai proses download dari URL:\n{url}")
    print(f"[FFMPEG] 💾 File output: {output_path}")

    try:
        # Jalankan ffmpeg
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",            # Overwrite tanpa konfirmasi
                "-i", url,       # Input M3U8
                "-c", "copy",    # Copy langsung tanpa re-encoding
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Cetak semua output dari ffmpeg untuk debug
        for line in process.stdout:
            print("[FFMPEG]", line.strip())

        process.wait()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        # Cek apakah file benar-benar dibuat
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"File tidak ditemukan: {output_path}")

        # Cek ukuran file
        size = os.path.getsize(output_path)
        print(f"[FFMPEG] ✅ Unduhan selesai, ukuran file: {size} byte")

        if size < 1024:
            raise Exception("Ukuran file terlalu kecil, kemungkinan file kosong atau gagal.")

    except Exception as e:
        print(f"[FFMPEG] ❌ Error: {e}")
        raise
