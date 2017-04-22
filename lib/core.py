#!/usr/bin/env python

import argparse
import logging
import os
import configparser
from urllib.request import FancyURLopener
from . import vars
import hashlib
import re

class SpoofOpen(FancyURLopener):
    version = 'e621dl / ' + vars.VERSION + ' / by Wulfre (GitHub)'

def get_verbosity():
    parser = argparse.ArgumentParser(prog = 'e621dl', description = 'An automated e621 downloader.')

    verbosity = parser.add_mutually_exclusive_group(required = False)
    verbosity.add_argument('-v', '--verbose', action = 'store_true', help = 'Display full debug \
        information while running.')
    verbosity.add_argument('-q', '--quiet', action = 'store_true', help = 'Display no output while \
        running, except for errors.')

    args = parser.parse_args()

    if args.quiet:
        return logging.ERROR
    elif args.verbose:
        return logging.DEBUG
    else:
        return logging.INFO

def print_log(logModule, logLevel, logMessage):
    log = logging.getLogger(logModule)
    getattr(log, logLevel)(logMessage)

def make_config(filename):
    with open(filename, 'w') as outfile:
        outfile.write(vars.DEFAULT_CONFIG_TEXT)
        print_log('config', 'info', 'New default file created: \"' + filename + '\".')

def get_config(filename):
    config = configparser.ConfigParser()

    if not os.path.isfile(filename):
        print_log('config', 'error', 'No config file found.')
        make_config(filename)

    with open(filename, 'r') as infile:
        config.read_file(infile)
        return config

def validate_tags(config):
    sections = 0
    for _ in config.sections():
        sections += 1

    if sections < 3:
        print_log('tags', 'error', 'Please add at least one tag group to \"config.ini\".')
        return True
    else:
        return False

def substitute_illegals(char):
    illegals = ['\\', ':', '*', '?', '\"', '<', '>', '|', ' ']
    return '_' if char in illegals else char

def make_path(dirName, post):
    cleanDirName = ''.join([substitute_illegals(char) for char in dirName]).lower()

    if not os.path.isdir('downloads/' + cleanDirName):
        os.makedirs('downloads/' + cleanDirName)

    path = 'downloads/' + cleanDirName + '/' + str(post.id) + '-' + \
    post.md5 + '.' + post.ext

    return path

def check_md5s():
    BYTE_SIZE = 65536
    numBadHashes = 0

    for root, dirs, files in os.walk('downloads'):
        for fileName in files:
            verifiedHash = fileName[fileName.find('-') + 1:fileName.find('.')]
            md5lib = hashlib.md5()

            with open(os.path.join(root, fileName), 'rb') as openfile:
                while True:
                    data = openfile.read(BYTE_SIZE)
                    if not data:
                        break
                    md5lib.update(data)

            hashSubstring = re.finditer(r'(?=(\b[A-Fa-f0-9]{32}\b))', verifiedHash)
            isValidHash = [match.group(1) for match in hashSubstring]

            if not md5lib.hexdigest() == verifiedHash and isValidHash:
                os.remove(os.path.join(root, fileName))
                numBadHashes += 1

    if numBadHashes > 0:
        print_log('e621dl', 'info', 'Removed ' + str(numBadHashes) + ' damaged files.')
    else:
        print_log('e621dl', 'info', 'No damaged files were found.')
