from requests_html import HTMLSession
import urllib.request, urllib.parse
from tqdm import tqdm
import re
import unicodedata
import time, os, inspect
from datetime import datetime
import random
import sys
import ssl
from plyer import notification

from mpi_template import *

ssl._create_default_https_context = ssl._create_unverified_context

currentDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

results_path = os.path.join(currentDirectory, 'results')
if not os.path.exists(results_path):
    os.makedirs(results_path)

def notify_user(title, message, timeout):
    notification.notify(
        title = title,
        message = message,
        timeout = timeout
    )

def download_gallery(gallery_list, folder_name):
    images_path = os.path.join(results_path, 'informacoes')
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    for image_url in gallery_list:
        image_url = image_url.attrs['href']
        file_name = image_url.split('/')[-1] 
        try:
            urllib.request.urlretrieve(f'{image_url}', f'{images_path}/{file_name}')
        except:
            print(f'Cannot download image from: {image_url}')

def create_vetkey(url_list, title_list):
    f = open(os.path.join(results_path, f'vetKey_crawled.php'), 'w+', encoding="utf-8")
    f.write(f'<?php $vetKey = array();\n')
    for i in range(len(url_list)):
        f.write(f'$vetKey[{i}] = array("url" => "{url_list[i]}", "key" => "{title_list[i]}", "desc" =>"");\n')
    f.write(f'?>')
    f.close()

def apply_regex(content):
    non_asc_blank = re.compile(' ')
    double_spaces = re.compile('\s{2,}')
    content = non_asc_blank.sub(' ', content)
    content = double_spaces.sub(' ', content)
    return re.sub(r'<h2>(.*)<\/h2>', lambda m: f'<h2>{m.group(1).upper()}</h2>', content)

def write_file(filename, mpi_title, mpi_desc, mpi_keywords, mpi_content):
    mpis_path = os.path.join(results_path, 'mpis')
    if not os.path.exists(mpis_path):
        os.makedirs(mpis_path)
    outputFile = open(os.path.join(mpis_path, f'{filename}.php'), 'w+', encoding="utf-8")
    sanitized_content = ''
    for element in content:
        sanitized_content += apply_regex(element.html)
    outputFile.write(fill_template(mpi_title, mpi_desc, mpi_keywords, sanitized_content.replace('><', f'>\n<')))
    outputFile.close()

urlFile = open(os.path.join(currentDirectory, 'mpi_urls.txt'), 'r')

linksToCrawl = []
for line in urlFile:
    linksToCrawl.append(line.rstrip())

urlFile.close()

session = HTMLSession()

mpi_url_list = []
mpi_title_list = []

for link in tqdm(linksToCrawl):
    print(link)

    try:
        r = session.get(link)
    except:
        print('Connection failed')
        print('Trying again in 3 seconds...')
        time.sleep(1)
        print('Trying again in em 2 seconds...')
        time.sleep(1)
        print('Trying again in em 1 seconds...')
        time.sleep(1)
        print('Connecting')
        r = session.get(link, verify=False)

    title = r.html.find('h1', first = True).text.strip()
    description = r.html.find('head meta[name="description"]', first = True).attrs['content'].strip()
    keywords = r.html.find('head meta[name="keywords"]', first = True).attrs['content'].strip()
    content = r.html.find('article > *:not(.gallery):not(.alerta):not(.more)')
    images = r.html.find('article > .gallery a')


    filename = link.split('/')[-1]

    mpi_url_list.append(filename)
    mpi_title_list.append(title)

    write_file(filename, title, description, keywords, content);
    download_gallery(images, filename)

create_vetkey(mpi_url_list, mpi_title_list)

NotifyUser('Finished MPI Crawler', f'All pages were generated successfully', 10)