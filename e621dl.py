#!/usr/bin/env python

import logging
import os
import sys
import datetime
from multiprocessing import freeze_support, cpu_count
from collections import namedtuple
from lib import const, core, api, downloader

if __name__ == '__main__':
    freeze_support()

    logging.basicConfig(level = core.get_verbosity(), format = const.LOGGER_FORMAT, stream = sys.stderr)
    core.print_log('e621dl', 'info', 'Running e621dl version ' + const.VERSION + '.')

    config = core.get_config('config.ini')

    early_terminate = False
    early_terminate |= core.validate_tags(config)

    if early_terminate:
        core.print_log('e621dl', 'info', 'Error(s) occurred during initialization, see above for more information.')
        sys.exit(-1)

    GROUP = namedtuple('Group', 'tags directory')
    blacklist = []
    tag_groups = []

    core.print_log('e621dl', 'info', 'Parsing config.')

    for section in config.sections():
        if section == 'Settings':
            pass
        elif section == 'Blacklist':
            for tag in config.get('Blacklist', 'tags').replace(',', '').split():
                blacklist.append(tag)
        else:
            for option, value in config.items(section):
                if option == 'tags':
                    tag_groups.append(GROUP(value.replace(',', ''), section))

    print('')

    ordinal_check_date = datetime.date.today().toordinal() - int((config.get('Settings', 'days_to_check')))
    if ordinal_check_date < 1:
        ordinal_check_date = 1
    elif ordinal_check_date > datetime.date.today().toordinal() - 1:
        ordinal_check_date = datetime.date.today().toordinal() - 1

    check_date = datetime.date.fromordinal(ordinal_check_date).strftime(const.DATE_FORMAT)

    core.print_log('e621dl', 'info', 'Looking for new posts since ' + check_date + '.')
    print('')

    download_list = []

    for group in tag_groups:
        core.print_log('e621dl', 'info', 'Group \"' + group.directory + '\" detected.')
        core.print_log('e621dl', 'info', 'Checking for new posts tagged: \"' + group.tags.replace(' ', ', ') + '\".')

        accumulating = True
        current_page = 1
        links_missing_tags = 0
        links_blacklisted = 0
        links_on_disk = 0
        will_download = 0
        post_list = []
        tag_overflow = []

        separated_tags = group.tags.split()

        if len(separated_tags) > 5:
            search_tags = ' '.join(separated_tags[0:5])

            for tag in separated_tags:
                if tag not in search_tags.split():
                    tag_overflow.append(tag)

        else:
            search_tags = group.tags

        while accumulating:
            links_found = api.get_posts(search_tags, check_date, current_page, const.MAX_RESULTS)

            if not links_found:
                accumulating = False

            else:
                post_list += links_found
                accumulating = len(links_found) == const.MAX_RESULTS
                current_page += 1

        if len(post_list) > 0:
            for i, post in enumerate(post_list):
                core.print_log('e621dl', 'debug', 'Item ' + str(i) + '\'s id is \"' + str(post.id) + '\".')

                filename = core.make_path(group.directory, post)
                current_tags = post.tags.split()

                if len(separated_tags) > 5 and not list(set(tag_overflow) & set(current_tags)):
                    links_missing_tags += 1
                    core.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Missing a requested tag.')

                elif list(set(blacklist) & set(current_tags)):
                    links_blacklisted += 1
                    core.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Contains a blacklisted tag.')

                elif os.path.isfile(filename):
                    links_on_disk += 1
                    core.print_log('e621dl', 'debug', 'Item ' + str(i) + ' was skipped. Already downloaded previously.')

                else:
                    core.print_log('e621dl', 'debug', 'Item ' + str(i) + ' will be downloaded.')
                    download_list.append((post.url, filename))
                    will_download += 1

            core.print_log('e621dl', 'info', str(will_download) + ' new files. (' + str(len(post_list)) + ' found, ' +
            str(links_missing_tags) + ' missing tags, ' + str(links_blacklisted) +
            ' blacklisted, ' + str(links_on_disk) + ' duplicate.)')

            print('')

        else:
            core.print_log('e621dl', 'info', '0 new files.')
            print('')

    if download_list:
        core.print_log('e621dl', 'info', 'Starting download of ' + str(len(download_list)) + ' files.')
        downloader.multi_download(download_list, cpu_count())
        print('')

        core.print_log('e621dl', 'info', 'Checking downloads for damaged files.')
        core.check_md5s()

    else:
        core.print_log('e621dl', 'info', 'Nothing to download.')

    sys.exit(0)
