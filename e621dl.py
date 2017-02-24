#!/usr/bin/env python

def pip_install(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

import logging
import os
import sys
from multiprocessing import freeze_support, cpu_count
from collections import namedtuple
from lib import constants, support, api, downloader

pip_install('imghdr')

if __name__ == '__main__':
    freeze_support()

    logging.basicConfig(level = support.get_verbosity(), format = constants.LOGGER_FORMAT,
        stream = sys.stderr)
    LOG = logging.getLogger('e621dl')
    LOG.info('Running e621dl version ' + constants.VERSION + '.')

    CONFIG = support.get_config('config.ini')

    early_terminate = False
    early_terminate |= not downloader.internet_connected()
    early_terminate |= support.validate_tags(CONFIG)

    if early_terminate:
        LOG.info('Error(s) occurred during initialization, see above for more information.')
        sys.exit(-1)

    GROUP = namedtuple('Group', 'tags directory')
    blacklist = []
    tag_groups = []

    LOG.info('Parsing config.')

    for section in CONFIG.sections():
        if section == 'Settings':
            pass
        elif section == 'Blacklist':
            for tag in CONFIG.get('Blacklist', 'tags').replace(',', '').split():
                blacklist.append(api.get_alias(tag))
        else:
            for option, value in CONFIG.items(section):
                if option == 'tags':
                    tag_groups.append(GROUP(value.replace(',', ''), section))

    print ''

    LOG.info('Searching download directory for damaged files.')

    prunedFiles = 0

    for root, dirs, files in os.walk('downloads'):
        for file in files:
            if imghdr.what(os.path.join(root, file)) == None:
                prunedFiles += 1
                os.remove(os.path.join(root, file))
                LOG.debug('Removed ' + os.path.join(root, file) + '.')

    if prunedFiles > 0:
        LOG.info('Removed ' + str(prunedFiles) + ' damaged files.')
    else:
        LOG.info('No damaged files were found.')

    print ''

    LOG.info('Looking for new posts since ' + CONFIG.get('Settings', 'last_run') + '.')
    print ''

    download_list = []

    for group in tag_groups:
        LOG.info('Checking for new posts tagged: \"' + group.tags.replace(' ', ', ') + '\".')

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
                    tag_overflow.append(api.get_alias(tag))

        else:
            search_tags = group.tags

        while accumulating:
            links_found = api.get_posts(search_tags, CONFIG.get('Settings', 'last_run'),
            current_page, constants.MAX_RESULTS)

            if not links_found:
                accumulating = False

            else:
                post_list += links_found
                accumulating = len(links_found) == constants.MAX_RESULTS
                current_page += 1

        if len(post_list) > 0:
            for i, post in enumerate(post_list):
                LOG.debug('Item ' + str(i) + '\'s id is \"' + str(post.id) + '\".')

                filename = support.make_filename(group.directory, post)
                current_tags = post.tags.split()

                if len(separated_tags) > 5 and not list(set(tag_overflow) & set(current_tags)):
                    links_missing_tags += 1
                    LOG.debug('Item ' + str(i) + ' was skipped. Missing a requested tag.')

                elif list(set(blacklist) & set(current_tags)):
                    links_blacklisted += 1
                    LOG.debug('Item ' + str(i) + ' was skipped. Contains a blacklisted tag.')

                elif os.path.isfile(filename):
                    links_on_disk += 1
                    LOG.debug('Item ' + str(i) + ' was skipped. Already downloaded previously.')

                else:
                    LOG.debug('Item ' + str(i) + ' will be downloaded.')
                    download_list.append((post.url, filename))
                    will_download += 1

            LOG.info(str(will_download) + ' new files. (' + str(len(post_list)) + ' found, ' +
            str(links_missing_tags) + ' missing tags, ' + str(links_blacklisted) +
            ' blacklisted, ' + str(links_on_disk) + ' duplicate.)')
            print ''

        else:
            LOG.info('0 new files.')
            print ''

    if download_list:
        LOG.info('Starting download of ' + str(len(download_list)) + ' files.')
        downloader.multi_download(download_list, cpu_count())
        print ''
        LOG.info('Successfully downloaded ' + str(len(download_list)) + ' files.')
    else:
        LOG.info('Nothing to download.')

    CONFIG.set('Settings', 'last_run', constants.YESTERDAY.strftime(constants.DATE_FORMAT))
    CONFIG.write(open('config.ini', 'w'))

    sys.exit(0)
