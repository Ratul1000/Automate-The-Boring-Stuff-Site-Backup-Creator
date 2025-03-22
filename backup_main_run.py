from helper_functions import *
from config import *
import threading


def download_chapter(link):
    global backup_directory, total_threads_finished
    print(Path(link).name + ' Started Downloading')
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

    

    lock.acquire()
    total_threads_finished += 1
    print(Path(link).name + ' Finished Downloading')
    lock.release()


lock = threading.Lock()
total_threads_finished = 0

page_links = [TOC_LINK_PAGE] + get_page_links(TOC_LINK_PAGE)[0:24]
path_of_css = Path(STYLE_FILE_PATH)


backup_directory = Path.cwd() / 'backup'
os.makedirs(backup_directory, exist_ok=True)

#store styles as styles is same for all html files
css_file_path = backup_directory / 'style'
os.makedirs(css_file_path, exist_ok=True)
css_file_final_path= css_file_path / 'automate2_website.css'
file_downloader(CSS_FILE_LINK, css_file_final_path)


move = 0
total_links = len(page_links)
current_threads = 0
run_block = True
while move < total_links:
    if run_block and (current_threads <= TOTAL_ALLOWED_THREADS):
        thread_obj = threading.Thread(target=download_chapter, args=[page_links[move]])
        thread_obj.start()
        current_threads += 1
        move += 1
        if current_threads == TOTAL_ALLOWED_THREADS:
            run_block = False


    if total_threads_finished:
        total_threads_finished -= 1
        run_block = True
        current_threads -= 1

    elif current_threads == TOTAL_ALLOWED_THREADS:
        time.sleep(1)



   

    
