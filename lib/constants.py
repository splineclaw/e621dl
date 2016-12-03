#!/usr/bin/env python

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
LOGGER_FORMAT = "%(name)-11s %(levelname)-8s %(message)s"
MAX_RESULTS = 100

VERSION = '3.0.0 -- Forked from 2.4.6'

CONFIG_FILE = '''[Settings]
file_name = id
last_run = ''' + datetime.now().strftime(DATE_FORMAT) + '''
parallel_downloads = 8

[Blacklist]
tags =

# New tag groups can be created by writing the following:
# [Folder Name]
# tags = tag1, tag2, tag3
#
# Example:
# [Cute Cats]
# tags = rating:s, cat, cute'''
