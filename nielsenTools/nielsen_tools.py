#!/usr/bin/env python
# -*- coding: utf8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import datetime
import os
import gc
import glob
import regex as re
from nielsenTools.database_tools import *
from nielsenTools.isbn_tools import *
from nielsenTools.network_tools import *


__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#       Classes
# ====================


class Nielsen:

    def __init__(self, string):
        entries = string.split(',')
        self.isbn = Isbn(entries[0], format='P' if any(entries[j + 22] == '13' for j in range (0, 10))
                         else 'E' if any(entries[j + 22] == '27' for j in range (0, 10))
                         else 'U')
        for j in range(0, 10):
            if entries[(5*j) + 48] == 'Nielsen Book Release ID' and entries[(5*j) + 47] != '' and entries[(5*j) + 46] == '01':
                self.isbn.set_work(entries[(5*j) + 47])
        self.related = [self.isbn]
        for j in range(0, 10):
            if entries[j + 22] in ['06', '13', '27']:
                # 06 = Alternative format
                # 13 = Epublication based on (print product)
                # 27 = Electronic version available as
                self.related.append(Isbn(entries[j + 2], format='P' if entries[j + 22] == '27'
                                         else 'E' if entries[j + 22] == '13'
                                         else 'U'))

    def get_isbns(self):
        return self.related


class NielsenProduct:

    def __init__(self, csv_row):
        self.row = csv_row
        test = self.row['PFC'] or 'U'
        self.isbn = Isbn((re.sub(r'[^0-9X]', '', self.row['ISBN13'].upper())),
                         format='P' if test[0] in ['B', 'P']
                         else 'A' if test[0] == 'A'
                         else 'O' if test[0] in ['C', 'F', 'L', 'M', 'S', 'V']
                         else 'E' if test[0] in ['D', 'E']
                         else 'U')

        for i in range(1, 10):
            RWI = self.row['RWI{}'.format(str(i))].strip()
            RWITN = self.row['RWITN{}'.format(str(i))].strip() or 'None'
            RWT = self.row['RWT{}'.format(str(i))].strip() or 'None'
            if RWI:
                if RWITN == 'Nielsen Book Release ID' and RWT == '01':
                    self.isbn.set_work(RWI)
            else: break

        self.related = [self.isbn]

        # ISBN13    ISBN13
        # REPIS13   ISBN-13 of book which it replaces
        # REPBIS13  ISBN-13 of book which it is replaced by
        # PUBAIS13  Publisher suggested alternative for this ISBN
        # EPRIS13   E-Publication rendering of this ISBN-13
        # EPBIS13   E-Publication based on this ISBN-13
        for c in ['REPIS13', 'REPBIS13', 'PUBAIS13', 'EPRIS13', 'EPBIS13']:
            v = re.sub(r'[^0-9X]', '', self.row[c].upper())
            if v:
                self.related.append(Isbn(v, 'E' if c in ['EPRIS13', 'EPBIS13'] else 'U'))

    def get_isbns(self):
        if not self.isbn: return None
        return self.related


# ====================
#      Functions
# ====================

def create_graph_from_nielsen_file(file, skip_check=False):

    G = Graph(skip_check=skip_check)

    print('\n\nSearching file {} ...'.format(str(file)))
    print('----------------------------------------')
    print(str(datetime.datetime.now()))

    record_count = 0
    file = open(file, mode='r', encoding='utf-8', errors='replace')

    for filelineno, line in enumerate(file):
        record_count += 1
        if record_count % 100 == 0:
            print('\r{} records processed'.format(str(record_count)), end='\r')

        nielsen = Nielsen(line)

        isbns = nielsen.get_isbns()

        if isbns:
            data = [(i.isbn, i.format, i.work) for i in isbns if i.isbn]
            G.add_nodes(data)
            data = [(i.isbn, j.isbn) for i in isbns for j in isbns if
                    i.isbn and j.isbn and i.isbn != j.isbn and i.format != 'C' and j.format != 'C']
            G.add_edges(data)

    G.check_graph()
    gc.collect()
    return G


def add_from_nielsen_files(input_path, skip_check=False):

    db = IsbnDatabase()

    for file in os.listdir(input_path):
        if file.endswith(('.add', '.upd', '.del')):
            G = create_graph_from_nielsen_file(os.path.join(input_path, file), skip_check=skip_check)
            db.add_graph_to_database(G, skip_check)

    db.close()