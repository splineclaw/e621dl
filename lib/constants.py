MAX_RESULTS = 320
DATE_FORMAT = '%Y-%m-%d'
LOGGER_FORMAT = '%(name)-11s %(levelname)-8s %(message)s'
VERSION = '4.1.1 -- Forked from 2.4.6'

DEFAULT_CONFIG_TEXT = ''';;;;;;;;;;;;;;
;; GENERAL  ;;
;;;;;;;;;;;;;;

[Defaults]
days_to_check = 1
ratings = s
min_score = 0

[Blacklist]
tags =

;;;;;;;;;;;;;;;;
;; TAG GROUPS ;;
;;;;;;;;;;;;;;;;

; New tag groups can be created by writing the following. (Do not include semicolons.):
; [Directory Name]
; days_to_check = 1
; ratings = s, q, e
; min_score = -100
; tags = tag1, tag2, tag3, ...

; Example:
; [Cute Cats]
; days_to_check = 30
; ratings = s
; min_score = 5
; tags = cat, cute'''
