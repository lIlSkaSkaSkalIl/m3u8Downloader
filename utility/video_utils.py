import aiohttp
import m3u8
import os
import subprocess
import asyncio

async def download_m3u8(url: str, output_path: str, progress_callback=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            playlist_text = await response.text()

    playlist = m3u8.loads(playlist_text)

    if not playlist.segments:
        raise ValueError("Playlist tidak memiliki segment!")

    segment_urls = [
        url if segment.uri.startswith("http") else os.path.join(os.path.dirname(url), segment.uri)
        for segment in playlist.segments
    ]

    temp_file = output_path + ".txt"
    with open(temp_file, "w") as f:
        for segment_url in segment_urls:
            f.write(f"file '{segment_url}'\n")

    total = len(segment_urls)
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", temp_file,
        "-c", "copy",
        "-y", output_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )

    while True:
        line = await proc.stderr.readline()
        if not line:
            break
        if progress_callback:
            current = int(len(line))  # Dummy progress, bisa dikembangkan
            await progress_callback(current, total)

    await proc.wait()
    os.remove(temp_file)
