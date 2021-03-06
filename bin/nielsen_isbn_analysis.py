#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import getopt
from collections import OrderedDict

from nielsenTools.database_tools import *
from nielsenTools.functions import *

# Set threshold for garbage collection (helps prevent the program run out of memory)
gc.set_threshold(400, 5, 5)

# Increase CSV field size limit because some fields are ENORMOUS
csv.field_size_limit(2147483647)

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#     Constants
# ====================


OPTIONS = OrderedDict([
    ('B', 'Search for clusters within BL data'),
    # ('M', 'Parse ISBNs from MARC file'),
    ('N', 'Parse ISBNs from Nielsen cluster files'),
    ('O', 'Parse Nielsen Organisation files'),
    ('P', 'Parse Nielsen Product files'),
    # ('T', 'Parse ISBNs from TSV file'),
    ('S', 'Search for ISBNs'),
    ('X', 'eXport graph'),
    ('E', 'Exit program'),
])


ACTIONS = {
    'B': search_bl,
    # 'M': parse_marc,
    'N': parse_nielsen,
    'O': parse_nielsen_org,
    'P': parse_nielsen_product,
    # 'T': parse_tsv,
    'S': search_isbns,
    'X': export_graph,
    'E': sys.exit,
}

EXTENSIONS = {
    'B': ('.lex',),
    'M': ('.lex',),
    'N': ('.add', '.del', '.upd'),
    'T': ('.tsv',),
    'S': ('.txt',),
}

NO_INPUT = ['I', 'X', 'E']


# ====================
#       Classes
# ====================


class OptionHandler:

    def __init__(self, input_path, selected_option=None, skip_check=False):
        self.input_path = input_path
        self.selection = None
        self.skip_check = skip_check
        if selected_option in OPTIONS:
            self.selection = selected_option
        else:
            self.get_selection()

    def get_selection(self):
        print('\n----------------------------------------')
        print('\n'.join('{}:\t{}'.format(opt, OPTIONS[opt]) for opt in OPTIONS))
        self.selection = input('Choose an option:').upper().strip()
        while self.selection not in OPTIONS:
            self.selection = input('Sorry, your choice was not recognised. '
                                   'Please enter one of {}:'.format(', '.join(opt for opt in OPTIONS))).upper()

    def set_selection(self, selected_option):
        if selected_option in OPTIONS:
            self.selection = selected_option

    def execute(self):

        if self.selection not in OPTIONS:
            self.get_selection()

        date_time(message(OPTIONS[self.selection]))

        if self.selection == 'E':
            sys.exit()

        ACTIONS[self.selection](self.input_path, self.skip_check)
        self.selection = None
        return


# ====================
#      Functions
# ====================


def usage():
    """Function to print information about the program"""
    print('Correct syntax is:')
    print('nielsen_isbn_analysis -i <input_path> [options]')
    print('    -i    path to FOLDER containing Input files')
    print('If not specified, input path will be /Input')
    print('\nUse quotation marks (") around arguments which contain spaces')
    print('\nOptions')
    print('EXACTLY ONE of the following:')
    for o in OPTIONS:
        print('    -{}    {}'.format(o.lower(), OPTIONS[o]))
    print('ANY of the following:')
    print('    -c        Check ISBN format conflicts using Google Books API')
    print('    --help    Display this message and exit')
    print('Option -i is not required with options {}'.format(', '.join(o.lower() for o in NO_INPUT)))
    for o in EXTENSIONS:
        print('If option -{} is selected, input files should end {}'.format(o.lower(), ', '.join(EXTENSIONS[o])))
    exit_prompt()


# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    selected_option = None
    skip_check = True

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_path = os.path.join(dir, 'Input', 'Nielsen')

    print('========================================')
    print('nielsen_isbn_analysis')
    print('========================================')
    print('\nThis program analyses data relating to ISBN relationships\n')
    magician()

    try: opts, args = getopt.getopt(argv, 'i:c' + ''.join(o.lower() for o in OPTIONS),
                                    ['input_path=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage()
        elif opt in ['-i', '--input_path']: input_path = arg
        elif opt == '-c': skip_check = False
        elif opt.upper().strip('-') in OPTIONS:
            selected_option = opt.upper().strip('-')
        else: exit_prompt('Error: Option {} not recognised'.format(opt))

    if selected_option == 's' and 'i' not in set(opt for opt, arg in opts):
        input_path = os.path.join(dir, 'Input', 'Search_lists')
    # Check that files exist
    if selected_option not in NO_INPUT and not input_path:
        exit_prompt('Error: No path to input files has been specified')
    if selected_option not in NO_INPUT and not os.path.isdir(input_path):
        exit_prompt('Error: Invalid path to input files')
    if not os.path.isfile(DATABASE_PATH):
        exit_prompt('Error: The file {} cannot be found'.format(DATABASE_PATH))

    if skip_check: print('ISBN format conflicts will not be checked')

    option = OptionHandler(input_path, selected_option, skip_check)

    while option.selection:
        option.execute()
        option.get_selection()

    date_time_exit()


if __name__ == '__main__':
    main(sys.argv[1:])
