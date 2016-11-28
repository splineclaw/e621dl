#!/usr/bin/env python

import logging
import sys
from json import loads
from collections import namedtuple
from support import SpoofOpen

UPLOAD = namedtuple('Upload', 'id url md5 ext tags')
ALIAS = namedtuple('Alias', 'alias_id name')
OFFICIAL = namedtuple('Official', 'name')

SPOOF = SpoofOpen()

LIST_BASE = 'https://e621.net/post/index.json?'
TAGS = 'tags='
DATE = ' date:>'
PAGE = '&page='
MAX = '&limit='

ALIAS_BASE = 'https://e621.net/tag_alias/index.json?query='
OFFICIAL_BASE = 'https://e621.net/tag/show.json?id='

log = logging.getLogger('e621_api')


def get_posts(search_term, uploaded_after, page_num, max_results):
    request = LIST_BASE + \
        TAGS + search_term + \
        DATE + str(uploaded_after) + \
        PAGE + str(page_num) + \
        MAX + str(max_results)

    log.debug('search url = ' + request)
    results = loads(SPOOF.open(request).read().decode())

    uploads = []
    for post in results:
        uploads.append(UPLOAD(post['id'], post['file_url'], post['md5'], post['file_ext'],
                              post['tags']))
    return uploads


def get_alias(tag):
    request = ALIAS_BASE + tag

    results = loads(SPOOF.open(request).read().decode())

    aliases = []
    for alias in results:
        aliases.append(ALIAS(alias['alias_id'], alias['name']))

    if aliases == []:
        log.error(
            'The tag %s does not exist, please remove it from your tags file or blacklist.', tag)
        sys.exit(-1)

    if tag == aliases[0].name:
        request = OFFICIAL_BASE + str(aliases[0].alias_id)

        results = loads('[' + SPOOF.open(request).read() + ']'.decode())

        officials = []
        for tag in results:
            officials.append(OFFICIAL(tag['name']))
        return officials[0].name

    else:
        return tag


def download(url, filename):
    with open(filename, 'wb') as dest:
        source = SPOOF.open(url)
        dest.write(source.read())
