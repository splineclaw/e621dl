#!/usr/bin/env python3

import shutil

from . import local

try:
    import requests
    from unidecode import unidecode
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

def get_posts(search_string, uploaded_after, page_number, max_results, session):
    request = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>' + str(uploaded_after) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    local.print_log('remote', 'debug', 'Post request URL: \"' + request + '\".')

    return session.get(request).json()

def download_post(url, path, session):
    data = session.get(url, stream = True)

    with open(path, 'wb') as outfile:
        shutil.copyfileobj(data.raw, outfile)

        local.print_log('single_dl', 'debug', 'Downloading' + '\"' + url + '\" to \"' + path + '\".')
