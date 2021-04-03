import os
import subprocess

directory = os.path.dirname(
    os.path.abspath(__file__)
)
downloads = os.path.join(directory, "downloads")

def parse_urls():
    file_path = os.path.join(directory, "m3u8_url.txt")

    with open(file_path) as file:
        return file.read().split("\n")

def get_name_from_m3u8_url(m3u8_url):
    return m3u8_url.split("/")[-1].replace(".m3u8", "")

def download_mkv_from_m3u8_url(m3u8_url):
    os.chdir(downloads)
    
    mkv_name = f"{get_name_from_m3u8_url(m3u8_url)}.mkv"
    # print(mkv_name)
    res = subprocess.run([
        "ffmpeg", "-i", m3u8_url, 
        "-c", "copy", mkv_name
    ])
    
    return res.returncode

def get_mp4_from_mkv(m3u8_url):
    os.chdir(downloads)

    mkv_name = f"{get_name_from_m3u8_url(m3u8_url)}.mkv"
    mp4_name = f"{get_name_from_m3u8_url(m3u8_url)}.mp4"

    res = subprocess.run([
        "ffmpeg", "-i", mkv_name, 
        "-c", "copy", mp4_name
    ])

    return res.returncode

m3u8_urls = parse_urls()

for m3u8_url in m3u8_urls:
    if m3u8_url.startswith("#") or m3u8_url == "" or m3u8_url.isspace():
        continue

    download_mkv_from_m3u8_url(m3u8_url)
    get_mp4_from_mkv(m3u8_url)
