#!/usr/bin/env python3

import shutil
from multiprocessing import Pool, cpu_count

from . import core

try:
    import requests
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

def update_progress(downloaded, total):
    progress = downloaded / total
    BAR_LENGTH = 36
    completed = int(round(BAR_LENGTH * progress))

    progress_bar = '\rDownloading          [{}] {}% {}'.format('>' * completed +
        ' ' * (BAR_LENGTH - completed), int(round(progress * 100)), '(' + str(downloaded) + ' / ' +
        str(total) + ')')
    print(progress_bar, end='')

def single_download(url_name_list):
    url, path = url_name_list
    data = requests.get(url, stream = True)

    with open(path, 'wb') as outfile:
        shutil.copyfileobj(data.raw, outfile)

    core.print_log('single_dl', 'debug', 'Downloading \"' + path + '\".')

def multi_download(url_name_list):
    num_processes = cpu_count() * 2

    core.print_log('multi_dl', 'debug', 'Staring download pool of ' + str(num_processes) +
    ' workers.')

    pool = Pool(processes = num_processes)
    work = pool.map_async(single_download, url_name_list, chunksize = 1)

    while not work.ready():
        update_progress(len(url_name_list) - work._number_left, len(url_name_list))
    if work.ready():
        update_progress(len(url_name_list), len(url_name_list))

    pool.close()
    pool.join()
