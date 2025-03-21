import requests, os, time, bs4
from pathlib import Path
from urllib.parse import urljoin

def get_page_links(base_link):
    
    try:
        site = requests.get(base_link)
        site.raise_for_status()

    except:
        print('Something went wrong. Please check internet and net connection')

    soup = bs4.BeautifulSoup(site.text, 'html.parser')
    site_links = [urljoin(base_link, link.attrs['href']) for link in soup.select('ul li a')]

    return site_links


print(get_page_links('https://automatetheboringstuff.com/#toc'))

'''
1.Css file is same for everyone. So, first download the file and put it in the backup directory and save its path in variable
2.loop through each link and create chapter as directory + image directory inside.
3.Change path of css file in html file
4.Download each image and replace the image path inside the main html file
5.Save the html file

'''