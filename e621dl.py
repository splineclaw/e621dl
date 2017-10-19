#!/usr/bin/env python3

import os
from itertools import count
from lib import constants, local, remote

try:
    import requests
except ImportError:
    import pip

    while True:
        response = input("You are missing at least one required package. Would you like to install missing packages? (y/n): ").lower()
        if response in ['yes', 'ye', 'y']:
            for package in constants.REQUIREMENTS:
                pip.main(['install', package])
            import requests
            break
        elif response in ['no', 'n']:
            break

if __name__ == '__main__':
    with requests.Session() as session:
        local.init_log()

        local.print_log('e621dl', 'info', 'Running e621dl version ' + constants.VERSION + '.')

        config = local.get_config()

        blacklist = []
        tag_groups = []

        default_date = local.get_date(1)
        default_score = -9999999
        default_ratings = ['s']

        print('')
        local.print_log('e621dl', 'info', 'Aliasing tags.')

        for section in config.sections():
            section_tags = []
            section_date = default_date
            section_score = default_score
            section_ratings = default_ratings

            if section.lower() == 'defaults':
                for option, value in config.items(section):
                    if option in {'days_to_check', 'days'}:
                        default_date = local.get_date(int(value))
                    elif option in {'min_score', 'score'}:
                        default_score = int(value)
                    elif option in {'ratings', 'rating'}:
                        default_ratings = value.replace(',', ' ').lower().strip().split()
            elif section.lower() == 'blacklist':
                blacklist = [remote.get_tag_alias(tag.lower(), session) for tag in config.get(section, 'tags').replace(',', ' ').lower().strip().split()]
            else:
                for option, value in config.items(section):
                    if option in {'tags', 'tag'}:
                        section_tags = [remote.get_tag_alias(tag.lower(), session) for tag in value.replace(',', ' ').lower().strip().split()]
                    elif option in {'days_to_check', 'days'}:
                        section_date = local.get_date(int(value))
                    elif option in {'min_score', 'score'}:
                        section_score = int(value)
                    elif option in {'ratings', 'rating'}:
                        section_ratings = value.replace(',', ' ').lower().strip().split()

                tag_groups.append([section, section_tags, section_ratings, section_score, section_date])

        for group in tag_groups:
            print('')

            directory = group[0]
            tags = group[1]
            ratings = group[2]
            min_score = group[3]
            earliest_date = group[4]

            col_titles = ['new', 'duplicate', 'rating conflict', 'blacklisted', 'missing tag']
            row_len = sum(len(x) for x in col_titles) + ((len(col_titles) * 3) - 1)

            print('┌' + '─' * row_len + '┐')
            print('│{:^{width}}│'.format(directory, width = row_len))
            print('├─' + '─' * len(col_titles[0]) + '─┬─' + '─' * len(col_titles[1]) + '─┬─' + '─' * len(col_titles[2]) + '─┬─' + '─' * len(col_titles[3]) + '─┬─' + '─' * len(col_titles[4]) + '─┤')

            in_storage = 0
            bad_rating = 0
            blacklisted = 0
            bad_tag = 0
            downloaded = 0

            if len(tags) > 4:
                search_string = ' '.join(tags[:4])
            else:
                search_string = ' '.join(tags)

            print('│ ' + ' │ '.join(col_titles) + ' │')
            print('├─' + '─' * len(col_titles[0]) + '─┼─' + '─' * len(col_titles[1]) + '─┼─' + '─' * len(col_titles[2]) + '─┼─' + '─' * len(col_titles[3]) + '─┼─' + '─' * len(col_titles[4]) + '─┤')

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

                    print('│ {:^{width0}} │ {:^{width1}} │ {:^{width2}} │ {:^{width3}} │ {:^{width4}} │'.format(
                        str(downloaded), str(in_storage), str(bad_rating), str(blacklisted), str(bad_tag),
                        width0 = len(col_titles[0]), width1 = len(col_titles[1]), width2 = len(col_titles[2]), width3 = len(col_titles[3]), width4 = len(col_titles[4])
                        ), end='\r', flush=True)

                if len(results) < constants.MAX_RESULTS:
                    # I know that it's bad to copy and paste code, but I'm having a hard time printing this row when there are no results.
                    if (downloaded + in_storage + bad_rating + blacklisted + bad_tag) == 0:
                        print('│ {:^{width0}} │ {:^{width1}} │ {:^{width2}} │ {:^{width3}} │ {:^{width4}} │'.format(
                        '0', '0', '0', '0', '0',
                        width0 = len(col_titles[0]), width1 = len(col_titles[1]), width2 = len(col_titles[2]), width3 = len(col_titles[3]), width4 = len(col_titles[4])
                        ), end='\r', flush=True)

                    print('')
                    print('└─' + '─' * len(col_titles[0]) + '─┴─' + '─' * len(col_titles[1]) + '─┴─' + '─' * len(col_titles[2]) + '─┴─' + '─' * len(col_titles[3]) + '─┴─' + '─' * len(col_titles[4]) + '─┘')

                    break
