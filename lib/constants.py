#!/usr/bin/env python

import datetime

DATE_FORMAT = "%Y-%m-%d"
YESTERDAY = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
LOGGER_FORMAT = "%(name)-11s %(levelname)-8s %(message)s"
MAX_RESULTS = 100
VERSION = '3.1.0 -- Forked from 2.4.6'

DEFAULT_CONFIG_TEXT = ''';;;;;;;;;;;;;;;;;;;
;; MAIN SETTINGS ;;
;;;;;;;;;;;;;;;;;;;

[Settings]
last_run = ''' + YESTERDAY.strftime(DATE_FORMAT) + '''
parallel_downloads = 8

[Blacklist]
tags =

;;;;;;;;;;;;;;;;
;; TAG GROUPS ;;
;;;;;;;;;;;;;;;;

; New tag groups can be created by writing the following:
; [Directory Name]
; tags = tag1, tag2, tag3, ...
;
; Example:
; [Cute Cats]
; tags = rating:s, cat, cute'''
