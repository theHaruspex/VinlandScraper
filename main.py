import os
import requests
from bs4 import BeautifulSoup
from os.path import basename
from os import makedirs
from time import sleep


def get_page_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html5lib')


def get_chapter_urls():
    toc_url = "https://read-vinlandsaga.com/"
    soup = get_page_soup(toc_url)
    nav_elements = soup.find_all("li", {"class": "su-post"})
    chapter_urls = []
    for element in nav_elements:
        a_element = element.find("a")
        url = a_element["href"]
        if url not in chapter_urls:
            chapter_urls.append(url)
    chapter_urls.reverse()
    return chapter_urls


def get_image_urls(chapter_url):
    soup = get_page_soup(chapter_url)
    img_elements = soup.findAll("img", {"class": "aligncenter"})
    image_urls = []
    for element in img_elements:
        img_url = element['src']
        if "cdn.hxmanga.com" in img_url:
            image_urls.append(img_url)
    return image_urls


def download_image(url, chapter_folderpath):
    page_number = basename(url)[:-4].zfill(3)
    file_extension = basename(url)[-4:]
    filename = page_number + file_extension
    filepath = f"{chapter_folderpath}/{filename}"
    print(f"Downloading: {filepath}")
    while True:
        try:
            with open(filepath, "wb") as file:
                file.write(requests.get(url).content)
            break
        except:
            sleep(5)




def download_chapter(chapter_url, master_folderpath):
    chapter_name = chapter_url[48:-1]
    image_urls = get_image_urls(chapter_url)
    for url in image_urls:
        chapter_folderpath = f"{master_folderpath}/{chapter_name}"
        makedirs(chapter_folderpath, exist_ok=True)
        download_image(url, chapter_folderpath)


def download_saga():
    master_folderpath = "Vinland_Saga"
    makedirs(master_folderpath, exist_ok=True)
    chapter_urls = get_chapter_urls()
    for i, url in enumerate(chapter_urls):
        if i < 200:
            continue
        print(f"{i}/{len(chapter_urls)}")
        download_chapter(url, master_folderpath)


chapters = os.listdir('Vinland_Saga')
chapters.remove('.DS_Store')
for chapter in chapters:
    if 'vol' in chapter:
        new_name = chapter[7:]
        os.rename(f"Vinland_Saga/{chapter}", f"Vinland_Saga/{new_name}")
