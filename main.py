import requests
from bs4 import BeautifulSoup


def get_page_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html5lib')


def get_chapter_links():
    toc_url = "https://read-vinlandsaga.com/"
    soup = get_page_soup(toc_url)
    nav_elements = [str(element) for element in soup.findAll(attrs={"class": "su-post"})]
    chapter_links = []
    for element in nav_elements:
        beginning_index = element.index("https")
        ending_index = element.index('/">')
        link = element[beginning_index:ending_index]
        if link not in chapter_links:
            chapter_links.append(link)
    chapter_links.reverse()
    return chapter_links

def get_image_links(chapter_url):
    soup = get_page_soup(chapter_url)




vinland_links = get_chapter_links()
image_links = get_image_links(vinland_links[0])
print(image_links)