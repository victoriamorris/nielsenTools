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
        ('isbn', 'TEXT PRIMARY KEY'),
        ('format', 'TEXT'),
        ('checked', 'BOOLEAN'),
    ]),
    'adjacencies': ([
        ('isbn', 'TEXT'),
        ('adjacency', 'TEXT'),
    ]),
}


# ====================
#       Classes
# ====================


class IsbnDatabase:

    def __init__(self):
        # Connect to database
        date_time_message('Connecting to local database')

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
        for table in GRAPH_TABLES:
            print('Creating table {} ...'.format(table))
            self.cursor.execute('CREATE TABLE IF NOT EXISTS {} '
                                '({}, UNIQUE({}));'
                                .format(table,
                                        ', '.join('{} {}'.format(key, value) for (key, value) in GRAPH_TABLES[table]),
                                        ', '.join(key for (key, value) in GRAPH_TABLES[table])))
        self.conn.commit()
        gc.collect()

    def close(self):
        self.conn.close()

    def clean(self):
        date_time_message('Cleaning database...')

        # Delete null entries
        for table in GRAPH_TABLES:
            print('Deleting NULL entries from table {} ...'.format(table))
            self.cursor.execute('DELETE FROM {} '
                                'WHERE {} IS NULL OR {} IS NULL OR {} = "" OR {} = "" ;'
                                .format(table, GRAPH_TABLES[table][0][0], GRAPH_TABLES[table][1][0],
                                        GRAPH_TABLES[table][0][0], GRAPH_TABLES[table][1][0]))
        self.conn.commit()
        gc.collect()

        # Remove adjacencies for collective ISBNs
        collective = set(item[0] for item in self.cursor.execute("""SELECT isbn FROM isbns WHERE format='C' ;""").fetchall())
        query = """
        DELETE FROM adjacencies
        WHERE isbn IN ({searchList});"""
        query = query.format(searchList='\'' + '\', \''.join(collective) + '\'')
        self.cursor.execute(query)
        query = """
        DELETE FROM adjacencies
        WHERE adjacency IN ({searchList});"""
        query = query.format(searchList='\'' + '\', \''.join(collective) + '\'')
        self.cursor.execute(query)
        self.conn.commit()
        del query
        gc.collect()

        date_time_message('Vacuuming')
        self.conn.execute("VACUUM")
        self.conn.commit()
        gc.collect()

    def build_index(self, table):
        """Function to build indexes in a table"""
        if table not in GRAPH_TABLES:
            print('Table name {} not recognised'.format(table))
            return None
        print('\nBuilding indexes in {} table ...'.format(table))

        self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_0 ;""".format(table))
        self.cursor.execute("""CREATE INDEX IDX_{}_0 ON {} ({});""".format(table, table, GRAPH_TABLES[table][0][0]))
        self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_1 ;""".format(table))
        self.cursor.execute("""CREATE INDEX IDX_{}_1 ON {} ({});""".format(table, table, GRAPH_TABLES[table][1][0]))
        self.conn.commit()
        gc.collect()

    def build_indexes(self):
        """Function to build indexes in the whole database"""
        print('\nBuilding indexes ...')
        print('----------------------------------------')
        print(str(datetime.datetime.now()))

        for table in GRAPH_TABLES:
            self.build_index(table)

    def drop_indexes(self):
        """Function to drop indexes in the whole database"""
        for table in GRAPH_TABLES:
            self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_0 ;""".format(table))
            self.cursor.execute("""DROP INDEX IF EXISTS IDX_{}_1 ;""".format(table))
            self.conn.commit()
        gc.collect()

    def dump_table(self, table):
        """Function to dump a database table into a text file"""
        print('Creating dump of {} table ...'.format(table))
        self.cursor.execute('SELECT * FROM {};'.format(table))
        file = open('{}_DUMP_.txt'.format(table), mode='w', encoding='utf-8', errors='replace')
        record_count = 0
        row = self.cursor.fetchone()
        while row:
            record_count += 1
            if record_count % 100 == 0:
                print('\r{} records processed'.format(str(record_count)), end='\r')
            file.write('{}\n'.format(str(row)))
            row = self.cursor.fetchone()
        del row
        print('\r{} records processed'.format(str(record_count)), end='\r')
        file.close()
        gc.collect()
        print('{} records in {} table'.format(str(record_count), table))
        return record_count

    def dump_database(self):
        """Function to create dumps of all tables within the database"""
        print('\nCreating dump of database ...')
        print('----------------------------------------')
        print(str(datetime.datetime.now()))

        self.count_nodes()
        self.count_adjacencies()

        for table in GRAPH_TABLES:
            self.dump_table('{}'.format(table))

    def add_nielsen(self, input_path, skip_check=True):
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith(('.add', '.upd', '.del')):
                    date_time_message('Searching file {}'.format(str(file)))

                    G = Graph(skip_check=skip_check)

                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                    i = 0
                    c = csv.DictReader(ifile, delimiter=',')
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

    def add_marc(self, input_path, skip_check=True):
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.lex'):
                    date_time_message('Searching file {}'.format(str(file)))
            return

    def search_for_isbns(self, input_path):
        for root, subdirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.txt'):
                    date_time_message('Searching file {}'.format(file))

                    connected_components = {}
                    isbn_list = set()
                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace')
                    for filelineno, line in enumerate(ifile):
                        line = line.strip()
                        isbn = Isbn(line)
                        if isbn.isbn:
                            isbn_list.add(isbn.isbn)
                            if isbn.isbn not in connected_components: connected_components[isbn.isbn] = set()
                    ifile.close()

                    for u in connected_components:
                        for v in connected_components:
                            if u in connected_components[v]:
                                connected_components[u] = connected_components[v]
                                connected_components[u].add(v)
                                break
                        if not connected_components[u]:
                            connected_components[u] = self.node_connected_component(u)

                    formats = self.get_formats([u for u in connected_components])

                    ofile = open(os.path.join(root, file.replace('.txt', '_out.txt')), mode='w',
                                 encoding='utf-8', errors='replace')
                    ofile.write('Input ISBN\t13-digit ISBN\tPrefix\tFormat\tValid?\tRelated Identifiers\n')
                    ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace')

                    for filelineno, line in enumerate(ifile):
                        line = line.strip()
                        isbn = Isbn(line)
                        if isbn.isbn in formats: isbn.format = formats[isbn.isbn]
                        ofile.write('{}\t{}\t{}\n'.format(line, str(isbn),
                                                          ';'.join(sorted(
                                                              connected_components[isbn.isbn])) if isbn.isbn else ''))
                    ifile.close()
                    ofile.close()

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
        return self.fetch_all("""SELECT isbn FROM adjacencies;""")

    def count_nodes(self):
        print('{} nodes in graph'.format(str(len(self.list_nodes()))))

    def count_adjacencies(self):
        print('{} edges in graph'.format(str(len(self.list_adjacencies()))))

    def write_adjacencies(self):
        print('Writing list adjacencies ...')
        file = open(os.path.join(self.output_path, 'ISBNs_list.txt'), 'w', encoding='utf-8', errors='replace')
        file.write('Identifier\tPrefix\tFormat\tFormat checked?\tValid?\tRelated Identifiers\n')
        query = """
        SELECT isbns.*, GROUP_CONCAT(adjacencies.adjacency, ';')
        FROM isbns LEFT JOIN adjacencies ON isbns.isbn = adjacencies.isbn
        GROUP BY isbns.isbn
        ORDER BY isbns.isbn ASC;"""
        self.cursor.execute(query)
        try: row = list(self.cursor.fetchone())
        except: row = None
        while row:
            isbn, format, checked, adjacencies = row[0], row[1], row[2], row[3]
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
        query = """SELECT isbn, format FROM isbns WHERE isbn IN ({searchList}) ORDER BY isbn ASC; """
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
            query = """SELECT adjacency FROM adjacencies WHERE isbn IN ({searchList}) ORDER BY isbn ASC; """
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
                self.cursor.executemany(query, values)
                values = []
        if values: self.cursor.executemany(query, values)
        self.conn.commit()
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
                    if update_formats:
                        self.cursor.executemany("""UPDATE OR REPLACE isbns SET format = ? WHERE isbn = ?;""", update_formats)
                    if update_checked:
                        self.cursor.executemany("""UPDATE OR REPLACE isbns SET checked = ? WHERE isbn = ?;""", update_checked)
                    update_formats, update_checked = [], []
                try:
                    row = list(self.cursor.fetchone())
                except:
                    break
            if update_formats:
                self.cursor.executemany("""UPDATE OR REPLACE isbns SET format = ? WHERE isbn = ?;""", update_formats)
            if update_checked:
                self.cursor.executemany("""UPDATE OR REPLACE isbns SET checked = ? WHERE isbn = ?;""", update_checked)
                self.conn.commit()
            print('{} existing nodes updated'.format(str(i)))

        # Add new adjacencies
        i = 0
        query = """
        INSERT OR IGNORE INTO adjacencies (isbn, adjacency)
        VALUES (?, ?); """
        values = []
        for node in graph.nodes:
            for adj in graph.adjacencies[node]:
                i += 1
                values.append((node, adj))
                if i % 1000 == 0:
                    self.cursor.executemany(query, values)
                    values = []
        if values: self.cursor.executemany(query, values)
        self.conn.commit()
        print('{} new adjacencies added to graph'.format(str(i)))

        self.clean()
        self.dump_database()


# ====================
#  Control functions
# ====================


def parse_marc(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_marc(input_path, skip_check)
    db.close()


def parse_nielsen(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.add_nielsen(input_path, skip_check)
    db.close()


def search_isbns(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.search_for_isbns(input_path)
    db.close()


def index(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.build_indexes()
    db.close()


def export_graph(input_path, skip_check=True) -> None:
    db = IsbnDatabase()
    db.clean()
    db.dump_database()
    for f in ISBN_FORMATS:
        db.write_isbns_by_format(f=f)
    db.write_adjacencies()
    db.close()





