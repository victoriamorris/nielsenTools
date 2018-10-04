#!/usr/bin/env python
# -*- coding: utf8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import csv
from nielsenTools.functions import *

# Set locale to assist with sorting
locale.setlocale(locale.LC_ALL, '')

# Set threshold for garbage collection (helps prevent the program run out of memory)
gc.set_threshold(400, 5, 5)

# Increase CSV field size limit because some fields are ENORMOUS
csv.field_size_limit(sys.maxsize)

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#   Global variables
# ====================


DISTRIBUTION_AREAS = {
    'UK': 'United Kingdom',
    'US': 'United States',
    'AUS': 'Australia',
    'NZ': 'New Zealand',
    'SA': 'South Africa',
    'EUR': 'Europe',
    'IN': 'India',
    'CAN': 'Canada',
    'IRL':  'Ireland',
    'HK':  'Honk Kong',
    'SING': 'Singapore',
}

# ====================
#      Functions
# ====================


def usage():
    """Function to print information about the program"""
    print('Correct syntax is:')
    print('nielsen2marc_organisations -i <input_path> -o <output_path>')
    print('    -i    path to FOLDER containing Input files')
    print('    -o    path to FOLDER to contain Output files')
    print('If not specified, input path will be /Input/Organisations')
    print('If not specified, output path will be /Output/Organisations')
    print('\nUse quotation marks (") around arguments which contain spaces')
    print('\nInput file names should begin 31_ and end .upd')
    print('\nOptions')
    print('    --help    Display this message and exit')
    exit_prompt()


# ====================
#      Classes
# ====================


class Reader:

    def __init__(self, marc_target):
        if hasattr(marc_target, 'read') and callable(marc_target.read):
            self.file_handle = marc_target

    def __iter__(self):
        return self

    def close(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None

    def __next__(self):
        chunk = ''
        line = self.file_handle.readline()
        if not line: raise StopIteration
        while line and not line.startswith('$'):
            chunk += line
            line = self.file_handle.readline()
            if not line: raise StopIteration

        return NielsenOrg(chunk)


class NielsenOrg:

    def __init__(self, data, status='c'):
        self.data = data
        self.status = status
        self.values = {
            'ORGID':    None,       # Unique Organisation Number
            'ORGN':     None,       # Full name
            'ORGAL1':   None,       # Line of address
            'ORGAL2':   None,
            'ORGAL3':   None,
            'ORGAL4':   None,
            'ORGAT':    None,       # Town
            'ORGACOS':  None,       # County or State
            'ORGAPC':   None,       # Post Code
            'ORGCTRY':  None,       # Country
            'ORGPA':    None,       # Member of Publisher Association –‘Y’es or ‘N’o
            'ORGCP':    None,       # ‘Y' indicates that the Publisher has 'Ceased Publishing'
            'ORGGA':    None,       # ‘Y' indicates that the Organisation is no longer at the stated address - but NBD do not have any forwarding information
            'ORGCGD':   None,       # The date the 'flag' was set
            'ORGCGN':   None,       # Any additional information about the cessation or move.
            'ORGVAT':   None,       # Organisation VAT number
            'ORGGIRO':  None,       # Organisation Giro number
            'ORGEDI':   None,       # Organisation EDI number
            'ORGPREF':  None,       # Publisher Prefix list
            'ORGTEL':   set(),      # Telephone numbers for the organisation
            'ORGEMAIL': set(),      # Email addresses
            'ORGFAX':   set(),      # Fax numbers
            'ORGMOB':   set(),      # Mobile Numbers
            'ORGTELX':  set(),      # Telex Details
            'ORGURL':   set(),      # URL Details
            'ORGREFN':  set(),      # Organisation now part of…
            'ORGPREVN': set(),      # Previous organisations now incorporated in the current one
            'ORGWAS':   set(),      # Org name has changed to…current record
            'AUSAORGSN': set(),     # Australia
            'CANAORGSN': set(),     # Canada
            'EURAORGSN': set(),     # Europe
            'HKAORGSN':  set(),     # Hong Kong
            'UKAORGSN':  set(),     # United Kingdom
            'IRLAORGSN': set(),     # Ireland
            'NZAORGSN':  set(),     # New Zealand
            'SAAORGSN':  set(),     # South Africa
            'SINGAORGSN':    set(), # Singapore
            'USAORGSN':  set(),     # USA
            'WWWAORGSN': set(),     # Internet
            'OTHERAORGSN':   set(), # Other
            'INAORGSN':  set(),     # India
        }

        for line in self.data.split('\n'):
            if not line or line.strip() in ['$', '*a']: continue
            tag, data = line.split(' ', 1)[0].upper().strip(), line.split(' ', 1)[1].strip()

            if tag not in self.values: tag = re.sub(r'[0-9]', '', tag)
            if tag in self.values:
                if tag in ['ORGTEL', 'ORGEMAIL', 'ORGFAX', 'ORGMOB', 'ORGTELX', 'ORGURL', 'ORGREFN', 'ORGPREVN',
                           'ORGWAS'] or tag.endswith('AORGSN'):
                    self.values[tag].add(data)
                else: self.values[tag] = data

    def marc(self):

        record = Record()

        # 001 - Control Number (NR)

        if self.values['ORGID']:
            record.add_field(Field(tag='001', data=self.values['ORGID']))

        # 003 - Control Number Identifier (NR)

        record.add_field(Field(tag='003', data='UK-WkNB'))

        # 005 - Date and Time of Latest Transaction (NR)

        record.add_field(Field(tag='005', data='{}.0'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))

        # 008 - Fixed-Length Data Elements (NR)

        # 00-05 - Date entered on file
        data = datetime.datetime.now().strftime('%y%m%d')
        # 06 - Direct or indirect geographic subdivision
        data += 'n'
        # 07 - Romanization scheme
        data += 'n'
        # 08 - Language of catalog
        data += 'e'
        # 09 - Kind of record
        data += 'b'
        # 10 - Descriptive cataloging rules
        data += 'n'
        # 11 - Subject heading system/thesaurus
        data += 'n'
        # 12 - Type of series
        data += 'n'
        # 13 - Numbered or unnumbered series
        data += 'n'
        # 14 - Heading use-main or added entry
        data += 'b'
        # 15 - Heading use-subject added entry
        data += 'b'
        # 16 - Heading use-series added entry
        data += 'b'
        # 17 - Type of subject subdivision
        data += 'n'
        # 18-27 - Undefined character positions
        data += '          '
        # 28 - Type of government agency
        data += ' '
        # 29 - Reference evaluation
        data += 'b'
        # 30 - Undefined character position
        data += ' '
        # 31 - Record update in process
        data += '|'
        # 32 - Undifferentiated personal name
        data += '|'
        # 33 - Level of establishment
        data += 'n'
        # 34-37 - Undefined character positions
        data += '    '
        # 38 - Modified record
        data += '|'
        # 39 - Cataloging source
        data += ' '
        record.add_field(Field(tag='008', data=data))

        # 024 - Other Standard Identifier (R)

        if self.values['ORGPREF']:
            for v in sorted(set(re.sub(r'[^0-9X ]', '', self.values['ORGPREF'].upper()).split(' '))):
                record.add_field(Field('024', ['7', ' '], ['a', re.sub(r'^978', '', v), '2', 'isbnre']))

        # 035 - System Control Number (R)

        if self.values['ORGID']:
            record.add_field(Field('035', [' ', ' '], ['a', '(UK-WkNB){}'.format(self.values['ORGID'])]))

        # 040 - Cataloging Source (NR)

        record.add_field(Field('040', [' ', ' '], ['a', 'UK-WkNB', 'b', 'eng', 'c', 'Uk', 'd', 'Uk']))

        # 075 - Type of Entity (R)

        record.add_field(Field('075', [' ', ' '], ['a', 'Publisher']))

        # 110 - Heading - Corporate Name (NR)

        if self.values['ORGN']:
            record.add_field(Field('035', ['2', ' '], ['a', self.values['ORGN']]))

        # 368 - Other Attributes of Person or Corporate Body (R)

        subfields = ['a', 'Publisher']
        if self.values['ORGCP'] == 'Y' and self.values['ORGCGD']:
            subfields.extend(['t', self.values['ORGCGD']])
        record.add_field(Field('368', [' ', ' '], subfields))

        # 370 - Associated Place (R)

        subfields = []
        if self.values['ORGCTRY']:
            subfields.extend(['c', self.values['ORGCTRY']])
        if self.values['ORGAT']:
            subfields.extend(['e', self.values['ORGAT']])
        if subfields:
            record.add_field(Field('370', [' ', ' '], subfields))

        # 371 - Address (R)

        subfields = []
        for i in range(1, 4):
            if self.values['ORGAL{}'.format(str(i))]:
                subfields.extend(['a', self.values['ORGAL{}'.format(str(i))]])
        if self.values['ORGAT']:
            subfields.extend(['b', self.values['ORGAT']])
        if self.values['ORGACOS']:
            subfields.extend(['c', self.values['ORGACOS']])
        if self.values['ORGCTRY']:
            subfields.extend(['d', self.values['ORGCTRY']])
        if self.values['ORGAPC']:
            subfields.extend(['e', self.values['ORGAPC']])
        for v in self.values['ORGEMAIL']:
            subfields.extend(['m', v])
        if self.values['ORGGA'] == 'Y' and self.values['ORGCGD']:
            subfields.extend(['t', self.values['ORGCGD']])
            subfields.extend(['z', 'Organisation not at this address since {}.'.format(self.values['ORGCGD'])])
            if self.values['ORGCGN']:
                subfields.extend(['z', self.values['ORGCGN']])
        if subfields:
            record.add_field(Field('371', [' ', ' '], subfields))

        # 372 - Field of Activity (R)

        subfields = ['a', 'Publishing']
        if self.values['ORGCP'] == 'Y' and self.values['ORGCGD']:
            subfields.extend(['t', self.values['ORGCGD']])
        record.add_field(Field('372', [' ', ' '], subfields))

        # 410 - See From Tracing-Corporate Name (R)

        for v in self.values['ORGPREVN']:
            record.add_field(Field('410', ['2', ' '], ['w', 'i', 'i', 'Organisation subsumes' 'a', v]))
        for v in self.values['ORGWAS']:
            record.add_field(Field('410', ['2', ' '], ['w', 'a', 'a', v]))

        # 510 - See Also From Tracing-Corporate Name (R)

        for v in self.values['ORGREFN']:
            record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Organisation now part of' 'a', v]))

        for c in DISTRIBUTION_AREAS:
            for v in self.values['{}AORGSN'.format(c)]:
                record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Distributor in {}'.format(DISTRIBUTION_AREAS[c]), 'a', v]))

        for v in self.values['OTHERAORGSN']:
            record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Other distributor', 'a', v]))

        for v in self.values['WWWAORGSN']:
            record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Internet distributor', 'a', v]))

        # 678 - Biographical or Historical Data(R)

        if self.values['ORGCP'] == 'Y':
            record.add_field(Field('678', [' ', ' '], ['a', 'Publisher has ceased publishing']))

        if self.values['ORGGA'] == 'Y':
            record.add_field(Field('678', [' ', ' '], ['a', 'Organisation is no longer at the stated address']))

        if self.values['ORGCGN']:
            record.add_field(Field('678', ['1', ' '], ['a', self.values['ORGCGN']]))

        if self.values['ORGPA'] == 'Y':
            record.add_field(Field('678', [' ', ' '], ['a', 'Member of Publisher Association']))

        for c in ['ORGVAT', 'ORGGIRO', 'ORGEDI']:
            if self.values[c]:
                record.add_field(Field('678', [' ', ' '], ['a', '{} number: {}'.format(c.replace('ORG', ''), self.values[c])]))


        for c in ['ORGTEL', 'ORGFAX', 'ORGMOB', 'ORGTELX']:
            for v in self.values[c]:
                record.add_field(Field('678', [' ', ' '],
                                       ['a', '{} number: {}'.format('Telephone' if c == 'ORGTEL' else 'Fax' if c == 'ORGFAX' else 'Mobile' if c == 'ORGMOB' else 'Telex', v)]))

        # 856 - Electronic Location and Access (R)

        for v in self.values['ORGURL']:
            record.add_field(Field('856', [' ', ' '], ['u', v]))




        return record


# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_path = os.path.join(dir, 'Input', 'Organisations')
    output_path = os.path.join(dir, 'Output', 'Organisations')

    print('========================================')
    print('nielsen2marc_organisations')
    print('========================================')
    print('\nThis program converts Nielsen TAGGED files\n'
          'for ORGANISATIONS to MARC 21 (Authority)\n')

    try:
        opts, args = getopt.getopt(argv, 'i:o:', ['input_path=', 'output_path=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage()
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
    if not os.path.exists(os.path.join(output_path, 'Publishers')):
        os.makedirs(os.path.join(output_path, 'Imprints'))

    # --------------------
    # Iterate through input files
    # --------------------

    for file in os.listdir(input_path):

        if file.startswith('31_') and file.endswith(('.add', '.upd', '.del')):
            status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
            print('\n\nProcessing file {} ...'.format(str(file)))
            print('----------------------------------------')
            print(str(datetime.datetime.now()))

            # Open input and output files
            ifile = open(os.path.join(input_path, file), mode='r', encoding='utf-8', errors='replace')
            ofile = open(os.path.join(output_path, file + '.lex'), 'wb')
            tfile = open(os.path.join(output_path, file + '.txt'), mode='w', encoding='utf-8', errors='replace')
            reader = Reader(ifile)
            writer = MARCWriter(ofile)
            i = 0

            for record in reader:
                i += 1
                print('{} records processed'.format(str(i)), end='\r')
                writer.write(record.marc())
                tfile.write(str(record.marc()) + '\n')

            # Close files
            for f in (ifile, ofile, tfile):
                f.close()

    date_time_exit()

if __name__ == '__main__':
    main(sys.argv[1:])