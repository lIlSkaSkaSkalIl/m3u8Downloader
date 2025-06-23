# Telegram M3U8 Downloader Bot (v1.00,0)

# 🎬 Telegram M3U8 Downloader Bot

Bot Telegram untuk mengunduh video dari link `.m3u8` langsung ke Telegram Anda secara otomatis.

---

## ✨ Fitur

- Unduh file `.m3u8` dan kirim hasilnya sebagai video ke Telegram
- Status progres unduhan (ukuran, kecepatan, ETA)
- Mendukung Google Colab (tidak perlu VPS)

---

## 🚀 Jalankan di Google Colab

Klik tombol di bawah untuk langsung membuka dan menjalankan bot di Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/lIlSkaSkaSkalIl/m3u8Downloader/blob/017a270b170bb302b8e42fc933cc6fb256d5a9da/M3U8_telegram_bot.ipynb)

---

## 🛠️ Cara Menggunakan

1. Klik tombol **"Open in Colab"** di atas
2. Masukkan `API_ID`, `API_HASH`, dan `BOT_TOKEN` Telegram Anda di form input
3. Jalankan semua sel
4. Bot akan aktif dan menunggu perintah `/m3u8` di Telegram

---

## 📦 Struktur Proyek

m3u8Downloader/ ├── main/ │   ├── main.py │   ├── config.py        # dibuat otomatis oleh Colab │   ├── utility/ │   │   └── video_utils.py │   │   └── status_format.py │   └── utils/ │       └── state.py

---

## 🧪 Contoh Penggunaan

Kirim ke bot Anda di Telegram:

/m3u8 https://example.com/video/stream.m3u8

---

## 📄 Lisensi

Proyek ini dirilis dengan lisensi MIT. Silakan gunakan dan modifikasi sesuai kebutuhan.
