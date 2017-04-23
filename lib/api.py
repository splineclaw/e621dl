#!/usr/bin/env python

from json import loads
from collections import namedtuple
from . import core

try:
    import requests
except(ImportError):
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

Post = namedtuple('Post', 'url id md5 ext tags')
UserTag = namedtuple('UserTag', 'alias_id name')
AliasedTag = namedtuple('AliasedTag', 'name')

def get_posts(search_string, uploaded_after, page_number, max_results):
    search_url = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>' + str(uploaded_after) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    core.print_log('api', 'debug', 'Post request URL: \"' + search_url + '\".')

    results = requests.get(search_url).json()

    posts = []
    for post in results:
        posts.append(Post(post['file_url'], post['id'], post['md5'], post['file_ext'],
        post['tags']))
    return posts

def get_alias(tag):
    search_url = 'https://e621.net/tag_alias/index.json?query=' + tag
    lib.core.print_log('api', 'debug', 'Tag alias request URL: \"' + request + '\".')

    results = requests.get(search_url).json()

    user_tags = []
    for user_tag in results:
        user_tags.append(UserTag(user_tag['alias_id'], user_tag['name']))

    if not user_tags:
        core.print_log('api', 'error', 'The tag \"' + tag + '\" does not exist, please remove it from your tags ' +
            'file or blacklist.')
        return ''

    if tag == user_tags[0].name:
        request = 'https://e621.net/tag/show.json?id=' + str(user_tags[0].alias_id)
        core.print_log('api', 'debug', 'Tag official request URL: \"' + request + '\".')

        # This will not work anymore. Use the requests module when you decide to fix tag aliasing.
        results = loads('[' + core.SpoofOpen().open(request).read() + ']'.decode())

        aliased_tags = []
        for aliased_tag in results:
            aliased_tags.append(AliasedTag(aliased_tag['name']))

        core.print_log('api', 'debug', 'Tag \"' + tag + '\" aliased to \"' + aliased_tags[0].name + '\".')
        return aliased_tags[0].name

    else:
        return tag
