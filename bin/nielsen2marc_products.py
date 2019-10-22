#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import getopt
import math
from nielsenTools.isbn_tools import *
from nielsenTools.nielsen_tools import *
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

MAX_RECORDS_PER_FILE = 1000000


# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_path = os.path.join(dir, 'Input', 'Products')
    output_path = os.path.join(dir, 'Output', 'Products')

    print('========================================')
    print('nielsen2marc_products')
    print('========================================')
    print('\nThis program converts Nielsen TSV files\n'
          'for PRODUCTS to MARC 21 (Bibliographic)\n')
    magician()

    try: opts, args = getopt.getopt(argv, 'i:o:', ['input_path=', 'output_path=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage(conversion_type='Products')
        elif opt in ['-i', '--input_path']: input_path = arg
        elif opt in ['-o', '--output_path']: output_path = arg
        else: exit_prompt('Error: Option {} not recognised'.format(opt))

    if not input_path:
        exit_prompt('Error: No path to input files has been specified')
    if not os.path.isdir(input_path):
        exit_prompt('Error: Invalid path to input files')
    if not output_path:
        exit_prompt('Error: No path to output files has been specified')
    if not os.path.isdir(output_path):
        exit_prompt('Error: Invalid path to output files')

    # --------------------
    # Parameters seem OK => start program
    # --------------------

    # Display confirmation information about the transformation

    print('Input folder: {}'.format(input_path))
    print('Output folder: {}'.format(output_path))
    if not os.path.exists(os.path.join(output_path, 'UK')):
        os.makedirs(os.path.join(output_path, 'UK'))

    # --------------------
    # Iterate through input files
    # --------------------

    file_count, record_count = 0, 0
    ids = set()
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Open input and output files
    ofile = open(os.path.join(output_path, '{n:03d}_product_{t}.lex'.format(n=file_count, t=today)), mode='wb')
    ofileUK = open(os.path.join(output_path, '{n:03d}_product_{t}_UK.lex'.format(n=file_count, t=today)), mode='wb')
    tfile = open(os.path.join(output_path, '{n:03d}_product_{t}.txt'.format(n=file_count, t=today)), mode='w', encoding='utf-8', errors='replace')
    dfile = open(os.path.join(output_path, '_duplicates_{}.txt'.format(today)), mode='w', encoding='utf-8', errors='replace')
    writer = MARCWriter(ofile)
    writerUK = MARCWriter(ofileUK)

    for root, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(('.add', '.upd', '.del')):

                status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
                date_time('Processing file {}'.format(str(file)))

                ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                i = 0

                c = csv.DictReader(ifile, delimiter='\t')
                for row in c:
                    i += 1
                    record_count += 1

                    if record_count % MAX_RECORDS_PER_FILE == 0:
                        date_time('Starting new output file')
                        # Start a new file
                        for f in (ofile, tfile):
                            f.close()
                        file_count += 1
                        ofile = open(os.path.join(output_path, '{n:03d}_product_{t}.lex'.format(n=file_count, t=today)), mode='wb')
                        ofileUK = open(os.path.join(output_path, '{n:03d}_product_{t}_UK.lex'.format(n=file_count, t=today)), mode='wb')
                        tfile = open(os.path.join(output_path, '{n:03d}_product_{t}.txt'.format(n=file_count, t=today)), mode='w', encoding='utf-8', errors='replace')
                        writer = MARCWriter(ofile)
                        writerUK = MARCWriter(ofileUK)

                    if i % 1000 == 0:
                        print('{} records processed'.format(str(i)), end='\r')

                    nielsen = NielsenTSVProducts(row, status)
                    marc = nielsen.marc()
                    record_id = nielsen.record_id()
                    writer.write(marc)
                    tfile.write(str(marc) + '\n')
                    if nielsen.is_uk():
                        writerUK.write(marc)
                    if record_id:
                        if record_id in ids:
                            dfile.write(record_id + '\n')
                        ids.add(record_id)

                print('{} records processed'.format(str(i)), end='\r')
                ifile.close()

    # Close files
    for f in (ofile, ofileUK, dfile, tfile):
        f.close()

    date_time_exit()


if __name__ == '__main__':
    main(sys.argv[1:])
