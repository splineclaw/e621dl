#!/usr/bin/env python

from urllib import FancyURLopener
import argparse
import logging
import constants
import ConfigParser
import os

class SpoofOpen(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) ' + \
        'Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'

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

def make_config(filename):
    log = logging.getLogger('config')

    with open(filename, 'w') as outfile:
            outfile.write(constants.CONFIG_FILE)
            log.info('New default file created: \"' + filename + '\".')

def get_config(filename):
    log = logging.getLogger('config')
    config = ConfigParser.ConfigParser()

    if not os.path.isfile(filename):
        log.error('No config file found.')
        return make_config(filename)
    else:
        with open(filename, 'r') as infile:
            config.readfp(infile)
            return config

def validate_tags(config):
    log = logging.getLogger('tags')

    sections = 0
    for section in config.sections():
        sections += 1

    if sections < 3:
        log.error('Please add at least one tag group to \"config.ini\".')
        return True
    else:
        return False



def substitute_illegals(char):
    illegals = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|', ' ']
    return '_' if char in illegals else char

def make_filename(directory_name, post, config):
    safe_directory = ''.join([substitute_illegals(char) for char in directory_name])
    name = str(getattr(post, config.get('Settings', 'file_name')))

    if not os.path.isdir('downloads/' + safe_directory.decode('utf-8')):
        os.makedirs('downloads/' + safe_directory)

    filename = 'downloads/' + safe_directory + '/' + name + '.' + post.ext

    return filename
