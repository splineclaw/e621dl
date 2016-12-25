#!/usr/bin/env python

from support import SpoofOpen
import logging
from time import sleep
from multiprocessing import Pool, Manager, Process
from itertools import repeat
import urllib2

def internet_connected():
    try:
        urllib2.urlopen('http://www.msftncsi.com/ncsi.txt', timeout = 5)
        return True
    except urllib2.URLError as err: pass
    log = logging.getLogger('internet')
    log.info('No internet connection detected.')
    return False

def update_progress(downloaded, total):
    progress = float(downloaded) / float(total)

    BAR_LENGTH = 36
    status = ''
    if isinstance(progress, int):
        progress = float(progress)
    if progress < 0:
        progress = 0
        status = '-- Stopped.\n'
    if progress >= 1:
        progress = 1
        status = '-- Done.\n'
    completed = int(round(BAR_LENGTH * progress))
    bar = '\rDownloading          [{}] {:6.2f}% {} {}'.format('>' * completed +
        ' ' * (BAR_LENGTH - completed), progress * 100, '(' + str(downloaded) + ' / ' + str(total) +
        ')', status)
    print bar,

def download_monitor(managedList, totalItems):
    while True:
        update_progress(len(managedList), totalItems)
        if totalItems == len(managedList):
            return
        sleep (0.2)

def single_download(zippedArgs):
    urlNameList, managedList = zippedArgs
    url, filename = urlNameList

    spoof = SpoofOpen()

    try:
        with open(filename, 'wb') as dest:
            source = spoof.open(url)
            dest.write(source.read())

        log = logging.getLogger('single_dl')
        log.debug('Downloading \"' + filename + '\".')
        managedList.append(filename)

    except KeyboardInterrupt, e:
        pass

def multi_download(urlNameList, numThreads):
    manager = Manager()
    managedList = manager.list()

    log = logging.getLogger('multi_dl')
    log.debug('Staring download pool of ' + str(numThreads) + ' workers.')

    monitor = Process(target = download_monitor, args = ((managedList, len(urlNameList))))
    monitor.start()

    workers = Pool(processes = numThreads)
    work = workers.map_async(single_download, zip(urlNameList, repeat(managedList)))

    try:
        work.get(0xFFFF)
        monitor.join()

    except KeyboardInterrupt:
        exit()
