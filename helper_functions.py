import requests, os, time, bs4
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import pathname2url


def get_page_links(base_link):
    
    try:
        site = requests.get(base_link)
        site.raise_for_status()

    except:
        print('Something went wrong. Please check internet and net connection')

    soup = bs4.BeautifulSoup(site.text, 'html.parser')
    site_links = [urljoin(base_link, link.attrs['href']) for link in soup.select('ul li a')]

    return site_links


def file_downloader(link, path):
    file = requests.get(link)
    file.raise_for_status()
    file_on_disk = open(path, 'wb')
    for chunk in file.iter_content(1000000):
        file_on_disk.write(file.content)
    file_on_disk.close()

