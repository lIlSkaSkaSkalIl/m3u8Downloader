import os

def human_readable_size(size: int) -> str:
    if size is None or size == 0:
        return "N/A"
    power = 1024
    n = 0
    Dic_powerN = {0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power and n < 4:
        size /= power
        n += 1
    return f"{size:.2f} {Dic_powerN[n]}"

def eta_str(elapsed, done, total) -> str:
    if done == 0 or elapsed == 0 or total == 0:
        return "N/A"
    speed = done / elapsed
    if speed == 0:
        return "N/A"
    remaining = total - done
    eta = remaining / speed
    return f"{int(eta)}s"

def format_status(phase: str, filename: str, done: int, total: int, elapsed: float) -> str:
    speed = done / elapsed if elapsed > 0 else 0
    ext = os.path.splitext(filename)[1] or "N/A"
    total_hr = human_readable_size(total)
    return (
        f"**{phase}...**\n"
        f"📄 Nama: `{filename}`\n"
        f"💾 Ukuran: `{human_readable_size(done)} / {total_hr}`\n"
        f"🚀 Kecepatan: `{human_readable_size(speed)}/s`\n"
        f"🧩 Ekstensi: `{ext}`\n"
        f"⏱ Waktu Berlalu: `{int(elapsed)}s`\n"
        f"⌛ ETA: `{eta_str(elapsed, done, total)}`"
    )
