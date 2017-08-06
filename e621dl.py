#!/usr/bin/env python3

#     __
# ___( o)> i am the wise duck of code, your code will compile without errors, but only if you say
# \ <_. )  "compile well ducko"
#  `---'

REQUIREMENTS = ['unidecode>=0.4.21', 'requests>=2.13.0', 'colorama>=0.3.9']

try:
    import requests
    from unidecode import unidecode
    import colorama
except ImportError:
    import pip

    while True:
        response = input("You are missing at least one required package. Would you like to install it? Yes / No: ").lower()
        if response in ['yes', 'y']:
            for package in REQUIREMENTS:
                pip.main(['install', package])
            break
        elif response in ['no', 'n']:
            break
finally:
    import requests
    from unidecode import unidecode
    import colorama

import datetime
import logging
import os
import sys
from itertools import count

from lib import constants, local, remote

if __name__ == '__main__':
    logging.basicConfig(level = local.get_verbosity(), format = constants.LOGGER_FORMAT, stream = sys.stderr)
    local.print_log('e621dl', 'info', 'Running e621dl version ' + constants.VERSION + '.')

    config = local.get_config('config.ini')

    if not local.tags_valid(config):
        local.print_log('e621dl', 'info', 'Error(s) occurred during initialization, see above for more information.')
        sys.exit(-1)

    ordinal_check_date = ordinal_check_date = datetime.date.today().toordinal() - 7
    timeout = 5
    blacklist = []
    tag_groups = []

    for section in config.sections():
        if section.lower() == 'settings':
            for option, value in config.items(section):
                if option == 'days_to_check':
                    ordinal_check_date = datetime.date.today().toordinal() - int((config.get('Settings', 'days_to_check')))

                    if ordinal_check_date < 1:
                        ordinal_check_date = 1
                    elif ordinal_check_date > datetime.date.today().toordinal() - 1:
                        ordinal_check_date = datetime.date.today().toordinal() - 1
                if option == 'connection_timeout':
                    timeout = int((config.get('Settings', 'connection_timeout')))

                    if timeout < 0:
                        timeout = None

        elif section.lower() == 'blacklist':
            blacklist = unidecode(config.get(section, 'tags').replace(',', '').strip()).lower().split()

        else:
            section_tags = []
            section_score = -999999
            section_ratings = ['s']
            for option, value in config.items(section):
                if option == 'tags':
                    section_tags = unidecode(value.replace(',', '').strip()).lower().split()
                elif option == 'min_score':
                    section_score = int(value)
                elif option == 'ratings':
                    section_ratings = value.replace(',', '').strip().lower().split()

            tag_groups.append([section, section_tags, section_ratings, section_score])

    print('')

    check_date = datetime.date.fromordinal(ordinal_check_date).strftime(constants.DATE_FORMAT)

    local.print_log('e621dl', 'info', 'Checking for new posts since ' + check_date + ' (' + str(config.get('Settings', 'days_to_check')) + ' days).')

    print('')

    # group[0] = directory
    # group[1] = tags
    # group[2] = ratings
    # group[3] = score

    with requests.Session() as session:
        for group in tag_groups:
            local.print_log('e621dl', 'info', 'Checking group \"' + group[0] + '\".')

            in_storage = 0
            bad_rating = 0
            bad_score = 0
            blacklisted = 0
            bad_tag = 0
            downloaded = 0

            if len(group[1]) > 5:
                search = ' '.join(group[1][:5])
            else:
                search = ' '.join(group[1])

            colorama.init()

            for i in count():
                results = remote.get_posts(search, check_date, i + 1, constants.MAX_RESULTS, session, timeout)

                for post in results:
                    filepath = local.make_path(group[0], [post['id'], post['md5'], post['file_ext']])

                    if os.path.isfile(filepath):
                        in_storage += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' skipped. Already downloaded.')
                    elif post['rating'] not in group[2]:
                        bad_rating += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' skipped. Bad rating.')
                    elif post['score'] < group[3]:
                        bad_score += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' skipped. Bad score.')
                    elif any(x in blacklist for x in unidecode(post['tags']).split()):
                        blacklisted += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' skipped. Blacklisted.')
                    elif not set(group[1][5:]).issubset(unidecode(post['tags']).split()):
                        bad_tag += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' skipped. Bad tag.')
                    else:
                        downloaded += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' will download.')
                        remote.download_post(post['file_url'], filepath, session, timeout)

                    print('                     ' + str(downloaded) + ' posts have been downloaded.\n' +
                        '                     ' + str(in_storage) + ' posts are already in storage.\n' +
                        '                     ' + str(bad_rating) + ' posts have an unwanted rating.\n' +
                        '                     ' + str(bad_score) + ' posts have a low score.\n' +
                        '                     ' + str(blacklisted) + ' posts contain a blacklisted tag.\n' +
                        '                     ' + str(bad_tag) + ' posts are missing a tag.' +

                        # This character moves the cursor back to the top of the post counting display.
                        # Multiply this character by the number of lines needed to move up.
                        '\x1b[1A' * 6)

                if len(results) < constants.MAX_RESULTS:
                    if(downloaded + in_storage + bad_rating + bad_score + blacklisted + bad_tag) == 0:
                        print('                     No results found.\n')
                    else:
                        # This character returns the cursor to the bottom of the display after checking all posts for a group.
                        # Multiply this character by the number of lines needed to move down.
                        print('\x1b[1B' * 6)

                    break
