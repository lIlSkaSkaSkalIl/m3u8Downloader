import os
import ffmpeg
import requests
import re

def get_available_qualities(m3u8_url):
    """
    Mengambil semua kualitas dari master playlist M3U8.
    Return dict: {'1080p': url, '720p': url, ...}
    """
    try:
        response = requests.get(m3u8_url)
        if response.status_code != 200:
            return {}

        pattern = r'#EXT-X-STREAM-INF:.*RESOLUTION=(\d+x\d+).*?\n(.*)'
        matches = re.findall(pattern, response.text)

        qualities = {}
        for res, stream_url in matches:
            resolution = res.split('x')[1] + 'p'  # contoh: 1920x1080 → '1080p'
            # Lengkapi jika URL relatif
            absolute_url = (
                stream_url if stream_url.startswith("http")
                else m3u8_url.rsplit("/", 1)[0] + "/" + stream_url
            )
            qualities[resolution] = absolute_url

        return qualities
    except Exception as e:
        print(f"❌ Gagal mengambil kualitas: {e}")
        return {}

def download_video(m3u8_url, resolution='720p', output_path='downloads/output.mp4'):
    """
    Unduh video dari M3U8 ke file mp4 menggunakan ffmpeg.
    """
    try:
        # ✅ Pastikan folder tujuan ada
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        qualities = get_available_qualities(m3u8_url)
        selected_url = qualities.get(resolution, m3u8_url)

        (
            ffmpeg
            .input(selected_url)
            .output(output_path, codec='copy')
            .run(overwrite_output=True)
        )
        return output_path if os.path.exists(output_path) else None
    except Exception as e:
        print(f"❌ Gagal mengunduh video: {e}")
        return None
