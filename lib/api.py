#!/usr/bin/env python

from collections import namedtuple
from support import SpoofOpen
import logging
from json import loads
import sys

POST = namedtuple('Post', 'url md5 ext id tags')
USER_TAG = namedtuple('User', 'alias_id name')
ALIASED_TAG = namedtuple('Alias', 'name')

spoof = SpoofOpen()
log = logging.getLogger('api')

def get_posts(search_string, uploaded_after, page_number, max_results):
    request = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>' + str(uploaded_after) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    log.debug('Post request URL: \"' + request + '\".')

    results = loads(spoof.open(request).read().decode())

    posts = []
    for post in results:
        posts.append(POST(post['file_url'], post['md5'], post['file_ext'], post['id'],
        post['tags']))
    return posts

def download_post(url, filename):
    with open(filename, 'wb') as dest:
        source = spoof.open(url)
        dest.write(source.read())

def get_alias(tag):
    request = 'https://e621.net/tag_alias/index.json?query=' + tag
    log.debug('Tag alias request URL: \"' + request + '\".')

    results = loads(spoof.open(request).read().decode())

    userTags = []
    for userTag in results:
        userTags.append(USER_TAG(userTag['alias_id'], userTag['name']))

    if userTags == []:
        log.error('The tag \"' + tag + '\" does not exist, please remove it from your tags ' +
            'file or blacklist.')
        return ''

    if tag == userTags[0].name:
        request = 'https://e621.net/tag/show.json?id=' + str(userTags[0].alias_id)
        log.debug('Tag official request URL: \"' + request + '\".')

        results = loads('[' + spoof.open(request).read() + ']'.decode())

        aliasedTags = []
        for aliasedTag in results:
            aliasedTags.append(ALIASED_TAG(aliasedTag['name']))

        log.debug('Tag \"' + tag + '\" aliased to \"' + aliasedTags[0].name + '\".')
        return aliasedTags[0].name

    else:
        return tag
