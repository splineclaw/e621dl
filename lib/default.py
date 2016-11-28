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
# Add any tags or meta-tags for posts you would like to download to this file.
#
#
# Each line in this file will be treated as a separate group, and a new folder inside the downloads
# directory will be created for each group.
#
# IF YOUR GROUP CONTAINS MORE THAN 5 TAGS, PLEASE CHECK THE E621 WIKI AND MAKE SURE TO CONVERT TAG
# ALIASES. DUE TO THE NATURE OF E621'S SEARCH FUNCTION, ONLY 5 TAGS CAN BE CONVERTED AUTOMATICALLY.
# ALL ADITIONAL TAGS ARE MANUALLY CHECKED BY E621DL. ANOTHER SIDE EFFECT OF THIS WORKAROUND IS THAT
# YOU MAY ONLY USE UP TO 5 META-TAGS PER GROUP, AND THEY MUST BE THE FIRST 5 ITEMS ON THE LINE.
#
'''

BLACKLIST_FILE = '''# NOTE: All lines in this file that begin with # are treated as comments and
# are ignored by e621dl.
#
# Add any tags for posts you would like to AVOID downloading to this file. Meta-tags will currently
# break the script, so do not use them in this file.
#
# PLEASE CHECK THE E621 WIKI AND MAKE SURE TO CONVERT TAG ALIASES. THIS SCRIPT, CURRENTLY, CAN
# ONLY BLACKLIST OFFICIAL TAGS.
#
# Give each tag its own new line.
#
'''
