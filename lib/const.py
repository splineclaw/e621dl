#!/usr/bin/env python

DATE_FORMAT = "%Y-%m-%d"
LOGGER_FORMAT = "%(name)-11s %(levelname)-8s %(message)s"
MAX_RESULTS = 100
VERSION = '3.1.1 -- Forked from 2.4.6'

DEFAULT_CONFIG_TEXT = ''';;;;;;;;;;;;;;;;;;;
;; MAIN SETTINGS ;;
;;;;;;;;;;;;;;;;;;;

[Settings]
days_to_check = 1

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
