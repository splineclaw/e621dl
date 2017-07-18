#!/usr/bin/env python3

import argparse
import configparser
import hashlib
import logging
import os
import re

from . import constants

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

def print_log(log_module, log_level, log_message):
    log = logging.getLogger(log_module)
    getattr(log, log_level)(log_message)

def make_config(path):
    with open(path, 'w') as outfile:
        outfile.write(constants.DEFAULT_CONFIG_TEXT)
        print_log('config', 'info', 'New default file created: \"' + path + '\".')

def get_config(path):
    config = configparser.ConfigParser()

    if not os.path.isfile(path):
        print_log('config', 'error', 'No config file found.')
        make_config(path)

    with open(path, 'r') as infile:
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

def make_path(dir_name, post):
    clean_dir_name = ''.join([substitute_illegals(char) for char in dir_name]).lower()

    if not os.path.isdir('downloads/' + clean_dir_name):
        os.makedirs('downloads/' + clean_dir_name)

    path = 'downloads/' + clean_dir_name + '/' + str(post.id) + '-' + \
    post.md5 + '.' + post.ext

    return path

def check_md5s():
    BYTE_SIZE = 65536
    bad_hashes = 0

    for root, dirs, files in os.walk('downloads'):
        for path in files:
            md5lib = hashlib.md5()

            with open(os.path.join(root, path), 'rb') as infile:
                while True:
                    data = infile.read(BYTE_SIZE)
                    if not data:
                        break
                    md5lib.update(data)

            hash_substring = re.findall(r'(?=(\b[A-Fa-f0-9]{32}\b))', path)

            if not hash_substring == [] and not md5lib.hexdigest() == hash_substring[0]:
                os.remove(os.path.join(root, path))
                bad_hashes += 1

    if bad_hashes > 0:
        print_log('e621dl', 'info', 'Removed ' + str(bad_hashes) + ' damaged files.')
    else:
        print_log('e621dl', 'info', 'No damaged files were found.')

def update_progressbar(partial, total):
    BAR_LENGTH = 36

    progress = partial / total
    completed_segments = int(round(BAR_LENGTH * progress))

    progress_bar = '\rDownloading          |{}| {}% {}'.format('█' * completed_segments +
        ' ' * (BAR_LENGTH - completed_segments), int(round(progress * 100)),
        '(' + str(partial) + ' / ' + str(total) + ')')

    print(progress_bar, end='')
