#!/usr/bin/env python
# -*- coding: utf8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
from collections import OrderedDict
import datetime
import os
import gc
import getopt
import glob
from nielsenTools.marc_data import *
from nielsenTools.database_tools import *
from nielsenTools.nielsen_tools import *
from nielsenTools.functions import *
import locale
import regex as re
import sqlite3
import sys

# Set locale to assist with sorting
locale.setlocale(locale.LC_ALL, '')

# Set threshold for garbage collection (helps prevent the program run out of memory)
gc.set_threshold(400, 5, 5)

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#     Constants
# ====================


OPTIONS = OrderedDict([
    ('M', 'Parse ISBNs from MARC field'),
    ('N', 'Parse ISBNs from Nielsen CSV file'),
    ('S', 'Search for ISBNs'),
    ('X', 'eXport graph'),
    ('E', 'Exit program'),
])


# ====================
#       Classes
# ====================


class OptionHandler():

    def __init__(self, input_path, selected_option=None, skip_check=False, quit=False):
        self.input_path = input_path
        self.selection = None
        if selected_option in OPTIONS:
            self.selection = selected_option
        else: self.get_selection()
        self.skip_check = skip_check
        self.quit = quit

    def get_selection(self):
        print('\n')
        print('----------------------------------------')
        print('\n'.join('{}:\t{}'.format(opt, OPTIONS[opt]) for opt in OPTIONS))
        self.selection = input('Choose an option:').upper()
        while self.selection not in OPTIONS:
            self.selection = input('Sorry, your choice was not recognised. '
                                   'Please enter one of {}:'.format(', '.join(opt for opt in OPTIONS))).upper()


    def set_selection(self, selected_option):
        if selected_option in OPTIONS:
            self.selection = selected_option

    def execute(self, search_path=None):

        if self.selection not in OPTIONS:
            self.get_selection()

        if self.selection == 'E':
            print('\n\nShutting down ...')
            print('----------------------------------------')
            print(str(datetime.datetime.now()))
            sys.exit()

        if self.selection == 'X':
            print('\n\nWriting graph ...')
            print('----------------------------------------')
            print(str(datetime.datetime.now()))
            export_database()
            self.input_path = None
            self.selection = None
            return

        if self.selection == 'M':
            print('\n\nParsing MARC files ...')
            print('----------------------------------------')
            print(str(datetime.datetime.now()))
            while self.input_path is None:
                self.input_path = input('Please enter the file path: ').strip('"')
            add_from_marc_files(self.input_path, self.skip_check)
            self.input_path = None
            self.selection = None
            return

        if self.selection == 'N':
            print('\n\nParsing Nielsen files ...')
            print('----------------------------------------')
            print(str(datetime.datetime.now()))
            while self.input_path is None:
                self.input_path = input('Please enter the file path: ').strip('"')
            add_from_nielsen_files(self.input_path, self.skip_check)
            self.input_path = None
            self.selection = None
            return

        if self.selection == 'S':
            print('\n\nSearching for ISBNs ...')
            print('----------------------------------------')
            print(str(datetime.datetime.now()))
            while search_path is None:
                search_path = input('Please enter the file path: ').strip('"')
            search_for_isbns(search_path)
            self.input_path = None
            self.selection = None
            if self.quit: date_time_exit()
            return

        self.get_selection()

# ====================
#      Functions
# ====================


def usage():
    """Function to print information about the program"""
    print('Correct syntax is:')
    print('nielsen_isbn_analysis [options]')
    print('\nOptions')
    print('AT MOST ONE of the following:')
    print('    -m    path to folder containing MARC files to be parsed')
    print('          Input file names should end .lex')
    print('    -n    path to folder containing Nielsen files to be parsed')
    print('          Input file names should end .add, .upd or .del')
    print('    -s    path to file containing ISBNs to be searched for')
    print('    -x    eXport graph')
    print('ANY of the following:')
    print('    --help    Display this message and exit')
    print('\nIf no options are specified, -n is assumed, with input folder Input\ISBNs')
    print('\nUse quotation marks (") around arguments which contain spaces')
    exit_prompt()


# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_path = os.path.join(dir, 'Input', 'ISBNs')

    search_list = None
    selected_option = 'N'
    skip_check = True
    quit = True

    print('========================================')
    print('nielsen_isbn_analysis')
    print('========================================')
    print('\nThis program collects ISBN cluster information\n'
          'from Nielsen CSV files\n')

    try:
        opts, args = getopt.getopt(argv, 'cn:m:qs:x', ['mpath=', 'npath=', 'search_list=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage()
        elif opt in ['-m', '--mpath']:
            selected_option = 'M'
            input_path = arg
        elif opt in ['-n', '--npath']:
            selected_option = 'N'
            input_path = arg
        elif opt in ['-s', '--search_list']:
            selected_option = 'S'
            quit = True
            search_list = arg
        elif opt == '-x': selected_option = 'X'
        elif opt == '-c': skip_check = False
        elif opt == '-q': quit = False
        else: exit_prompt('Error: Option {} not recognised'.format(opt))

    # Check that files exist

    if selected_option in ['M', 'N']:
        if not input_path:
            exit_prompt('Error: No path to input files has been specified')
        if not os.path.isdir(input_path):
            exit_prompt('Error: Invalid path to input files')

    if not os.path.isfile(DATABASE_PATH):
        exit_prompt('Error: The file {} cannot be found'.format(DATABASE_PATH))
    if skip_check: print('ISBN formats will not be checked')

    # --------------------
    # Parameters seem OK => start program
    # --------------------

    # Display confirmation information about the transformation

    if selected_option in ['M', 'N']:
        print('Input folder: {}'.format(input_path))

    option = OptionHandler(input_path, selected_option, skip_check, quit)

    while option.selection:
        option.execute(search_path=search_list)
        option.get_selection()

    date_time_exit()

if __name__ == '__main__':
    main(sys.argv[1:])
