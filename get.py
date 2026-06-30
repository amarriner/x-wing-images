from bs4 import BeautifulSoup

import os
import requests

URL = "https://infinitearenas.com"
SUBDIRS = [
    "pilots",
    "upgrades"
]
IMAGE_DIR = "images"

if not os.path.isdir(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)

for dir in SUBDIRS:
    subdir = f"{URL}/xw2/images/{dir}"
    print(f"--> Parsing {subdir}")

    image_subdir = f"{IMAGE_DIR}/{dir}"
    if not os.path.isdir(image_subdir):
        os.mkdir(image_subdir)

    soup = BeautifulSoup(requests.get(subdir).text, "html.parser")
    first_td_elements = soup.select("table#table-content tr td:first-of-type a")

    for a in first_td_elements:
        url = f"{URL}/{a['href']}"
        filename = f"{image_subdir}/{a.get_text(strip=True)}"
        with requests.get(url, stream=True) as response:
            if os.path.isfile(filename):
                continue
            if not filename.endswith('.png'):
                continue
            print(f" -  Downloading {a.get_text(strip=True)}")
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
