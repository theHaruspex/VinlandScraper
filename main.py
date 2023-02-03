import requests
from bs4 import BeautifulSoup
from os.path import basename


def get_page_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html5lib')


def get_chapter_links():
    toc_url = "https://read-vinlandsaga.com/"
    soup = get_page_soup(toc_url)
    nav_elements = soup.find_all("li", {"class": "su-post"})
    chapter_links = []
    for element in nav_elements:
        a_element = element.find("a")
        link = a_element["href"]
        if link not in chapter_links:
            chapter_links.append(link)
    chapter_links.reverse()
    return chapter_links

def get_image_urls(chapter_url):
    soup = get_page_soup(chapter_url)
    nav_elements = soup.findAll("img", {"class": "aligncenter"})
    image_links = []
    for element in nav_elements:
        img_url = element['src']
        if "cdn.hxmanga.com" in img_url:
            image_links.append(img_url)
    return image_links


def download_image(url, folderpath):
    filepath = f"{folderpath}/{basename(url)}"
    with open(filepath, "wb") as file:
        file.write(requests.get(url).content)





vinland_links = get_chapter_links()
image_urls = get_image_urls(vinland_links[0])
for url in image_urls:
    download_image(url, "Chapter 1")