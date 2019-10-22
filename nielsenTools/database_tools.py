#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import csv
import gc
import os
import sqlite3

from nielsenTools.functions import *
from nielsenTools.network_tools import *
from nielsenTools.nielsen_tools import *

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#      Constants
# ====================


DATABASE_PATH = 'isbns.db'


GRAPH_TABLES = {
    'isbns': ([
        ('isbn', 'NCHAR(13) PRIMARY KEY'),
        ('format', 'NCHAR(1)'),
        ('checked', 'BOOLEAN'),
    ]),
    'isbn_equivalents': ([
        ('isbna', 'NCHAR(13)'),
        ('isbnb', 'NCHAR(13)'),
    ]),
    'bl_isbns': ([
        ('bl', 'NCHAR(9)'),
        ('isbn', 'NCHAR(13)'),
    ]),
    'bl_dewey': ([
        ('bl', 'NCHAR(9)'),
        ('dewey', 'NTEXT'),
    ]),
    'bl_lc': ([
        ('bl', 'NCHAR(9)'),
        ('lc', 'NTEXT'),
    ]),
    'organisations': ([
        ('org_id', 'NTEXT PRIMARY KEY'),
        ('org_name', 'NTEXT'),
        ('org_address', 'NTEXT'),
        ('org_email', 'NTEXT'),
        ('org_url', 'NTEXT'),
        ('date_valid', 'TEXT'),
    ]),
    'isbn_org_links': ([
        ('isbn', 'NCHAR(13) PRIMARY KEY'),
        ('org_id', 'NTEXT'),
        ('imp_id', 'NTEXT'),
        ('pub_status', 'TEXT'),
        ('avail_status', 'TEXT'),
        ('avail_date', 'TEXT'),
        ('date_valid', 'TEXT'),
    ]),
}


# ====================
#      Functions
# ====================


def dedupe_row(row):
    row = list(map(str, row))
    for i in range(len(row)):
        if ';' in row[i]:
            row[i] = ';'.join(sorted(set(row[i].split(';'))))
        else:
            row[i] = '|'.join(sorted(set(row[i].split('|'))))
    return row


def diff(l1, l2):
    s1 = set(l1.split(';'))
    s2 = set(l2.split(';')) - s1
    return ';'.join(sorted(s1)), ';'.join(sorted(s2))

# ====================
#       Classes
# ====================


class IsbnGraphTable:

    def __init__(self, table_name, conn, cursor):
        self.name = table_name
        self.conn = conn
        self.cursor = cursor
        self.columns = GRAPH_TABLES[table_name]
        self.create()

    def create(self, silent=False):
        if not silent: print('Creating table {} ...'.format(self.name))
        self.cursor.execute('CREATE TABLE IF NOT EXISTS {} ({}, UNIQUE({}));'
                            .format(self.name,
                                    ', '.join('{} {}'.format(key, value) for (key, value) in self.columns),
                                    ', '.join(key for (key, value) in self.columns)))
        self.conn.commit()
        gc.collect()

    def rebuild(self):
        print('Rebuilding table {} ...'.format(self.name))
        self.cursor.execute('DROP TABLE IF EXISTS {} ;'.format(self.name))
        self.create(silent=True)

    def clean(self):
        print('Deleting NULL entries from table {} ...'.format(self.name))
        self.cursor.execute('DELETE FROM {} WHERE {} IS NULL OR {} IS NULL OR {} = "" OR {} = "" ;'
                            .format(self.name, self.columns[0][0], self.columns[1][0],
                                    self.columns[0][0], self.columns[1][0]))
        self.conn.commit()
        gc.collect()

    def build_index(self):
        """Function to build indexes in a table"""
        print('Building indexes in {} table ...'.format(self.name))
        self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_0 ;""".format(self.name))
        self.cursor.execute("""CREATE INDEX IDX_{}_0 ON {} ({});""".format(self.name, self.name, self.columns[0][0]))
        self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_1 ;""".format(self.name))
        self.cursor.execute("""CREATE INDEX IDX_{}_1 ON {} ({});""".format(self.name, self.name, self.columns[1][0]))
        self.conn.commit()
        gc.collect()

    def drop_index(self):
        """Function to drop indexes in a table"""
        self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_0 ;""".format(self.name))
        self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_1 ;""".format(self.name))
        self.conn.commit()
        gc.collect()

    def dump_table(self):
        """Function to dump a database table into a text file"""
        print('Creating dump of {} table ...'.format(self.name))
        self.cursor.execute('SELECT * FROM {};'.format(self.name))
        file = open('{}_DUMP_.txt'.format(self.name), mode='w', encoding='utf-8', errors='replace')
        record_count = 0
        try: row = self.cursor.fetchone()
        except: row = None
        while row:
            record_count += 1
            if record_count % 10000 == 0:
                print('\r{} records processed'.format(str(record_count)), end='\r')
            file.write('{}\n'.format(str(row)))
            row = self.cursor.fetchone()
        del row
        print('\r{} records processed'.format(str(record_count)), end='\r')
        file.close()
        gc.collect()
        print('{} records in {} table'.format(str(record_count), self.name))
        return record_count


class IsbnDatabase:

    def __init__(self):
        """Open a new database connection, and ensure that the correct tables are present"""
        date_time('Connecting to local database')

        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

        self.output_path = os.path.dirname(DATABASE_PATH)
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

        # Set up database
        self.cursor.execute('PRAGMA synchronous = OFF')
        self.cursor.execute('PRAGMA journal_mode = OFF')
        self.cursor.execute('PRAGMA locking_mode = EXCLUSIVE')
        self.cursor.execute('PRAGMA count_changes = FALSE')

        # Create tables
        self.tables = {table: IsbnGraphTable(table, self.conn, self.cursor) for table in GRAPH_TABLES}

    def close(self):
        """Close the database connection"""
        self.conn.close()
        gc.collect()

    def clean(self, quick_clean=False, transitive=False):
        """Clean the database to remove unnecessary values"""
        date_time('Cleaning')

        self.remove_adjacencies_from_collective()

        if transitive:
            self.transitive_closure()

        # Delete null entries
        for table in self.tables:
            self.tables[table].clean()

        print('Deleting old records')
        self.cursor.execute('DELETE FROM organisations WHERE rowid NOT IN (SELECT MAX(rowid) FROM organisations '
                            'GROUP BY org_id ORDER BY date_valid ASC )')
        self.cursor.execute('DELETE FROM isbn_org_links WHERE rowid NOT IN (SELECT MAX(rowid) FROM isbn_org_links '
                            'GROUP BY isbn ORDER BY date_valid ASC )')
        self.conn.commit()

        if not quick_clean:
            date_time('Vacuuming')
            self.conn.execute("VACUUM")
            self.conn.commit()
        gc.collect()

    def remove_adjacencies_from_collective(self):
        # Remove adjacencies for collective ISBNs
        collective = set(item[0] for item in self.cursor.execute("""SELECT isbn FROM isbns WHERE format='C' ;""").fetchall())
        searchList = '\'' + '\', \''.join(collective) + '\''
        for c in GRAPH_TABLES['isbn_equivalents']:
            self.cursor.execute('DELETE FROM isbn_equivalents WHERE {} IN ({});'.format(c[0], searchList))
            self.conn.commit()
        del collective
        del searchList
        gc.collect()

    def transitive_closure(self, isbn_list=None):
        """Ensure that the ISBN table is complete by computing the transitive closure
        (i.e. all subgraphs are complete)"""
        date_time('Computing transitive closure of isbn_equivalents')
        tfile = open('TRANSITIVE_CLOSURE_.txt', mode='w', encoding='utf-8', errors='replace')
        record_count = 0

        if isbn_list:
            self._transitive_closure(isbn_list, record_count, tfile)
        else:
            self.cursor.execute('SELECT DISTINCT isbna FROM isbn_equivalents')
            result_list = self.cursor.fetchmany()
            while result_list:
                isbn_list = set(i[0] for i in result_list)
                self._transitive_closure(isbn_list, record_count, tfile)
                result_list = self.cursor.fetchmany()
        tfile.close()
        gc.collect()
        date_time('Reading transitive closure data from temporary file')
        tfile = open('TRANSITIVE_CLOSURE_.txt', mode='r', encoding='utf-8', errors='replace')
        sql_query = 'INSERT OR IGNORE INTO isbn_equivalents (isbna, isbnb) VALUES (?, ?) ;'
        values = []
        for filelineno, line in enumerate(tfile):
            isbna, isbnb = line.strip().split('\t')
            values.append((isbna, isbnb))
            values.append((isbnb, isbna))
            if filelineno % 10000 == 0:
                print('\r{} records processed'.format(str(filelineno)), end='\r')
                values = self.execute_all(sql_query, values)
        print('\r{} records processed'.format(str(filelineno)), end='\r')
        self.execute_all(sql_query, values)
        tfile.close()
        return set()

    def _transitive_closure(self, isbn_list, record_count, tfile):
        while isbn_list:
            isbn = isbn_list.pop()
            record_count += 1
            related_isbns = self.node_connected_component(isbn)
            for isbna in related_isbns:
                isbn_list.discard(isbna)
                for isbnb in related_isbns:
                    if isbna != isbnb:
                        tfile.write('{}\t{}\n'.format(isbna, isbnb))
            if record_count % 10000 == 0:
                print('\r{} records processed'.format(str(record_count)), end='\r')
        return record_count

    def execute_all(self, query, values):
        if values:
            self.cursor.executemany(query, values)
            self.conn.commit()
            gc.collect()
        return []

    def execute_all_many(self, queries, values):
        for v in queries:
            values[v] = self.execute_all(queries[v], values[v])
        return values

    def build_indexes(self):
        """Function to build indexes in the whole database"""
        date_time('Building indexes ...')
        for table in self.tables:
            self.tables[table].build_index()

    def drop_indexes(self):
        """Function to drop indexes in the whole database"""
        date_time('Dropping indexes ...')
        for table in self.tables:
            self.tables[table].drop_index()

    def dump_database(self):
        """Function to create dumps of all tables within the database"""
        date_time('Creating dump of database ...')
        for table in self.tables:
            self.tables[table].dump_table()

    def add_nielsen_product(self, input_path, skip_check=True):
        """Function to add odata from Nielsen product files"""
        query = 'INSERT OR IGNORE INTO isbn_org_links (isbn, org_id, imp_id, pub_status, avail_status, avail_date, date_valid) ' \
                'VALUES (?, ?, ?, ?, ?, ?, ?);'
        values = []
        now = datetime.datetime.now()
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith(('.add', '.upd', '.del')):
                    status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
                    date_time('Parsing Nielsen product file {} ...'.format(str(file)))
                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                    i = 0
                    c = csv.DictReader(ifile, delimiter='\t')
                    for row in c:
                        i += 1
                        nielsen = NielsenTSVProducts(row, status)
                        values.append((nielsen.sql_values() + (now,)))
                        if i % 10000 == 0:
                            print('\r{} records processed'.format(str(i)), end='\r')
                            values = self.execute_all(query, values)
                    print('\r{} records processed'.format(str(i)), end='\r')
                    values = self.execute_all(query, values)

    def add_nielsen_org(self, input_path, skip_check=True):
        """Function to add odata from Nielsen organisation files"""
        query = 'INSERT OR IGNORE INTO organisations (org_id, org_name, org_address, org_email, org_url, date_valid) ' \
                'VALUES (?, ?, ?, ?, ?, ?);'
        values = []
        now = datetime.datetime.now()
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith(('.add', '.upd', '.del')):
                    status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
                    date_time('Parsing Nielsen organisation file {} ...'.format(str(file)))
                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                    i = 0
                    c = csv.DictReader(ifile, delimiter='\t')
                    for row in c:
                        i += 1
                        nielsen = NielsenTSVOrganisations(row, status)
                        values.append((nielsen.sql_values() + (now,)))
                        if i % 10000 == 0:
                            print('\r{} records processed'.format(str(i)), end='\r')
                            values = self.execute_all(query, values)
                    print('\r{} records processed'.format(str(i)), end='\r')
                    values = self.execute_all(query, values)

    def add_nielsen(self, input_path, skip_check=True):
        """Function to add ISBN equivalences from Nielsen cluster files"""
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith(('.add', '.upd', '.del')):
                    date_time('Parsing ISBN equivalences from Nielsen cluster file {} ...'.format(str(file)))

                    G = Graph(skip_check=skip_check)

                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                    i = 0
                    c = csv.DictReader(ifile, delimiter='\t')
                    for row in c:
                        i += 1
                        if i % 100 == 0:
                            print('{} records processed'.format(str(i)), end='\r')
                        nielsen = NielsenCluster(row)
                        isbns = nielsen.get_alternative_formats()

                        if isbns:
                            data = [(i.isbn, i.format) for i in isbns if i.isbn]
                            G.add_nodes(data)
                            data = [(i.isbn, j.isbn) for i in isbns for j in isbns if
                                    i.isbn and j.isbn and i.isbn != j.isbn and i.format != 'C' and j.format != 'C']

                            G.add_edges(data)
                    print('{} records processed'.format(str(i)), end='\r')

                    ifile.close()
                    G.check_graph()
                    self.add_graph_to_database(G, skip_check)

    '''
    def add_marc(self, input_path, skip_check=True):
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.lex'):
                    date_time('Searching file {}'.format(str(file)))
            return
    '''

    def search_bl(self, input_path):
        """Function to search for transferrable information within BL records"""
        queries = {'isbns': 'INSERT OR IGNORE INTO bl_isbns (bl, isbn) VALUES (?, ?);',
                   'dewey': 'INSERT OR IGNORE INTO bl_dewey (bl, dewey) VALUES (?, ?);',
                   'lc': 'INSERT OR IGNORE INTO bl_lc (bl, lc) VALUES (?, ?);'}
        values = {q: [] for q in queries}
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.startswith('full') and file.endswith('.lex'):
                    date_time('Reading file {}'.format(file))
                    ifile = open(os.path.join(root, file), mode='rb')
                    reader = MARCReader(ifile)
                    record_count = 0
                    for record in reader:
                        record_count += 1
                        record_id = record.get_id()
                        isbns = record.get_isbns_as_strings()
                        dewey = record.get_dewey()
                        lc = record.get_lc()
                        for i in isbns:
                            values['isbns'].append((record_id, i))
                        for d in dewey:
                            values['dewey'].append((record_id, d))
                        for l in lc:
                            values['lc'].append((record_id, l))
                        if record_count % 10000 == 0:
                            print('\r{} records processed'.format(str(record_count)), end='\r')
                            values = self.execute_all_many(queries, values)

                    ifile.close()
                    print('\r{} records processed'.format(str(record_count)), end='\r')
                    values = self.execute_all_many(queries, values)

    def match_bl(self):
        ofile = open('bl_cross_references.txt', mode='w', encoding='utf-8', errors='replace')
        ofile.write('Record ID\tISBNs\tDewey\tLC\tRelated ISBNs\tRelated BL record IDs\tPossible Dewey\tPossible LC\n')
        self.cursor.execute("SELECT bl_isbns.bl, GROUP_CONCAT(bl_isbns.isbn, ';'), "
                            "GROUP_CONCAT(bl_dewey.dewey, ';'), "
                            "GROUP_CONCAT(bl_lc.lc, ';'), "
                            "GROUP_CONCAT(isbn_equivalents.isbnb, ';'), "
                            "GROUP_CONCAT(bl_isbns2.bl, ';'), "
                            "GROUP_CONCAT(bl_dewey2.dewey, ';'), "
                            "GROUP_CONCAT(bl_lc2.lc, ';') "
                            "FROM bl_isbns "
                            "LEFT JOIN bl_dewey ON bl_isbns.bl = bl_dewey.bl "
                            "LEFT JOIN bl_lc ON bl_isbns.bl = bl_lc.bl "
                            "INNER JOIN isbn_equivalents ON bl_isbns.isbn = isbn_equivalents.isbna "
                            "INNER JOIN bl_isbns AS bl_isbns2 ON isbn_equivalents.isbnb = bl_isbns2.isbn "
                            "LEFT JOIN bl_dewey AS bl_dewey2 ON bl_isbns2.bl = bl_dewey2.bl "
                            "LEFT JOIN bl_lc AS bl_lc2 ON bl_isbns2.bl = bl_lc2.bl "
                            "GROUP BY bl_isbns.bl "
                            "ORDER BY bl_isbns.bl ASC ;")
        try: row = list(self.cursor.fetchone())
        except: row = None
        while row:
            record, isbn, dewey, lc, related_isbn, related_bl, related_dewey, related_lc = dedupe_row(row)
            dewey, related_dewey = diff(dewey, related_dewey)
            lc, related_lc = diff(lc, related_lc)
            ofile.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(record, isbn, dewey, lc, related_isbn, related_bl, related_dewey, related_lc))
            try: row = list(self.cursor.fetchone())
            except: row = None
        ofile.close()
        gc.collect()

    def search_for_isbns(self, input_path):
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.txt'):
                    date_time('Reading file {}'.format(file))

                    isbn_list = {}
                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace')
                    tfile = open(os.path.join(root, file.replace('.txt', '_temp.txt')), mode='w', encoding='utf-8', errors='replace')

                    for filelineno, line in enumerate(ifile):
                        if filelineno % 10000 == 0:
                            print('\r{} records processed'.format(str(filelineno)), end='\r')
                        line = line.strip()
                        isbn = Isbn(line)
                        if isbn.isbn:
                            isbn_list[isbn.isbn] = [line, isbn.isbn, isbn.prefix, isbn.valid]
                            # Input ISBN, 13-digit ISBN, Prefix, Valid?
                    ifile.close()
                    print('\r{} records processed'.format(str(filelineno)), end='\r')

                    date_time('Searching for matches from file {}'.format(file))
                    searchList = '\'' + '\', \''.join(i for i in isbn_list) + '\''
                    self.cursor.execute("SELECT isbns.isbn, isbns.format, GROUP_CONCAT(isbn_equivalents.isbnb, ';'), "
                                        "isbn_org_links.pub_status, isbn_org_links.avail_status, isbn_org_links.avail_date, "
                                        "isbn_org_links.org_id, o1.org_name, o1.org_address, o1.org_email, o1.org_url, "
                                        "isbn_org_links.imp_id, o2.org_name, o2.org_address, o2.org_email, o2.org_url "
                                        "FROM isbns INNER JOIN isbn_equivalents ON isbns.isbn = isbn_equivalents.isbna "
                                        "LEFT JOIN isbn_org_links ON isbns.isbn = isbn_org_links.isbn "
                                        "LEFT JOIN organisations AS o1 on isbn_org_links.org_id = o1.org_id "
                                        "LEFT JOIN organisations AS o2 on isbn_org_links.imp_id = o2.org_id "
                                        "WHERE isbns.isbn IN ({}) "
                                        "GROUP BY isbns.isbn "
                                        "ORDER BY isbns.isbn ASC ;".format(searchList))
                    record_count = 0
                    try: row = list(self.cursor.fetchone())
                    except: row = None
                    while row:
                        record_count += 1
                        if record_count % 10000 == 0:
                            print('\r{} records processed'.format(str(record_count)), end='\r')
                        isbn, format, related, pub_status, avail_status, avail_date, \
                        org_id, org_name, org_address, org_email, org_url, \
                        imp_id, imp_name, imp_address, imp_email, imp_url = dedupe_row(row)
                        if isbn in isbn_list:
                            line = isbn_list[isbn][0]
                            prefix = isbn_list[isbn][2]
                            valid = isbn_list[isbn][3]
                            try: pub_status = '{} ({})'.format(pub_status, ONIX_PUBLISHING_STATUS_CODES[pub_status])
                            except KeyError: pass
                            try: avail_status= '{} ({})'.format(avail_status, ONIX_AVAILABILITY_CODES[avail_status])
                            except KeyError: pass
                            tfile.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.
                                        format(line, isbn, prefix, format, valid, related,
                                               pub_status, avail_status, avail_date,
                                               org_id, org_name, org_address, org_email, org_url,
                                               imp_id, imp_name, imp_address, imp_email, imp_url))
                        try: row = list(self.cursor.fetchone())
                        except: row = None
                    del row
                    print('\r{} records processed'.format(str(record_count)), end='\r')
                    tfile.close()
                    del tfile
                    del isbn_list
                    gc.collect()

                    date_time('Reading ISBN matches from temporary file')
                    isbn_list = {}
                    tfile = open(os.path.join(root, file.replace('.txt', '_temp.txt')), mode='r', encoding='utf-8', errors='replace')
                    for filelineno, line in enumerate(tfile):
                        if filelineno % 10000 == 0:
                            print('\r{} records processed'.format(str(filelineno)), end='\r')
                        line = line.strip()
                        isbn_list[line.split('\t')[0]] = line.split('\t')
                    tfile.close()
                    del tfile
                    print('\r{} records processed'.format(str(filelineno)), end='\r')
                    gc.collect()

                    date_time('Writing matches to output')
                    ofile = open(os.path.join(root, file.replace('.txt', '_out.txt')), mode='w', encoding='utf-8', errors='replace')
                    ofile.write('Input ISBN\t13-digit ISBN\tPrefix\tFormat\tValid?\tRelated Identifiers\tPublication status\tAvailability status\tAvailability date\tPublisher ID\tPublisher name\tPublisher address\tPublisher email\tPublisher URL\tImprint ID\tImprint name\tImprint address\tImprint email\tImprint URL\n')
                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace')
                    for filelineno, line in enumerate(ifile):
                        if filelineno % 10000 == 0:
                            print('\r{} records processed'.format(str(filelineno)), end='\r')
                        line = line.strip()
                        if line in isbn_list:
                            ofile.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(*isbn_list[line]))
                        else: ofile.write('{}\t\t\t\tFalse\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n'.format(line))
                    ifile.close()
                    ofile.close()
                    print('\r{} records processed'.format(str(filelineno)), end='\r')
                    gc.collect()
                    return record_count

    def fetch_all(self, query):
        self.cursor.execute(query)
        try: s = set(item[0] for item in self.cursor.fetchall())
        except: s = None
        if s: return s
        s = set()
        for item in self.cursor:
            s.add(item[0])
        return s

    def list_nodes(self):
        return self.fetch_all("""SELECT isbn FROM isbns;""")

    def list_adjacencies(self):
        return self.fetch_all("""SELECT * FROM isbn_equivalents;""")

    def count_nodes(self):
        print('{} nodes in graph'.format(str(len(self.list_nodes()))))

    def count_adjacencies(self):
        print('{} edges in graph'.format(str(len(self.list_adjacencies()))))

    def write_adjacencies(self):
        print('Writing list of adjacencies ...')
        file = open(os.path.join(self.output_path, 'ISBNs_list.txt'), 'w', encoding='utf-8', errors='replace')
        file.write('Identifier\tPrefix\tFormat\tFormat checked?\tValid?\tRelated Identifiers\n')
        query = """
        SELECT isbns.*, GROUP_CONCAT(isbn_equivalents.isbnb, ';')
        FROM isbns LEFT JOIN isbn_equivalents ON isbns.isbn = isbn_equivalents.isbna
        GROUP BY isbns.isbn
        ORDER BY isbns.isbn ASC;"""
        self.cursor.execute(query)
        try: row = list(self.cursor.fetchone())
        except: row = None
        while row:
            isbn, format, checked, adjacencies = dedupe_row(row)
            isbn = Isbn(content=isbn, format=format)
            file.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(isbn.isbn, isbn.prefix, format,
                                                         'True' if checked == 1 else 'False', str(isbn.valid),
                                                         str(adjacencies)))
            try: row = list(self.cursor.fetchone())
            except: break
        file.close()

    def write_isbns_by_format(self, f):
        print('Writing list of {} ISBNs ...'.format(f))
        file = open(os.path.join(self.output_path, 'ISBNS_{}.txt'.format(f)), 'w', encoding='utf-8', errors='replace')
        query = """SELECT isbn FROM isbns WHERE format='{f}' ORDER BY isbn ASC;"""
        self.cursor.execute(query.format(f=f))
        try: row = self.cursor.fetchone()
        except: row = list(self.cursor.fetchone())
        while row:
            file.write('{}\n'.format(str(row[0])))
            try: row = list(self.cursor.fetchone())
            except: break
        file.close()

    def get_formats(self, nodes):
        if not nodes: return None
        formats = {}
        query = """SELECT isbn, format FROM isbns WHERE isbn IN ({searchList}) ORDER BY isbn ASC;"""
        self.cursor.execute(query.format(searchList='\'' + '\', \''.join(nodes) + '\''))
        try: row = self.cursor.fetchone()
        except: row = list(self.cursor.fetchone())
        while row:
            isbn, format = row[0], row[1]
            formats[isbn] = format
            try: row = list(self.cursor.fetchone())
            except: break
        return formats

    def node_connected_component(self, source):
        seen = set()
        nextlevel = {source}
        while nextlevel:
            thislevel = nextlevel
            nextlevel = set()
            query = """SELECT isbnb FROM isbn_equivalents WHERE isbna IN ({searchList}) ORDER BY isbna ASC; """
            self.cursor.execute(query.format(searchList='\'' + '\', \''.join(thislevel) + '\''))
            row = self.cursor.fetchone()
            while row:
                for v in row:
                    if v not in seen:
                        seen.add(v)
                        nextlevel.add(v)
                row = self.cursor.fetchone()
        return seen

    def add_graph_to_database(self, graph, skip_check=False):

        nodes = self.list_nodes()
        print('\nMerging new file into exisiting graph ...')
        print('{} nodes already in graph'.format(str(len(nodes))))
        already_seen = graph.nodes.intersection(nodes)
        new = graph.nodes.difference(already_seen)
        print('{} nodes from file already in graph'.format(str(len(already_seen))))
        print('{} nodes from file to be added to graph'.format(str(len(new))))
        print('Check: {} + {} = {} should be the same as {}'.format(str(len(already_seen)),
                                                                    str(len(new)),
                                                                    str(len(already_seen) + len(new)),
                                                                    str(len(graph.nodes))))
        # Add new nodes
        print('\nAdding new nodes ...')
        i = 0
        query = """
        INSERT OR IGNORE INTO isbns (isbn, format, checked)
        VALUES (?, ?, ?); """
        values = []
        for node in new:
            i += 1
            values.append((node, graph.formats[node], graph.checked[node]))
            if i % 1000 == 0:
                values = self.execute_all(query, values)
        self.execute_all(query, values)
        print('{} new nodes added to graph'.format(str(i)))

        # Update existing nodes
        print('\nUpdating existing nodes ...')
        if already_seen:
            i = 0
            update_formats, update_checked = [], []
            query = """
            SELECT isbn, format, checked FROM isbns WHERE isbn IN ({searchList});"""
            query = query.format(searchList='\'' + '\', \''.join(already_seen) + '\'')
            self.cursor.execute(query)
            row = list(self.cursor.fetchone())
            while row:
                isbn, format, checked = row[0], row[1], row[2]
                if graph.checked[isbn]:
                    i += 1
                    update_formats.append([graph.formats[isbn], isbn])
                    update_checked.append([graph.checked[isbn], isbn])
                elif format != graph.formats[isbn]:
                    i += 1
                    f, c = check_format(isbn, format, graph.formats[isbn], checked, skip_check=skip_check)
                    if f != format:
                        update_formats.append([f, isbn])
                    if c != checked:
                        update_checked.append([c, isbn])
                if i % 1000 == 0:
                    update_formats = self.execute_all("""UPDATE OR REPLACE isbns SET format = ? WHERE isbn = ?;""", update_formats)
                    update_checked = self.execute_all("""UPDATE OR REPLACE isbns SET checked = ? WHERE isbn = ?;""", update_checked)
                try: row = list(self.cursor.fetchone())
                except: break
            self.execute_all("""UPDATE OR REPLACE isbns SET format = ? WHERE isbn = ?;""", update_formats)
            self.execute_all("""UPDATE OR REPLACE isbns SET checked = ? WHERE isbn = ?;""", update_checked)
            print('{} existing nodes updated'.format(str(i)))

        # Add new adjacencies
        i = 0
        query = """INSERT OR IGNORE INTO isbn_equivalents (isbna, isbnb) VALUES (?, ?); """
        values = []
        for node in graph.nodes:
            for adj in graph.adjacencies[node]:
                i += 1
                values.append((node, adj))
                if i % 1000 == 0:
                    values = self.execute_all(query, values)
        self.execute_all(query, values)
        print('{} new adjacencies added to graph'.format(str(i)))

        #self.clean()
        #self.dump_database()


# ====================
#  Control functions
# ====================


'''
def parse_marc(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_marc(input_path, skip_check)
    db.dump_database()
    db.close()
'''


def parse_nielsen(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_nielsen(input_path, skip_check)
    db.dump_database()
    db.close()


def parse_nielsen_org(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_nielsen_org(input_path, skip_check)
    db.dump_database()
    db.close()


def parse_nielsen_product(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_nielsen_product(input_path, skip_check)
    db.dump_database()
    db.close()


'''
def parse_tsv(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_tsv(input_path, skip_check)
    db.dump_database()
    db.close()
'''


def search_isbns(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.search_for_isbns(input_path)
    db.close()


def search_bl(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    #db.search_bl(input_path)
    db.match_bl()
    db.close()


def index(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.build_indexes()
    db.close()


def export_graph(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.clean(transitive=True)
    db.dump_database()
    for f in ISBN_FORMATS:
        db.write_isbns_by_format(f=f)
    db.write_adjacencies()
    db.close()





