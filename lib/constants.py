MAX_RESULTS = 320
DATE_FORMAT = '%Y-%m-%d'
LOGGER_FORMAT = '%(name)-11s %(levelname)-8s %(message)s'
VERSION = '4.0.1 -- Forked from 2.4.6'


DEFAULT_CONFIG_TEXT = ''';;;;;;;;;;;;;;;;;;;
;; MAIN SETTINGS ;;
;;;;;;;;;;;;;;;;;;;

; You may set connection_timeout to a negative number to allow the connection to be attempted indefinitely, however if e621's servers are down, the program will never exit on its own.
; This is not recommended unless your internet connection is extremely unreliable. If you need to force exit the program, press CTRL + C.

[Settings]
days_to_check = 1

[Blacklist]
tags =

;;;;;;;;;;;;;;;;
;; TAG GROUPS ;;
;;;;;;;;;;;;;;;;

; New tag groups can be created by writing the following. (Do not include semicolons.):
; [Directory Name]
; ratings = s, q, e
; min_score = -100
; tags = tag1, tag2, tag3, ...

; Example:
; [Cute Cats]
; ratings = s
; min_score = 5
; tags = cat, cute'''
