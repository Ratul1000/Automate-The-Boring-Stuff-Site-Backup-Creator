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


page_links = get_page_links('https://automatetheboringstuff.com/#toc')

def file_downloader(link, path):
    file = requests.get(link, stream=True)
    file.raise_for_status()
    file_on_disk = open(path, 'wb')
    for chunk in file.iter_content(1000000):
        file_on_disk.write(chunk)

    print('File Download Successfull')


'''
1.Css file is same for everyone. So, first download the file and put it in the backup directory and save its path in variable
2.loop through each link and create chapter as directory + image directory inside.
3.Change path of css file in html file
4.Download each image and replace the image path inside the main html file
5.Save the html file

'''
path_of_css = Path('../style/automate2_website.css')


backup_directory = Path.cwd() / 'backup'
os.makedirs(backup_directory, exist_ok=True)
css_file_path = backup_directory / 'style'
os.makedirs(css_file_path, exist_ok=True)
css_file_final_path= css_file_path / 'automate2_website.css'

file_downloader('https://automatetheboringstuff.com/automate2_website.css', css_file_final_path)


for link in page_links:
    site = requests.get(link)
    site.raise_for_status()
    chapter_path = backup_directory / Path(link).name
    os.makedirs(chapter_path, exist_ok=True)

    soup = bs4.BeautifulSoup(site.content, 'html.parser')
    (soup.select('head link')[0]).attrs['href'] = str(Path('../style/automate2_website.css'))
    image_folder = chapter_path/'images'

    os.makedirs(image_folder)


    for link2 in soup.select('img'):
        image_link = urljoin(link, link2.attrs['src'])
        image_path = image_folder / (Path(image_link).name)

        link2.attrs['src'] = Path('images') / Path(image_link).name
        file_downloader(image_link, image_path)

    file = open(chapter_path / (Path(link).name + '.html'), 'wb')
    
    file.write(soup.prettify(soup.original_encoding))

    print(Path(link).name + ' Done')
   

    
