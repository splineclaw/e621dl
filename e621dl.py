#!/usr/bin/env python3

#     __
# ___( o)> i am the wise duck of code, your code will compile without errors, but only if you say
# \ <_. )  "compile well ducko"
#  `---'

import datetime
import logging
import os
import sys
from collections import namedtuple

from lib import constants, local, remote

try:
    import requests
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

if __name__ == '__main__':

    logging.basicConfig(level = local.get_verbosity(), format = constants.LOGGER_FORMAT, stream = sys.stderr)
    local.print_log('e621dl', 'info', 'Running e621dl version ' + constants.VERSION + '.')

    config = local.get_config('config.ini')

    if local.tags_valid(config):
        local.print_log('e621dl', 'info', 'Error(s) occurred during initialization, see above for more information.')
        sys.exit(-1)

    Group = namedtuple('Group', 'tags score ratings directory')
    blacklist = []
    tag_groups = []

    local.print_log('e621dl', 'info', 'Parsing config.')

    for section in config.sections():
        if section == 'Settings':
            pass
        elif section == 'Blacklist':
            for tag in config.get('Blacklist', 'tags').replace(',', '').strip().split():
                blacklist.append(tag)
        else:
            section_tags = ''
            section_score = ''
            section_ratings = ''
            for option, value in config.items(section):
                if option == 'tags':
                    section_tags = value.replace(',', '').strip()
                elif option == 'min_score':
                    section_score = int(value)
                elif option == 'ratings':
                    section_ratings = value.replace(',', '').strip()

            tag_groups.append(Group(section_tags, section_score, section_ratings, section))

    print('')

    ordinal_check_date = datetime.date.today().toordinal() - int((config.get('Settings', 'days_to_check')))
    if ordinal_check_date < 1:
        ordinal_check_date = 1
    elif ordinal_check_date > datetime.date.today().toordinal() - 1:
        ordinal_check_date = datetime.date.today().toordinal() - 1

    check_date = datetime.date.fromordinal(ordinal_check_date).strftime(constants.DATE_FORMAT)

    local.print_log('e621dl', 'info', 'Looking for new posts since ' + check_date + '.')
    print('')

    download_list = []

    with requests.Session() as session:
        for group in tag_groups:
            local.print_log('e621dl', 'info', 'Group \"' + group.directory + '\" detected, checking for new posts tagged: \"' + group.tags.replace(' ', ', ') + '\".')

            accumulating = True
            current_page = 1
            posts_found = []
            tag_overflow = []

            separated_tags = group.tags.split()
            separated_ratings = group.ratings.split()

            if len(separated_tags) > 5:
                search_tags = ' '.join(separated_tags[0:5])

                for tag in separated_tags:
                    if tag not in search_tags.split():
                        tag_overflow.append(tag)
            else:
                search_tags = group.tags

            while accumulating:
                search_results = remote.get_posts(search_tags, check_date, current_page, constants.MAX_RESULTS, session)

                if not search_results:
                    accumulating = False
                else:
                    posts_found += search_results
                    accumulating = len(search_results) == constants.MAX_RESULTS
                    current_page += 1

            if len(posts_found) > 0:
                bad_tags = 0
                blacklisted = 0
                bad_score = 0
                bad_rating = 0
                on_disk = 0
                will_download = 0

                for i, post in enumerate(posts_found):
                    local.print_log('e621dl', 'debug', 'Item ' + str(i) + '\'s id is \"' + str(post.id) + '\".')

                    filename = local.make_path(group.directory, post)
                    current_tags = post.tags.split()

                    if post.rating not in separated_ratings:
                        bad_rating += 1
                        local.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Has the wrong rating.')
                    elif int(post.score) < group.score:
                        bad_score += 1
                        local.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Has a lower score than requested.')
                    elif len(separated_tags) > 5 and not list(set(tag_overflow) & set(current_tags)):
                        bad_tags += 1
                        local.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Missing a requested tag.')
                    elif list(set(blacklist) & set(current_tags)):
                        blacklisted += 1
                        local.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Contains a blacklisted tag.')
                    elif os.path.isfile(filename):
                        on_disk += 1
                        local.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Already downloaded previously.')
                    else:
                        local.print_log('e621dl', 'debug', 'Item ' + str(i) + ' will be downloaded.')
                        download_list.append((post.url, filename))
                        will_download += 1

                # I probably should not be using hard-coded spacing in here. Maybe I'll fix it later.
                local.print_log('e621dl', 'info', str(will_download) + ' new files.\n' +
                '                     ' + str(len(posts_found)) + ' total files found.\n' +
                '                     ' + str(bad_rating) + ' have an unwanted rating.\n' +
                '                     ' + str(bad_score) + ' have a low score.\n' +
                '                     ' + str(bad_tags) + ' are missing tags.\n' +
                '                     ' + str(blacklisted) + ' are blacklisted.\n' +
                '                     ' + str(on_disk) + ' have been previously downloaded.')

                print('')
            else:
                local.print_log('e621dl', 'info', '0 new files.')
                print('')

        if download_list:
            local.print_log('e621dl', 'info', 'Starting download of ' + str(len(download_list)) + ' files.')
            remote.download_posts(download_list, session)
            print('')

            # Make the damaged file check more efficient.
            #local.print_log('e621dl', 'info', 'Checking downloads for damaged files.')
            #local.check_md5s()
        else:
            local.print_log('e621dl', 'info', 'Nothing to download.')

    sys.exit(0)
