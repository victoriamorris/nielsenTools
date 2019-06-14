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


class NielsenTSVProducts:

    def __init__(self, csv_row, status):
        self.row = csv_row
        self.status = status
        self.UK = False

        self.values = {}
        for v in ['CBMCCODE', 'CIS', 'COP', 'CY', 'FICGH', 'IA', 'ILL', 'IMPID', 'ISBN13', 'KEYWORDS', 'PFC', 'PFCT',
                  'PPTCT', 'PRODCT', 'PSF', 'PUBID', 'PUBPD', 'RA', 'REISD', 'RSS', 'USGCT']:
            try: self.values[v] = clean(self.row[v])
            except: self.values[v] = None
        if not self.values['ISBN13']: self.values['ISBN13'] = '[NO RECORD IDENTIFIER]'
        if not self.values['PUBPD']:
            if 'UKLPUBD' in self.row: self.values['PUBPD'] = clean(self.row['UKLPUBD'])
            elif 'UKNBDLPD' in self.row: self.values['PUBPD'] = clean(self.row['UKNBDLPD'])
        self.values['NAC'], i = '|', 1
        while self.values['NAC'] == '|' and i in range(1, 10):
            try: self.values['NAC'] = AUDIENCE_CODES[clean(self.row['NAC{}'.format(str(i))])]
            except:
                try: self.values['NAC'] = ONIX_AUDIENCE_CODES[clean(self.row['OAC{}'.format(str(i))])]
                except: self.values['NAC'] = '|'
            i += 1
        i = 1
        while not self.values['PFC'] and i in range(1, 10):
            try: self.values['PFC'] = clean(self.row['PFD{}'.format(str(i))])
            except: self.values['PFC'] = None
            i += 1

        self.material_type = self.material_type()

    def is_uk(self):
        return self.UK

    def record_id(self):
        if self.values['ISBN13'] and self.values['ISBN13'] != '[NO RECORD IDENTIFIER]':
            return self.values['ISBN13']
        return None

    def material_type(self):
        if not self.values['PFC']: return None
        if self.values['PFC'][0] == 'A': return 'MU'
        if self.values['PFC'] in ['PI']: return 'MU'
        if self.values['PFC'][0] in ['B', 'M', 'E']: return 'BK'
        if self.values['PFC'] in ['PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PL', 'PR', 'PS', 'PU', 'PZ']: return 'BK'
        if self.values['PFC'][0] == 'C': return 'MP'
        if self.values['PFC'][0] in ['D']: return 'CF'
        if self.values['PFC'][0] in ['F', 'L', 'V', 'X', 'Z']: return 'VM'
        if self.values['PFC'] in ['PG', 'PH', 'PJ', 'PK', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PT']: return 'VM'
        if self.values['PFC'][0] == 'S': return 'MX'
        if self.values['PFC'][:2] in ['P1', 'P2']: return 'BK'
        if self.values['PFC'][:2] == 'P3': return 'VM'
        return None

    def marc(self):

        # Leader (NR)
        try: p6 = ONIX_PRODUCT_CONTENT_TYPE[clean(self.row['PCTC1'])].leader_06
        except:
            try: p6 = ONIX_PRODUCT_FORM[self.values['PFC']][4]
            except: p6 = 'a'
        if p6 == 'a': self.material_type = 'BK'
        leader = '     {}{}m a22     2  4500'.format(self.status, p6)

        record = Record(leader=leader)

        record.add_field(Field(tag='FMT', data=self.material_type))

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
        # PUBPD     Date of Publication: as supplied by Publisher or approved source
        # UKNBDLPD  Date of Publication: as supplied by Publisher or approved source
        # REISD     Re-issue date
        # CY        Copyright Year
        if self.values['PUBPD'] and self.values['REISD'] and self.values['PUBPD'] != self.values['REISD']:
            data += 'r' + format_date(self.values['REISD']) + format_date(self.values['PUBPD'])
        elif self.values['PUBPD'] and self.values['CY'] and self.values['CY'] != self.values['PUBPD']:
            data += 't' + format_date(self.values['PUBPD']) + format_date(self.values['CY'])
        elif self.values['PUBPD']:
            data += 's' + format_date(self.values['PUBPD']) + '    '
        else: data += 'nuuuuuuuu'
        # 15-17 - Place of publication, production, or execution
        # COP   Country of publication
        if self.values['COP'] and self.values['COP'] in COUNTRY_CODES and COUNTRY_CODES[self.values['COP']] in ['xxk', 'enk', 'ie ', 'nik', 'stk', 'wlk']: self.UK = True
        try: data += COUNTRY_CODES[self.values['COP']]
        except:
            if self.values['COP']: print(self.values['COP'] + '\n')
            data += 'xx '

        # Positions 18 to 34 depend upon the material type
        if self.material_type == 'MP':
            # 18-21 - Relief
            data += '||||'
            # 22-23 - Projection
            data += '||'
            # 24 - Undefined
            data += ' '
            # 25 - Type of cartographic material
            try: data += ONIX_PRODUCT_FORM[self.values['PFC']][0]
            except: data += '|'
            # 26 - 27 - Undefined
            data += '  '
            # 28 - Government publication
            data += '|'
            # 29 - Form of item
            if self.values['PFC'][0] == 'C': data += 'r'
            else: data += '|'
            # 30 - Undefined
            data += ' '
            # 31 - Index
            data += '|'
            # 32 - Undefined
            data += ' '
            # 33-34 - Special format characteristics
            data += '||'
        elif self.material_type == 'MU':
            # 18-19 - Form of composition
            data += '||'
            # 20 - Format of music
            if self.values['PFC'] == 'PI': data += 'u'
            else: data += 'n'
            # 21 - Music parts
            if self.values['PFC'] == 'PI': data += 'u'
            else: data += 'n'
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            # OAC*  ONIX Audience level: Code
            data += self.values['NAC']
            # 23 - Form of item
            if self.values['PFC'] == 'PI': data += 'r'
            elif self.values['PFC'] in ['AN', 'AO']: data += 'o'
            elif self.values['PFC'] in ['AJ', 'AK', 'AL']: data += 's'
            else: data += '|'
            # 24-29 - Accompanying matter
            data += '||||||'
            # 30-31 - Literary text for sound recordings
            test_string = '|' + '|'.join(self.row['{}{}'.format(subject_type, str(i))]
                                         for subject_type in [s for s in ['BIC2ST', 'BISACT', 'THEMAST', 'UKSLCAFT', 'UKSLCANFT', 'UKSLCCT'] if '{}1'.format(s) in self.row]
                                         for i in range(1, 6 if subject_type.startswith('UKSLC') else 10)).lower()
            data += 'a' if 'autobiography' in test_string \
                else 'b' if 'biography' in test_string \
                else 'd' if '|drama' in test_string \
                else 'e' if ('|essays' in test_string or '/ essays' in test_string) \
                else 'k' if 'comedy' in test_string \
                else 'm' if ('|memoir' in test_string or '/ memoir' in test_string) \
                else 'o' if ('folk tale' in test_string or 'folklore' in test_string or 'fairy tale' in test_string) \
                else 'p' if '|poetry' in test_string \
                else 'f' if ('|fiction' in test_string or ' fiction' in test_string) \
                else '|'
            # 32 - Undefined
            data += ' '
            # 33 - Transposition and arrangement
            data += '|'
            # 34 - Undefined
            data += ' '
        elif self.material_type == 'VM':
            # RUN   Running Time
            try: RUN = clean(re.sub(r'[^0-9]', '', self.row['RUN']))
            except: RUN = None
            if RUN:
                RUN = int(RUN)
                if RUN < 999: data += '{m:03d}'.format(m=RUN)
                else: data += '000'
            elif self.values['PFC'][0] == 'V': data += '---'
            else: data += 'nnn'
            # 21 - Undefined
            data += ' '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            # OAC*  ONIX Audience level: Code
            data += self.values['NAC']
            # 23-27 - Undefined
            data += '     '
            # 28 - Government publication
            data += '|'
            # 29 - Form of item
            if self.values['PFC'][0] == 'F' or self.values['PFC'] in ['PH', 'PM']: data += ' '
            elif self.values['PFC'] in ['PG', 'PJ', 'PK']: data += 'r'
            else: data += '|'
            # 30-32 - Undefined
            data += '   '
            # 33 - Type of visual material
            try: data += ONIX_PRODUCT_FORM[self.values['PFC']][0]
            except: data += '|'
            # 34 - Technique
            data += '|'
        elif self.material_type == 'CF':
            # 18-21 - Undefined
            data += '    '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            # OAC*  ONIX Audience level: Code
            data += self.values['NAC']
            # 23 - Form of item
            data += 'o' if self.values['PFC'] == 'EC' else '|'
            # 24-25 - Undefined
            data += '  '
            # 26 - Type of computer file
            data += 'g' if self.values['PFC'] == 'DE' else '|'
            # 27 - Undefined
            data += ' '
            # 28 - Government publication
            data += '|'
            # 29-34 - Undefined
            data += '      '
        elif self.material_type == 'BK':
            # 18-21 - Illustrations
            # ILL   Illustrations and other contents note.
            if self.values['ILL']: data += (''.join(ILLUSTRATIONS[x] for x in ILLUSTRATIONS if x in self.values['ILL']) + '    ')[:4]
            else: data += '    '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            # OAC*  ONIX Audience level: Code
            data += self.values['NAC']
            # 23 - Form of item
            # PFC   Product Form: Code
            try: data += ONIX_PRODUCT_FORM[self.values['PFC']][0]
            except: data += '|'
            # 24-27 - Nature of contents
            # PFCT      Product Form :Text Description
            # PCTCT*    Product Content: Text Description
            test_string = self.values['PFCT'] or ''
            test_string += '|' + (self.values['ILL'] or '')
            try: test_string += '|' + '|'.join(self.row['PCTCT{}'.format(i)] for i in range(1, 10))
            except: pass
            data += (''.join(RE_NATURE_OF_CONTENTS[x] for x in RE_NATURE_OF_CONTENTS if re.search(x, test_string)) + '||||')[:4]
            # 28 - Government publication
            data += '|'
            # 29 - Conference publication
            data += '|'
            # 30 - Festschrift
            data += '|'
            # 31 - Index
            data += '|'
            # 32 - Undefined
            data += ' '
            # 33 - Literary form
            test_string = '|' + '|'.join(self.row['{}{}'.format(subject_type, str(i))]
                                         for subject_type in [s for s in ['BIC2ST', 'BISACT', 'THEMAST', 'UKSLCAFT', 'UKSLCANFT', 'UKSLCCT'] if '{}1'.format(s) in self.row]
                                         for i in range(1, 6 if subject_type.startswith('UKSLC') else 10)).lower()
            data += 'd' if '|drama' in test_string \
                else 'e' if ('|essays' in test_string or '/ essays' in test_string) \
                else 'i' if '/ letters' in test_string \
                else 'j' if ('|short stories' in test_string or '/ short stories' in test_string) \
                else 'p' if '|poetry' in test_string \
                else '1' if ('|fiction' in test_string or ' fiction' in test_string) \
                else '0' if ('nonfiction' in test_string or 'non-fiction' in test_string) \
                else '|'
            # 34 - Biography
            data += 'a' if 'autobiography' in test_string else 'd' if 'biography' in test_string else '|'
        elif self.material_type == 'MX': data += '     |           '
        else: data += '|||||||||||||||||'
        # 35-37 - Language
        try: data += clean(self.row['LC1'] + '   ')[:3]
        except: data += '   '
        # 38 - Modified record
        data += '|'
        # 39 - Cataloging source
        data += ' '
        record.add_field(Field(tag='008', data=data))

        # 020 - International Standard Book Number (R)
        fmts = set()
        for c in ['EPT', 'EPF', 'EPFS']:
            try: v = clean(self.row[c])
            except: v = None
            if v and v not in ['Unspecified', 'Format code not yet allocated']:
                fmts.add(re.sub(r'\s*format$', '', v))

        # ISBN13    ISBN13
        # REPIS13   ISBN-13 of book which it replaces
        # REPBIS13  ISBN-13 of book which it is replaced by
        # PUBAIS13  Publisher suggested alternative for this ISBN
        # EPRIS13   E-Publication rendering of this ISBN-13
        # EPBIS13   E-Publication based on this ISBN-13
        for c in ['ISBN13', 'REPIS13', 'REPBIS13', 'PUBAIS13', 'EPRIS13', 'EPBIS13']:
            try: v = clean(re.sub(r'[^0-9X]', '', self.row[c].upper()))
            except: v = None
            if v:
                subfields = ['a' if c == 'ISBN13' else 'z', v]
                if c in ['EPRIS13', 'EPBIS13']:
                    subfields.extend(['q', 'electronic'])
                elif c == 'ISBN13':
                    qualifier = None
                    if self.values['PFCT'] and ('PFC' not in self.row or (self.values['PFC'][0] != 'X' and self.values['PFC'] not in ['00', 'ZZ'])):
                        qualifier = clean(re.sub(r'undefined|other|miscellaneous|\b(carrier|format|text)$', '', self.values['PFCT'], re.I))
                        if re.match(r'[A-Z][a-z]', qualifier): qualifier = qualifier[0].lower() + qualifier[1:]
                    if not qualifier and fmts: qualifier = 'electronic book'
                    if qualifier:
                        if fmts: qualifier += ' ({} format)'.format(list(fmts)[0])
                        subfields.extend(['q', qualifier])
                record.add_field(Field('020', [' ', ' '], subfields))

        # 024 - Other Standard Identifier (R)
        for c in ['EAN', 'ISMN', 'DOI']:
            try: v = self.row[c].strip()
            except: v = None
            if v == '': v = None
            if v:
                subfields = ['a', v]
                if c == 'DOI': subfields.extend(['2', 'doi'])
                indicators = ['3' if c == 'EAN' else '2' if c == 'ISMN' else '7', ' ']
                record.add_field(Field('024', indicators, subfields))

        # 034 - Coded Cartographic Mathematical Data (R)
        # MS*   Map scale as stored
        for i in range(1, 2):
            try: MS = clean(self.row['MS{}'.format(str(i))])
            except: MS = None
            if MS:
                MS = re.sub(r'[^0-9]', '', MS.split(':')[-1])
                record.add_field(Field('034', ['1', ' '], ['a', 'a', 'b', MS]))

        # 040 - Cataloging Source (NR)
        record.add_field(Field('040', [' ', ' '], ['a', 'UK-WkNB', 'b', 'eng', 'c', 'Uk', 'd', 'Uk']))

        # 041 - Language Code (R)
        # LC*   Language of Text: Code
        # LT*   Language of Text: Text Description
        # TFC*  Language translated from original language: Code
        # TFT*  Language translated from original language: Text Description
        languages = set()
        translations = set()
        for i in range(1, 10):
            try: l = clean(self.row['LC{}'.format(str(i))])
            except: l = None
            if l: languages.add(l)
        for i in range(1, 10):
            try: LT =  clean(self.row['LT{}'.format(str(i))])
            except: LT = None
            if LT:
                for l in LANGUAGE_REPLACEMENTS: LT = LT.replace(l, LANGUAGE_REPLACEMENTS[l])
                for l in LT.split(','):
                    try: languages.add(LANGUAGES_CODES[l.strip()])
                    except: pass
        for i in range(1, 5):
            try: l = clean(self.row['TFC{}'.format(str(i))])
            except: l = None
            if l: translations.add(l)
        for i in range(1, 10):
            try: TFT =  clean(self.row['TFT{}'.format(str(i))])
            except: TFT = None
            if TFT:
                for l in LANGUAGE_REPLACEMENTS: TFT = TFT.replace(l, LANGUAGE_REPLACEMENTS[l])
                for l in TFT.split(','):
                    try: translations.add(LANGUAGES_CODES[l.strip()])
                    except: pass
        if len(languages) > 0 or len(translations) > 0:
            subfields = []
            for l in languages:
                subfields.extend(['a', l])
            for l in translations:
                subfields.extend(['h', l])
            record.add_field(Field('041', ['1' if len(translations) > 0 else '0', ' '], subfields))

        # 050 - Library of Congress Call Number (R)
        # LOCC*     Library of Congress Classification as stored
        for i in range(1, 10):
            try: LOCC = clean(self.row['LOCC{}'.format(str(i))])
            except: LOCC = None
            if LOCC: record.add_field(Field('050', [' ', '4'], ['a', LOCC]))
            else: break

        # 072 - Subject Category Code (R)
        for c in ['BIC2SC', 'BISACC', 'THEMASC', 'UKSLCAFC', 'UKSLCANFC', 'UKSLCCC']:
            terms = set()
            for i in range(1, 6 if c.startswith('UKSLC') else 10):
                try: v = clean(self.row['{}{}'.format(c, str(i))])
                except: v = None
                if v: terms.add(v)
            for v in sorted(terms):
                record.add_field(Field('072', [' ', '7'], ['a', v, '2', SUBJECT_CATEGORY_SOURCE_CODES[c]]))

        # PRODCC    Product Class: Code
        try: PRODCC = clean(self.row['PRODCC'])
        except: PRODCC = None
        if PRODCC: record.add_field(Field('072', [' ' , ' '], ['a', PRODCC]))

        # 082 - Dewey Decimal Classification Number (R)
        # DEWS*     DDC Edition No
        # DEWEY*    DDC value
        for i in range(1, 10):
            try: DEWS = clean(re.sub(r'[^0-9]', '', self.row['DEWS{}'.format(str(i))]))
            except: DEWS = None
            try: DEWEY = clean(re.sub(r'[^0-9\.]', '', self.row['DEWEY{}'.format(str(i))]))
            except: DEWEY = None
            if DEWEY:
                subfields = ['a', DEWEY]
                if DEWS: subfields.extend(['2', DEWS])
                record.add_field(Field('082', ['0', '4'], subfields))
            else: break

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
        try: LA = clean(self.row['LA'])
        except: LA = None
        try: TL = clean(self.row['TL'])
        except:
            try: TL = clean(self.row['FTS'])
            except: TL = None
        if not TL: TL = '[TITLE NOT PROVIDED]'
        try: PVNO1 = clean(self.row['PVNO1'])
        except: PVNO1 = None
        try: PVNO2 = clean(self.row['PVNO2'])
        except: PVNO2 = None
        try: PT1 = clean(self.row['PT1'])
        except: PT1 = None
        try: PT2 = clean(self.row['PT2'])
        except: PT2 = None
        try: YS = clean(self.row['YS'])
        except: YS = None
        if LA: TL = clean(LA + ' ' + TL)
        try: ST = clean(self.row['ST'])
        except: ST = None
        if ST: TL += ' :'
        elif PVNO1 or PVNO2 or PT1 or PT2: TL += '.'
        elif YS: TL += ','
        elif resp: TL += ' /'
        else: TL += '.'
        subfields = ['a', TL]
        if ST:
            if PVNO1 or PVNO2 or PT1 or PT2: ST += '.'
            elif YS: ST += ','
            elif resp: ST += ' /'
            else: ST += '.'
            subfields.extend(['b', ST])
        if PVNO1:
            if PT1: PVNO1 += ','
            elif PVNO2 or PT2: PVNO1 += '.'
            elif YS: PVNO1 += ','
            elif resp: PVNO1 += ' /'
            else: PVNO1 += '.'
            subfields.extend(['n', PVNO1])
        if PT1:
            if PVNO2 or PT2: PT1 += '.'
            elif YS: PT1 += ','
            elif resp: PT1 += ' /'
            else: PT1 += '.'
            subfields.extend(['p', PT1])
        if PVNO2:
            if PT2: PVNO2 += '.'
            elif YS: PVNO2 += ','
            elif resp: PVNO2 += ' /'
            else: PVNO2 += '.'
            subfields.extend(['n', PVNO2])
        if PT2:
            if YS: PT2 += ','
            elif resp: PT2 += ' /'
            else: PT2 += '.'
            subfields.extend(['p', PT2])
        if YS:
            if resp: YS += ' /'
            else: YS += '.'
            subfields.extend(['f', YS])
        if resp: subfields.extend(['c', resp])
        indicators = ['1' if resp else '0', str(len(LA) + 1) if LA else '0']
        record.add_field(Field('245', indicators, subfields))

        # 250 - Edition Statement (R)
        try: EDSL = clean(self.row['EDSL'])
        except:
            try: EDSL = clean(self.row['EDSS'])
            except: EDSL = None
        if not EDSL:
            try: EDSL = re.sub(r'[^0-9]', '', self.row['EDN'])
            except: EDSL = None
            if EDSL: EDSL = str(ordinal(int(EDSL))) + ' edition'
        if EDSL:
            EDSL = clean_edition(EDSL)
            record.add_field(Field('250', [' ', ' '], ['a', '{}.'.format(EDSL)]))

        # 255 - Cartographic Mathematical Data (R)
        # MS*   Map scale as stored
        for i in range(1, 2):
            try: MS = clean(self.row['MS{}'.format(str(i))])
            except: MS = None
            if MS and ':' in MS:
                MS = MS.split(':', 1)
                MS = '{}:{}'.format(re.sub(r'[^0-9]', '', MS[0]), re.sub(r'[^0-9,]]', '', re.sub(r'\s+', ',', MS[1].strip())))
                record.add_field(Field('255', [' ', ' '], ['a', 'Scale {}.'.format(MS)]))

        # 263 - Projected Publication Date (NR)
        try: PUBST = clean(self.row['PUBST'])
        except: PUBST = None
        if PUBST == 'Forthcoming':
            try: PUBPD = re.sub(r'[^0-9]', '', clean(self.row['PUBPD']))
            except:
                try: PUBPD = re.sub(r'[^0-9]', '', clean(self.row['UKLPUBD']))
                except:
                    try: PUBPD = re.sub(r'[^0-9]', '', clean(self.row['UKNBDLPD']))
                    except: PUBPD = None
            if PUBPD and len(PUBPD) >= 4:
                record.add_field(Field('263', [' ', ' '], ['a', (PUBPD + '------')[:6]]))


        # 264 - Production, Publication, Distribution, Manufacture, and Copyright Notice (R)
        # POP       Place of publication
        # COP       Country of publication
        # IMPN      Imprint Name
        # PUBPD     Date of Publication: as supplied by Publisher or approved source
        try: POP = clean(self.row['POP'])
        except: POP = None
        try: COP = clean(self.row['COP'])
        except: COP = None
        try: IMPN = clean(self.row['IMPN'])
        except:
            try: IMPN = clean(self.row['PUBN'])
            except: IMPN = None
        if 'PUBPD' in self.row: PUBPD = format_date(clean(self.row['PUBPD']))
        elif 'UKLPUBD' in self.row: PUBPD = format_date(clean(self.row['UKLPUBD']))
        elif 'UKNBDLPD' in self.row: PUBPD = format_date(clean(self.row['UKNBDLPD']))
        else: PUBPD = None
        if POP and COP and COP not in ['United States', 'United Kingdom'] and COP != POP:
            POP = '{}, {}'.format(POP, COP)
        if not POP: POP = '[Place of publication not identified]'
        if not IMPN: IMPN = '[publisher not identified]'
        subfields = []
        if POP:
            if IMPN: POP += ' :'
            elif PUBPD: POP += ','
            else: POP += '.'
            subfields.extend(['a', POP])
        if IMPN:
            if PUBPD: IMPN += ','
            else: IMPN += '.'
            subfields.extend(['b', IMPN])
        if PUBPD:
            PUBPD += '.'
            subfields.extend(['c', PUBPD])
        if subfields:
            record.add_field(Field('264', [' ', '1'], subfields))

        # xxxtDN*       The Org name of the 'distributor'
        for c in DISTRIBUTION_AREAS:
            d = set()
            subfields = ['a', '[{}] :'.format(DISTRIBUTION_AREAS[c][0])]
            for i in range (1, 10):
                for distributor_type in ['A', 'P', 'R', 'D', 'W', 'U']:
                    try: DN = clean(self.row['{}{}DN{}'.format(c, distributor_type, str(i))])
                    except: DN = None
                    if DN: d.add(DN)
            if d:
                d = '[distributor] ' + ' :|[distributor] '.join(d) + '.'
                for DN in d.split('|'):
                    subfields.extend(['b', DN])
                record.add_field(Field('264', ['3', '2'], subfields))

        # CY        Copyright Year
        try: CY = format_date(clean(self.row['CY']))
        except: CY = None
        if CY: record.add_field(Field('264', [' ', '4'], ['c', '\u00A9{}.'.format(CY)]))

        # 300 - Physical Description (R)
        # NOI   Number of Items
        # PAG   Pagination, as supplied
        # ILL   Illustrations and other contents note
        # HMM   Height along spine in mm
        # RUN   Running Time
        try: NOI = clean(self.row['NOI'].lower())
        except:
            try: NOI = clean(self.row['NOP'])
            except: NOI = None
        if NOI and (NOI == '1' or NOI.startswith('1 ')): NOI = None
        try: PAG = re.sub(r'[\spP]*$', '', clean(self.row['PAG']))
        except:
            try: PAG = re.sub(r'[\spP]*$', '', clean(self.row['PAGNUM']))
            except: PAG = None
        try: RUN = clean(re.sub(r'[^0-9]', '', self.row['RUN']))
        except: RUN = None
        ILL = clean_description(self.values['ILL'])
        try: HMM = re.sub(r'[^0-9]', '', self.row['HMM'])
        except: HMM = None
        subfields = []
        if PAG:
            PAG += ' pages'
            if NOI: PAG = '{} ({})'.format(NOI, PAG)
            if ILL:  PAG += ' :'
            elif HMM: PAG += ' ;'
            elif clean(self.row['SN']): PAG += '.'
            subfields.extend(['a', PAG])
        elif RUN:
            RUN = int(RUN)
            if RUN % 60 == 0: RUN = '{h:d} hours'.format(h=RUN // 60)
            else: RUN = '{h:d} hours {m:02d} minutes'.format(h=RUN // 60, m=RUN % 60)
            if NOI: RUN = '{} ({})'.format(NOI, RUN)
            subfields.extend(['a', RUN])
        if ILL:
            if HMM: ILL += ' ;'
            elif clean(self.row['SN']): ILL += '.'
            subfields.extend(['b', ILL])
        if HMM:
            HMM += ' mm'
            if clean(self.row['SN']): HMM += '.'
            subfields.extend(['c', HMM])
        if subfields: record.add_field(Field('300', [' ', ' '], subfields))

        # 306 - Playing Time (NR)
        # RUN   Running Time
        try: RUN = clean(re.sub(r'[^0-9]', '', self.row['RUN']))
        except: RUN = None
        if RUN:
            RUN = int(RUN)
            record.add_field(Field('306', [' ', ' '], ['a', '{h:02d}{m:02d}00'.format(h=RUN // 60, m=RUN % 60)]))

        # 336 - Content Type (R)
        content_types = set()
        try: content_types.add(ONIX_PRODUCT_FORM[self.values['PFC']][1])
        except: pass
        for i in range(1, 10):
            try: content_types.add(ONIX_PRODUCT_CONTENT_TYPE[clean(self.row['PCTC{}'.format(str(i))])].rda_text)
            except: pass
        for v in content_types:
            record.add_field(Field('336', [' ', ' '], ['a', v, '2', 'rdacontent']))

        # 337 - Media Type (R)
        # A categorization reflecting the general type of intermediation device required
        # to view, play, run, etc., the content of a manifestation.
        try: v = ONIX_PRODUCT_FORM[self.values['PFC']][2]
        except: v = 'unspecified'
        record.add_field(Field('337', [' ', ' '], ['a', v, '2', 'rdamedia']))

        # 338 - Carrier Type (R)
        try: v = ONIX_PRODUCT_FORM[self.values['PFC']][3]
        except: v = 'unspecified'
        record.add_field(Field('338', [' ', ' '], ['a', v, '2', 'rdacarrier']))

        # 365 - Trade Price (R)
        for c in DISTRIBUTION_AREAS:
            if c != 'IRL':
                cur = DISTRIBUTION_AREAS[c][1]
                # xxxCCPTC      Price Type – Code
                # xxxCCPRRRP    The Current Price Of The Record (inc Taxes)
                # xxxCCPRPN     Any supplementary notes regarding tax information
                # xxxCCPRTOP    The actual tax amount (may be zero)
                # xxxCCPRA      The area as stored on the Nielsen system

                try: CCPTC = clean(self.row['{}CCPTC'.format(cur)])
                except: CCPTC = '02'
                try: CCPRRRP = clean(self.row['{}CCPRRRP'.format(cur)])
                except: CCPRRRP = None
                try: CCPRPN = clean(self.row['{}CCPRPN'.format(cur)])
                except: CCPRPN = None
                try: CCPRA = clean(self.row['{}CCPRA'.format(cur)])
                except: CCPRA = None

                if CCPRRRP:
                    self.UK = True
                    subfields = ['a', CCPTC or '02', 'b', CCPRRRP, 'c', cur, 'd', '00']
                    if CCPRPN: subfields.extend(['e', CCPRPN])
                    try: CCPRTOP = clean(self.row['{}CCPRPTOP'.format(cur)])
                    except: CCPRTOP = None
                    if CCPRTOP:
                        subfields.extend(['h', '{} tax'.format(CCPRTOP)])
                    if CCPRA: subfields.extend(['j', CCPRA])
                    # xxxtDN*       The Org name of the 'distributor'
                    i = 1
                    DN = None
                    while not DN and i in range(1, 10):
                        for distributor_type in ['A', 'P', 'R', 'D', 'W', 'U']:
                            try: DN = clean(self.row['{}{}DN{}'.format(c, distributor_type, str(i))])
                            except: pass
                            if DN: break
                        i += 1
                    if DN: subfields.extend(['m', DN])
                    subfields.extend(['2', 'onixpt'])
                    record.add_field(Field('365', [' ', ' '], subfields))

        # 366 - Trade Availability Information (R)
        for c in DISTRIBUTION_AREAS:
            if c != 'IRL':
                # xxxNBDEAD     Availability Date
                # xxxNBDPAC     ONIX Product Availability – Code
                try: NBDEAD = clean(re.sub(r'[^0-9]', '', self.row['{}NBDEAD'.format(c)]))
                except: NBDEAD = None
                try: NBDPAC = clean(self.row['{}NBDPAC'.format(c)])
                except: NBDPAC = None
                if NBDEAD:
                    self.UK = True
                    subfields = ['b', NBDEAD]
                    if NBDPAC: subfields.extend(['c', NBDPAC])
                    subfields.extend(['j', c])
                    if c != 'EUR': subfields.extend(['k', DISTRIBUTION_AREAS[c][2]])
                    if NBDPAC: subfields.extend(['2', 'onixas'])
                    record.add_field(Field('366', [' ', ' '], subfields))

        # EMBD      Embargo Date
        # PUBSC     ONIX Publishing Status - Code
        # PUBST     ONIX Publishing Status – Text Description
        # MOPD      Date the system was informed that the record is no longer available
        try: EMBD = clean(re.sub(r'[^0-9]', '', self.row['EMBD']))
        except: EMBD = None
        try: PUBSC = clean(self.row['PUBSC'])
        except: PUBSC = None
        try: PUBST = clean(self.row['PUBST'])
        except: PUBST = None
        try: MOPD = clean(self.row['MOPD'])
        except: MOPD = None
        subfields = []
        if PUBSC:
            if MOPD: PUBSC += ' ' + MOPD
            subfields.extend(['c', PUBSC])
        if EMBD: subfields.extend(['d', EMBD])
        if PUBST: subfields.extend(['e', PUBST])
        if PUBSC: subfields.extend(['2', 'onixas'])
        if subfields: record.add_field(Field('366', [' ', ' '], subfields))

        # 490 - Series Statement (R)
        # SN    Series Title
        # NWS   Series Part/volume number
        # ISSN  Series ISSN
        try: SN = clean(self.row['SN'])
        except: SN = None
        try: NWS = clean(self.row['NWS'])
        except: NWS = None
        try: ISSN = clean(self.row['ISSN'])
        except: ISSN = None
        if SN:
            if ISSN:
                SN += ','
                if NWS: NWS += ' ;'
            elif NWS:
                SN += ' ;'
            subfields = ['a', SN]
            if ISSN: subfields.extend(['x', ISSN])
            if NWS: subfields.extend(['v', NWS])
            record.add_field(Field('490', ['0', ' '], subfields))

        # 500 - General Note (R)
        PREAMBLES = {
            'IMPID':    'Nielsen imprint code, correct as of {}: '.format(datetime.date.today()),
            'PUBID':    'Nielsen publisher code, correct as of {}: '.format(datetime.date.today()),
            'PFCT':     '',
            'PPTCT':    'Packaging: ',
            'CBMCCODE': 'BIC children’s book marketing category: ',
        }
        # IMPID     Nielsen Code for Imprint
        # PUBID     Nielsen Code for Publisher
        # PFCT      Product Form: Text Description
        # PPTCT     Product Packaging Type: Text Description
        # CBMCCODE  BIC Children’s Book Marketing Category: Code
        for c in PREAMBLES:
            if self.values[c]:
                record.add_field(Field('500', [' ', ' '], ['a', '{}{}.'.format(PREAMBLES[c], self.values[c])]))
                if c in ['IMPID', 'PUBID']:
                    record.add_field(Field('N{}I'.format(c[0]), [' ', ' '], ['a', self.values[c]], ['d', datetime.date.today()]))

        # PFDT*     Product Form Detail: Text Description
        # PFFSD*    Product Form Feature Safety Type: Text Description
        for c in ['PFDT', 'PFFSD']:
            for i in range(1, 10):
                try: v = clean(self.row['{}{}'.format(c, str(i))])
                except: v = None
                if v: record.add_field(Field('500', [' ', ' '], ['a', '{}.'.format(v)]))
                else: break

        # PWU*      Product Website URL
        # PWTT*     Product Website Type: Text Description
        for i in range(1, 10):
            try: PWU = self.row['PWU{}'.format(str(i))].strip()
            except: PWU = None
            if PWU == '': PWU = None
            try: PWTT = clean(self.row['PWTT{}'.format(str(i))])
            except: PWTT = None
            if not PWTT or 'unspecified' in PWTT.lower(): PWTT = 'Related website'
            if PWU: record.add_field(Field('500', [' ', ' '], ['a', '{}: {}.'.format(PWTT, PWU)]))
            else: break

        # 521 - Target Audience Note (R)
        # OAT*  ONIX Audience level: Text Description
        for i in range(1, 10):
            try: OAT = clean(self.row['OAT{}'.format(str(i))])
            except: OAT = None
            if OAT: record.add_field(Field('521', [' ', ' '], ['a', '{}.'.format(OAT)]))
            else: break

        # USGCT     ONIX US grade: Text Description
        # IA    Interest Age
        # RA    Reading Age
        for c in ['USGCT', 'IA', 'RA']:
            if self.values[c]: record.add_field(Field('521', ['0' if c == 'USGCT' else '1' if c == 'IA' else '2', ' '],
                                         ['a', '{}.'.format(self.values[c])]))

        # CBMCCODE  BIC Children’s Book Marketing Category: Code
        try: CBMCCODE = BIC_CBMC_CODES[self.values['CBMCCODE'][0]]
        except: CBMCCODE = None
        if CBMCCODE: record.add_field(Field('521', ['1', ' '], ['a', '{}.'.format(CBMCCODE)]))

        # 501 - With Note (R)
        # CIS   A statement of the contained items
        if self.values['CIS']: record.add_field(Field('501', [' ', ' '], ['a', self.values['CIS'] + '.']))

        for i in range(1, 10):
            # CIID*     Contained Item Identifier
            # CIPFCT*   Contained Item: Product Form Text Description
            # CINOP*    Contained item number of identical pieces
            try: CIID = clean(self.row['CIID{}'.format(str(i))])
            except: CIID = None
            try: CIPFCT = clean(self.row['CIPFCT{}'.format(str(i))])
            except: CIPFCT = None
            try: CINOP = clean(self.row['CINOP{}'.format(str(i))])
            except: CINOP = None
            if CIID:
                CIID = 'Contains {} of {}{}.'.format('a copy' if CINOP == '1' else '{} copies'.format(CINOP),
                                                    CIID, ' ({})'.format(CIPFCT) if CIPFCT else '')
                record.add_field(Field('501', [' ', ' '], ['a', CIID]))
            if not CIID: break

        # 505 - Formatted Contents Note (R)
        # 520 - Summary, Etc. (R)
        # 545 - Biographical or Historical Data (R)
        for c in ['TOC', 'LD', 'REV', 'P', 'BIOG']:
            try: v = clean(self.row['NBDF{}'.format(c)]) or clean(self.row['NBD{}'.format(c)])
            except: v = None
            if c == 'LD' and not v:
                try: v = clean(self.row['NBDFSD'])
                except:
                    try: v = clean(self.row['NBDSD'])
                    except: v = None
            if v: v = clean_html(v)
            if v:
                i = 0
                for part in split_long(v, isbn=str(self.values['ISBN13'])):
                    record.add_field(Field('505' if c == 'TOC' else '545' if c == 'BIOG' else '520',
                                           ['8' if i == 0 and c == 'TOC' else '0' if c in ['BIOG', 'TOC'] else '1' if c in ['REV', 'P'] else ' ', ' '],
                                           ['a', part + '.']))
                    i += 1

        # 506 - Restrictions on Access Note (R)
        # RSS    Restricted Sales statement
        if self.values['RSS']: record.add_field(Field('506', [' ', ' '], ['a', '{}.'.format(self.values['RSS'])]))

        # 538 - System Details Note (R)
        # 563 - Binding Information (R)
        for i in range(1, 10):
            # PFFT*     Product Form Feature Type: Code (ONIX code list 79)
            # PFFTT*    Product Form Feature Type: Text Description
            # PFFVT*    Product Form Feature Value: Text
            # PFFD*     Product Form Feature Description
            try: PFFT = clean(self.row['PFFT{}'.format(str(i))])
            except: PFFT = None
            try: PFFTT = clean(self.row['PFFTT{}'.format(str(i))])
            except: PFFTT = None
            try: PFFVT = clean(self.row['PFFVT{}'.format(str(i))])
            except: PFFVT = None
            try: PFFD = clean(self.row['PFFD{}'.format(str(i))])
            except: PFFD = None
            if PFFT and PFFTT:
                if PFFVT: PFFTT = PFFVT.replace(' - ', ': ')
                if PFFD: PFFTT = '{} ({})'.format(PFFTT, PFFD)
                PFFTT = clean(PFFTT) + '.'
                record.add_field(Field(
                    '563' if PFFT in ['01', '02', '04'] else '538' if PFFT in ['05', '06', '07'] else '500',
                    [' ', ' '],
                    ['a', PFFTT]))
            if not PFFT: break

        # 546 - Language Note (R)
        # LS    Language statement
        # TS    Translation statement
        languages = set()
        for i in range(1, 10):
            try: l = clean(self.row['LT{}'.format(str(i))])
            except: l = None
            if l: languages.add(l)
        LS = ', '.join(languages)
        try: TS = clean(self.row['TS'])
        except: TS = None
        if LS or TS:
            for l in LANGUAGE_REPLACEMENTS:
                if LS: LS = LS.replace(l, LANGUAGE_REPLACEMENTS[l])
                if TS: TS = TS.replace(l, LANGUAGE_REPLACEMENTS[l])
            text = 'In {}{}'.format(rreplace(LS, ', ', ' and '), '; ' if TS else '.') if LS else ''
            if TS: text += '{}ranslated from {}.'.format('t' if LS else 'T', rreplace(TS, ', ', ' and '))
            record.add_field(Field('546', [' ', ' '], ['a', text]))

        # 586 - Awards Note (R)
        # PSF   Structured Prize details for all Prizes combined
        if self.values['PSF']: record.add_field(Field('586', [' ', ' '], ['a', '{}.'.format(self.values['PSF'])]))

        # 588 - Source of Description Note (R)
        record.add_field(Field('588', [' ', ' '], ['a', 'Description based on CIP data; item not viewed.']))

        # 650 - Subject Added Entry-Topical Term (R)
        # BIC2QT*   BIC Qualifier, version 2.1: Text Description
        bic_qualifiers = []
        for i in range(1, 10):
            try: BIC2QC = clean(self.row['BIC2QC{}'.format(str(i))])
            except: BIC2QC = None
            try: BIC2QT = clean(self.row['BIC2QT{}'.format(str(i))])
            except: BIC2QT = None
            if BIC2QT and BIC2QC:
                bic_qualifiers.extend(['z' if BIC2QC[0] == '1' else 'y' if BIC2QC[0] == '3' else 'x', BIC2QT])
            else: break

        # THEMAQT*  Thema Qualifier: Text
        thema_qualifiers = []
        for i in range(1, 10):
            try: THEMAQC = clean(self.row['THEMAQC{}'.format(str(i))])
            except: THEMAQC = None
            try: THEMAQT = clean(self.row['THEMAQT{}'.format(str(i))])
            except: THEMAQT = None
            if THEMAQC and THEMAQT:
                thema_qualifiers.extend(['z' if THEMAQC[0] == '1' else 'y' if THEMAQC[0] == '3' else 'x', THEMAQT])
            else: break

        # BIC2ST*       BIC Subject, version 2.1: Text Description
        # BISACT*       BISAC: Text Description
        # THEMAST*      Thema Subject: Text
        # UKSLCAFT*     UKSLC Adult Fiction: Text
        # UKSLCANFT*    UKSLC Adult Non Fiction: Text
        # UKSLCCT*      UKSLC Children: Text
        # LOCSH*        Library of Congress Subject Headings as stored
        # NASI*         Name as Subject, name inverted
        for c in ['BIC2ST', 'BISACT', 'THEMAST', 'UKSLCAFT', 'UKSLCANFT', 'UKSLCCT', 'LOCSH', 'NASI']:
            delim = ' / ' if c == 'BISACT' else ' - ' if c == 'LOCSH' else None
            terms = set()
            for i in range(1, 6 if c.startswith('UKSLC') else 10):
                try: v = clean(self.row['{}{}'.format(c, str(i))])
                except: v = None
                if v: terms.add(v)
                else: break
            for v in sorted(terms):
                if delim: subfields = ['a', v.split(delim)[0]]
                else: subfields = ['a', v]
                if c == 'BIC2ST': subfields.extend(bic_qualifiers)
                elif c == 'THEMAST': subfields.extend(thema_qualifiers)
                elif delim:
                    for s in v.split(delim)[1:]:
                        subfields.extend(['x', s])
                if c not in ['LOCSH', 'NASI']: subfields.extend(['2', SUBJECT_CATEGORY_SOURCE_CODES[c]])
                record.add_field(Field('600' if c == 'NASI' else '650',
                                       ['1' if c == 'NASI' else ' ', '0' if c == 'LOCSH' else '4' if c == 'NASI' else '7'],
                                       subfields))

        # PRODCT        Product Class: Text Description
        if self.values['PRODCT']:
            subfields = ['a', self.values['PRODCT'].split(': ')[0]]
            for s in self.values['PRODCT'].split(': ')[1:]:
                subfields.extend(['x', s])
            record.add_field(Field('650', [' ', '4'], subfields))

        # 653 - Index Term-Uncontrolled (R)
        # KEYWORDS      Key Words
        if self.values['KEYWORDS']:
            KEYWORDS = set(k.strip() for k in self.values['KEYWORDS'].split(';') if k)
            for k in sorted(KEYWORDS):
                record.add_field(Field('653', [' ', ' '], ['a', k]))

        # 655 - Index Term-Genre/Form (R)
        # FICGH     British Library Fiction Genre Heading
        if self.values['FICGH']: record.add_field(Field('655', [' ', '4'], self.values['FICGH'] + '.'))

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
        # RWI*      Related Work ID
        # RWITN*    Related Work ID Name
        # RWTT*     Related Work Type Text
        for i in range(1, 10):
            try: RWI = clean(self.row['RWI{}'.format(str(i))])
            except: RWI = None
            try: RWITN = clean(self.row['RWITN{}'.format(str(i))])
            except: RWITN = None
            try: RWTT = clean(self.row['RWTT{}'.format(str(i))])
            except: RWTT = None
            if RWI:
                subfields = []
                if RWTT: subfields.extend(['i', RWTT])
                subfields.extend(['z' if RWITN and 'ISBN' in RWITN else 'o', RWI])
                record.add_field(Field('787', ['1', ' '], subfields))
            else: break

        record.add_field(Field('SRC', [' ', ' '], ['a', 'Record converted from Nielsen TSV data to MARC21 by Collection Metadata.']))

        return record


# ====================
#      Main code
# ====================


def main(argv=None):
    if argv is None:
        name = str(sys.argv[1])

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    input_path = os.path.join(dir, 'Input', 'Products')
    output_path = os.path.join(dir, 'Output', 'Products')
    database = False

    print('========================================')
    print('nielsen2marc_products')
    print('========================================')
    print('\nThis program converts Nielsen TSV files\n'
          'for PRODUCTS to MARC 21 (Bibliographic)\n')

    try: opts, args = getopt.getopt(argv, 'i:o:', ['input_path=', 'output_path=', 'help', 'database'])
    except getopt.GetoptError as err:
        exit_prompt('Error: {}'.format(err))
    for opt, arg in opts:
        if opt == '--help': usage(conversion_type='Products')
        elif opt == '--database': database = True
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
    if not os.path.exists(os.path.join(output_path, 'UK')):
        os.makedirs(os.path.join(output_path, 'UK'))

    if database:
        if not os.path.isfile(DATABASE_PATH):
            exit_prompt('Error: The file {} cannot be found'.format(DATABASE_PATH))
        db = IsbnDatabase()

    skip_check = True

    # --------------------
    # Iterate through input files
    # --------------------

    for root, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(('.add', '.upd', '.del')):

                # Graph for ISBN information
                G = Graph(skip_check=skip_check)

                status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
                ids = set()
                date_time_message('Processing file {}'.format(str(file)))

                # Open input and output files
                ifile = open(os.path.join(root, file), mode='r', encoding='utf-8', errors='replace', newline='')
                ofile = open(os.path.join(output_path, file + '.lex'), 'wb')
                ofileUK = open(os.path.join(output_path, 'UK', file + '_UK.lex'), 'wb')
                tfile = open(os.path.join(output_path, file + '.txt'), mode='w', encoding='utf-8', errors='replace')
                dfile = open(os.path.join(output_path, file + '_duplicates.txt'), mode='w', encoding='utf-8', errors='replace')
                writer = MARCWriter(ofile)
                writerUK = MARCWriter(ofileUK)
                i = 0
                c = csv.DictReader(ifile, delimiter='\t')
                for row in c:
                    i += 1
                    if i % 100 == 0:
                        print('{} records processed'.format(str(i)), end='\r')
                    nielsen = NielsenTSVProducts(row, status)
                    marc = nielsen.marc()
                    record_id = nielsen.record_id()
                    writer.write(marc)
                    tfile.write(str(marc) + '\n')
                    if nielsen.is_uk():
                        writerUK.write(marc)
                    if record_id:
                        if record_id in ids:
                            dfile.write(record_id + '\n')
                        else: ids.add(record_id)

                    # Get ISBN information
                    if database:
                        nielsen = NielsenCluster(row)
                        isbns = nielsen.get_alternative_formats()
                        if isbns:
                            data = [(i.isbn, i.format) for i in isbns if i.isbn]
                            G.add_nodes(data)
                            data = [(i.isbn, j.isbn) for i in isbns for j in isbns if
                                    i.isbn and j.isbn and i.isbn != j.isbn and i.format != 'C' and j.format != 'C']
                            G.add_edges(data)
                print('{} records processed'.format(str(i)), end='\r')

                # Close files
                for f in (ifile, ofile, ofileUK, tfile, dfile):
                    f.close()

                if database:
                    G.check_graph()
                    db.add_graph_to_database(G, skip_check=skip_check)

    date_time_exit()


if __name__ == '__main__':
    main(sys.argv[1:])
