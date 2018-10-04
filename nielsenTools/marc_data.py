#  -*- coding: utf8 -*-

"""MARC record processing tools used within nielsenTools."""

# Import required modules
import datetime
import os
import gc
import glob
import regex as re
from nielsenTools.functions import *
from nielsenTools.database_tools import *
from nielsenTools.isbn_tools import *
from nielsenTools.network_tools import *

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#     Constants
# ====================

LEADER_LENGTH, DIRECTORY_ENTRY_LENGTH = 24, 12
SUBFIELD_INDICATOR, END_OF_FIELD, END_OF_RECORD = chr(0x1F), chr(0x1E), chr(0x1D)
ALEPH_CONTROL_FIELDS = ['DB ', 'FMT', 'SYS']

ILLUSTRATIONS = {
    'ill': 'a',
    'map': 'b',
    'portrait': 'c',
    'chart': 'd',
    'plan': 'e',
    'plate': 'f',
    'music': 'g',
    'facsim': 'h',
    'of arms': 'i',
    'genealogical table': 'j',
    }

# ====================
#     Exceptions
# ====================


class RecordLengthError(Exception):
    def __str__(self): return 'Invalid record length in first 5 bytes of record'


class LeaderError(Exception):
    def __str__(self): return 'Error reading record leader'


class DirectoryError(Exception):
    def __str__(self): return 'Record directory is invalid'


class FieldsError(Exception):
    def __str__(self): return 'Error locating fields in record'


class BaseAddressLengthError(Exception):
    def __str__(self): return 'Base address exceeds size of record'


class BaseAddressError(Exception):
    def __str__(self): return 'Error locating base address of record'


class RecordWritingError(Exception):
    def __str__(self): return 'Error writing record'


# ====================
#       Classes
# ====================


class MARCReader(object):

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
        first5 = self.file_handle.read(5)
        if not first5: raise StopIteration
        if len(first5) < 5: raise RecordLengthError
        return Record(first5 + self.file_handle.read(int(first5) - 5))


class MARCWriter(object):
    def __init__(self, file_handle):
        self.file_handle = file_handle

    def write(self, record):
        if not isinstance(record, Record): raise RecordWritingError
        self.file_handle.write(record.as_marc())

    def close(self):
        self.file_handle.close()
        self.file_handle = None


class Record(object):
    def __init__(self, data='', leader=' ' * LEADER_LENGTH):
        self.leader = '{}22{}4500'.format(leader[0:10], leader[12:20])
        self.fields = list()
        self.pos = 0
        if len(data) > 0: self.decode_marc(data)

    def __getitem__(self, tag):
        fields = self.get_fields(tag)
        if len(fields) > 0: return fields[0]
        return None

    def __contains__(self, tag):
        fields = self.get_fields(tag)
        return len(fields) > 0

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        if self.__pos >= len(self.fields): raise StopIteration
        self.__pos += 1
        return self.fields[self.__pos - 1]

    def __str__(self):
        text_list = ['=LDR  {}'.format(self.leader)]
        text_list.extend([str(field) for field in self.fields])
        return '\n'.join(text_list) + '\n'

    def add_field(self, *fields):
        self.fields.extend(fields)

    def add_ordered_field(self, *fields):
        for f in fields:
            if len(self.fields) == 0 or not f.tag.isdigit():
                self.fields.append(f)
                continue
            self._sort_fields(f)

    def _sort_fields(self, field):
        tag = int(field.tag)

        i, last_tag = 0, 0
        for selff in self.fields:
            i += 1
            if not selff.tag.isdigit() and selff.tag not in ALEPH_CONTROL_FIELDS:
                self.fields.insert(i - 1, field)
                break

            if selff.tag not in ALEPH_CONTROL_FIELDS:
                last_tag = int(selff.tag)

            if last_tag > tag:
                self.fields.insert(i - 1, field)
                break
            if len(self.fields) == i:
                self.fields.append(field)
                break

    def get_fields(self, *args):
        if len(args) == 0: return self.fields
        return [f for f in self.fields if f.tag.upper() in args]

    def decode_marc(self, marc):
        # Extract record leader
        try: self.leader = marc[0:LEADER_LENGTH].decode('ascii')
        except: print('Record has problem with Leader and cannot be processed')
        if len(self.leader) != LEADER_LENGTH: raise LeaderError

        # Determine character encoding
        self.leader = self.leader[0:9] + 'a' + self.leader[10:]

        # Extract the byte offset where the record data starts
        base_address = int(marc[12:17])
        if base_address <= 0: raise BaseAddressError
        if base_address >= len(marc): raise BaseAddressLengthError

        # Extract directory
        # base_address-1 is used since the directory ends with an END_OF_FIELD byte
        directory = marc[LEADER_LENGTH:base_address - 1].decode('ascii')

        # Determine the number of fields in record
        if len(directory) % DIRECTORY_ENTRY_LENGTH != 0:
            raise DirectoryError
        field_total = len(directory) / DIRECTORY_ENTRY_LENGTH

        # Add fields to record using directory offsets
        field_count = 0
        while field_count < field_total:
            entry_start = field_count * DIRECTORY_ENTRY_LENGTH
            entry_end = entry_start + DIRECTORY_ENTRY_LENGTH
            entry = directory[entry_start:entry_end]
            entry_tag = entry[0:3]
            entry_length = int(entry[3:7])
            entry_offset = int(entry[7:12])
            entry_data = marc[base_address + entry_offset:base_address + entry_offset + entry_length - 1]

            # Check if tag is a control field
            if str(entry_tag) < '010' and entry_tag.isdigit():
                field = Field(tag=entry_tag, data=entry_data.decode('utf-8'))
            elif str(entry_tag) in ALEPH_CONTROL_FIELDS:
                field = Field(tag=entry_tag, data=entry_data.decode('utf-8'))

            else:
                subfields = list()
                subs = entry_data.split(SUBFIELD_INDICATOR.encode('ascii'))
                # Missing indicators are recorded as blank spaces.
                # Extra indicators are ignored.

                subs[0] = subs[0].decode('ascii') + '  '
                first_indicator, second_indicator = subs[0][0], subs[0][1]

                for subfield in subs[1:]:
                    if len(subfield) == 0: continue
                    try:
                        code, data = subfield[0:1].decode('ascii'), subfield[1:].decode('utf-8', 'strict')
                        subfields.append(code)
                        subfields.append(data)
                    except:
                        print('Error in subfield code in field {}'.format(entry_tag))
                field = Field(
                    tag=entry_tag,
                    indicators=[first_indicator, second_indicator],
                    subfields=subfields,
                )
            self.add_field(field)
            field_count += 1

        if field_count == 0: raise FieldsError

    def as_marc(self):
        fields, directory, base_address, record_length = self._as_marc()
        if record_length > 99999:
            print('Record size exceeds 99999 octets - removing fields')
        while record_length > 99999:
            for f in self.get_fields('505', '520', '545'):
                self.fields.remove(f)
                break
            fields, directory, base_address, record_length = self._as_marc()

        strleader = '%05d%s%05d%s' % (record_length, self.leader[5:12], base_address, self.leader[17:])
        leader = strleader.encode('utf-8')
        return leader + directory + fields

    def _as_marc(self):
        fields, directory = b'', b''
        offset = 0

        for field in self.fields:
            field_data = field.as_marc()
            fields += field_data
            if field.tag.isdigit():
                directory += ('%03d' % int(field.tag)).encode('utf-8')
            else:
                directory += ('%03s' % field.tag).encode('utf-8')
            directory += ('%04d%05d' % (len(field_data), offset)).encode('utf-8')
            offset += len(field_data)

        directory += END_OF_FIELD.encode('utf-8')
        fields += END_OF_RECORD.encode('utf-8')
        base_address = LEADER_LENGTH + len(directory)
        record_length = base_address + len(fields)
        return fields, directory, base_address, record_length

    def get_isbns(self):
        isbns = set()
        for field in self.get_fields('020'):
            format = 'U'
            for subfield in field.get_subfields('q'):
                if get_resource_format(subfield):
                    format = get_resource_format(subfield)
            for subfield in field.get_subfields('a'):
                isbn = Isbn(subfield, format=format)
                if isbn.isbn and isbn.isbn not in '|'.join(i.isbn for i in isbns):
                    isbns.add(isbn)
            for subfield in field.get_subfields('z'):
                isbn = Isbn(subfield, format=format)
                if isbn.isbn and isbn.isbn not in '|'.join(i.isbn for i in isbns):
                    isbns.add(isbn)
        return isbns


class Field(object):

    def __init__(self, tag, indicators=None, subfields=None, data=''):
        if indicators is None: indicators = []
        if subfields is None: subfields = []
        indicators = [str(x) for x in indicators]

        # Normalize tag to three digits
        self.tag = '%03s' % tag

        # Check if tag is a control field
        if self.tag < '010' and self.tag.isdigit():
            self.data = str(data)
        elif self.tag in ALEPH_CONTROL_FIELDS:
            self.data = str(data)
        else:
            self.indicator1, self.indicator2 = self.indicators = indicators
            self.subfields = subfields

    def __iter__(self):
        self.__pos = 0
        return self

    def __getitem__(self, subfield):
        subfields = self.get_subfields(subfield)
        if len(subfields) > 0: return subfields[0]
        return None

    def __contains__(self, subfield):
        subfields = self.get_subfields(subfield)
        return len(subfields) > 0

    def __next__(self):
        if not hasattr(self, 'subfields'):
            raise StopIteration
        while self.__pos + 1 < len(self.subfields):
            subfield = (self.subfields[self.__pos], self.subfields[self.__pos + 1])
            self.__pos += 2
            return subfield
        raise StopIteration

    def __str__(self):
        if self.is_control_field() or self.tag in ALEPH_CONTROL_FIELDS:
            text = '={}  {}'.format(self.tag, self.data.replace(' ', '#'))
        else:
            text = '={}  '.format(self.tag)
            for indicator in self.indicators:
                if indicator in (' ', '\\'):
                    text += '#'
                else:
                    text += indicator
            text += ' '
            for subfield in self: text += '${}{}'.format(subfield[0], subfield[1])
        return text

    def get_subfields(self, *codes):
        """Accepts one or more subfield codes and returns a list of subfield values"""
        values = []
        for subfield in self:
            if len(codes) == 0 or subfield[0] in codes:
                values.append(str(subfield[1]))
        return values

    def add_subfield(self, code, value):
        self.subfields.append(code)
        self.subfields.append(clean(value))

    def is_control_field(self):
        if self.tag < '010' and self.tag.isdigit(): return True
        if self.tag in ALEPH_CONTROL_FIELDS: return True
        return False

    def as_marc(self):
        if self.is_control_field():
            return (self.data + END_OF_FIELD).encode('utf-8')
        marc = self.indicator1 + self.indicator2
        for subfield in self:
            marc += SUBFIELD_INDICATOR + subfield[0] + subfield[1]
        return (marc + END_OF_FIELD).encode('utf-8')


# ====================
#      Functions
# ====================


def create_graph_from_marc_file(file, skip_check=False):

    G = Graph(skip_check=skip_check)

    print('\n\nSearching file {} ...'.format(str(file)))
    print('----------------------------------------')
    print(str(datetime.datetime.now()))

    record_count = 0
    file = open(file, mode='rb')
    reader = MARCReader(file)
    for record in reader:
        record_count += 1
        if record_count % 100 == 0:
            print('\r{} records processed'.format(str(record_count)), end='\r')

        isbns = record.get_isbns()

        if isbns:
            data = [(i.isbn, i.format, None) for i in isbns if i.isbn]
            G.add_nodes(data)
            data = [(i.isbn, j.isbn) for i in isbns for j in isbns if
                    i.isbn and j.isbn and i.isbn != j.isbn and i.format != 'C' and j.format != 'C']
            G.add_edges(data)

    G.check_graph()
    gc.collect()
    return G


def add_from_marc_files(input_path, skip_check=False):

    db = IsbnDatabase()

    for file in os.listdir(input_path):
        if file.endswith('.lex'):
            G = create_graph_from_marc_file(os.path.join(input_path, file), skip_check=skip_check)
            db.add_graph_to_database(G, skip_check)

    db.close()
