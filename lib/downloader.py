#!/usr/bin/env python3

from itertools import repeat
from multiprocessing import Pool, Manager, Process
from time import sleep
from . import core

try:
    import requests
except(ImportError):
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

def update_progress(downloaded, total):
    progress = downloaded / total

    BAR_LENGTH = 36
    status = ''

    completed = int(round(BAR_LENGTH * progress))
    progress_bar = '\rDownloading          [{}] {}% {}'.format('>' * completed +
        ' ' * (BAR_LENGTH - completed), int(round(progress * 100)), '(' + str(downloaded) + ' / ' +
        str(total) + ')')
    print(progress_bar, end='')

def download_monitor(managed_list, total_items):
    while True:
        update_progress(len(managed_list), total_items)
        if total_items == len(managed_list):
            return
        sleep(0.05)

def single_download(zipped_args):
    url_name_list, managed_list = zipped_args
    url, path = url_name_list

    data = requests.get(url, stream = True)

    with open(path, 'wb') as outfile:
        for chunk in data:
            outfile.write(chunk)

    core.print_log('single_dl', 'debug', 'Downloading \"' + path + '\".')
    managed_list.append(path)

def multi_download(url_name_list, num_threads):
    manager = Manager()
    managed_list = manager.list()

    core.print_log('multi_dl', 'debug', 'Staring download pool of ' + str(num_threads) + ' workers.')

    monitor = Process(target = download_monitor, args = (managed_list, len(url_name_list)))
    monitor.start()

    pool = Pool(processes = num_threads)
    work = pool.map_async(single_download, list(zip(url_name_list, repeat(managed_list))))

    try:
        work.get(65535)
        monitor.join()
        pool.close()
        pool.join()

    except(KeyboardInterrupt):
        pool.terminate()
        pool.join()
