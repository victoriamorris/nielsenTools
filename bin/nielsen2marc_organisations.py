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


ORG_FIELDS = {
    'ORGID',    # Unique Organisation Number
    'ORGN',     # Full name
    'ORGAL1',   # Line of address
    'ORGAL2',
    'ORGAL3',
    'ORGAL4',
    'ORGAT',    # Town
    'ORGACOS',  # County or State
    'ORGAPC',   # Post Code
    'ORGCTRY',  # Country
    'ORGPA',    # Member of Publisher Association –‘Y’es or ‘N’o
    'ORGCP',    # ‘Y' indicates that the Publisher has 'Ceased Publishing'
    'ORGGA',    # ‘Y' indicates that the Organisation is no longer at the stated address - but NBD do not have any forwarding information
    'ORGCGD',   # The date the 'flag' was set
    'ORGCGN',   # Any additional information about the cessation or move.
    'ORGVAT',   # Organisation VAT number
    'ORGGIRO',  # Organisation Giro number
    'ORGEDI',   # Organisation EDI number
    'ORGPREF',  # Publisher Prefix list
    'ORGREFN',  # Organisation now part of…
    'ORGPREVN', # Previous organisations now incorporated in the current one
    'ORGWAS',   # Org name has changed to…current record
    'AUSAORGSN',    # Australia
    'CANAORGSN',    # Canada
    'EURAORGSN',    # Europe
    'HKAORGSN',     # Hong Kong
    'UKAORGSN',     # United Kingdom
    'IRLAORGSN',    # Ireland
    'NZAORGSN',     # New Zealand
    'SAAORGSN',     # South Africa
    'SINGAORGSN',   # Singapore
    'USAORGSN',     # USA
    'WWWAORGSN',    # Internet
    'OTHERAORGSN',  # Other
    'INAORGSN',     # India
}


ORG_FIELDS_REPEATABLE = {
    'ORGTEL',   # Telephone numbers for the organisation
    'ORGEMAIL', # Email addresses
    'ORGFAX',   # Fax numbers
    'ORGMOB',   # Mobile Numbers
    'ORGTELX',  # Telex Details
    'ORGURL',   # URL Details
}


ORG_FIELDS_MULTIVALUED = {
    'ORGREFN',  # Organisation now part of…
    'ORGPREVN', # Previous organisations now incorporated in the current one
    'ORGWAS',   # Org name has changed to…current record
    'AUSAORGSN',    # Australia
    'CANAORGSN',    # Canada
    'EURAORGSN',    # Europe
    'HKAORGSN',     # Hong Kong
    'UKAORGSN',     # United Kingdom
    'IRLAORGSN',    # Ireland
    'NZAORGSN',     # New Zealand
    'SAAORGSN',     # South Africa
    'SINGAORGSN',   # Singapore
    'USAORGSN',     # USA
    'WWWAORGSN',    # Internet
    'OTHERAORGSN',  # Other
    'INAORGSN',     # India
}


# ====================
#      Classes
# ====================


class NielsenTSVOrganisations:

    def __init__(self, csv_row, status='c'):
        self.row = csv_row
        self.status = status

        self.values = {}
        for v in ORG_FIELDS:
            try: self.values[v] = clean(self.row[v])
            except: self.values[v] = None
        for v in ORG_FIELDS_REPEATABLE:
            self.values[v] = set()
            for i in range(1, 5):
                try: val =  clean(self.row['{}{}'.format(v, str(i))])
                except: val = None
                if val: self.values[v].add(val)
        for v in ORG_FIELDS_MULTIVALUED:
            if self.values[v]:
                self.values[v] = set([clean(val) for val in self.values[v].split(';') if clean(val)])
            else: self.values[v] = set()

    def marc(self):

        record = Record(leader='     {}z  a22     o  4500'.format(self.status))

        # 001 - Control Number (NR)
        if self.values['ORGID']:
            record.add_field(Field(tag='001', data=self.values['ORGID'] or '[NO ORGANISATION IDENTIFIER]'))

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
        record.add_field(Field('040', [' ', ' '], ['a', 'UK-WkNB', 'b', 'eng', 'c', 'Uk']))

        # 075 - Type of Entity (R)
        record.add_field(Field('075', [' ', ' '], ['a', 'Publisher']))

        # 110 - Heading - Corporate Name (NR)
        if self.values['ORGN']:
            record.add_field(Field('110', ['2', ' '], ['a', self.values['ORGN']]))

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
            record.add_field(Field('856', ['4', ' '], ['u', v]))

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
    print('\nThis program converts Nielsen TSV files\n'
          'for ORGANISATIONS to MARC 21 (Authority)\n')

    try: opts, args = getopt.getopt(argv, 'i:o:', ['input_path=', 'output_path=', 'help'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage(conversion_type='Organisations')
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
                date_time_message('Processing file {}'.format(str(file)))

                # Open input and output files
                ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace')
                ofile = open(os.path.join(output_path, file + '.lex'), 'wb')
                tfile = open(os.path.join(output_path, file + '.txt'), mode='w', encoding='utf-8', errors='replace')

                writer = MARCWriter(ofile)
                i = 0
                c = csv.DictReader(ifile, delimiter='\t')
                for row in c:
                    i += 1
                    print('{} records processed'.format(str(i)), end='\r')
                    nielsen = NielsenTSVOrganisations(row, status)
                    marc = nielsen.marc()
                    writer.write(marc)
                    tfile.write(str(marc) + '\n')

                # Close files
                for f in (ifile, ofile, tfile):
                    f.close()

    date_time_exit()

if __name__ == '__main__':
    main(sys.argv[1:])
