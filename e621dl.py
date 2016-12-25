import logging
import lib.constants as constants
import sys
import lib.support as support
import ConfigParser
import os
import lib.api as api
from collections import namedtuple
import lib.downloader as downloader
from multiprocessing import freeze_support
import datetime

if __name__ == '__main__':
    freeze_support()

    logging.basicConfig(level = support.get_verbosity(), format = constants.LOGGER_FORMAT,
        stream = sys.stderr)
    log = logging.getLogger('e621dl')
    log.info('Running e621dl version ' + constants.VERSION + '.')

    earlyTerminate = False

    earlyTerminate |= not downloader.internet_connected()

    earlyTerminate |= not os.path.isfile('config.ini')
    config = support.get_config('config.ini')

    earlyTerminate |= support.validate_tags(config)

    if earlyTerminate:
        log.info('Error(s) occurred during initialization, see above for more information.')
        sys.exit(-1)

    GROUP = namedtuple('Group', 'tags directory')
    blacklist = []
    tagGroups = []

    for section in config.sections():
        if section == 'Settings':
            pass
        elif section == 'Blacklist':
            for tag in config.get('Blacklist', 'tags').replace(',', '').split():
                blacklist.append(api.get_alias(tag))
        else:
            for option, value in config.items(section):
                if option == 'tags':
                    tagGroups.append(GROUP(value.replace(',', ''), section))

    log.info('e621dl was last run on ' + config.get('Settings', 'last_run') + '.')

    downloadList = []

    for group in tagGroups:
        log.info('Checking for new posts tagged: \"' + group.tags + '\".')

        accumulating = True
        currentPage = 1
        linksMissingTags = 0
        linksBlacklisted = 0
        linksOnDisk = 0
        willDownload = 0
        postList = []
        tagOverflow = []

        separatedTags = group.tags.split()

        if len(separatedTags) > 5:
            searchTags = ' '.join(separatedTags[0:5])

            for tag in separatedTags:
                if tag not in searchTags.split():
                    tagOverflow.append(api.get_alias(tag))

        else:
            searchTags = group.tags

        while accumulating:
            linksFound = api.get_posts(searchTags, config.get('Settings', 'last_run'),
            currentPage, constants.MAX_RESULTS)

            if not linksFound:
                accumulating = False

            else:
                postList += linksFound
                accumulating = len(linksFound) == constants.MAX_RESULTS
                currentPage += 1

        if len(postList) > 0:
            for i, post in enumerate(postList):
                log.debug('Item ' + str(i) + '\'s md5 is \"' + post.md5 + '\", and its id is ' +
                    '\"' + str(post.id) + '\".')

                filename = support.make_filename(group.directory, post, config)
                currentTags = post.tags.split()

                if len(separatedTags) > 5 and list(set(tagOverflow) & set(currentTags)) == []:
                    linksMissingTags += 1
                    log.debug('Item ' + str(i) + ' was skipped. Missing a requested tag.')

                elif list(set(blacklist) & set(currentTags)) != []:
                    linksBlacklisted += 1
                    log.debug('Item ' + str(i) + ' was skipped. Contains a blacklisted tag.')

                elif os.path.isfile(filename):
                    linksOnDisk += 1
                    log.debug('Item ' + str(i) + ' was skipped. Already downloaded previously.')

                else:
                    log.debug('Item ' + str(i) + ' will be downloaded.')
                    downloadList.append((post.url, filename))
                    willDownload += 1

            log.info(str(willDownload) + ' new files. (' + str(len(postList)) + ' found, ' +
            str(linksMissingTags) + ' missing tags, ' + str(linksBlacklisted) + ' blacklisted, ' +
            str(linksOnDisk) + ' duplicate.)')

    if downloadList:
        log.info('Starting download of ' + str(len(downloadList)) + ' files.')
        downloader.multi_download(downloadList, config.getint('Settings', 'parallel_downloads'))
        log.info('Successfully downloaded ' + str(len(downloadList)) + ' files.')
    else:
        log.info('Nothing to download.')

    yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)

    with open('config.ini', 'w') as outfile:
        config.set('Settings', 'last_run', yesterday.strftime(constants.DATE_FORMAT))
        config.write(outfile)

    log.info('Last run date updated to ' + config.get('Settings', 'last_run') + '.')
    sys.exit(0)
