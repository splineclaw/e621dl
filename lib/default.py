#!/usr/bin/env python
# pylint: disable=bad-whitespace, missing-docstring

from datetime import datetime

DATETIME_FMT = "%Y-%m-%d"
LOGGER_FMT = "%(name)-11s %(levelname)-8s %(message)s"
MAX_RESULTS = 100

CONFIG_FILE = {
    'cache_name':   ".cache",
    'cache_size':   65536,
    'download_directory':    "downloads/",
    'part_used_as_name':    "id",
    'last_run':     datetime.now().strftime(DATETIME_FMT),
    'parallel_downloads':   8,
    'create_subdirectories': True
}

TAG_FILE = '''# NOTE: All lines in this file that begin with # are treated as comments and are
# ignored by e621dl.
#
# Add any tags for posts you would like to download to this file. Any tag combination that works on
# the web site will work here, including all meta-tags.
# See https://e621.net/help/cheatsheet for more information.
#
# Each line in this file will be treated as a separate group, and a new folder inside the downloads
# directory will be created for each group.
#
'''

BLACKLIST_FILE = '''# NOTE: All lines in this file that begin with # are treated as comments and
# are ignored by e621dl.
#
# Add any tags for posts you would like to AVOID downloading to this file. Meta-tags will break the
# program, so do not use them in this file.
#
# Please include each blacklist tag on a different line.
#
'''
