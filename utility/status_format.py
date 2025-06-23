import os

def human_readable_size(size: int) -> str:
    if not size:
        return "0 B"
    power = 1024
    n = 0
    Dic_powerN = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{size:.2f} {Dic_powerN[n]}"

def eta_str(elapsed, done, total) -> str:
    try:
        if done == 0 or elapsed == 0 or total == 0:
            return "Menghitung..."
        speed = done / elapsed
        remaining = total - done
        eta = int(remaining / speed)
        minutes, seconds = divmod(eta, 60)
        return f"{minutes}m {seconds}s" if minutes else f"{seconds}s"
    except:
        return "Menghitung..."

def progress_bar(done, total, width=20):
    if total == 0:
        return ""
    filled = int((done / total) * width)
    bar = '▰' * filled + '▱' * (width - filled)
    percent = (done / total) * 100
    return f"{bar} `{percent:.2f}%`"

def format_status(phase: str, filename: str, done: int, total: int, elapsed: float) -> str:
    speed = done / elapsed if elapsed > 0 else 0
    ext = os.path.splitext(filename)[1] or "Tidak diketahui"
    total_hr = human_readable_size(total) if total > 0 else "?"
    speed_hr = human_readable_size(speed) + "/s" if speed > 0 else "-"
    return (
        f"**{phase}** 📥\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📄 **Nama File:** `{os.path.basename(filename)}`\n"
        f"🧩 **Ekstensi:** `{ext}`\n"
        f"💾 **Ukuran:** `{human_readable_size(done)} / {total_hr}`\n"
        f"🚀 **Kecepatan:** `{speed_hr}`\n"
        f"⏱ **Waktu Berlalu:** `{int(elapsed)}s`\n"
        f"⌛ **Estimasi Selesai:** `{eta_str(elapsed, done, total)}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{progress_bar(done, total)}"
    )
