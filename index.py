import re
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

def download_mkv_from_m3u8_url(m3u8_url, output_name):
    
    subprocess.run([
        "ffmpeg", "-i", m3u8_url, 
        "-c", "copy", f"{output_name}.mkv"
    ])

def get_mp4_from_mkv(m3u8_url, output_name):

    subprocess.run([
        "ffmpeg", "-i", f"{output_name}.mkv", 
        "-c", "copy", f"{output_name}.mp4"
    ])

def get_title_from_line(line):
    return re.search(r"^\[\*\]\s(.*)\s[0-9]{8}$", line).group(1)

def create_and_enter_title_folder(title):
    title_dir = os.path.join(directory, "downloads", title)

    if not os.path.isdir(title_dir):
        os.mkdir(title_dir)

    os.chdir(title_dir)

def find_group_urls_belonging_to_title(m3u8_urls, title_index):
    group_urls = []
    for index in range(title_index+1, len(m3u8_urls)):
        if m3u8_urls[index].startswith("#"):
            continue
        if m3u8_urls[index] == "" or m3u8_urls[index].isspace():
            break
        
        group_urls.append(m3u8_urls[index])

    return group_urls

def download_group(title, group_urls):

    create_and_enter_title_folder(title)

    for index, group_url in enumerate(group_urls):
        output_name = f"{title}_{index+1}"
        print(output_name)
        download_mkv_from_m3u8_url(group_url, output_name)
        get_mp4_from_mkv(group_url, output_name)

    print(os.getcwd())

m3u8_urls = parse_urls()

for index, line in enumerate(m3u8_urls):

    if line.startswith("[*]"):
        title = get_title_from_line(line)
        group_urls = find_group_urls_belonging_to_title(m3u8_urls, index)

        print(group_urls)
        download_group(title, group_urls)

    # download_mkv_from_m3u8_url(m3u8_url)
    # get_mp4_from_mkv(m3u8_url)
