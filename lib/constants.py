VERSION = '4.2.3'
VERSION_NOTE = 'Forked from 2.4.6'
USER_AGENT = 'e621dl (Wulfre) -- Version ' + VERSION

MAX_RESULTS = 320
DATE_FORMAT = '%Y-%m-%d'
LOGGER_FORMAT = '%(name)-11s %(levelname)-8s %(message)s'

DEFAULT_CONFIG_TEXT = ''';;;;;;;;;;;;;;
;; GENERAL  ;;
;;;;;;;;;;;;;;

[Defaults]
days = 1
ratings = s
min_score = 0

[Blacklist]
tags =

;;;;;;;;;;;;;;;;;;;
;; SEARCH GROUPS ;;
;;;;;;;;;;;;;;;;;;;

; New search groups can be created by writing the following. (Do not include semicolons.):
; [Directory Name]
; days = 1
; ratings = s, q, e
; min_score = -100
; tags = tag1, tag2, tag3, ...

; Example:
; [Cute Cats]
; days = 30
; ratings = s
; min_score = 5
; tags = cat, cute'''
