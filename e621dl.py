#!/usr/bin/env python3

#     __
# ___( o)> i am the wise duck of code, your code will compile without errors, but only if you say
# \ <_. )  "compile well ducko"
#  `---'

import os
from itertools import count

from lib import constants, local, remote

REQUIREMENTS = ['requests>=2.13.0', 'colorama>=0.3.9']

try:
    import requests
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
    import colorama

if __name__ == '__main__':
    with requests.Session() as session:
        local.init_log()
        colorama.init()

        local.print_log('e621dl', 'info', 'Running e621dl version ' + constants.VERSION + '.')

        config = local.get_config()

        blacklist = []
        tag_groups = []

        default_date = local.get_date(1)
        default_score = -9999999
        default_ratings = ['s']

        print('')
        local.print_log('e621dl', 'info', 'Converting tag aliases.')

        for section in config.sections():
            section_tags = []
            section_date = default_date
            section_score = default_score
            section_ratings = default_ratings

            if section.lower() == 'defaults':
                for option, value in config.items(section):
                    if option == 'days_to_check':
                        default_date = local.get_date(int(value))
                    elif option == 'min_score':
                        default_score = int(value)
                    elif option == 'ratings':
                        default_ratings = value.replace(',', ' ').lower().strip().split()
            elif section.lower() == 'blacklist':
                blacklist = [remote.get_tag_alias(tag.lower(), session) for tag in config.get(section, 'tags').replace(',', ' ').lower().strip().split()]
            else:
                for option, value in config.items(section):
                    if option == 'tags':
                        section_tags = [remote.get_tag_alias(tag.lower(), session) for tag in value.replace(',', ' ').lower().strip().split()]
                    elif option == 'days_to_check':
                        section_date = local.get_date(int(value))
                    elif option == 'min_score':
                        section_score = int(value)
                    elif option == 'ratings':
                        section_ratings = value.replace(',', ' ').lower().strip().split()

                tag_groups.append([section, section_tags, section_ratings, section_score, section_date])

        for group in tag_groups:
            print('')

            directory = group[0]
            tags = group[1]
            ratings = group[2]
            min_score = group[3]
            earliest_date = group[4]

            local.print_log('e621dl', 'info', 'Checking group \"' + directory + '\".')

            in_storage = 0
            bad_rating = 0
            blacklisted = 0
            bad_tag = 0
            downloaded = 0

            if len(tags) > 4:
                search_string = ' '.join(tags[:4])
            else:
                search_string = ' '.join(tags)

            for i in count(start = 1):
                results = remote.get_posts(search_string, min_score, earliest_date, i, constants.MAX_RESULTS, session)

                for post in results:
                    path = local.make_path(directory, [post['id'], post['md5'], post['file_ext']])

                    if os.path.isfile(path):
                        in_storage += 1
                    elif post['rating'] not in ratings:
                        bad_rating += 1
                    elif any(x in blacklist for x in post['tags'].split()):
                        blacklisted += 1
                    elif not set(tags[4:]).issubset(post['tags'].split()):
                        bad_tag += 1
                    else:
                        downloaded += 1
                        remote.download_post(post['file_url'], path, session)

                    print('                     ' + str(downloaded) + ' posts have been downloaded.\n' +
                        '                     ' + str(in_storage) + ' posts are already in storage.\n' +
                        '                     ' + str(bad_rating) + ' posts have an unwanted rating.\n' +
                        '                     ' + str(blacklisted) + ' posts contain a blacklisted tag.\n' +
                        '                     ' + str(bad_tag) + ' posts are missing a tag.' +

                        # This character moves the cursor back to the top of the post counting display.
                        # Multiply this character by the number of lines needed to move up.
                        '\x1b[1A' * 5)

                if len(results) < constants.MAX_RESULTS:
                    if (downloaded + in_storage + bad_rating + blacklisted + bad_tag) == 0:
                        print('                     No results found.')
                    else:
                        # This character returns the cursor to the bottom of the display after checking all posts for a group.
                        # Multiply this character by the number of lines needed to move down.
                        print('\x1b[1B' * 4)

                    break
