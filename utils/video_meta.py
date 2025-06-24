def get_thumbnail(path: str, thumb_path: str) -> str:
    """Membuat thumbnail JPG ukuran 320x180 dari detik ke-1 video."""
    try:
        result = subprocess.run(
            [
                "ffmpeg", "-y", "-i", path,
                "-ss", "00:00:01.000", "-vframes", "1",
                "-s", "320x180",
                thumb_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if os.path.exists(thumb_path):
            print(f"✅ Thumbnail berhasil dibuat di: {thumb_path}")
        else:
            print(f"❌ Thumbnail gagal dibuat di: {thumb_path}")
        return thumb_path if os.path.exists(thumb_path) else None
    except Exception as e:
        print(f"❌ Gagal membuat thumbnail: {e}")
        return None
