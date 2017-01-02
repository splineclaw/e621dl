#!/usr/bin/env python

import logging
from json import loads
from collections import namedtuple
from support import SpoofOpen
import sqlite3 as sqlite

Post = namedtuple('Post', 'url id ext tags')
UserTag = namedtuple('UserTag', 'alias_id name')
AliasedTag = namedtuple('AliasedTag', 'name')

LOG = logging.getLogger('api')

def get_posts(search_string, uploaded_after, page_number, max_results):
    request = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>' + str(uploaded_after) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    LOG.debug('Post request URL: \"' + request + '\".')

    results = loads(SpoofOpen().open(request).read().decode())

    connection = sqlite.connect('.download_list.db')

    posts = []
    with connection:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS Posts')
        cursor.execute('CREATE TABLE Posts(url TEXT, id INT, ext TEXT, tags TEXT)')
        for post in results:
            cursor.execute('INSERT INTO Posts VALUES(?, ?, ?, ?);', (post['file_url'], post['id'],
                post['file_ext'], post['tags']))
            posts.append(Post(post['file_url'], post['id'], post['file_ext'], post['tags']))
    return posts

def download_post(url, filename):
    open(filename, 'wb').write(SpoofOpen().open(url).read())

def get_alias(tag):
    request = 'https://e621.net/tag_alias/index.json?query=' + tag
    LOG.debug('Tag alias request URL: \"' + request + '\".')

    results = loads(SpoofOpen().open(request).read().decode())

    user_tags = []
    for user_tag in results:
        user_tags.append(UserTag(user_tag['alias_id'], user_tag['name']))

    if not user_tags:
        LOG.error('The tag \"' + tag + '\" does not exist, please remove it from your tags ' +
            'file or blacklist.')
        return ''

    if tag == user_tags[0].name:
        request = 'https://e621.net/tag/show.json?id=' + str(user_tags[0].alias_id)
        LOG.debug('Tag official request URL: \"' + request + '\".')

        results = loads('[' + SpoofOpen().open(request).read() + ']'.decode())

        aliased_tags = []
        for aliased_tag in results:
            aliased_tags.append(AliasedTag(aliased_tag['name']))

        LOG.debug('Tag \"' + tag + '\" aliased to \"' + aliased_tags[0].name + '\".')
        return aliased_tags[0].name

    else:
        return tag
