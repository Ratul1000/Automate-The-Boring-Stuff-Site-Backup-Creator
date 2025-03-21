from helper_functions import *
from config import *
import threading


def download_chapter(link):
    global backup_directory
    site = requests.get(link)
    site.raise_for_status()
    chapter_path = backup_directory / Path(link).name
    os.makedirs(chapter_path, exist_ok=True)

    soup = bs4.BeautifulSoup(site.content, 'html.parser')
    (soup.select('head link')[0]).attrs['href'] = Path('../style/automate2_website.css')
    image_folder = chapter_path/'images'

    os.makedirs(image_folder)


    for link2 in soup.select('img'):
        image_link = urljoin(link, link2.attrs['src'])
        image_path = image_folder / (Path(image_link).name)

        link2.attrs['src'] = Path('images') / Path(image_link).name
        file_downloader(image_link, image_path)

    file = open(chapter_path / (Path(link).name + '.html'), 'wb')
    
    file.write(soup.prettify(soup.original_encoding))
    file.close()

    print(Path(link).name + ' Done')


page_links = get_page_links(TOC_LINK_PAGE)[0:24]
path_of_css = Path(STYLE_FILE_PATH)


backup_directory = Path.cwd() / 'backup'
os.makedirs(backup_directory, exist_ok=True)

#store styles as styles is same for all html files
css_file_path = backup_directory / 'style'
os.makedirs(css_file_path, exist_ok=True)
css_file_final_path= css_file_path / 'automate2_website.css'
file_downloader(CSS_FILE_LINK, css_file_final_path)

threads = []
for link in page_links:
    print(link)
    thread_obj = threading.Thread(target=download_chapter, args=[link])
    threads.append(thread_obj)
    thread_obj.start()
    print('Started a thread')

    if len(threads) == TOTAL_RUN_THREADS:
        for obj in threads:
            obj.join()

        threads = []
   

    
