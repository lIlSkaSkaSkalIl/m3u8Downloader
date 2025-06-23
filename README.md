
# 📥 m3u8Downloader Bot v2

Bot Telegram berbasis Python untuk mengunduh video dari URL M3U8 dan mengunggah hasilnya ke Telegram dalam format MP4. Dirancang untuk berjalan di lingkungan Google Colab dengan dukungan progres download dan upload secara paralel.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lIlSkaSkaSkalIl/m3u8Downloader/blob/main/M3U8_telegram_bot.ipynb)

---

## 🚀 Fitur yang Tersedia (v2)
- ✅ Unduh video dari file M3U8 dan konversi otomatis ke MP4.
- ✅ Progres **download** berjalan paralel dan ditampilkan berkala.
- ✅ Progres **upload** ke Telegram ditampilkan saat proses berlangsung.
- ✅ Struktur modular dan scalable (terpisah per fungsi: utility, handler, dll).
- ✅ Mendukung upload file berukuran besar ke Telegram.

---

## 🛠️ Fitur yang Akan Ditambahkan
| Fitur                                        | Status |
|---------------------------------------------|--------|
| Upload video sebagai **streamable** Telegram | 🔜 Segera |
| Resume download jika terputus               | 🔜 Segera |
| Deteksi **master playlist** M3U8 dan pilih resolusi | 🔜 Segera |
| Perintah `/status` untuk lihat progres      | 🔜 Segera |
| Opsi konversi ukuran file (MB/GB) pada progres | 🔜 Segera |

---

## 🧑‍💻 Cara Menjalankan di Google Colab

1. Klik tombol **Open in Colab** di atas.
2. Jalankan setiap sel secara berurutan.
3. Masukkan **Bot Token Telegram** dan jalankan bot.

---

## 💬 Perintah Bot

| Perintah     | Deskripsi                                      |
|--------------|------------------------------------------------|
| `/start`     | Menyapa dan memberi info awal penggunaan bot. |
| Kirim URL M3U8 | Bot akan mulai proses download dan upload.    |

---

## 🗂️ Struktur Direktori

```
m3u8Downloader/
├── main.py                  # Entry point bot Telegram
├── config.py                # Konfigurasi token dan path
├── requirements.txt         # Daftar pustaka yang dibutuhkan
├── M3U8_telegram_bot.ipynb  # Notebook untuk Colab
├── utility/
│   ├── video_utils.py       # Fungsi untuk unduh dan konversi M3U8
│   └── status_format.py     # Format teks progres
├── utils/
│   └── state.py             # Menyimpan status progres
```

---

## 📄 Lisensi

Proyek ini dirilis dengan lisensi **MIT**. Bebas digunakan dan dimodifikasi dengan menyertakan atribusi.

---

## 📬 Kontak

Dikembangkan oleh [Ska Ska](https://github.com/lIlSkaSkaSkalIl). Untuk pertanyaan, saran, atau kontribusi, silakan buat issue di GitHub.

