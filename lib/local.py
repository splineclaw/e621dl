import argparse
import configparser
import logging
import os

from . import constants

def get_verbosity():
    parser = argparse.ArgumentParser(prog = 'e621dl', description = 'An automated e621 downloader.')
    verbosity = parser.add_mutually_exclusive_group(required = False)

    verbosity.add_argument('-v', '--verbose', action = 'store_true', help = 'Display full debug information while running.')
    verbosity.add_argument('-q', '--quiet', action = 'store_true', help = 'Display no output while running, except for errors.')

    args = parser.parse_args()

    if args.quiet:
        return logging.ERROR
    elif args.verbose:
        return logging.DEBUG

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

def tags_valid(config):
    for section in config.sections():
        if section.lower() == 'settings' or section.lower() == 'blacklist':
            pass
        else:
            return True

    print_log('config', 'error', 'No tag groups found.')
    return False

def substitute_illegals(char):
    illegals = ['\\', ':', '*', '?', '\"', '<', '>', '|', ' ']

    return '_' if char in illegals else char

def make_path(dir_name, post):
    clean_dir_name = ''.join([substitute_illegals(char) for char in dir_name]).lower()

    if not os.path.isdir('downloads/' + clean_dir_name):
        os.makedirs('downloads/' + clean_dir_name)

    return 'downloads/' + clean_dir_name + '/' + str(post[0]) + '-' + post[1] + '.' + post[2]
