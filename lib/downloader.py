#!/usr/bin/env python3

import shutil

from . import core

try:
    import requests
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

def update_progress(downloaded, total):
    BAR_LENGTH = 36

    progress = downloaded / total
    completed_segments = int(round(BAR_LENGTH * progress))

    progress_bar = '\rDownloading          [{}] {}% {}'.format('>' * completed_segments +
        ' ' * (BAR_LENGTH - completed_segments), int(round(progress * 100)),
        '(' + str(downloaded) + ' / ' + str(total) + ')')
    print(progress_bar, end='')

def download_posts(url_name_list):
    session = requests.Session()
    downloads_completed = 0

    for i, item in enumerate(url_name_list):
        url, path = url_name_list[i]
        data = session.get(url, stream = True)

        with open(path, 'wb') as outfile:
            shutil.copyfileobj(data.raw, outfile)

        downloads_completed +=1
        update_progress(downloads_completed, len(url_name_list))

    core.print_log('single_dl', 'debug', 'Downloading \"' + path + '\".')
