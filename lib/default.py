#!/usr/bin/env python

from datetime import datetime

DATETIME_FMT = "%Y-%m-%d"
LOGGER_FMT = "%(name)-11s %(levelname)-8s %(message)s"
MAX_RESULTS = 100

CONFIG_FILE = {
    'cache_name':   ".cache",
    'cache_size':   65536,
    'download_directory':    "downloads/",
    'file_name':    "id",
    'last_run':     datetime.now().strftime(DATETIME_FMT),
    'parallel_downloads':   8,
    'create_subdirectories': True
}

TAG_FILE = '''# NOTE: All lines in this file that begin with # are treated as comments and are
# ignored by e621dl.
#
# Add any tags or meta-tags for posts you would like to download to this file. Each line in this
# file will be treated as a separate group, and a new folder inside the downloads directory will be
# created for each group.
#
# If your group contains more than 5 tags, e621dl will try to automatically convert all additional
# tags to their proper alias and filter posts found from the first 5 tags. Until this feature is
# more thoroughly developed, you may need to consult the e621 tag list
# (https://e621.net/tag_alias/) and manually convert aliases that do not get converted
# automatically. Otherwise, it would be greatly appreciated that you test the automatic tag
# conversion and report any issues.
#
# One side effect of the workaround used to search an unlimited number tags is that you may only
# use up to 5 meta tags `:`, negative tags `-`, operational tags `~`, or wildcard tags `*` per
# group, and they must be the first 5 items in the group. See the e621 cheatsheet
# (https://e621.net/help/show/cheatsheet) for more information on these special types of tags.
'''

BLACKLIST_FILE = '''# NOTE: All lines in this file that begin with # are treated as comments and
# are ignored by e621dl.
#
# Add any tags for posts you would like to avoid downloading to this file. Meta tags `:`, negative
# tags `:`, operational tags `~`, and wildcard tags `*` will currently break the script, as they
# are not filtered out of the blacklist, so do not use them in this file.
#
# e621dl will try to automatically convert all tags to their proper aliases. Until this feature is
# more thoroughly developed, you may want to check your tags against the e621 tag list
# (https://e621.net/tag_alias/) and manually convert any tags for content you absolutely do not
# want to see. Otherwise, it would be greatly appreciated that you test the automatic tag
# conversion and report any issues.
#
# Give each tag its own new line.
'''
