#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import getopt
from nielsenTools.nielsen_tools import *

# Set threshold for garbage collection (helps prevent the program run out of memory)
gc.set_threshold(400, 5, 5)

# Increase CSV field size limit because some fields are ENORMOUS
csv.field_size_limit(sys.maxsize)

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#      Classes
# ====================

class NielsenCSVProducts:

    def __init__(self, csv_row, status):
        self.row = csv_row
        self.status = status
        self.values = {}
        for v in ['ISBN13', 'FTS']:
            try: self.values[v] = clean(self.row[v])
            except: self.values[v] = None
        if not self.values['ISBN13']: self.values['ISBN13'] = '[NO RECORD IDENTIFIER]'

    def record_id(self):
        if self.values['ISBN13'] and self.values['ISBN13'] != '[NO RECORD IDENTIFIER]':
            return self.values['ISBN13']
        return None

    def marc(self):

        # Leader (NR)
        record = Record(leader='     {}am a22     2  4500'.format(self.status))

        record.add_field(Field(tag='FMT', data='BK'))

        # 001 - Control Number
        record.add_field(Field(tag='001', data=self.values['ISBN13']))

        # 003 - Control Number Identifier (NR)
        record.add_field(Field(tag='003', data='UK-WkNB'))

        # 005 - Date and Time of Latest Transaction (NR)
        record.add_field(Field(tag='005', data='{}.0'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))

        # 007 - Physical Description Fixed Field-General Information (R)

        # 008 - Fixed-Length Data Elements-General Information (NR)
        # 00-05 - Date entered on file
        data = datetime.datetime.now().strftime('%y%m%d')
        # 06 - Type of date/Publication status
        # 07-10 - Date 1
        # 11-14 - Date 2
        data += 'nuuuuuuuu'
        # 15-17 - Place of publication, production, or execution
        data += 'xx '
        data += '|||||||||||||||||'
        # 35-37 - Language
        data += '   '
        # 38 - Modified record
        data += '|'
        # 39 - Cataloging source
        data += ' '
        record.add_field(Field(tag='008', data=data))

        # 020 - International Standard Book Number (R)
        try: v = clean(re.sub(r'[^0-9X]', '', self.row['ISBN13'].upper()))
        except: v = None
        if v: record.add_field(Field('020', [' ', ' '], ['a', v]))

        cluster = NielsenCluster(self.row)
        for isbn in cluster.isbns:
            if ':' not in isbn:
                record.add_field(Field('020', [' ', ' '], ['z', isbn]))

        for isbn in cluster.isbns:
            if ':' in isbn:
                identifier_type, identifier = isbn.split(':', 1)
                record.add_field(Field('024', ['7', ' '], ['a', identifier, '2', identifier_type]))

        # 100 - Main Entry-Personal Name (NR)
        names = set()
        for i in range(1, 10):
            name = ContribName(i, self.row)
            if str(name) != '':
                names.add(name)

        authors = [str(n) for n in names if n.role == 'author']
        if len(authors) > 1: resp = ', '.join(authors[:-1]) + ' and ' + authors[-1]
        elif authors: resp = authors[0]
        else: resp = ''

        editors = [str(n) for n in names if n.role == 'editor']
        if len(editors) > 1: resp += ' ; edited by ' + ', '.join(editors[:-1]) + ' and ' + editors[-1]
        elif editors: resp += ' ; edited by ' + editors[0]

        others = [clean('{} {}'.format(n.role, str(n))) for n in names if n.role not in ['author', 'editor']]
        resp += ' ; '.join(others)

        if resp != '': resp = clean(resp) + '.'

        authors = [n for n in names if n.role == 'author']
        if authors:
            author = authors[0]
            record.add_field(author.as_marc())
            authors.remove(author)

        # 245 - Title Statement (NR)
        # LA    Leading Article of Title. Usually A or The
        # TL    Main text of Title
        # ST    Subtitle of text
        # PVNO* Volume or Part number
        # PT*   Title of this volume or part
        # YS    Year Statement
        try: TL = clean(self.row['FTS'])
        except: TL = None
        if not TL: TL = '[TITLE NOT PROVIDED]'
        if resp: TL += ' /'
        else: TL += '.'
        subfields = ['a', TL]
        if resp: subfields.extend(['c', resp])
        indicators = ['1' if resp else '0', '0']
        record.add_field(Field('245', indicators, subfields))

        # 700 - Added Entry-Personal Name (R)
        for name in authors:
            record.add_field(name.as_marc(tag_start='7'))

        editors = [n for n in names if n.role == 'editor']
        for name in editors:
            record.add_field(name.as_marc(tag_start='7'))

        others = [n for n in names if n.role not in ['author', 'editor']]
        for name in others:
            record.add_field(name.as_marc(tag_start='7'))

        # 787 - Other Relationship Entry (R)
        for isbn, relationship in cluster.related:
            record.add_field(Field('787', ['1', ' '], ['i', relationship, 'z', isbn.isbn]))

        record.add_field(Field('SRC', [' ', ' '], ['a', 'Record converted from Nielsen CSV data to MARC21 by Collection Metadata.']))

        return record


# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_path = os.path.join(dir, 'Input', 'Clusters')
    output_path = os.path.join(dir, 'Output', 'Clusters')

    print('========================================')
    print('nielsen2marc_clusters')
    print('========================================')
    print('\nThis program converts Nielsen CSV files\n'
          'for CLUSTERS to MARC 21 (Bibliographic)\n')

    try: opts, args = getopt.getopt(argv, 'i:o:', ['input_path=', 'output_path=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage(conversion_type='Clusters')
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

    # --------------------
    # Iterate through input files
    # --------------------

    for root, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(('.add', '.upd', '.del')):
                status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
                ids = set()
                print('\n\nProcessing file {} ...'.format(str(file)))
                print('----------------------------------------')
                print(str(datetime.datetime.now()))

                # Open input and output files
                ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                ofile = open(os.path.join(output_path, file + '.lex'), 'wb')
                tfile = open(os.path.join(output_path, file + '.txt'), mode='w', encoding='utf-8', errors='replace')
                dfile = open(os.path.join(output_path, file + '_duplicates.txt'), mode='w', encoding='utf-8', errors='replace')
                writer = MARCWriter(ofile)
                i = 0
                c = csv.DictReader(ifile, delimiter=',')
                for row in c:
                    i += 1
                    print('{} records processed'.format(str(i)), end='\r')
                    nielsen = NielsenCSVProducts(row, status)
                    marc = nielsen.marc()
                    record_id = nielsen.record_id()
                    writer.write(marc)
                    tfile.write(str(marc) + '\n')
                    if record_id:
                        if record_id in ids:
                            dfile.write(record_id + '\n')
                        else: ids.add(record_id)

                # Close files
                for f in (ifile, ofile, tfile, dfile):
                    f.close()

    date_time_exit()

if __name__ == '__main__':
    main(sys.argv[1:])
