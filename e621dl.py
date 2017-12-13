#!/usr/bin/env python3

import os, sys, requests
from fnmatch import fnmatch
from itertools import count
from distutils.version import StrictVersion
from lib import constants, local, remote

if __name__ == '__main__':
    with requests.Session() as session:
        session.headers['User-Agent'] = constants.USER_AGENT

        local.init_log()

        if StrictVersion(constants.VERSION) < StrictVersion(remote.get_github_release(session)):
            local.print_log('e621dl', 'info', 'A NEW VERSION OF E621DL IS AVAILABLE ON GITHUB: (https://github.com/Wulfre/e621dl/releases/latest).')

        local.print_log('e621dl', 'info', 'Running e621dl version ' + constants.VERSION + '.')

        print('')

        local.print_log('e621dl', 'info', 'Checking for partial downloads.')

        remote.finish_partial_downloads(session)

        print('')

        local.print_log('e621dl', 'info', 'Parsing config.')

        config = local.get_config()

        blacklist = []
        tag_groups = []

        default_date = local.get_date(1)
        default_score = -sys.maxsize
        default_ratings = ['s']

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

            col_titles = ['downloaded', 'duplicate', 'rating conflict', 'blacklisted', 'missing tag']
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

            last_id = sys.maxsize

            while True:
                results = remote.get_posts(search_string, min_score, earliest_date, last_id, session)
                last_id = results[-1]['id']

                # This dummy result makes sure that the for loop is always executed even for 0 real results.
                # This is so the table will print 0.
                dummy_id = 'Q'
                results.append({'id': dummy_id, 'file_ext': dummy_id})

                for post in results:
                    path = local.make_path(directory, post['id'], post['file_ext'])

                    if post['id'] == dummy_id:
                        pass
                    elif os.path.isfile(path):
                        in_storage += 1
                    elif post['rating'] not in ratings:
                        bad_rating += 1
                    elif [x for x in post['tags'].split() if any(fnmatch(x, y) for y in blacklist)]:
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

                if len(results) < constants.MAX_RESULTS + 1: # Max results + 1 to account for the dummy result.
                    print('')
                    print('└─' + '─' * len(col_titles[0]) + '─┴─' + '─' * len(col_titles[1]) + '─┴─' + '─' * len(col_titles[2]) + '─┴─' + '─' * len(col_titles[3]) + '─┴─' + '─' * len(col_titles[4]) + '─┘')

                    break
