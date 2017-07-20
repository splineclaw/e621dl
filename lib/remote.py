#!/usr/bin/env python3

import shutil
from collections import namedtuple

from . import local

try:
    import requests
    from unidecode import unidecode
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

def get_posts(search_string, uploaded_after, page_number, max_results, session):
    Post = namedtuple('Post', 'url id md5 ext tags rating score')

    request = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>' + str(uploaded_after) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    local.print_log('remote', 'debug', 'Post request URL: \"' + request + '\".')

    results = session.get(request).json()

    posts = []
    for post in results:
        posts.append(Post(post['file_url'], post['id'], post['md5'],
        post['file_ext'], unidecode(post['tags']), post['rating'], post['score']))
    return posts

def download_posts(url_name_list, session):
    downloads_completed = 0

    for i, item in enumerate(url_name_list):
        url, path = url_name_list[i]
        data = session.get(url, stream = True)

        with open(path, 'wb') as outfile:
            shutil.copyfileobj(data.raw, outfile)

        downloads_completed +=1
        local.update_progressbar(downloads_completed, len(url_name_list))

    local.print_log('single_dl', 'debug', 'Downloading \"' + path + '\".')
