#!/usr/bin/env python

from support import SpoofOpen
import logging
from time import sleep
from multiprocessing import Pool, Manager, Process
from itertools import repeat

def update_progress(progress):
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
    bar = '\rDownloading          [{0}] {1:6.2f}% {2}'.format('>' * completed +
        ' ' * (BAR_LENGTH - completed), progress * 100, status)
    print bar,

def download_monitor(managedList, totalItems):
    while True:
        progress = float(len(managedList)) / float(totalItems)
        update_progress(progress)
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
