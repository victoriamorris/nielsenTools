#  -*- coding: utf-8 -*-

"""Tools for working with Nielsen data used within nielsenTools."""

# Import required modules
from nielsenTools.marc_data import *
from nielsenTools.onix import *

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
    'Afghanistan':	'af ',
    'Alabama':	'alu',
    'Alaska':	'aku',
    'Albania':	'aa ',
    'Alberta':	'abc',
    'Algeria':	'ae ',
    'American Samoa':	'as ',
    'Andorra':	'an ',
    'Angola':	'ao ',
    'Anguilla':	'am ',
    'Antarctica':	'ay ',
    'Antigua and Barbuda':	'aq ',
    'Argentina':	'ag ',
    'Arizona':	'azu',
    'Arkansas':	'aru',
    'Armenia (Republic)':	'ai ',
    'Aruba':	'aw ',
    'Australia':	'at ',
    'Australian Capital Territory':	'aca',
    'Austria':	'au ',
    'Azerbaijan':	'aj ',
    'Bahamas':	'bf ',
    'Bahrain':	'ba ',
    'Bangladesh':	'bg ',
    'Barbados':	'bb ',
    'Belarus':	'bw ',
    'Belgium':	'be ',
    'Belize':	'bh ',
    'Benin':	'dm ',
    'Bermuda Islands':	'bm ',
    'Bermuda':	'bm ',
    'Bhutan':	'bt ',
    'Bolivia':	'bo ',
    'Bosnia and Herzegovina':	'bn ',
    'Botswana':	'bs ',
    'Bouvet Island':	'bv ',
    'Brazil':	'bl ',
    'British Columbia':	'bcc',
    'British Indian Ocean Territory':	'bi ',
    'British Virgin Islands':	'vb ',
    'Brunei':	'bx ',
    'Bulgaria':	'bu ',
    'Burkina Faso':	'uv ',
    'Burma':	'br ',
    'Burundi':	'bd ',
    'C\u00F4te d\'Ivoire':	'iv ',
    'Cabo Verde':	'cv ',
    'California':	'cau',
    'Cambodia':	'cb ',
    'Cameroon':	'cm ',
    'Canada':	'xxc',
    'Caribbean Netherlands':	'ca ',
    'Cayman Islands':	'cj ',
    'Central African Republic':	'cx ',
    'Chad':	'cd ',
    'Chile':	'cl ',
    'China (Republic :	1949- )':	'ch ',
    'China':	'cc ',
    'Christmas Island (Indian Ocean)':	'xa ',
    'Cocos (Keeling) Islands':	'xb ',
    'Colombia':	'ck ',
    'Colorado':	'cou',
    'Comoros':	'cq ',
    'Congo (Brazzaville)':	'cf ',
    'Congo (Democratic Republic)':	'cg ',
    'Connecticut':	'ctu',
    'Cook Islands':	'cw ',
    'Coral Sea Islands Territory':	'xga',
    'Costa Rica':	'cr ',
    'Croatia (Local Name:	Hrvatska)':	'ci ',
    'Croatia':	'ci ',
    'Cuba':	'cu ',
    'Cura\u00E7ao':	'co ',
    'Cyprus':	'cy ',
    'Czech Republic':	'xr ',
    'Czechia':	'xr ',
    'Delaware':	'deu',
    'Denmark':	'dk ',
    'District of Columbia':	'dcu',
    'Djibouti':	'ft ',
    'Dominica':	'dq ',
    'Dominican Republic':	'dr ',
    'Ecuador':	'ec ',
    'Egypt':	'ua ',
    'El Salvador':	'es ',
    'England':	'enk',
    'Equatorial Guinea':	'eg ',
    'Eritrea':	'ea ',
    'Estonia':	'er ',
    'Eswatini':	'sq ',
    'Ethiopia':	'et ',
    'Falkland Islands':	'fk ',
    'Faroe Islands':	'fa ',
    'Fiji':	'fj ',
    'Finland':	'fi ',
    'Florida':	'flu',
    'France':	'fr ',
    'French Guiana':	'fg ',
    'French Polynesia':	'fp ',
    'Gabon':	'go ',
    'Gambia':	'gm ',
    'Gaza Strip':	'gz ',
    'Georgia (Republic)':	'gs ',
    'Georgia':	'gau',
    'Germany':	'gw ',
    'Ghana':	'gh ',
    'Gibraltar':	'gi ',
    'Greece':	'gr ',
    'Greenland':	'gl ',
    'Grenada':	'gd ',
    'Guadeloupe':	'gp ',
    'Guam':	'gu ',
    'Guatemala':	'gt ',
    'Guernsey':	'gg ',
    'Guinea':	'gv ',
    'Guinea-Bissau':	'pg ',
    'Guyana':	'gy ',
    'Haiti':	'ht ',
    'Hawaii':	'hiu',
    'Heard and McDonald Islands':	'hm ',
    'Honduras':	'ho ',
    'Hong Kong':	'cc ',
    'Hungary':	'hu ',
    'Iceland':	'ic ',
    'Idaho':	'idu',
    'Illinois':	'ilu',
    'India':	'ii ',
    'Indiana':	'inu',
    'Indonesia':	'io ',
    'Iowa':	'iau',
    'Iran, Islamic Republic of':	'ir ',
    'Iran':	'ir ',
    'Iraq':	'iq ',
    'Iraq-Saudi Arabia Neutral Zone':	'iy ',
    'Ireland':	'ie ',
    'Isle of Man':	'im ',
    'Isle Of Man':	'im ',
    'Israel':	'is ',
    'Italy':	'it ',
    'Jamaica':	'jm ',
    'Japan':	'ja ',
    'Jersey':	'je ',
    'Johnston Atoll':	'ji ',
    'Jordan':	'jo ',
    'Kansas':	'ksu',
    'Kazakhstan':	'kz ',
    'Kentucky':	'kyu',
    'Kenya':	'ke ',
    'Kiribati':	'gb ',
    'Korea (North)':	'kn ',
    'Korea (South)':	'ko ',
    'Korea, Democratic People\'S Republic Of':	'ko ',      # South Korea
    'Korea, Democratic People\'s Republic of':	'ko ',      # South Korea
    'Korea, Republic of':	'ko ',      # South Korea
    'Korea, Republic Of':	'ko ',      # South Korea
    'Kosovo':	'kv ',
    'Kuwait':	'ku ',
    'Kyrgyzstan':	'kg ',
    'Laos':	'ls ',
    'Latvia':	'lv ',
    'Lebanon':	'le ',
    'Lesotho':	'lo ',
    'Liberia':	'lb ',
    'Libya':	'ly ',
    'Liechtenstein':	'lh ',
    'Lithuania':	'li ',
    'Louisiana':	'lau',
    'Luxembourg':	'lu ',
    'Madagascar':	'mg ',
    'Maine':	'meu',
    'Malawi':	'mw ',
    'Malaysia':	'my ',
    'Maldives':	'xc ',
    'Mali':	'ml ',
    'Malta':	'mm ',
    'Manitoba':	'mbc',
    'Marshall Islands':	'xe ',
    'Martinique':	'mq ',
    'Maryland':	'mdu',
    'Massachusetts':	'mau',
    'Mauritania':	'mu ',
    'Mauritius':	'mf ',
    'Mayotte':	'ot ',
    'Mexico':	'mx ',
    'Michigan':	'miu',
    'Micronesia (Federated States)':	'fm ',
    'Midway Islands':	'xf ',
    'Minnesota':	'mnu',
    'Mississippi':	'msu',
    'Missouri':	'mou',
    'Moldova':	'mv ',
    'Monaco':	'mc ',
    'Mongolia':	'mp ',
    'Montana':	'mtu',
    'Montenegro':	'mo ',
    'Montserrat':	'mj ',
    'Morocco':	'mr ',
    'Mozambique':	'mz ',
    'Namibia':	'sx ',
    'Nauru':	'nu ',
    'Nebraska':	'nbu',
    'Nepal':	'np ',
    'Netherlands':	'ne ',
    'Nevada':	'nvu',
    'New Brunswick':	'nkc',
    'New Caledonia':	'nl ',
    'New Hampshire':	'nhu',
    'New Jersey':	'nju',
    'New Mexico':	'nmu',
    'New South Wales':	'xna',
    'New York (State)':	'nyu',
    'New Zealand':	'nz ',
    'Newfoundland and Labrador':	'nfc',
    'Nicaragua':	'nq ',
    'Niger':	'ng ',
    'Nigeria':	'nr ',
    'Niue':	'xh ',
    'No place, unknown, or undetermined':	'xx ',
    'Norfolk Island':	'nx ',
    'North Carolina':	'ncu',
    'North Dakota':	'ndu',
    'North Macedonia':	'xn ',
    'Macedonia':	'xn ',
    'Macedonia, the former Yugoslav Republic of':	'xn ',
    'Northern Ireland':	'nik',
    'Northern Mariana Islands':	'nw ',
    'Northern Territory':	'xoa',
    'Northwest Territories':	'ntc',
    'Norway':	'no ',
    'Nova Scotia':	'nsc',
    'Nunavut':	'nuc',
    'Ohio':	'ohu',
    'Oklahoma':	'oku',
    'Oman':	'mk ',
    'Ontario':	'onc',
    'Oregon':	'oru',
    'Pakistan':	'pk ',
    'Palau':	'pw ',
    'Panama':	'pn ',
    'Papua New Guinea':	'pp ',
    'Paracel Islands':	'pf ',
    'Paraguay':	'py ',
    'Pennsylvania':	'pau',
    'Peru':	'pe ',
    'Philippines':	'ph ',
    'Pitcairn Island':	'pc ',
    'Poland':	'pl ',
    'Portugal':	'po ',
    'Prince Edward Island':	'pic',
    'Puerto Rico':	'pr ',
    'Qatar':	'qa ',
    'Qu\u00E9bec (Province)':	'quc',
    'Queensland':	'qea',
    'R\u00E9union':	're ',
    'Rhode Island':	'riu',
    'Romania':	'rm ',
    'Russia (Federation)':	'ru ',
    'Russian Federation':	'ru ',
    'Rwanda':	'rw ',
    'Saint Helena':	'xj ',
    'Saint Kitts-Nevis':	'xd ',
    'Saint Lucia':	'xk ',
    'Saint Pierre and Miquelon':	'xl ',
    'Saint Vincent and the Grenadines':	'xm ',
    'Saint-Barth\u00E9lemy':	'sc ',
    'Saint-Martin':	'st ',
    'Samoa':	'ws ',
    'San Marino':	'sm ',
    'Sao Tome and Principe':	'sf ',
    'Saskatchewan':	'snc',
    'Saudi Arabia':	'su ',
    'Scotland':	'stk',
    'Senegal':	'sg ',
    'Serbia and Montenegro':	'rb ',  # Code for Serbia; Montenegro = mo
    'Serbia':	'rb ',
    'Seychelles':	'se ',
    'Sierra Leone':	'sl ',
    'Singapore':	'si ',
    'Sint Maarten':	'sn ',
    'Slovakia':	'xo ',
    'Slovenia':	'xv ',
    'Solomon Islands':	'bp ',
    'Somalia':	'so ',
    'South Africa':	'sa ',
    'South Australia':	'xra',
    'South Carolina':	'scu',
    'South Dakota':	'sdu',
    'South Georgia and the South Sandwich Islands':	'xs ',
    'South Sudan':	'sd ',
    'Spain':	'sp ',
    'Spanish North Africa':	'sh ',
    'Spratly Island':	'xp ',
    'Sri Lanka':	'ce ',
    'Sudan':	'sj ',
    'Surinam':	'sr ',
    'Swaziland':	'sq ',
    'Sweden':	'sw ',
    'Switzerland':	'sz ',
    'Syria':	'sy ',
    'Taiwan':	'ch ',
    'Taiwan, Province of China':	'ch ',
    'Tajikistan':	'ta ',
    'Tanzania':	'tz ',
    'Tanzania, United Republic of':	'tz ',
    'Tasmania':	'tma',
    'Tennessee':	'tnu',
    'Terres australes et antarctiques fran\u00E7aises':	'fs ',
    'Texas':	'txu',
    'Thailand':	'th ',
    'Timor-Leste':	'em ',
    'Togo':	'tg ',
    'Tokelau':	'tl ',
    'Tonga':	'to ',
    'Trinidad and Tobago':	'tr ',
    'Tunisia':	'ti ',
    'Turkey':	'tu ',
    'Turkmenistan':	'tk ',
    'Turks and Caicos Islands':	'tc ',
    'Tuvalu':	'tv ',
    'Uganda':	'ug ',
    'Ukraine':	'un ',
    'United Arab Emirates':	'ts ',
    'United Kingdom':	'xxk',
    'United States Misc. Caribbean Islands':	'uc ',
    'United States Misc. Pacific Islands':	'up ',
    'United States':	'xxu',
    'Uruguay':	'uy ',
    'Utah':	'utu',
    'Uzbekistan':	'uz ',
    'Vanuatu':	'nn ',
    'Various places':	'vp ',
    'Vatican City':	'vc ',
    'Venezuela':	've ',
    'Venezuela, Bolivarian Republic of':	've ',
    'Vermont':	'vtu',
    'Victoria':	'vra',
    'Viet Nam':	'vm ',
    'Vietnam':	'vm ',
    'Virgin Islands (British)':	'vb ',
    'Virgin Islands of the United States':	'vi ',
    'Virgin Islands, British':	'vb ',
    'Virginia':	'vau',
    'Wake Island':	'wk ',
    'Wales':	'wlk',
    'Wallis and Futuna':	'wf ',
    'Washington (State)':	'wau',
    'West Bank of the Jordan River':	'wj ',
    'West Virginia':	'wvu',
    'Western Australia':	'wea',
    'Western Sahara':	'ss ',
    'Wisconsin':	'wiu',
    'Wyoming':	'wyu',
    'Yemen':	'ye ',
    'Yukon Territory':	'ykc',
    'Zambia':	'za ',
    'Zimbabwe':	'rh ',
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
#      Classes
# ====================

class ContribName:

    def __init__(self, i, row):
        self.name = {}
        for name_part in ['CR', 'CRT', 'CCI',
                          'ICTBN', 'ICFN', 'ICKNP', 'ICKN', 'ICNAK', 'ICKNS',
                          'ICLAN', 'ICTAN', 'ICCY', 'ICPP', 'ICAFF']:
            try: self.name[name_part] = clean(row['{}{}'.format(name_part, str(i))])
            except: self.name[name_part] = None

        try: self.role = ONIX_CONTRIBUTOR_ROLES[self.name['CR']]
        except: self.role = None
        if self.role: self.name['CRT'] = self.role
        elif self.name['CRT']:
            self.name['CRT'] = re.sub(r'\([^()]*\)|\bother\b', '', self.name['CRT'])
            self.role = self.name['CRT']

        self.surname = clean('{} {}'.format(self.name['ICKN'] or '', self.name['ICNAK'] or ''))
        self.forename = clean('{} {}'.format(self.name['ICFN'] or '', self.name['ICKNP'] or ''))

    def __str__(self):
        s = clean('{} {} {} {} {} {}'.format(self.name['ICTBN'] or '', self.name['ICFN'] or '', self.name['ICKNP'] or '',
                                             self.name['ICKN'] or '', self.name['ICNAK'] or '', self.name['ICKNS'] or ''))
        if s is None or not s: return ''
        return s

    def as_marc(self, tag_start='1'):
        if not str(self): return None
        s = '{}, {}'.format(self.surname, self.forename).strip(',').strip()
        s += ',' if any(self.name[p] for p in ['ICTBN', 'ICKNS', 'ICTAN', 'ICCY', 'CRT']) else '.'
        subfields = ['a', s]
        if self.name['ICTBN']:
            subfields.extend(['c', self.name['ICTBN'] + (',' if any(self.name[p] for p in ['ICKNS', 'ICTAN', 'ICCY', 'CRT']) else '.')])
        if self.name['ICKNS']:
            subfields.extend(['c', self.name['ICKNS'] + (',' if any(self.name[p] for p in ['ICTAN', 'ICCY', 'CRT']) else '.')])
        if self.name['ICTAN']:
            subfields.extend(['c', self.name['ICTAN'] + (',' if any(self.name[p] for p in ['ICCY', 'CRT']) else '.')])
        if self.name['ICCY']:
            subfields.extend(['d', self.name['ICCY'] + (',' if self.name['CRT'] else '.')])
        if self.name['CRT']:
            subfields.extend(['e', self.name['CRT'] + '.'])
        return Field('{}{}0'.format(tag_start, '1' if self.name['CCI'] == 'Y' else '0'),
                     ['2' if self.name['CCI'] == 'Y' else '1', ' '], subfields)


class NielsenCluster:

    def __init__(self, csv_row):
        self.row = csv_row
        try: self.isbn = Isbn(clean(self.row['ISBN13']), format='U')
        except: self.isbn = None
        self.isbns = set()
        self.related = set()
        self.alternative_formats = set()
        if self.isbn:
            self.alternative_formats.add(self.isbn)

        for letter in ['I', 'W']:
            for i in range(1, 10):
                try: related_id = clean(self.row['R{}I{}'.format(letter, str(i))])
                except: related_id = None
                try: related_id_type = clean(self.row['R{}IT{}'.format(letter, str(i))])
                except: related_id_type = None
                try: relationship = clean(self.row['R{}T{}'.format(letter, str(i))])
                except: relationship = None
                try: related_id_type_name = clean(self.row['R{}ITN{}'.format(letter, str(i))])
                except: related_id_type_name = None
                if related_id and related_id_type and relationship:
                    if related_id_type in ['02', '03', '15'] or is_isbn_13(related_id) or related_id_type_name in ['Contract_Head_ISBN', 'Release Identifier']:
                        # ISBNs
                        isbn = Isbn(related_id, format='P' if relationship == '27' else 'E' if relationship == '13' else 'U')
                        if isbn.isbn:
                            if relationship in ['06', '13', '27']:
                                self.alternative_formats.add(isbn)
                                # 06 = Alternative format
                                # 13 = Epublication based on (print product)
                                # 27 = Electronic version available as
                            try: relationship = ONIX_PRODUCT_RELATION[relationship]
                            except: relationship = 'Unknown'
                            self.related.add((isbn, relationship))
                            self.isbns.add(isbn.isbn)
                    elif related_id_type == '01':
                        # Proprietary identifiers
                        if related_id_type_name == 'Biblio Work ID': related_id_type_name = 'BiblioWorkID'
                        isbn = Isbn(related_id, format=related_id_type_name if related_id_type_name else 'U')
                        if isbn.isbn:
                            if relationship == '01':
                                self.alternative_formats.add(isbn)
                            try: relationship = ONIX_WORK_RELATION[relationship]
                            except: relationship = 'Unknown'
                            self.related.add((isbn, relationship))
                            self.isbns.add('{}:{}'.format(related_id_type_name, isbn.isbn))

    def get_alternative_formats(self):
        return self.alternative_formats
