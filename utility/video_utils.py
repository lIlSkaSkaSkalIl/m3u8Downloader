import aiohttp
import asyncio
import os
import time
from utility.status_format import format_status

async def download_m3u8_video(url: str, output_path: str, status_msg, client) -> bool:
    start_time = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await status_msg.edit("❌ Gagal mengambil playlist M3U8.")
                    return False
                playlist_text = await resp.text()

        base_url = url.rsplit("/", 1)[0]
        lines = playlist_text.splitlines()
        segments = [line for line in lines if line and not line.startswith("#")]

        total = len(segments)
        downloaded = 0
        temp_dir = f"{output_path}_parts"
        os.makedirs(temp_dir, exist_ok=True)

        for i, segment in enumerate(segments):
            segment_url = segment if segment.startswith("http") else f"{base_url}/{segment}"
            segment_path = os.path.join(temp_dir, f"{i:04d}.ts")

            async with aiohttp.ClientSession() as session:
                async with session.get(segment_url) as segment_resp:
                    if segment_resp.status == 200:
                        with open(segment_path, "wb") as f:
                            f.write(await segment_resp.read())

            downloaded += 1
            if i % 5 == 0 or i == total - 1:
                elapsed = time.time() - start_time
                done_size = sum(os.path.getsize(os.path.join(temp_dir, f)) for f in os.listdir(temp_dir))
                status_text = format_status("📥 Mengunduh", output_path, done_size, total, elapsed)
                try:
                    await status_msg.edit(status_text)
                except:
                    pass

        # Gabungkan semua .ts menjadi satu .mp4
        with open(os.path.join(temp_dir, "list.txt"), "w") as f:
            for i in range(total):
                f.write(f"file '{os.path.abspath(os.path.join(temp_dir, f'{i:04d}.ts'))}'\n")

        ffmpeg_cmd = f"ffmpeg -y -f concat -safe 0 -i {os.path.join(temp_dir, 'list.txt')} -c copy {output_path}"
        proc = await asyncio.create_subprocess_shell(ffmpeg_cmd)
        await proc.wait()

        # Bersihkan
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)

        return os.path.exists(output_path)

    except Exception as e:
        await status_msg.edit(f"❌ Terjadi error: {e}")
        return False
