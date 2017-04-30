#!/usr/bin/env python3

import shutil
from collections import namedtuple

from . import local

try:
    import requests
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

Post = namedtuple('Post', 'url id md5 ext tags rating score')
UserTag = namedtuple('UserTag', 'alias_id name')
AliasedTag = namedtuple('AliasedTag', 'name')

def get_posts(search_string, uploaded_after, page_number, max_results, session):
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
        post['file_ext'], post['tags'], post['rating'], post['score']))
    return posts

def get_alias(tag):
    request = 'https://e621.net/tag_alias/index.json?query=' + tag
    local.print_log('remote', 'debug', 'Tag alias request URL: \"' + request + '\".')

    results = requests.get(request).json()

    user_tags = []
    for user_tag in results:
        user_tags.append(UserTag(user_tag['alias_id'], user_tag['name']))

    if not user_tags:
        local.print_log('remote', 'error', 'The tag \"' + tag + '\" does not exist, please remove it from your tags ' +
            'file or blacklist.')
        return ''

    if tag == user_tags[0].name:
        request = 'https://e621.net/tag/show.json?id=' + str(user_tags[0].alias_id)
        local.print_log('remote', 'debug', 'Tag official request URL: \"' + request + '\".')

        # This will not work anymore. Use the requests module when you decide to fix tag aliasing.
        results = loads('[' + local.SpoofOpen().open(request).read() + ']'.decode())

        aliased_tags = []
        for aliased_tag in results:
            aliased_tags.append(AliasedTag(aliased_tag['name']))

        local.print_log('remote', 'debug', 'Tag \"' + tag + '\" aliased to \"' + aliased_tags[0].name + '\".')
        return aliased_tags[0].name

    else:
        return tag

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
