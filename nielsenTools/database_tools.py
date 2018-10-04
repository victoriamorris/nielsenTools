#!/usr/bin/env python
# -*- coding: utf8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import datetime
import gc
import os
import sqlite3
from nielsenTools.isbn_tools import *

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'

# ====================
#      Constants
# ====================

DATABASE_PATH = 'Database\\ISBNs.db'


# ====================
#       Classes
# ====================


class IsbnDatabase:

    def __init__(self):
        # Connect to database
        print('\n\nConnecting to local database ...')
        print('----------------------------------------')
        print(str(datetime.datetime.now()))

        self.output_path = os.path.dirname(DATABASE_PATH)
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

        # Set up database
        self.cursor.execute('PRAGMA synchronous=OFF')
        self.cursor.execute('PRAGMA journal_mode = OFF')
        self.cursor.execute('PRAGMA locking_mode = EXCLUSIVE')
        self.cursor.execute('PRAGMA count_changes = FALSE')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS isbns (isbn TEXT PRIMARY KEY, format TEXT, checked BOOLEAN);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS adjacencies (isbn TEXT, adjacency TEXT);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS works (isbn TEXT, nielsen_id TEXT);')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def clean(self):
        print('\nCleaning database...')

        # Delete duplicate adjacencies
        self.cursor.execute("""
        DELETE FROM adjacencies
        WHERE rowid NOT IN (SELECT min(rowid) FROM adjacencies GROUP BY isbn, adjacency);""")
        self.conn.commit()

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
        self.conn.execute("VACUUM")
        gc.collect()

    def dump_table(self, table_name):
        """Function to dump a database table into a text file"""
        record_count = 0
        self.cursor.execute('SELECT * FROM {};'.format(table_name))
        print('Creating dump of {} table'.format(table_name))
        file = open(os.path.join(self.output_path, '{}_DUMP_.txt'.format(table_name)), mode='w', encoding='utf-8', errors='replace')
        row = self.cursor.fetchone()
        while row:
            record_count += 1
            file.write('{}\n'.format(str(row)))
            row = self.cursor.fetchone()
        file.close()
        gc.collect()
        print('{} records in {} table'.format(str(record_count), table_name))
        return record_count

    def list_nodes(self):
        self.cursor.execute("""SELECT isbn FROM isbns;""")
        return set(item[0] for item in self.cursor.fetchall())

    def list_adjacencies(self):
        self.cursor.execute("""SELECT isbn FROM adjacencies;""")
        return set(item[0] for item in self.cursor.fetchall())

    def list_works(self):
        self.cursor.execute("""SELECT isbn FROM works;""")
        return set(item[0] for item in self.cursor.fetchall())

    def count_nodes(self):
        print('{} nodes in graph'.format(str(len(self.list_nodes()))))

    def count_adjacencies(self):
        print('{} edges in graph'.format(str(len(self.list_adjacencies()))))

    def count_works(self):
        print('{} works in graph'.format(str(len(self.list_works()))))

    def write_adjacencies(self):
        print('Writing list adjacencies ...')
        file = open(os.path.join(self.output_path, 'ISBNs_list.txt'), 'w', encoding='utf-8', errors='replace')
        file.write('ISBN\tPrefix\tFormat\tFormat checked?\tValid?\tRelated ISBNs\n')
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

    def get_works(self, nodes):
        if not nodes: return None
        works = {}
        query = """SELECT isbn, nielsen_id FROM works WHERE isbn IN ({searchList}) ORDER BY isbn ASC; """
        self.cursor.execute(query.format(searchList='\'' + '\', \''.join(nodes) + '\''))
        try: row = self.cursor.fetchone()
        except: row = list(self.cursor.fetchone())
        while row:
            isbn, work = row[0], row[1]
            works[isbn] = work
            try: row = list(self.cursor.fetchone())
            except: break
        return works

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
        INSERT INTO isbns (isbn, format, checked)
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
                        self.cursor.executemany("""UPDATE isbns SET format = ? WHERE isbn = ?;""", update_formats)
                    if update_checked:
                        self.cursor.executemany("""UPDATE isbns SET checked = ? WHERE isbn = ?;""", update_checked)
                    update_formats, update_checked = [], []
                try:
                    row = list(self.cursor.fetchone())
                except:
                    break
            if update_formats:
                self.cursor.executemany("""UPDATE isbns SET format = ? WHERE isbn = ?;""", update_formats)
            if update_checked:
                self.cursor.executemany("""UPDATE isbns SET checked = ? WHERE isbn = ?;""", update_checked)
                self.conn.commit()
            print('{} existing nodes updated'.format(str(i)))

        # Add new adjacencies
        i = 0
        query = """
        INSERT INTO adjacencies (isbn, adjacency)
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

        # Add new work IDs
        i = 0
        query = """
                INSERT INTO works (isbn, nielsen_id)
                VALUES (?, ?); """
        values = []
        for node in graph.nodes:
            if node in graph.works and graph.works[node]:
                i += 1
                values.append((node, graph.works[node]))
                if i % 1000 == 0:
                    self.cursor.executemany(query, values)
                    values = []
        if values: self.cursor.executemany(query, values)
        self.conn.commit()
        print('{} new work relationships added to graph'.format(str(i)))

        self.clean()

        self.dump_table('isbns')
        self.dump_table('adjacencies')
        self.dump_table('works')

        # Display graph properties
        self.count_nodes()
        self.count_adjacencies()
        self.count_works()


# ====================
#      Functions
# ====================


def export_database():

    db = IsbnDatabase()
    for f in ISBN_FORMATS:
        db.write_isbns_by_format(f=f)
    db.write_adjacencies()
    db.close()


def search_for_isbns(path):

    db = IsbnDatabase()

    connected_components = {}
    isbn_list = set()
    ifile = open(path, mode='r', encoding='utf-8', errors='replace')
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
            connected_components[u] = db.node_connected_component(u)

    formats = db.get_formats([u for u in connected_components])
    works = db.get_works([u for u in isbn_list])

    ofile = open(path.replace('.txt', '_out.txt'), mode='w', encoding='utf-8', errors='replace')
    ofile.write('Input ISBN\t13-digit ISBN\tPrefix\tFormat\tValid?\tNielsen Work ID\t\tRelated ISBNs\n')
    ifile = open(path, mode='r', encoding='utf-8', errors='replace')

    for filelineno, line in enumerate(ifile):
        line = line.strip()
        isbn = Isbn(line)
        if isbn.isbn in formats: isbn.format = formats[isbn.isbn]
        if works and isbn.isbn in works: isbn.work = works[isbn.isbn]
        ofile.write('{}\t{}\t{}\n'.format(line, str(isbn),
                                          ';'.join(sorted(connected_components[isbn.isbn])) if isbn.isbn else ''))
    ifile.close()
    ofile.close()

    db.close()






