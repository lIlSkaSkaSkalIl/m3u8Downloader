# Telegram M3U8 Downloader Bot (v1.00,0)

Bot Telegram ini khusus dibuat untuk mengunduh video dari link `.m3u8` streaming dan mengirimkannya langsung ke obrolan Telegram Anda.

## 🎯 Fitur
- Perintah `/m3u8` untuk mengunduh video dari link m3u8
- Progres status ter-update setiap 5 detik
- Mendukung upload video langsung ke Telegram
- Menggunakan `ffmpeg` untuk download cepat dengan metadata yang valid

## 🚀 Cara Menjalankan

1. Edit `config.py`:
```python
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
```

2. Install dependensi:
```bash
pip install pyrogram tgcrypto
sudo apt install ffmpeg
```

3. Jalankan bot:
```bash
python3 main.py
```

## 📌 Catatan
- Bot hanya merespons perintah `/m3u8` dan menunggu link video dari pengguna.
- Metadata video akan ditata ulang agar Telegram menampilkan thumbnail dan durasi.

## 🧪 Versi
**v1.00,0** — Versi stabil awal khusus untuk fitur `.m3u8` saja.