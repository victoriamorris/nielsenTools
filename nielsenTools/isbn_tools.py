#!/usr/bin/env python
# -*- coding: utf8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import pyperclip
import regex as re


__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ISBN format codes
# U - unknown
# P - print book
# E - e-book
# A - audio-book
# C - collective
# O - other
# X - contradiction

import json
from time import sleep, time as timestamp
from urllib.request import Request, urlopen

SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}' \
              '&fields=items/volumeInfo(title,authors,industryIdentifiers),items/saleInfo&maxResults=1'
URLOPEN_TIMEOUT = 10  # seconds

class WEBService(object):

    def __init__(self, url):
        self._url = url
        self._request = Request(url, None)
        self.response = None

    def _response(self):
        try: self.response = urlopen(self._request, timeout=URLOPEN_TIMEOUT)
        except: self.response = None

    def data(self):
        self._response()
        return self.response.read().decode(encoding='utf-8', errors='replace')


class WEBQuery(object):
    """Base class to query a webservice and parse the result to py objects."""

    T = {'id': timestamp()}

    def __init__(self, service_url):
        srv = service_url[8:20]
        last = WEBQuery.T[srv] if srv in WEBQuery.T else 0.0
        wait = 0 if timestamp() - last > 1 else 1
        sleep(wait)
        self.url = service_url
        self.service = WEBService(service_url)
        self.data = self.service.data()
        WEBQuery.T[srv] = timestamp()

    def check_data(self):
        if self.data == '{}':
            print('Not found')
        if 'No results match your search' in self.data:
            print('Not found')
        if 'Temporarily out of service' in self.data:
            print('Out of service')
        return True

    def parse_data(self):
        decoder = json.JSONDecoder()
        return decoder.decode(str(self.data))


def _records(isbn, data):
    try: recs = data['items'][0]['volumeInfo']
    except: return None
    if recs:
        ids = recs.get('industryIdentifiers', '')
        if 'ISBN_13' in repr(ids) and isbn not in repr(ids): return None
        try: return data['items'][0]['saleInfo'].get('isEbook', '')
        except: return None

def query(isbn):
    """Query the Google Books (JSON API v1) service for metadata."""
    wq = WEBQuery(SERVICE_URL.format(isbn=isbn))
    r = wq.parse_data() if wq.check_data() else None
    if r:
        return _records(isbn, r)
    return r

# ====================
#      Constants
# ====================


ISBN_FORMATS = ['U', 'P', 'E', 'A', 'C', 'O', 'X']


# ====================
#  Regular expressions
# ====================


RE_ISBN10 = re.compile(r'ISBN\x20(?=.{13}$)\d{1,5}([- ])\d{1,7}'r'\1\d{1,6}\1(\d|X)$|[- 0-9X]{10,16}')
RE_ISBN13 = re.compile(r'97[89]{1}(?:-?\d){10,16}|97[89]{1}[- 0-9]{10,16}')

RE_PUB_PREFIX = re.compile(r'^(?P<pub>0[01][0-9]|'
                           r'0[2-6][0-9]{2}|'
                           r'07[0-9]{3}|'
                           r'08[0-4][0-9]{2}|08[5-9][0-9]{3}|'
                           r'09[0-4][0-9]{4}|09[5-9][0-9]{5}|'
                           r'10[0-9]|'
                           r'1[1-3][0-9]{2}|14[0-9]{3}|'
                           r'15[0-4][0-9]{2}|15[5-8][0-9]{3}|159[0-8][0-9]{2}|1599[0-8][0-9]|15999[0-9]|'
                           r'1[67][0-9]{4}|'
                           r'18[0-5][0-9]{3}|186[0-8][0-9]{2}|1869[0-6][0-9]|18697[0-9]|18698[0-9]{2}|'
                           r'18699[0-8][0-9]|186999[0-9]|18[7-9][0-9]{4}|'
                           r'19[0-8][0-9]{4}|199[0-7][0-9]{3}|1998[0-8][0-9]{2}|19989[0-8][0-9]|'
                           r'199899[0-9]1999[0-8][0-9]{3}|19999[0-8][0-9]{2}|199999[0-8][0-9]|'
                           r'1999999[0-9]|'
                           r'[2-5]|6[01][0-9]|62[01]|[7-8]|9[0-4]|'
                           r'9[5-7][0-9]|98[0-9]|99[0-7][0-9]|998[0-9]|999[0-8][0-9]|9999[0-9])')
# Captures the publisher group for area codes 0 and 1, but only the language area for other ISBNs
RE_PUB_PREFIX_979 = re.compile(r'^(?P<pub>(10(?:[01][0-9]|[2-6][0-9]{2}|[7-8][0-9]{3}|9[0-9]{4}))|'
                               r'(11(?:[01][0-9]|[2-4][0-9]{2}|[5-7][0-9]{3}|8[0-9]{4}|9[0-9]{5}))|'
                               r'(12(?:[01][0-9]|[2-6][0-9]{2}|[7-8][0-9]{3}|9[0-9]{4})))')


# ====================
#       Classes
# ====================


class Isbn(object):

    def __init__(self, content, format='U'):
        self.valid = True
        self.isbn = re.sub(r'[^0-9X]', '', content.upper())
        if is_isbn_10(self.isbn):
            self.isbn = isbn_convert(self.isbn)
        if not is_isbn_13(self.isbn):
            self.valid = False
            if not (len(self.isbn) == 10 or len(self.isbn) == 13):
                self.isbn = None
        self.format = format
        self.prefix = isbn_prefix(self.isbn)
        self.work = None

        if get_resource_format(content):
            self.format = get_resource_format(content)

    def set_format(self, format):
        self.format = format

    def set_work(self, work):
        self.work = work

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}'.format(self.isbn, self.prefix, self.format, str(self.valid), str(self.work))


# ====================
#      Functions
# ====================


def isbn_10_check_digit(nine_digits):
    """Function to get the check digit for a 10-digit ISBN"""
    if len(nine_digits) != 9: return None
    try: int(nine_digits)
    except: return None
    remainder = int(sum((i + 2) * int(x) for i, x in enumerate(reversed(nine_digits))) % 11)
    if remainder == 0: tenth_digit = 0
    else: tenth_digit = 11 - remainder
    if tenth_digit == 10: tenth_digit = 'X'
    return str(tenth_digit)


def isbn_13_check_digit(twelve_digits):
    """Function to get the check digit for a 13-digit ISBN"""
    if len(twelve_digits) != 12: return None
    try: int(twelve_digits)
    except: return None
    thirteenth_digit = 10 - int(sum((i % 2 * 2 + 1) * int(x) for i, x in enumerate(twelve_digits)) % 10)
    if thirteenth_digit == 10: thirteenth_digit = '0'
    return str(thirteenth_digit)


def isbn_10_check_structure(isbn10):
    """Function to check the structure of a 10-digit ISBN"""
    return True if re.match(RE_ISBN10, isbn10) else False


def isbn_13_check_structure(isbn13):
    """Function to check the structure of a 13-digit ISBN"""
    return True if re.match(RE_ISBN13, isbn13) else False


def is_isbn_10(isbn10):
    """Function to validate a 10-digit ISBN"""
    isbn10 = re.sub(r'[^0-9X]', '', isbn10.replace('x', 'X'))
    if len(isbn10) != 10: return False
    return False if isbn_10_check_digit(isbn10[:-1]) != isbn10[-1] else True


def is_isbn_13(isbn13):
    """Function to validate a 13-digit ISBN"""
    isbn13 = re.sub(r'[^0-9X]', '', isbn13.replace('x', 'X'))
    if len(isbn13) != 13: return False
    if isbn13[0:3] not in ('978', '979'): return False
    return False if isbn_13_check_digit(isbn13[:-1]) != isbn13[-1] else True


def isbn_convert(isbn10):
    """Function to convert a 10-digit ISBN to a 13-digit ISBN"""
    if not is_isbn_10(isbn10): return None
    return '978' + isbn10[:-1] + isbn_13_check_digit('978' + isbn10[:-1])


def get_resource_format(s):
    if re.search(r'\b(pack|set|seri(es|a))\b', s, re.I):
        return 'C'
    if re.search(r'\baudio[\-\s]*(b(oo)?k)?\b', s, re.I):
        return 'A'
    if re.search(r'\b(p(aper)?|h(ar)?d?)b(ac|oo)?k?\b|(hard|soft)[\-\s]*cover|(case|spiral)[\-\s]*bound|cased|'
                 r'alk(aline)?\.? paper|print(\b|ed)|\bpaper\b|loose[\-\s]*leaf|\b(h|s)b\b|p-?isbn|\bcloth', s, re.I):
        return 'P'
    if re.search(r'e-?p(ub|df)|\be(-|lectronic)?\s*b(oo)?k|e-?isbn|electronic|'
                 r'\b(adobe|digital|eb|kindle|mobi(pocket)?|myilibrary|u?pdf|online)\b', s, re.I):
        return 'E'
    if re.search(r'\b(cassette|cd(-?rom)?|map)\b', s, re.I):
        return 'O'
    return None


def check_format(isbn, current_format, new_format, checked, skip_check=False):

    if 'C' in [current_format, new_format]:
        return 'C', True
    if checked:
        return current_format, True
    if current_format == new_format:
        return current_format, checked
    if new_format == 'U':
        return current_format, checked
    if current_format == 'U' and new_format in ISBN_FORMATS:
        return new_format, checked
    if isbn.startswith(('978311', '9783484')):
        return 'P', True
    if 'E' in [current_format, new_format] and 'P' in [current_format, new_format]:
        print('\nTrying Google ...')
        try: e = query(isbn)
        except: e = None
        else:
            print('Resolved format of {} using Google Books'.format(isbn))
            if e: return 'P', True
            else: return 'E', True
    if skip_check:
        return 'X', False
    f = None
    while f not in ISBN_FORMATS:
        pyperclip.copy(isbn)
        f = input('Please enter the format of ISBN {} '
                  '(current formats are {}, {}): '.format(isbn, current_format, new_format)).upper()
    return f, True


def isbn_prefix(isbn):
    """Function to return the publisher prefix from a 13-digit ISBN"""
    if is_null(isbn): return ''
    if is_isbn_10(isbn): isbn = isbn_convert(isbn)
    if not is_isbn_13(isbn): return ''
    if isbn.startswith('979'):
        isbn = isbn[3:]
        try: return '979' + RE_PUB_PREFIX_979.search(isbn).group('pub')
        except: return '979' + isbn[3:5]
    elif isbn.startswith('978'):
        isbn = isbn[3:]
        try: return '978' + RE_PUB_PREFIX.search(isbn).group('pub')
        except: return ''
    return ''


def is_null(var):
    """Function to test whether a variable is null"""
    if var is None or not var: return True
    if any(isinstance(var, s) for s in [str, list, tuple, set]) and len(var) == 0: return True
    if isinstance(var, str) and var == '': return True
    if any( isinstance(var, s) for s in [int, float, complex, bool] ) and int(var) == 0: return True
    return False