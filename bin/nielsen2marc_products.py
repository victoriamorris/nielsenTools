#!/usr/bin/env python
# -*- coding: utf8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
import csv
from nielsenTools.functions import *
from nielsenTools.nielsen_tools import *

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


AUDIENCE_CODES = {
    'G':    'g',  # General
    'J':	'j',  # Children / Juvenile
    'JN':	'a',  # Preschool (0-5)
    'JC':	'b',  # Children's (6-12)
    'Y':	'd',  # Teenage / Young adult
    'E':	'f',  # Educational: Primary & Secondary
    'EJ':	'f',  # Primary
    'ES':	'f',  # Secondary
    'U':	'f',  # Tertiary & Higher Education
    'UA':	'f',  # A / AS level
    'UF':	'f',  # Further / Higher Education
    'UU':	'f',  # Undergraduate
    'UP':	'f',  # Postgraduate, Research & Scholarly
    'P':	'f',  # Professional & Vocational
    'L':	'f',  # ELT General
    'LB':	'f',  # ELT Beginner
    'LI':	'f',  # ELT Intermediate
    'LA':	'f',  # ELT Advanced
    'LS':	'f',  # English as a second language
    'XV':	'f',  # Technical / Manuals
    'XT':	'f',  # Teacher Text
    'XS':	'f',  # Student Text
    'XR':	'f',  # Revision / Study Guides
    'XX':	'f',  # Exams / Tests / Exercises
    'XO':	'f',  # Open University set text
}


COUNTRY_CODES = {
    'Albania':  'aa ',
    'Australia':	'at ',
    'Austria':	'au ',
    'Belgium':	'be ',
    'Canada':	'xxc',
    'China':	'cc ',
    'Croatia':	'ci ',
    'Czech Republic':	'xr ',
    'Denmark':	'dk ',
    'Egypt':	'ua ',
    'Finland':	'fi ',
    'France':	'fr ',
    'Germany':	'gw ',
    'Greece':	'gr ',
    'Hong Kong':	'cc ',
    'Hungary':	'hu ',
    'India':	'ii ',
    'Ireland':	'ie ',
    'Israel':	'is ',
    'Italy':	'it ',
    'Jamaica':	'jm ',
    'Japan':	'ja ',
    'Jersey':	'je ',
    'Jordan':	'jo ',
    'Kenya':	'ke ',
    'Korea, Republic of':	'ko ',      # South Korea
    'Lebanon':	'le ',
    'Luxembourg':	'lu ',
    'Malaysia':	'my ',
    'Malta':	'mm ',
    'Mexico':	'mx ',
    'Netherlands':	'ne ',
    'New Zealand':	'nz ',
    'Nigeria':  'nr ',
    'Norway':	'no ',
    'Pakistan':	'pk ',
    'Philippines':	'ph ',
    'Poland':	'pl ',
    'Portugal':	'po ',
    'Qatar':	'qa ',
    'Romania':	'rm ',
    'Russian Federation':	'ru ',
    'Serbia and Montenegro':	'rb ',  # Code for Serbia; Montenegro = mo
    'Singapore':	'si ',
    'Slovenia':	'xv ',
    'South Africa':	'sa ',
    'Spain':	'sp ',
    'Sweden':	'sw ',
    'Switzerland':	'sz ',
    'Thailand':	'th ',
    'Tonga':	'to ',
    'Turkey':	'tu ',
    'Uganda':	'ug ',
    'United Arab Emirates':	'ts ',
    'United Kingdom':	'xxk',
    'United States':	'xxu',
    'Virgin Islands, British':	'vb ',
}


DISTRIBUTION_AREAS = {
    'UK': ['United Kingdom', 'GBP', 'xxk'],
    # 'US': ['United States', 'USD', 'xxu'],
    # 'AUS': ['Australia', 'AUD', 'at'],
    # 'NZ': ['New Zealand', 'NZD', 'nz'],
    # 'SA': ['South Africa', 'ZAR', 'sa'],
    # 'EUR': ['Europe', 'EUR'],
    # 'IN': ['India', 'INR', 'ii'],
    # 'CAN': ['Canada', 'CAD', 'xxc'],
    'IRL':  ['Ireland', 'EUR', 'ie']
}


LANGUAGES_CODES = {
    'Abkhaz':	'abk',
    'Achinese':	'ace',
    'Acoli':	'ach',
    'Adangme':	'ada',
    'Adygei':	'ady',
    'Afar':	'aar',
    'Afrihili (Artificial language)':	'afh',
    'Afrikaans':	'afr',
    'Afroasiatic':	'afa',
    'Ainu':	'ain',
    'Akan':	'aka',
    'Akkadian':	'akk',
    'Albanian':	'alb',
    'Aleut':	'ale',
    'Algonquian':	'alg',
    'Altai':	'alt',
    'Altaic':	'tut',
    'Amharic':	'amh',
    'Ancient Greek':	'grc',
    'Angika':	'anp',
    'Apache languages':	'apa',
    'Arabic':	'ara',
    'Aragonese':	'arg',
    'Aramaic':	'arc',
    'Arapaho':	'arp',
    'Arawak':	'arw',
    'Armenian':	'arm',
    'Aromanian':	'rup',
    'Artificial':	'art',
    'Assamese':	'asm',
    'Athapascan':	'ath',
    'Australian languages':	'aus',
    'Austronesian':	'map',
    'Avaric':	'ava',
    'Avestan':	'ave',
    'Awadhi':	'awa',
    'Aymara':	'aym',
    'Azerbaijani':	'aze',
    'Bable':	'ast',
    'Balinese':	'ban',
    'Baltic':	'bat',
    'Baluchi':	'bal',
    'Bambara':	'bam',
    'Bamileke languages':	'bai',
    'Banda languages':	'bad',
    'Bantu':	'bnt',
    'Basa':	'bas',
    'Bashkir':	'bak',
    'Basque':	'baq',
    'Batak':	'btk',
    'Beja':	'bej',
    'Belarusian':	'bel',
    'Bemba':	'bem',
    'Bengali':	'ben',
    'Berber':	'ber',
    'Bhojpuri':	'bho',
    'Bihari':	'bih',
    'Bikol':	'bik',
    'Bilin':	'byn',
    'Bislama':	'bis',
    'Blissymbolics':	'zbl',
    'Bosnian':	'bos',
    'Braj':	'bra',
    'Breton':	'bre',
    'Bugis':	'bug',
    'Bulgarian':	'bul',
    'Buriat':	'bua',
    'Burmese':	'bur',
    'Caddo':	'cad',
    'Carib':	'car',
    'Catalan':	'cat',
    'Caucasian':	'cau',
    'Cebuano':	'ceb',
    'Celtic':	'cel',
    'Central American Indian':	'cai',
    'Chagatai':	'chg',
    'Chamic languages':	'cmc',
    'Chamorro':	'cha',
    'Chechen':	'che',
    'Cherokee':	'chr',
    'Cheyenne':	'chy',
    'Chibcha':	'chb',
    'Chinese':	'chi',
    'Chinook jargon':	'chn',
    'Chipewyan':	'chp',
    'Choctaw':	'cho',
    'Church Slavic':	'chu',
    'Chuukese':	'chk',
    'Chuvash':	'chv',
    'Coptic':	'cop',
    'Cornish':	'cor',
    'Corsican':	'cos',
    'Cree':	'cre',
    'Creek':	'mus',
    'Creoles and Pidgins':	'crp',
    'Crimean Tatar':	'crh',
    'Croatian':	'hrv',
    'Cushitic':	'cus',
    'Czech':	'cze',
    'Dakota':	'dak',
    'Danish':	'dan',
    'Dargwa':	'dar',
    'Dayak':	'day',
    'Delaware':	'del',
    'Dinka':	'din',
    'Divehi':	'div',
    'Dogri':	'doi',
    'Dogrib':	'dgr',
    'Dravidian':	'dra',
    'Duala':	'dua',
    'Dutch':	'dut',
    'Dyula':	'dyu',
    'Dzongkha':	'dzo',
    'East Frisian':	'frs',
    'Edo':	'bin',
    'Efik':	'efi',
    'Egyptian':	'egy',
    'Ekajuk':	'eka',
    'Elamite':	'elx',
    'English Creole':	'cpe',
    'English':	'eng',
    'Erzya':	'myv',
    'Esperanto':	'epo',
    'Estonian':	'est',
    'Ethiopic':	'gez',
    'Ewe':	'ewe',
    'Ewondo':	'ewo',
    'Fang':	'fan',
    'Fanti':	'fat',
    'Faroese':	'fao',
    'Fijian':	'fij',
    'Filipino':	'fil',
    'Finnish':	'fin',
    'Finno-Ugrian':	'fiu',
    'Fon':	'fon',
    'French Creole':	'cpf',
    'French':	'fre',
    'Frisian':	'fry',
    'Friulian':	'fur',
    'Fula':	'ful',
    'Gã':	'gaa',
    'Galician':	'glg',
    'Ganda':	'lug',
    'Gayo':	'gay',
    'Gbaya':	'gba',
    'Georgian':	'geo',
    'German':	'ger',
    'Germanic':	'gem',
    'Gilbertese':	'gil',
    'Gondi':	'gon',
    'Gorontalo':	'gor',
    'Gothic':	'got',
    'Grebo':	'grb',
    'Greek':	'gre',
    'Guarani':	'grn',
    'Gujarati':	'guj',
    'Gwich\'in':	'gwi',
    'Haida':	'hai',
    'Haitian French Creole':	'hat',
    'Hausa':	'hau',
    'Hawaiian':	'haw',
    'Hebrew':	'heb',
    'Herero':	'her',
    'Hiligaynon':	'hil',
    'Hindi':	'hin',
    'Hiri Motu':	'hmo',
    'Hittite':	'hit',
    'Hmong':	'hmn',
    'Hungarian':	'hun',
    'Hupa':	'hup',
    'Iban':	'iba',
    'Icelandic':	'ice',
    'Ido':	'ido',
    'Igbo':	'ibo',
    'Ijo':	'ijo',
    'Iloko':	'ilo',
    'Inari Sami':	'smn',
    'Indic':	'inc',
    'Indo-European':	'ine',
    'Indonesian':	'ind',
    'Ingush':	'inh',
    'Interlingua (International Auxiliary Language Association)':	'ina',
    'Interlingue':	'ile',
    'Inuktitut':	'iku',
    'Inupiaq':	'ipk',
    'Iranian':	'ira',
    'Irish':	'gle',
    'Iroquoian':	'iro',
    'Italian':	'ita',
    'Japanese':	'jpn',
    'Javanese':	'jav',
    'Judeo-Arabic':	'jrb',
    'Judeo-Persian':	'jpr',
    'Kabardian':	'kbd',
    'Kabyle':	'kab',
    'Kachin':	'kac',
    'Kalâtdlisut':	'kal',
    'Kamba':	'kam',
    'Kannada':	'kan',
    'Kanuri':	'kau',
    'Karachay-Balkar':	'krc',
    'Kara-Kalpak':	'kaa',
    'Karelian':	'krl',
    'Karen languages':	'kar',
    'Kashmiri':	'kas',
    'Kashubian':	'csb',
    'Kawi':	'kaw',
    'Kazakh':	'kaz',
    'Khasi':	'kha',
    'Khmer':	'khm',
    'Khoisan':	'khi',
    'Khotanese':	'kho',
    'Kikuyu':	'kik',
    'Kimbundu':	'kmb',
    'Kinyarwanda':	'kin',
    'Klingon (Artificial language)':	'tlh',
    'Komi':	'kom',
    'Kongo':	'kon',
    'Konkani':	'kok',
    'Kootenai':	'kut',
    'Korean':	'kor',
    'Kosraean':	'kos',
    'Kpelle':	'kpe',
    'Kru':	'kro',
    'Kuanyama':	'kua',
    'Kumyk':	'kum',
    'Kurdish':	'kur',
    'Kurukh':	'kru',
    'Kyrgyz':	'kir',
    'Ladino':	'lad',
    'Lahndā':	'lah',
    'Lamba (Zambia and Congo)':	'lam',
    'Lao':	'lao',
    'Latin':	'lat',
    'Latvian':	'lav',
    'Lezgian':	'lez',
    'Limburgish':	'lim',
    'Lingala':	'lin',
    'Lithuanian':	'lit',
    'Lojban (Artificial language)':	'jbo',
    'Low German':	'nds',
    'Lower Sorbian':	'dsb',
    'Lozi':	'loz',
    'Luba-Katanga':	'lub',
    'Luba-Lulua':	'lua',
    'Luiseño':	'lui',
    'Lule Sami':	'smj',
    'Lunda':	'lun',
    'Luo (Kenya and Tanzania)':	'luo',
    'Lushai':	'lus',
    'Luxembourgish':	'ltz',
    'Maasai':	'mas',
    'Macedonian':	'mac',
    'Madurese':	'mad',
    'Magahi':	'mag',
    'Maithili':	'mai',
    'Makasar':	'mak',
    'Malagasy':	'mlg',
    'Malay':	'may',
    'Malayalam':	'mal',
    'Maltese':	'mlt',
    'Manchu':	'mnc',
    'Mandar':	'mdr',
    'Mandingo':	'man',
    'Manipuri':	'mni',
    'Manobo languages':	'mno',
    'Manx':	'glv',
    'Maori':	'mao',
    'Mapuche':	'arn',
    'Marathi':	'mar',
    'Mari':	'chm',
    'Marshallese':	'mah',
    'Marwari':	'mwr',
    'Mayan languages':	'myn',
    'Mende':	'men',
    'Micmac':	'mic',
    'Middle Dutch':	'dum',
    'Middle English':	'enm',
    'Middle French':	'frm',
    'Middle High German':	'gmh',
    'Middle Irish':	'mga',
    'Minangkabau':	'min',
    'Mirandese':	'mwl',
    'Modern Syriac':	'syr',
    'Mohawk':	'moh',
    'Moksha':	'mdf',
    'Mongolian':	'mon',
    'Mongo-Nkundu':	'lol',
    'Mon-Khmer':	'mkh',
    'Montenegrin':	'cnr',
    'Mooré':	'mos',
    'Multiple languages':	'mul',
    'Munda':	'mun',
    'Nahuatl':	'nah',
    'Nauru':	'nau',
    'Navajo':	'nav',
    'Ndebele (South Africa)':	'nbl',
    'Ndebele (Zimbabwe)':	'nde',
    'Ndonga':	'ndo',
    'Neapolitan Italian':	'nap',
    'Nepali':	'nep',
    'Newari':	'new',
    'Nias':	'nia',
    'Niger-Kordofanian':	'nic',
    'Nilo-Saharan':	'ssa',
    'Niuean':	'niu',
    'N\'Ko':	'nqo',
    'Nogai':	'nog',
    'North American Indian':	'nai',
    'North Frisian':	'frr',
    'Northern Sami':	'sme',
    'Northern Sotho':	'nso',
    'Norwegian (Bokmål)':	'nob',
    'Norwegian (Nynorsk)':	'nno',
    'Norwegian':	'nor',
    'Nubian languages':	'nub',
    'Nyamwezi':	'nym',
    'Nyanja':	'nya',
    'Nyankole':	'nyn',
    'Nyoro':	'nyo',
    'Nzima':	'nzi',
    'Occitan (post-1500)':	'oci',
    'Oirat':	'xal',
    'Ojibwa':	'oji',
    'Old English':	'ang',
    'Old French':	'fro',
    'Old High German':	'goh',
    'Old Irish':	'sga',
    'Old Newari':	'nwc',
    'Old Norse':	'non',
    'Old Persian (ca. 600-400 B.C.)':	'peo',
    'Oriya':	'ori',
    'Oromo':	'orm',
    'Osage':	'osa',
    'Ossetic':	'oss',
    'Otomian languages':	'oto',
    'Ottoman Turkish':	'ota',
    'Pahlavi':	'pal',
    'Palauan':	'pau',
    'Pali':	'pli',
    'Pampanga':	'pam',
    'Pangasinan':	'pag',
    'Panjabi':	'pan',
    'Papiamento':	'pap',
    'Papuan':	'paa',
    'Persian':	'per',
    'Philippine':	'phi',
    'Phoenician':	'phn',
    'Pohnpeian':	'pon',
    'Polish':	'pol',
    'Portuguese Creole':	'cpp',
    'Portuguese':	'por',
    'Prakrit languages':	'pra',
    'Provençal (to 1500)':	'pro',
    'Pushto':	'pus',
    'Quechua':	'que',
    'Raeto-Romance':	'roh',
    'Rajasthani':	'raj',
    'Rapanui':	'rap',
    'Rarotongan':	'rar',
    'Romance':	'roa',
    'Romani':	'rom',
    'Romanian':	'rum',
    'Rundi':	'run',
    'Russian':	'rus',
    'Salishan languages':	'sal',
    'Samaritan Aramaic':	'sam',
    'Sami':	'smi',
    'Samoan':	'smo',
    'Sandawe':	'sad',
    'Sango (Ubangi Creole)':	'sag',
    'Sanskrit':	'san',
    'Santali':	'sat',
    'Sardinian':	'srd',
    'Sasak':	'sas',
    'Scots':	'sco',
    'Scottish Gaelic':	'gla',
    'Selkup':	'sel',
    'Semitic':	'sem',
    'Serbian':	'srp',
    'Serer':	'srr',
    'Shan':	'shn',
    'Shona':	'sna',
    'Sichuan Yi':	'iii',
    'Sicilian Italian':	'scn',
    'Sidamo':	'sid',
    'Sign languages':	'sgn',
    'Siksika':	'bla',
    'Sindhi':	'snd',
    'Sinhalese':	'sin',
    'Sino-Tibetan':	'sit',
    'Siouan':	'sio',
    'Skolt Sami':	'sms',
    'Slavey':	'den',
    'Slavic':	'sla',
    'Slovak':	'slo',
    'Slovenian':	'slv',
    'Sogdian':	'sog',
    'Somali':	'som',
    'Songhai':	'son',
    'Soninke':	'snk',
    'Sorbian':	'wen',
    'Sotho':	'sot',
    'South American Indian':	'sai',
    'Southern Sami':	'sma',
    'Spanish':	'spa',
    'Sranan':	'srn',
    'Sukuma':	'suk',
    'Sumerian':	'sux',
    'Sundanese':	'sun',
    'Susu':	'sus',
    'Swahili':	'swa',
    'Swazi':	'ssw',
    'Swedish':	'swe',
    'Swiss German':	'gsw',
    'Syriac':	'syc',
    'Tagalog':	'tgl',
    'Tahitian':	'tah',
    'Tai':	'tai',
    'Tajik':	'tgk',
    'Tamashek':	'tmh',
    'Tamil':	'tam',
    'Tatar':	'tat',
    'Telugu':	'tel',
    'Temne':	'tem',
    'Terena':	'ter',
    'Tetum':	'tet',
    'Thai':	'tha',
    'Tibetan':	'tib',
    'Tigré':	'tig',
    'Tigrinya':	'tir',
    'Tiv':	'tiv',
    'Tlingit':	'tli',
    'Tok Pisin':	'tpi',
    'Tokelauan':	'tkl',
    'Tonga (Nyasa)':	'tog',
    'Tongan':	'ton',
    'Tsimshian':	'tsi',
    'Tsonga':	'tso',
    'Tswana':	'tsn',
    'Tumbuka':	'tum',
    'Tupi languages':	'tup',
    'Turkish':	'tur',
    'Turkmen':	'tuk',
    'Tuvaluan':	'tvl',
    'Tuvinian':	'tyv',
    'Twi':	'twi',
    'Udmurt':	'udm',
    'Ugaritic':	'uga',
    'Uighur':	'uig',
    'Ukrainian':	'ukr',
    'Umbundu':	'umb',
    'Upper Sorbian':	'hsb',
    'Urdu':	'urd',
    'Uzbek':	'uzb',
    'Vai':	'vai',
    'Venda':	'ven',
    'Vietnamese':	'vie',
    'Volapük':	'vol',
    'Votic':	'vot',
    'Wakashan languages':	'wak',
    'Walloon':	'wln',
    'Waray':	'war',
    'Washoe':	'was',
    'Welsh':	'wel',
    'Western Pahari languages':	'him',
    'Wolayta':	'wal',
    'Wolof':	'wol',
    'Xhosa':	'xho',
    'Yakut':	'sah',
    'Yao (Africa)':	'yao',
    'Yapese':	'yap',
    'Yiddish':	'yid',
    'Yoruba':	'yor',
    'Yupik languages':	'ypk',
    'Zande languages':	'znd',
    'Zapotec':	'zap',
    'Zaza':	'zza',
    'Zenaga':	'zen',
    'Zhuang':	'zha',
    'Zulu':	'zul',
    'Zuni':	'zun',
}


LANGUAGE_REPLACEMENTS = {
    ';':    ',',
    'English, Old (ca. 450-1100)':  'Old English',
    'Creoles and Pidgins, English-based (Other)':   'English Creole',
    'Creoles and Pidgins, French-based (Other)':    'French Creole',
    'Creoles and Pidgins, Portuguese-based (Other)':    'Portuguese Creole',
    'Dutch, Middle (ca. 1050-1350)':    'Middle Dutch',
    'English, Middle (1100-1500)':      'Middle English',
    'French, Middle (ca. 1300-1600)':   'Middle French',
    'French, Old (ca. 842-1300)':       'Old French',
    'German, Middle High (ca. 1050-1500)':  'Middle High German',
    'German, Old High (ca. 750-1050)':      'Old High German',
    'Greek, Ancient (to 1453)':         'Ancient Greek',
    'Greek, Modern (1453-)':            'Greek',
    'Irish, Middle (ca. 1100-1550)':    'Middle Irish',
    'Newari, Old':                      'Old Newari',
    'Turkish, Ottoman':                 'Ottoman Turkish',
    'Irish, Old (to 1100)':             'Old Irish',
    'Syriac, Modern':                   'Modern Syriac',
    ' (Other)': '',
}


SUBJECT_CATEGORY_SOURCE_CODES = {
    'BIC2SC':       'bicssc',
    'BISACC':       'bisacsh',
    'THEMASC':      'thema',
    'UKSLCAFC':     'ukslc',
    'UKSLCANFC':    'ukslc',
    'UKSLCCC':      'ukslc',
    'BIC2ST':       'bicssc',
    'BISACT':       'bisacsh',
    'THEMAST':      'thema',
    'UKSLCAFT':     'ukslc',
    'UKSLCANFT':    'ukslc',
    'UKSLCCT':      'ukslc',
}


RE_NATURE_OF_CONTENTS = {
    re.compile(r'\b(abstract|summary)', re.I): 'a',
    re.compile(r'\bbibliograph', re.I): 'b',
    re.compile(r'\bcatalog', re.I): 'c',
    re.compile(r'\bdiction+ai?r', re.I): 'd',
    re.compile(r'\bencyclop', re.I): 'e',
    re.compile(r'\bhand-?book', re.I): 'f',
    re.compile(r'\blegal\b', re.I): 'g',
    re.compile(r'\bindex', re.I): 'i',
    re.compile(r'\bpatent', re.I): 'j',
    re.compile(r'\bdiscograph', re.I): 'k',
    re.compile(r'\blegislat', re.I): 'l',
    re.compile(r'\bthes[ei]s\b|\bdissertatio', re.I): 'm',
    re.compile(r'\bliterature review', re.I): 'n',
    re.compile(r'\breview', re.I): 'o',
    # omitted p - Programmed texts
    re.compile(r'\bfilmograph', re.I): 'q',
    re.compile(r'\bdirector', re.I): 'r',
    re.compile(r'\bstatistic', re.I): 's',
    re.compile(r'\btechnical report', re.I): 't',
    re.compile(r'\b(standard|specific)', re.I): 'u',
    re.compile(r'\bcase note', re.I): 'v',
    re.compile(r'\blaw (report|digest)', re.I): 'w',
    re.compile(r'\byear-?book', re.I): 'y',
    re.compile(r'\btreat(y|ies)', re.I): 'z',
    re.compile(r'\boff-?print', re.I): '2',
    re.compile(r'\bcalendar', re.I): '5',
    re.compile(r'\b(comic|graphic novel)', re.I): '6',
    }


BIC_CBMC_CODES = {
    # Interest levek
    'A':    '0-5 years',
    'B':    '5-7 years',
    'C':    '7-9 years',
    'D':    '9-11 years',
    'E':    '12+ years',
    # Broad subject
    '1':    'Poetry & Plays / Songs & Music',
    '2':    'Home / Early Learning ',
    '3':    'Fiction',
    '4':    'Reference',
    '5':    'Non-fiction',
    # Type / format
    'F':    'Electronic Format ',
    'G':    'Annual',
    'H':    'Treasury / Gift Anthology',
    'J':    'Novelty Book',
    'K':    'Board / Bath / Rag Book',
    'L':    'Activity Book',
    'M':    'Picture Book',
    'N':    'Ordinary Printed Book Format',
    'P':    'Stationery & Other Merchandise',
    # Character
    '6':    'Character',
    '7':    'Non-character',
    # Tie-in
    '8':    'TV / Film Tie-in',
    '9':    'Non Tie-in',
}


# ====================
#      Functions
# ====================


def usage():
    """Function to print information about the program"""
    print('Correct syntax is:')
    print('nielsen2marc_products -i <input_path> -o <output_path>')
    print('    -i    path to FOLDER containing Input files')
    print('    -o    path to FOLDER to contain Output files')
    print('If not specified, input path will be /Input/Products')
    print('If not specified, output path will be /Output/Products')
    print('\nUse quotation marks (") around arguments which contain spaces')
    print('\nInput file names should end .add, .upd or .del')
    print('\nOptions')
    print('    --help    Display this message and exit')
    exit_prompt()


# ====================
#      Classes
# ====================

class ContribName:

    def __init__(self, i, row):
        self.role_code = row['CR{}'.format(str(i))]
        try: self.role = ONIX_CONTRIBUTOR_ROLES[self.role_code]
        except: self.role = re.sub(r'\([^()]*\)|\bother\b', '', row['CRT{}'.format(str(i))])
        self.type = 'person' if row['CCI{}'.format(str(i))] == 'N' else 'corporate' if row['CCI{}'.format(str(i))] == 'Y' else None
        self.full_name = clean(row['CNF{}'.format(str(i))])
        if self.type == 'person' and '(' in row['CNF{}'.format(str(i))]:
            self.institution = clean(re.sub(r'^(.*)\s*\(([^()]*)\).*$', r'\2', self.full_name))
        else: self.institution = None
        if self.full_name:
            self.name = re.sub(r'\b([A-Z])\b', r'\1.', clean(re.sub(r',.*$', '', re.sub(r'\([^()]*\)', '', self.full_name))))
            self.inverted_name = re.sub(r'\b([A-Z])\b', r'\1.', clean(re.sub(r'^\s*(.+)\s+([^\s]+)\s*$', r'\2, \1', self.name)))


class NielsenCSVProducts:

    def __init__(self, csv_row, status):
        self.row = csv_row
        self.status = status
        self.material_type = None
        self.UK = False

    def is_uk(self):
        return self.UK

    def record_id(self):
        if self.row['ISBN13']:
            return self.row['ISBN13']
        return None

    def marc(self):

        # NEEDS WORK - need to make sure e-books get treated as books, not computer files

        PFC = clean(self.row['PFC'])
        if PFC:
            if PFC[0] == 'A' or PFC in ['PI']: self.material_type = 'MU'
            if PFC[0] in ['B', 'M'] or PFC in ['PA', 'PB', 'PC', 'PD', 'PE', 'PF',
                                               'PL', 'PR', 'PS', 'PU', 'PZ']: self.material_type = 'BK'
            if PFC[0] == 'C': self.material_type = 'MP'
            if PFC[0] in ['D', 'E', 'L']: self.material_type = 'CF'
            if PFC[0] in ['F', 'V', 'X', 'Z'] or PFC in ['PG', 'PH', 'PJ', 'PK', 'PM',
                                                         'PN', 'PO', 'PP', 'PQ', 'PT']: self.material_type = 'VM'
            if PFC[0] == 'S': self.material_type = 'MX'

        # Leader (NR)

        try: p6 = ONIX_PRODUCT_CONTENT_TYPE[clean(self.row['PCTC1'])].leader_06
        except:
            try: p6 = ONIX_PRODUCT_FORM[PFC][4]
            except: p6 = 'a'
        if p6 == 'a': self.material_type = 'BK'
        leader = '     {}{}m a22     2  4500'.format(self.status, p6)

        record = Record(leader=leader)

        record.add_field(Field(tag='FMT', data=self.material_type))

        # 001 - Control Number

        if self.row['ISBN13']:
            record.add_field(Field(tag='001', data=self.row['ISBN13']))

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
        PUBPD = format_date(clean(self.row['PUBPD']))
        REISD = format_date(clean(self.row['REISD']))
        CY = format_date(clean(self.row['CY']))
        if PUBPD and REISD and REISD != PUBPD:
            data += 'r' + REISD + PUBPD
        elif PUBPD and CY and CY != PUBPD:
            data += 't' + PUBPD + CY
        elif PUBPD:
            data += 's' + PUBPD + '    '
        else: data += 'nuuuuuuuu'
        # 15-17 - Place of publication, production, or execution
        # COP   Country of publication
        COP = clean(self.row['COP'])
        if COP and COUNTRY_CODES[COP] in ['xxk', 'enk', 'ie ', 'nik', 'stk', 'wlk']: self.UK = True
        try: data += COUNTRY_CODES[COP]
        except:
            if COP: print(COP + '\n')
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
            try: data += ONIX_PRODUCT_FORM[PFC][0]
            except: data += '|'
            # 26 - 27 - Undefined
            data += '  '
            # 28 - Government publication
            data += '|'
            # 29 - Form of item
            if PFC[0] == 'C': data += 'r'
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
            if PFC == 'PI': data += 'u'
            else: data += 'n'
            # 21 - Music parts
            if PFC == 'PI': data += 'u'
            else: data += 'n'
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            NAC, i = '|', 1
            while NAC == '|' and i in range(1, 10):
                try: NAC = AUDIENCE_CODES[clean(self.row['NAC{}'.format(str(i))])]
                except: NAC = '|'
                i += 1
            data += NAC
            # 23 - Form of item
            if PFC == 'PI': data += 'r'
            elif PFC in ['AN', 'AO']: data += 'o'
            elif PFC in ['AJ', 'AK', 'AL']: data += 's'
            else: data += '|'
            # 24-29 - Accompanying matter
            data += '||||||'
            # 30-31 - Literary text for sound recordings
            test_string = '|' + '|'.join(self.row['{}{}'.format(subject_type, str(i))]
                                         for subject_type in ['BIC2ST', 'BISACT', 'THEMAST', 'UKSLCAFT', 'UKSLCANFT', 'UKSLCCT']
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
            RUN = clean(re.sub(r'[^0-9]', '', self.row['RUN']))
            if RUN:
                RUN = int(RUN)
                if RUN < 999: data += '{m:03d}'.format(m=RUN)
                else: data += '000'
            elif PFC[0] == 'V': data += '---'
            else: data += 'nnn'
            # 21 - Undefined
            data += ' '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            NAC, i = '|', 1
            while NAC == '|' and i in range(1, 10):
                try: NAC = AUDIENCE_CODES[clean(self.row['NAC{}'.format(str(i))])]
                except: NAC = '|'
                i += 1
            data += NAC
            # 23-27 - Undefined
            data += '     '
            # 28 - Government publication
            data += '|'
            # 29 - Form of item
            if PFC[0] == 'F' or PFC in ['PH', 'PM']: data += ' '
            elif PFC in ['PG', 'PJ', 'PK']: data += 'r'
            else: data += '|'
            # 30-32 - Undefined
            data += '   '
            # 33 - Type of visual material
            try: data += ONIX_PRODUCT_FORM[PFC][0]
            except: data += '|'
            # 34 - Technique
            data += '|'
        elif self.material_type == 'CF':
            # 18-21 - Undefined
            data += '    '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            NAC, i = '|', 1
            while NAC == '|' and i in range(1, 10):
                try: NAC = AUDIENCE_CODES[clean(self.row['NAC{}'.format(str(i))])]
                except: NAC = '|'
                i += 1
            data += NAC
            # 23 - Form of item
            data += 'o' if PFC == 'EC' else '|'
            # 24-25 - Undefined
            data += '  '
            # 26 - Type of computer file
            data += 'g' if PFC == 'DE' else '|'
            # 27 - Undefined
            data += ' '
            # 28 - Government publication
            data += '|'
            # 29-34 - Undefined
            data += '      '
        elif self.material_type == 'BK':
            # 18-21 - Illustrations
            # ILL   Illustrations and other contents note.
            ILL = clean(self.row['ILL'])
            if ILL: data += (''.join(ILLUSTRATIONS[x] for x in ILLUSTRATIONS if x in ILL) + '    ')[:4]
            else: data += '    '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            NAC, i = '|', 1
            while NAC == '|' and i in range(1, 10):
                try: NAC = AUDIENCE_CODES[clean(self.row['NAC{}'.format(str(i))])]
                except: NAC = '|'
                i += 1
            data += NAC
            # 23 - Form of item
            # PFC   Product Form: Code
            try: data += ONIX_PRODUCT_FORM[PFC][0]
            except: data += '|'
            # 24-27 - Nature of contents
            # PFCT      Product Form :Text Description
            # PCTCT*    Product Content: Text Description
            test_string = self.row['PFCT'] + '|' + self.row['ILL'] + '|' + '|'.join(self.row['PCTCT{}'.format(i)] for i in range(1, 10))
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
                                         for subject_type in ['BIC2ST', 'BISACT', 'THEMAST', 'UKSLCAFT', 'UKSLCANFT', 'UKSLCCT']
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
        try: data += clean(self.row['SLC'] + '   ')[:3]
        except: data += '   '
        # 38 - Modified record
        data += '|'
        # 39 - Cataloging source
        data += ' '
        record.add_field(Field(tag='008', data=data))

        # 020 - International Standard Book Number (R)

        fmts = set()
        for c in ['EPT', 'EPF', 'EPFS']:
            v = clean(self.row[c])
            if v and v not in ['Unspecified', 'Format code not yet allocated']:
                fmts.add(re.sub(r'\s*format$', '', v))

        # ISBN13    ISBN13
        # REPIS13   ISBN-13 of book which it replaces
        # REPBIS13  ISBN-13 of book which it is replaced by
        # PUBAIS13  Publisher suggested alternative for this ISBN
        # EPRIS13   E-Publication rendering of this ISBN-13
        # EPBIS13   E-Publication based on this ISBN-13
        for c in ['ISBN13', 'REPIS13', 'REPBIS13', 'PUBAIS13', 'EPRIS13', 'EPBIS13']:
            v = clean(re.sub(r'[^0-9X]', '', self.row[c].upper()))
            if v:
                subfields = ['a' if c == 'ISBN13' else 'z', v]
                if c in ['EPRIS13', 'EPBIS13']:
                    subfields.extend(['q', 'electronic'])
                elif c == 'ISBN13':
                    qualifier = None
                    if self.row['PFCT'] and self.row['PFC'][0] != 'X' and self.row['PFC'] not in ['00', 'ZZ']:
                        qualifier = clean(re.sub(r'undefined|other|miscellaneous|\b(carrier|format|text)$', '', self.row['PFCT'], re.I))
                        if re.match(r'[A-Z][a-z]', qualifier): qualifier = qualifier[0].lower() + qualifier[1:]
                    if not qualifier and fmts: qualifier = 'electronic book'
                    if qualifier:
                        if fmts: qualifier += ' ({} format)'.format(list(fmts)[0])
                        subfields.extend(['q', qualifier])
                record.add_field(Field('020', [' ', ' '], subfields))

        # 024 - Other Standard Identifier (R)

        for c in ['EAN', 'ISMN', 'DOI']:
            v = self.row[c].strip()
            if v == '': v = None
            if v:
                subfields = ['a', v]
                if c == 'DOI': subfields.extend(['2', 'doi'])
                indicators = ['3' if c == 'EAN' else '2' if c == 'ISMN' else '7', ' ']
                record.add_field(Field('024', indicators, subfields))

        # 034 - Coded Cartographic Mathematical Data (R)

        # MS*   Map scale as stored
        for i in range(1, 2):
            MS = clean(self.row['MS{}'.format(str(i))])
            if MS:
                MS = re.sub(r'[^0-9]', '', MS.split(':')[-1])
                record.add_field(Field('034', ['1', ' '], ['a', 'a', 'b', MS]))

        # 040 - Cataloging Source (NR)

        record.add_field(Field('040', [' ', ' '], ['a', 'UK-WkNB', 'b', 'eng', 'c', 'Uk', 'd', 'Uk']))

        # 041 - Language Code (R)
        # SLC   Language of Text: Code
        # LS    Language statement
        # TFC*  Language translated from original language: Code
        languages = set()
        translations = set()
        SLC = clean(self.row['SLC'])
        if SLC: languages.add(SLC)
        LS = clean(self.row['LS'])
        if LS:
            for l in LANGUAGE_REPLACEMENTS: LS = LS.replace(l, LANGUAGE_REPLACEMENTS[l])
            for l in LS.split(','):
                try: languages.add(LANGUAGES_CODES[l.strip()])
                except: pass
        for i in range(1, 5):
            TFC = clean(self.row['TFC{}'.format(str(i))])
            if TFC: translations.add(TFC)
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
            LOCC = clean(self.row['LOCC{}'.format(str(i))])
            if LOCC: record.add_field(Field('050', [' ', '4'], ['a', LOCC]))
            else: break

        # 072 - Subject Category Code (R)

        for c in ['BIC2SC', 'BISACC', 'THEMASC', 'UKSLCAFC', 'UKSLCANFC', 'UKSLCCC']:
            terms = set()
            for i in range(1, 6 if c.startswith('UKSLC') else 10):
                v = clean(self.row['{}{}'.format(c, str(i))])
                if v: terms.add(v)
            for v in sorted(terms):
                record.add_field(Field('072', [' ', '7'], ['a', v, '2', SUBJECT_CATEGORY_SOURCE_CODES[c]]))

        # PRODCC    Product Class: Code
        PRODCC = clean(self.row['PRODCC'])
        if PRODCC: record.add_field(Field('072', [' ' , ' '], ['a', PRODCC]))

        # 082 - Dewey Decimal Classification Number (R)

        # DEWS*     DDC Edition No
        # DEWEY*    DDC value
        for i in range(1, 10):
            DEWS = clean(re.sub(r'[^0-9]', '', self.row['DEWS{}'.format(str(i))]))
            DEWEY = clean(re.sub(r'[^0-9\.]', '', self.row['DEWEY{}'.format(str(i))]))
            if DEWEY:
                subfields = ['a', DEWEY]
                if DEWS: subfields.extend(['2', DEWS])
                record.add_field(Field('082', ['0', '4'], subfields))
            else: break

        # 100 - Main Entry-Personal Name (NR)

        names = set()
        for i in range(1, 10):
            name = ContribName(i, self.row)
            if name.full_name: names.add(name)

        authors = [n.full_name for n in names if n.role == 'author']
        if len(authors) > 1: resp = ', '.join(authors[:-1]) + ' and ' + authors[-1]
        elif authors: resp = authors[0]
        else: resp = ''

        editors = [n.full_name for n in names if n.role == 'editor']
        if len(editors) > 1: resp += ' ; edited by ' + ', '.join(editors[:-1]) + ' and ' + editors[-1]
        elif editors: resp += ' ; edited by ' + editors[0]

        others = [clean('{} {}'.format(n.role, n.full_name)) for n in names if n.role not in ['author', 'editor']]
        resp += ' ; '.join(others)

        if resp != '': resp = clean(resp) + '.'

        authors = [n for n in names if n.role == 'author']
        if authors:
            author = authors[0]
            record.add_field(Field('110' if author.type == 'corporate' else '100',
                                   ['2' if author.type == 'corporate' else '1', ' '],
                                   ['a', author.inverted_name + ',', 'e', 'author.']))
            authors.remove(author)

        # 245 - Title Statement (NR)

        # LA    Leading Article of Title. Usually A or The
        # TL    Main text of Title
        # ST    Subtitle of text
        # PVNO* Volume or Part number
        # PT*   Title of this volume or part
        # YS    Year Statement
        LA = clean(self.row['LA'])
        TL = clean(self.row['TL']) or clean(self.row['FTS']) or '[TITLE NOT PROVIDED]'
        PVNO1 = clean(self.row['PVNO1'])
        PVNO2 = clean(self.row['PVNO2'])
        PT1 = clean(self.row['PT1'])
        PT2 = clean(self.row['PT2'])
        YS = clean(self.row['YS'])
        if LA: TL = clean(LA + ' ' + TL)
        ST = clean(self.row['ST'])
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

        EDSL = clean(self.row['EDSL']) or clean(self.row['EDSS'])
        if not EDSL:
            EDSL = re.sub(r'[^0-9]', '', self.row['EDN'])
            if EDSL: EDSL = str(ordinal(int(EDSL))) + ' edition'
        if EDSL:
            EDSL = clean_edition(EDSL)
            record.add_field(Field('250', [' ', ' '], ['a', '{}.'.format(EDSL)]))

        # 255 - Cartographic Mathematical Data (R)

        # MS*   Map scale as stored
        for i in range(1, 2):
            MS = clean(self.row['MS{}'.format(str(i))])
            if MS:
                MS = MS.split(':', 1)
                MS = '{}:{}'.format(re.sub(r'[^0-9]', '', MS[0]), re.sub(r'[^0-9,]]', '', re.sub(r'\s+', ',', MS[1].strip())))
                record.add_field(Field('255', [' ', ' '], ['a', 'Scale {}.'.format(MS)]))

        # 264 - Production, Publication, Distribution, Manufacture, and Copyright Notice (R)

        # POP       Place of publication
        # COP       Country of publication
        # IMPN      Imprint Name
        # PUBPD     Date of Publication: as supplied by Publisher or approved source
        POP = clean(self.row['POP'])
        COP = clean(self.row['COP'])
        IMPN = clean(self.row['IMPN']) or clean(self.row['PUBN'])
        PUBPD = format_date(clean(self.row['PUBPD']))
        if POP and COP and COP not in ['United States', 'United Kingdom'] and COP != POP:
            POP = '{}, {}'.format(POP, COP)
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
                DN = clean(self.row['{}ADN{}'.format(c, str(i))])
                if DN: d.add(DN)
            if d:
                d = '[distributor] ' + ' :|[distributor] '.join(d) + '.'
                for DN in d.split('|'):
                    subfields.extend(['b', DN])
                record.add_field(Field('264', ['3', '2'], subfields))

        # CY        Copyright Year
        CY = format_date(clean(self.row['CY']))
        if CY: record.add_field(Field('264', [' ', '4'], ['c', '\u00A9{}.'.format(CY)]))

        # 300 - Physical Description (R)

        # NOI   Number of Items
        # PAG   Pagination, as supplied
        # ILL   Illustrations and other contents note
        # HMM   Height along spine in mm
        # RUN   Running Time
        NOI = clean(self.row['NOI'].lower()) or clean(self.row['NOP'])
        if NOI and (NOI == '1' or NOI.startswith('1 ')): NOI = None
        PAG = clean(self.row['PAG']) or clean(self.row['PAGNUM'])
        RUN = clean(re.sub(r'[^0-9]', '', self.row['RUN']))
        ILL = clean_description(self.row['ILL'])
        HMM = re.sub(r'[^0-9]', '', self.row['HMM'])
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
        RUN = clean(re.sub(r'[^0-9]', '', self.row['RUN']))
        if RUN:
            RUN = int(RUN)
            record.add_field(Field('306', [' ', ' '], ['a', '{h:02d}{m:02d}00'.format(h=RUN // 60, m=RUN % 60)]))

        # 336 - Content Type (R)

        content_types = set()
        try: content_types.add(ONIX_PRODUCT_FORM[clean(self.row['PFC'])][1])
        except: pass
        for i in range(1, 10):
            try: content_types.add(ONIX_PRODUCT_CONTENT_TYPE[clean(self.row['PCTC{}'.format(str(i))])].rda_text)
            except: pass
        for v in content_types:
            record.add_field(Field('336', [' ', ' '], ['a', v, '2', 'rdacontent']))

        # 337 - Media Type (R)
        # A categorization reflecting the general type of intermediation device required
        # to view, play, run, etc., the content of a manifestation.

        try: v = ONIX_PRODUCT_FORM[clean(self.row['PFC'])][2]
        except: v = 'unspecified'
        record.add_field(Field('337', [' ', ' '], ['a', v, '2', 'rdamedia']))

        # 338 - Carrier Type (R)

        try: v = ONIX_PRODUCT_FORM[clean(self.row['PFC'])][3]
        except: v = 'unspecified'
        record.add_field(Field('338', [' ', ' '], ['a', v, '2', 'rdacarrier']))

        # 365 - Trade Price (R)

        for c in DISTRIBUTION_AREAS:
            if c != 'IRL':
                cur = DISTRIBUTION_AREAS[c][1]
                # xxxCCPTC      Price Type – Code
                # xxxCCPRRRP    The Current Price Of The Record (inc Taxes)
                # xxxCCPRPN     Any supplementary notes regarding tax information
                # xxxCCPRPxTC   A code which specifies a value-added tax rate applying to the whole of the price, or to the amount of a price which is specified in xxxCCPRP1TP.
                # xxxCCPRPxTR   The tax rate value
                # xxxCCPRPxTP   The amount that is taxable
                # xxxCCPRPxTOP  The amount of tax
                # xxxCCPRA      The area as stored on the Nielsen system
                CCPTC = clean(self.row['{}CCPTC'.format(cur)]) or '02'
                CCPRRRP = clean(self.row['{}CCPRRRP'.format(cur)])
                CCPRPN = clean(self.row['{}CCPRPN'.format(cur)])
                CCPRA = clean(self.row['{}CCPRA'.format(cur)])

                if CCPRRRP:
                    self.UK = True
                    subfields = ['a', CCPTC, 'b', CCPRRRP, 'c', cur, 'd', '00']
                    if CCPRPN: subfields.extend(['e', CCPRPN])
                    for i in range(1, 2):
                        CCPRP1TC = clean(self.row['{}CCPRP{}TC'.format(cur, str(i))])
                        CCPRP1TR = clean(self.row['{}CCPRP{}TR'.format(cur, str(i))])
                        CCPRP1TP = clean(self.row['{}CCPRP{}TP'.format(cur, str(i))])
                        CCPRP1TOP = clean(self.row['{}CCPRP{}TOP'.format(cur, str(i))])
                        if CCPRP1TC and CCPRP1TP and CCPRP1TR and CCPRRRP and CCPRP1TOP:
                            subfields.extend(['h' if i == '1' else 'i', '{} {} {} {}'.format(CCPRP1TC, CCPRP1TP, CCPRP1TR, CCPRRRP, CCPRP1TOP)])
                    if CCPRA: subfields.extend(['j', CCPRA])
                    # xxxtDN*       The Org name of the 'distributor'
                    DN = clean(self.row['{}ADN1'.format(c)])
                    if DN: subfields.extend(['m', DN])
                    subfields.extend(['2', 'onixpt'])
                    record.add_field(Field('365', [' ', ' '], subfields))

        # 366 - Trade Availability Information (R)

        for c in DISTRIBUTION_AREAS:
            if c != 'IRL':
                # xxxNBDEAD     Availability Date
                # xxxNBDPAC     ONIX Product Availability – Code
                NBDEAD = clean(re.sub(r'[^0-9]', '', self.row['{}NBDEAD'.format(c)]))
                NBDPAC = clean(self.row['{}NBDPAC'.format(c)])
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
        EMBD = clean(re.sub(r'[^0-9]', '', self.row['EMBD']))
        PUBSC = clean(self.row['PUBSC'])
        PUBST = clean(self.row['PUBST'])
        MOPD = clean(self.row['MOPD'])
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
        SN = clean(self.row['SN'])
        NWS = clean(self.row['NWS'])
        ISSN = clean(self.row['ISSN'])
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
            v = clean(self.row[c])
            if v:
                record.add_field(Field('500', [' ', ' '], ['a', '{}{}.'.format(PREAMBLES[c], v)]))
                if c in ['IMPID', 'PUBID']:
                    record.add_field(Field('N{}I'.format(c[0]), [' ', ' '], ['a', v], ['d', datetime.date.today()]))

        # PFDT*     Product Form Detail: Text Description
        # PFFSD*    Product Form Feature Safety Type: Text Description

        for c in ['PFDT', 'PFFSD']:
            for i in range(1, 10):
                v = clean(self.row['{}{}'.format(c, str(i))])
                if v: record.add_field(Field('500', [' ', ' '], ['a', '{}.'.format(v)]))
                else: break

        # PWU*      Product Website URL
        # PWTT*     Product Website Type: Text Description
        for i in range(1, 10):
            PWU = self.row['PWU{}'.format(str(i))].strip()
            if PWU == '': PWU = None
            PWTT = clean(self.row['PWTT{}'.format(str(i))])
            if not PWTT or 'unspecified' in PWTT.lower(): PWTT = 'Related website'
            if PWU: record.add_field(Field('500', [' ', ' '], ['a', '{}: {}.'.format(PWTT, PWU)]))
            else: break

        # 521 - Target Audience Note (R)

        for i in range(1, 10):
            # OAT*  ONIX Audience level: Text Description
            OAT = clean(self.row['OAT{}'.format(str(i))])
            if OAT: record.add_field(Field('521', [' ', ' '], ['a', '{}.'.format(OAT)]))
            else: break

        # USGCT     ONIX US grade: Text Description
        # IA    Interest Age
        # RA    Reading Age
        for c in ['USGCT', 'IA', 'RA']:
            c = clean(self.row[c])
            if c: record.add_field(Field('521', ['0' if c == 'USGCT' else '1' if c == 'IA' else '2', ' '],
                                         ['a', '{}.'.format(c)]))

        # CBMCCODE  BIC Children’s Book Marketing Category: Code
        try: CBMCCODE = BIC_CBMC_CODES[clean(self.row['CBMCCODE'])[0]]
        except: CBMCCODE = None
        if CBMCCODE: record.add_field(Field('521', ['1', ' '], ['a', '{}.'.format(CBMCCODE)]))

        # 501 - With Note (R)

        # CIS   A statement of the contained items
        CIS = clean(self.row['CIS'])
        if CIS: record.add_field(Field('501', [' ', ' '], ['a', CIS + '.']))

        for i in range(1, 10):
            # CIID*     Contained Item Identifier
            # CIPFCT*   Contained Item: Product Form Text Description
            # CINOP*    Contained item number of identical pieces
            CIID = clean(self.row['CIID{}'.format(str(i))])
            CIPFCT = clean(self.row['CIPFCT{}'.format(str(i))])
            CINOP = clean(self.row['CINOP{}'.format(str(i))])
            if CIID:
                CIID = 'Contains {} of {}{}.'.format('a copy' if CINOP == '1' else '{} copies'.format(CINOP),
                                                    CIID, ' ({})'.format(CIPFCT) if CIPFCT else '')
                record.add_field(Field('501', [' ', ' '], ['a', CIID]))
            if not CIID: break

        # 505 - Formatted Contents Note (R)
        # 520 - Summary, Etc. (R)
        # 545 - Biographical or Historical Data (R)

        for c in ['TOC', 'LD', 'REV', 'P', 'BIOG']:
            v = clean(self.row['NBDF{}'.format(c)]) or clean(self.row['NBD{}'.format(c)])
            if c == 'LD' and not v: v = clean(self.row['NBDFSD']) or clean(self.row['NBDSD'])
            v = clean_html(v)
            if v:
                i = 0
                for part in split_long(v, isbn=str(self.row['ISBN13'])):
                    record.add_field(Field('505' if c == 'TOC' else '545' if c == 'BIOG' else '520',
                                           ['8' if i == 0 and c == 'TOC' else '0' if c in ['BIOG', 'TOC'] else '1' if c in ['REV', 'P'] else ' ', ' '],
                                           ['a', part + '.']))
                    i += 1

        # 506 - Restrictions on Access Note (R)

        # RSS    Restricted Sales statement
        RSS = clean(self.row['RSS'])
        if RSS: record.add_field(Field('506', [' ', ' '], ['a', '{}.'.format(RSS)]))

        # 538 - System Details Note (R)
        # 563 - Binding Information (R)

        for i in range(1, 10):
            # PFFT*     Product Form Feature Type: Code (ONIX code list 79)
            # PFFTT*    Product Form Feature Type: Text Description
            # PFFVT*    Product Form Feature Value: Text
            # PFFD*     Product Form Feature Description
            PFFT = clean(self.row['PFFT{}'.format(str(i))])
            PFFTT = clean(self.row['PFFTT{}'.format(str(i))])
            PFFVT = clean(self.row['PFFVT{}'.format(str(i))])
            PFFD = clean(self.row['PFFD{}'.format(str(i))])
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
        LS = clean(self.row['LS'])
        TS = clean(self.row['TS'])
        if LS or TS:
            for l in LANGUAGE_REPLACEMENTS:
                if LS: LS = LS.replace(l, LANGUAGE_REPLACEMENTS[l])
                if TS: TS = TS.replace(l, LANGUAGE_REPLACEMENTS[l])
            text = 'In {}{}'.format(rreplace(LS, ', ', ' and '), '; ' if TS else '.') if LS else ''
            if TS: text += '{}ranslated from {}.'.format('t' if LS else 'T', rreplace(TS, ', ', ' and '))
            record.add_field(Field('546', [' ', ' '], ['a', text]))

        # 586 - Awards Note (R)

        # PSF   Structured Prize details for all Prizes combined
        PSF = clean(self.row['PSF'])
        if PSF: record.add_field(Field('586', [' ', ' '], ['a', '{}.'.format(PSF)]))

        # 588 - Source of Description Note (R)

        record.add_field(Field('588', [' ', ' '], ['a', 'Description based on CIP data; item not viewed.']))

        # 650 - Subject Added Entry-Topical Term (R)

        # BIC2QT*   BIC Qualifier, version 2.1: Text Description
        bic_qualifiers = []
        for i in range(1, 10):
            BIC2QC = clean(self.row['BIC2QC{}'.format(str(i))])
            BIC2QT = clean(self.row['BIC2QT{}'.format(str(i))])
            if BIC2QT and BIC2QC:
                bic_qualifiers.extend(['z' if BIC2QC[0] == '1' else 'y' if BIC2QC[0] == '3' else 'x', BIC2QT])
            else: break

        # THEMAQT*  Thema Qualifier: Text
        thema_qualifiers = []
        for i in range(1, 10):
            THEMAQC = clean(self.row['THEMAQC{}'.format(str(i))])
            THEMAQT = clean(self.row['THEMAQT{}'.format(str(i))])
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
                v = clean(self.row['{}{}'.format(c, str(i))])
                if v: terms.add(clean(v))
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
        PRODCT = clean(self.row['PRODCT'])
        if PRODCT:
            subfields = ['a', PRODCT.split(': ')[0]]
            for s in PRODCT.split(': ')[1:]:
                subfields.extend(['x', s])
            record.add_field(Field('650', [' ', '4'], subfields))

        # 653 - Index Term-Uncontrolled (R)

        # KEYWORDS      Key Words
        KEYWORDS = clean_html(clean(self.row['KEYWORDS']))
        if KEYWORDS:
            KEYWORDS = set(k.strip() for k in KEYWORDS.split(';') if k)
            for k in sorted(KEYWORDS):
                record.add_field(Field('653', [' ', ' '], ['a', k]))

        # 655 - Index Term-Genre/Form (R)

        # FICGH     British Library Fiction Genre Heading
        FICGH = clean(self.row['FICGH'])
        if FICGH: record.add_field(Field('655', [' ', '4'], FICGH + '.'))

        # 700 - Added Entry-Personal Name (R)

        for name in authors:
            record.add_field(Field('710' if name.type == 'corporate' else '700',
                                   ['2' if name.type == 'corporate' else '1', ' '],
                                   ['a', name.inverted_name + ',', 'e', 'author.']))

        editors = [n for n in names if n.role == 'editor']
        for name in editors:
            record.add_field(Field('710' if name.type == 'corporate' else '700',
                                   ['2' if name.type == 'corporate' else '1', ' '],
                                   ['a', name.inverted_name + ',', 'e', 'editor.']))

        others = [n for n in names if n.role not in ['author', 'editor']]
        for name in others:
            record.add_field(Field('710' if name.type == 'corporate' else '700',
                                   ['2' if name.type == 'corporate' else '1', ' '],
                                   ['a', name.inverted_name + ',', 'e', name.role + '.']))

        # 787 - Other Relationship Entry (R)

        # RWI*      Related Work ID
        # RWITN*    Related Work ID Name
        # RWTT*     Related Work Type Text
        for i in range(1, 10):
            RWI = clean(self.row['RWI{}'.format(str(i))])
            RWITN = clean(self.row['RWITN{}'.format(str(i))])
            RWTT = clean(self.row['RWTT{}'.format(str(i))])
            if RWI:
                subfields = []
                if RWTT: subfields.extend(['i', RWTT])
                subfields.extend(['z' if RWITN and 'SIBN' in RWITN else 'o', RWI])
                record.add_field(Field('787', ['1', ' '], subfields))
            else: break

        record.add_field(Field('SRC', [' ', ' '], ['a', 'Record converted from Nielsen CSV data to MARC21 by Collection Metadata.']))

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

    print('========================================')
    print('nielsen2marc_products')
    print('========================================')
    print('\nThis program converts Nielsen CSV files\n'
          'for PRODUCTS to MARC 21 (Bibliographic)\n')

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
    if not os.path.exists(os.path.join(output_path, 'UK')):
        os.makedirs(os.path.join(output_path, 'UK'))

    if not os.path.isfile(DATABASE_PATH):
        exit_prompt('Error: The file {} cannot be found'.format(DATABASE_PATH))

    db = IsbnDatabase()
    skip_check = True

    # --------------------
    # Iterate through input files
    # --------------------

    for file in os.listdir(input_path):

        if file.endswith(('.add', '.upd', '.del')):

            # Graph for ISBN information
            G = Graph(skip_check=skip_check)

            status = {'add': 'n', 'upd': 'c', 'del': 'd'}[file[-3:]]
            ids = set()
            print('\n\nProcessing file {} ...'.format(str(file)))
            print('----------------------------------------')
            print(str(datetime.datetime.now()))

            # Open input and output files
            ifile = open(os.path.join(input_path, file), mode='r', encoding='utf-8', errors='replace', newline='')
            ofile = open(os.path.join(output_path, file + '.lex'), 'wb')
            ofileUK = open(os.path.join(output_path, 'UK', file + '_UK.lex'), 'wb')
            tfile = open(os.path.join(output_path, file + '.txt'), mode='w', encoding='utf-8', errors='replace')
            dfile = open(os.path.join(output_path, file + '_duplicates.txt'), mode='w', encoding='utf-8', errors='replace')
            writer = MARCWriter(ofile)
            writerUK = MARCWriter(ofileUK)
            i = 0
            c = csv.DictReader(ifile, delimiter=',')
            for row in c:
                i += 1
                print('{} records processed'.format(str(i)), end='\r')
                nielsen = NielsenCSVProducts(row, status)
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
                nielsen = NielsenProduct(row)
                isbns = nielsen.get_isbns()
                if isbns:
                    data = [(i.isbn, i.format, i.work) for i in isbns if i.isbn]
                    G.add_nodes(data)
                    data = [(i.isbn, j.isbn) for i in isbns for j in isbns if
                            i.isbn and j.isbn and i.isbn != j.isbn and i.format != 'C' and j.format != 'C']
                    G.add_edges(data)

            # Close files
            for f in (ifile, ofile, ofileUK, tfile, dfile):
                f.close()

            G.check_graph()
            db.add_graph_to_database(G, skip_check=skip_check)

    date_time_exit()

if __name__ == '__main__':
    main(sys.argv[1:])
