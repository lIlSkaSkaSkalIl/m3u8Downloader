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

def progress_bar(done, total, width=20) -> str:
    if total == 0 or done == 0:
        return "⏳ [progress tidak tersedia]"

    # Batasi maksimal 100%
    progress = min(done / total, 1.0)
    filled = int(progress * width)
    bar = '▰' * filled + '▱' * (width - filled)
    percent = progress * 100
    return f"{bar} `{percent:.2f}%`"

def format_status(phase: str, filename: str, done: int, total: int, elapsed: float) -> str:
    speed = done / elapsed if elapsed > 0 else 0
    ext = os.path.splitext(filename)[1] or "N/A"
    total_hr = human_readable_size(total)

    return (
        f"📩 **{phase}** 📩\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📁 Nama File: `{os.path.basename(filename)}`\n"
        f"🧩 Ekstensi: `{ext}`\n"
        f"💽 Ukuran: `{human_readable_size(done)} / {total_hr}`\n"
        f"🚀 Kecepatan: `{human_readable_size(speed)}/s`\n"
        f"⏱ Waktu Berlalu: `{int(elapsed)}s`\n"
        f"⏳ Estimasi Selesai: `{eta_str(elapsed, done, total)}`\n"
        f"{progress_bar(done, total)}"
    )
