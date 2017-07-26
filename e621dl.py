#!/usr/bin/env python3

#     __
# ___( o)> i am the wise duck of code, your code will compile without errors, but only if you say
# \ <_. )  "compile well ducko"
#  `---'

import datetime
import logging
import os
import sys
from itertools import count

from lib import constants, local, remote

try:
    import requests
    from unidecode import unidecode
    import colorama
except ImportError:
    exit('Required packages are missing. Run \"pip install -r requirements.txt\" to install them.')

if __name__ == '__main__':
    colorama.init()

    logging.basicConfig(level = local.get_verbosity(), format = constants.LOGGER_FORMAT, stream = sys.stderr)
    local.print_log('e621dl', 'info', 'Running e621dl version ' + constants.VERSION + '.')

    config = local.get_config('config.ini')

    if not local.tags_valid(config):
        local.print_log('e621dl', 'info', 'Error(s) occurred during initialization, see above for more information.')
        sys.exit(-1)

    blacklist = []
    tag_groups = []

    for section in config.sections():
        if section.lower() == 'settings':
            pass

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

    ordinal_check_date = datetime.date.today().toordinal() - int((config.get('Settings', 'days_to_check')))

    if ordinal_check_date < 1:
        ordinal_check_date = 1
    elif ordinal_check_date > datetime.date.today().toordinal() - 1:
        ordinal_check_date = datetime.date.today().toordinal() - 1

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

            on_disk = 0
            bad_rating = 0
            bad_score = 0
            bad_tags = 0
            blacklisted = 0
            downloaded = 0

            if len(group[1]) > 5:
                search = ' '.join(group[1][:5])
            else:
                search = ' '.join(group[1])

            for i in count():
                results = remote.get_posts(search, check_date, i + 1, constants.MAX_RESULTS, session)

                for post in results:
                    filepath = local.make_path(group[0], [post['id'], post['md5'], post['file_ext']])

                    if os.path.isfile(filepath):
                        on_disk += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' was skipped. Already downloaded.')
                    elif post['rating'] not in group[2]:
                        bad_rating += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' was skipped. Has the wrong rating.')
                    elif post['score'] < group[3]:
                        bad_score += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' was skipped. Has too low a score.')
                    elif not set(group[1][5:]).issubset(unidecode(post['tags']).split()):
                        bad_tags += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' was skipped. Missing tags.')
                    elif any(x in blacklist for x in unidecode(post['tags']).split()):
                        blacklisted += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' was skipped. Contains a blacklisted tag.')
                    else:
                        downloaded += 1
                        local.print_log('e621dl', 'debug', 'Post ' + str(post['id']) + ' will be downloaded.')
                        remote.download_post(post['file_url'], filepath, session)

                    print('                     ' + str(downloaded) + ' new posts have been downloaded.\n' +
                        '                     ' + str(bad_rating) + ' posts have an unwanted rating.\n' +
                        '                     ' + str(bad_score) + ' posts have a low score.\n' +
                        '                     ' + str(bad_tags) + ' posts are missing tags.\n' +
                        '                     ' + str(blacklisted) + ' posts contain blacklisted tags.\n' +
                        '                     ' + str(on_disk) + ' posts have been previously downloaded.' +

                        # This character moves the cursor back to the top of the post counting display.
                        # ESC[?A where ? is the number of lines to go up.
                        '\x1b[6A')

                if len(results) < constants.MAX_RESULTS:
                    # Multiply this character by the number of lines needed to move down after checking all posts for a group.
                    # For whatever reason, ESC[?B does not work.
                    print('\x1b[1B' * 6)

                    break

            print('')

    sys.exit(0)
