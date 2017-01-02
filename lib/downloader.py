#!/usr/bin/env python

import logging
import urllib2
from itertools import repeat
from multiprocessing import Pool, Manager, Process
from time import sleep
from support import SpoofOpen

def internet_connected():
    try:
        urllib2.urlopen('http://www.msftncsi.com/ncsi.txt', timeout = 5)
        return True
    except urllib2.URLError:
        pass
    LOG = logging.getLogger('internet')
    LOG.info('No internet connection detected.')
    return False

def update_progress(downloaded, total):
    progress = float(downloaded) / float(total)

    BAR_LENGTH = 36
    status = ''
    if isinstance(progress, int):
        progress = float(progress)
    if progress < 0:
        progress = 0.0
        status = '-- Stopped.\n'
    if progress >= 1:
        progress = 1.0
        status = '-- Done.\n'
    completed = int(round(BAR_LENGTH * progress))
    progress_bar = '\rDownloading          [{}] {:6.2f}% {} {}'.format('>' * completed +
        ' ' * (BAR_LENGTH - completed), progress * 100, '(' + str(downloaded) + ' / ' + str(total) +
        ')', status)
    print progress_bar,

def download_monitor(managed_list, total_items):
    while True:
        update_progress(len(managed_list), total_items)
        if total_items == len(managed_list):
            return
        sleep(0.2)

def single_download(zipped_args):
    url_name_list, managed_list = zipped_args
    url, filename = url_name_list

    spoof = SpoofOpen()

    try:
        with open(filename, 'wb') as dest:
            source = spoof.open(url)
            dest.write(source.read())

        LOG = logging.getLogger('single_dl')
        LOG.debug('Downloading \"' + filename + '\".')
        managed_list.append(filename)

    except KeyboardInterrupt:
        pass

def multi_download(url_name_list, num_threads):
    manager = Manager()
    managed_list = manager.list()

    LOG = logging.getLogger('multi_dl')
    LOG.debug('Staring download pool of ' + str(num_threads) + ' workers.')

    monitor = Process(target = download_monitor, args = (managed_list, len(url_name_list)))
    monitor.start()

    workers = Pool(processes = num_threads)
    work = workers.map_async(single_download, zip(url_name_list, repeat(managed_list)))

    try:
        work.get(0xFFFF)
        monitor.join()

    except KeyboardInterrupt:
        exit()
