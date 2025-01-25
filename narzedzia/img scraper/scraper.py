import os
import re
import requests
from bs4 import BeautifulSoup


html_file_path = "experimental.html"
base_url = "https://wiki.bloodontheclocktower.com"
output_folder = "img"


def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def download_image(src_url, save_path):
    if os.path.exists(save_path):
        print(f"Plik już istnieje: {save_path}")
        return
    try:
        response = requests.get(src_url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Pobrano: {save_path}")
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania {src_url}: {e}")

if __name__ == "__main__":
    
    html_content = load_html(html_file_path)
    soup = BeautifulSoup(html_content, "html.parser")

    images = soup.find_all("img", src=re.compile(r"^/images/.+/.+/.+\.png$"))

    for img in images:
        src = img["src"]
        file_name = os.path.basename(src)
        full_url = f"{base_url}{src}"
        save_path = os.path.join(output_folder, file_name)

        #print(file_name, full_url, save_path)
        download_image(full_url, save_path)

    print("Pobieranie zakończone.")
