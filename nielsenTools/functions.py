#  -*- coding: utf-8 -*-

"""Functions used within nielsenTools."""

# Import required modules
import datetime
import locale
import sys
import unicodedata
import regex as re

import nielsenTools.multiregex as mrx

# Set locale to assist with sorting
locale.setlocale(locale.LC_ALL, '')
__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#      Constants
# ====================

BRACKETS = [('[', ']'), ('(', ')'), ('{', '}')]


# ====================
#  General Functions
# ====================


def usage(conversion_type='Products'):
    """Function to print information about the program"""
    print('Correct syntax is:')
    print('nielsen2marc_{} -i <input_path> -o <output_path> [options]'.format(conversion_type.lower()))
    print('    -i    path to FOLDER containing Input files')
    print('    -o    path to FOLDER to contain Output files')
    print('If not specified, input path will be /Input/{}'.format(conversion_type))
    print('If not specified, output path will be /Output/{}'.format(conversion_type))
    print('\nUse quotation marks (") around arguments which contain spaces')
    print('\nInput file names should end .add, .upd or .del')
    print('\nOptions')
    print('    --help      Display this message and exit')
    if conversion_type=='Products':
        print('    --database  Add ISBN information to database')
    exit_prompt()


def date_time_message(message=None):
    if message: print('\n\n{} ...'.format(message))
    print('----------------------------------------')
    print(str(datetime.datetime.now()))


def date_time_exit():
    date_time_message(message='All processing complete')
    sys.exit()


def message(s) -> str:
    """Function to convert OPTIONS description to present tense"""
    if s == 'Exit program': return 'Shutting down'
    return s.replace('Parse', 'Parsing').replace('eXport', 'Exporting').replace('Search', 'Searching').replace('build', 'Building').replace('Index', 'index')


def exit_prompt(message=None):
    """Function to exit the program after prompting the use to press Enter"""
    if message: print(str(message))
    input('\nPress [Enter] to exit...')
    sys.exit()


'''
def check_file_location(file_path, file_ext='', function='input', exists=False):
    """Function to check whether a file exists and has the correct file extension"""
    folder, file, ext = '', '', ''
    try:
        file, ext = os.path.splitext(os.path.basename(file_path))
        ext = ext.lower()
        folder = os.path.dirname(file_path)
    except:
        exit_prompt('Error: Could not parse path to {} file'.format(function))
    if file_ext != '' and ext != file_ext:
        exit_prompt('Error: The {} file should have the extension {}'.format(function, file_ext))
    if exists and not os.path.isfile(os.path.join(folder, file + ext)):
        exit_prompt('Error: The specified {} file cannot be found'.format(function))
    return folder, file, ext
'''

# ====================
#    Functions for
#   cleaning strings
# ====================


def clean(string):
    if string is None or not string: return None
    string = re.sub(r'[\u0022\u055A\u05F4\u2018-\u201F\u275B-\u275E\uFF07]', '\'', string)
    string = re.sub(r'[\u0000-\u001F\u0080-\u009F\u2028\u2029]+', '', string)
    string = re.sub(r'^[:;/\s\?\$\.,\\\]\)}]|[;/\s\$\.,\\\[\({]+$', '', string.strip())
    '''if to_strip:
        while len(string) > 0 and string[-1] in to_strip:
            string = re.sub(r'^[:;/\s]|[;/\s]+$', '',  string[:-1])'''
    string = re.sub(r'\s+', ' ', string).strip()
    if string is None or not string: return None
    return unicodedata.normalize('NFC', string)


def clean_html(string):
    if string is None or not string: return None
    string = re.sub(r'</?(br|p|li|ul|ol)\s*/?>|\t', '\n', string)
    string = re.sub(r'</?(b|i|ul)\s*>', '', string)
    string = re.sub(r'<(?:[A-Za-z]+:)?([A-Za-z][A-Za-z0-9]*)\b[^>]*>(.*?)</\1>', r'\2', string)
    string = re.sub(r'[\r\n]+', '\n', string)
    string = re.sub(r' +', ' ', string)
    return string


def check_brackets(string):
    """Function to check for inconsistent brackets"""
    if string is None or not string: return None
    string = clean(string)
    for (oB, cB) in [('[', ']'), ('<', '>')]:
        while string.startswith(oB) and string.endswith(cB):
            string = clean(string[1:-1])
    for (oB, cB) in BRACKETS:
        while string.startswith(oB) and cB not in string:
            string = clean(string[1:])
        while string.endswith(cB) and oB not in string:
            string = clean(string[:-1])
    for (oB, cB) in BRACKETS:
        while string.count(oB) > string.count(cB):
            string = string + cB
        while string.count(cB) > string.count(oB):
            string = oB + string
        string = clean(string)
    for (oB, cB) in BRACKETS:
        if oB in string and cB in string and string.index(cB) < string.index(oB):
            string = clean(string.replace(cB, '').replace(oB, ''))
    string = string.replace('()', '').replace('{}', '').replace('[]', '').replace('<>', '')
    return clean(string)


def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])


def rreplace(string, old, new, occurrence=1):
    return new.join(string.rsplit(old, occurrence))


def format_date(d):
    if not d: return None
    d = re.sub(r'[^0-9]]', '', d)
    if d and len(d) >= 4: return d[:4]
    return None


def _split_long(text, regex, separator='. '):
    sentences = iter(regex.split(text))
    lines, current = [], next(sentences)
    for sentence in sentences:
        if len(current) + 2 + len(sentence) > 5000:
            current = clean(current)
            if current:
                lines.append(current)
            current = sentence
        else:
            current += separator + sentence
    current = clean(current)
    if current:
        lines.append(current)
    return lines


def split_long(text, isbn=None):
    lines = _split_long(text, regex=re.compile(r'[\n\r]+'), separator=' ')
    if not lines: return []
    if max(len(l) for l in lines) <= 5000:
        return lines
    regex = re.compile(r'\.\-|\.?\t|\.?\s{2,}|\s(?=[0-9]+\.|\*\s+|\n)')
    if not regex.search(text): regex = re.compile(r'\.\s+')
    lines = _split_long(text, regex=regex, separator='. ')
    if lines == []: return []
    if max(len(l) for l in lines) <= 5000:
        return lines
    lines = _split_long(text, regex=re.compile(r'\s+'), separator=' ')
    if max(len(l) for l in lines) > 5000:
        print('Error 2: ' + str(max(len(l) for l in lines)) + ': ' + str(isbn))
    return lines


def expand_abbreviations(string, plurals=True, case=True):
    if string is None or not string: return None

    # Expand single-word abbreviations
    words = re.split('([\w\-]+\.*)', string)
    for i, word in enumerate(words):
        words[i] = mrx.Abbreviations().sub(words[i])
        if word != '' and case:
            if word.isupper():
                words[i] = words[i].upper()
            elif word[0].isupper():
                words[i] = words[i].capitalize()
        if words[i] in ['numbers', 'volumes', 'parts'] and not plurals:
            words[i] = words[i].rstrip('s')

    # Re-join string
    string = clean(''.join(words))
    return string


def change_case_specific(string, words, case='lower'):
    """Function to convert specific words in a string to a specific case"""
    if string == '': return ''
    if not words or len(words) == 0: return string
    if case not in ['lower', 'upper', 'caps']: return string
    try:
        rx = re.compile('\b(' + '|'.join(w.lower() for w in words) + ')\b', flags=re.IGNORECASE)
        if case == 'lower': string = rx.sub(lambda m: m.group(1).lower(), string)
        elif case == 'upper': string = rx.sub(lambda m: m.group(1).upper(), string)
        elif case == 'caps': string = rx.sub(lambda m: m.group(1).capitalise(), string)
        return clean(string)
    except: return string


def clean_edition(string):
    if string is None or not string: return None
    string = expand_abbreviations(string)
    words = ('a', 'abridged', 'another', 'augmented', 'by', 'complete', 'critical',
             'edition', 'edited', 'editor', 'editors', 'exclusive',
             'first', 'further', 'illustrated', 'imprinted', 'international', 'limited', 'new', 'notes',
             'prepared', 'printed', 'reprinted', 'revised', 'series', 'special', 'the', 'unabridged', 'with')
    string = change_case_specific(string, words, case='lower')
    string = clean(string)
    return string


def clean_description(string):
    if string is None or not string: return None
    string = expand_abbreviations(string)
    if string is None or not string: return None
    string = string.replace('color', 'colour').lower()
    string = re.sub(r', unspecified\s*$', '', re.sub(r'\s*\b(b[&/]?w|black-and-white)\b\s*', ' black and white ', string))
    if string in ['0', 'total illustrations: 0']: return None
    if string == 'total illustrations: 1': return '1 illustration'
    string = re.sub(r'^total illustrations: ([0-9]+)$', r'\1 illustrations', string)
    string = clean(string)
    return string
