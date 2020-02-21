#  -*- coding: utf-8 -*-

"""Tools for working with Nielsen data used within nielsenTools."""

# Import required modules
import math
from nielsenTools.marc_data import *
from nielsenTools.onix import *
from nielsenTools.functions import *

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#   Global variables
# ====================


STATUSES = ['add', 'upd', 'del']


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
    'Antigua And Barbuda':	'aq ',
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
    'Bosnia And Herzegovina':	'bn ',
    'Bosnia-Herzegovina':	'bn ',
    'Bosnia and Herzegowina':	'bn ',
    'Bosnia And Herzegowina':	'bn ',
    'Bosnia-Herzegowina':	'bn ',
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
    'Myanmar':	'br ',
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
    'Croatia (Local Name: Hrvatska)': 'ci ',
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
    'Falkland Islands (Malvinas)':	'fk ',
    'Malvinas':	'fk ',
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
    'Iran  (Islamic Republic Of)': 'ir ',
    'Iran  (Islamic Republic of)': 'ir ',
    'Iran, Republic of': 'ir ',
    'Iran,  Republic Of': 'ir ',
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
    'Macao':        'cc ',
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
    'Netherlands Antilles':	'na ',
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
    'Palestine':	'xx ',
    'Palestine, State of ':	'xx ',
    'Palestine, State Of ':	'xx ',
    'Palistine, State of ':	'xx ',
    'Palistine, State Of ':	'xx ',
    'Palestine, State of':	'xx ',
    'Palestine, State Of':	'xx ',
    'Palistine, State of':	'xx ',
    'Palistine, State Of':	'xx ',
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
    'St Helena':	'xj ',
    'St. Helena':	'xj ',
    'Saint Kitts-Nevis':	'xd ',
    'Saint Kitts and Nevis':	'xd ',
    'Saint Kitts And Nevis':	'xd ',
    'St Kitts-Nevis':	'xd ',
    'St Kitts and Nevis':	'xd ',
    'St Kitts And Nevis':	'xd ',
    'St. Kitts-Nevis': 'xd ',
    'St. Kitts and Nevis': 'xd ',
    'St. Kitts And Nevis': 'xd ',
    'Saint Lucia':	'xk ',
    'St Lucia': 'xk ',
    'St. Lucia': 'xk ',
    'Saint Pierre and Miquelon':	'xl ',
    'Saint Pierre And Miquelon': 'xl ',
    'St Pierre and Miquelon':	'xl ',
    'St Pierre And Miquelon': 'xl ',
    'St. Pierre and Miquelon': 'xl ',
    'St. Pierre And Miquelon': 'xl ',
    'Saint Vincent and the Grenadines':	'xm ',
    'St Vincent and the Grenadines': 'xm ',
    'St. Vincent and the Grenadines': 'xm ',
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
    'Serbia And Montenegro': 'rb ',
    'Serbia':	'rb ',
    'Seychelles':	'se ',
    'Sierra Leone':	'sl ',
    'Singapore':	'si ',
    'Sint Maarten':	'sn ',
    'Slovakia':	'xo ',
    'Slovakia (Slovak Republic)': 'xo ',
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
    'Trinidad And Tobago':	'tr ',
    'Tunisia':	'ti ',
    'Turkey':	'tu ',
    'Turkmenistan':	'tk ',
    'Turks and Caicos Islands':	'tc ',
    'Turks And Caicos Islands':	'tc ',
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
    'Holy See (Vatican City State)':	'vc ',
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
    'Yugoslavia':	'yu ',
    'Yukon Territory':	'ykc',
    'Zambia':	'za ',
    'Zimbabwe':	'rh ',
}


DISTRIBUTION_AREAS = {
    'UK': ['United Kingdom', 'GBP', 'xxk'],
    'US': ['United States', 'USD', 'xxu'],
    'AUS': ['Australia', 'AUD', 'at'],
    'NZ': ['New Zealand', 'NZD', 'nz'],
    'SA': ['South Africa', 'ZAR', 'sa'],
    'EUR': ['Europe', 'EUR'],
    'IN': ['India', 'INR', 'ii'],
    'CAN': ['Canada', 'CAD', 'xxc'],
    'IRL':  ['Ireland', 'EUR', 'ie'],
    'HK':  ['Honk Kong', 'HKD', 'cc'],
    'SING': ['Singapore', 'SGD', 'si'],
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


ORG_FIELDS = {
    'ORGID',    # Unique Organisation Number
    'ORGN',     # Full name
    'ORGAL1',   # Line of address
    'ORGAL2',
    'ORGAL3',
    'ORGAL4',
    'ORGAT',    # Town
    'ORGACOS',  # County or State
    'ORGAPC',   # Post Code
    'ORGCTRY',  # Country
    'ORGPA',    # Member of Publisher Association –‘Y’es or ‘N’o
    'ORGCP',    # ‘Y' indicates that the Publisher has 'Ceased Publishing'
    'ORGGA',    # ‘Y' indicates that the Organisation is no longer at the stated address - but NBD do not have any forwarding information
    'ORGCGD',   # The date the 'flag' was set
    'ORGCGN',   # Any additional information about the cessation or move.
    'ORGVAT',   # Organisation VAT number
    'ORGGIRO',  # Organisation Giro number
    'ORGEDI',   # Organisation EDI number
    'ORGPREF',  # Publisher Prefix list
    'ORGREFN',  # Organisation now part of…
    'ORGPREVN', # Previous organisations now incorporated in the current one
    'ORGWAS',   # Org name has changed to…current record
    'AUSAORGSN',    # Australia
    'CANAORGSN',    # Canada
    'EURAORGSN',    # Europe
    'HKAORGSN',     # Hong Kong
    'UKAORGSN',     # United Kingdom
    'IRLAORGSN',    # Ireland
    'NZAORGSN',     # New Zealand
    'SAAORGSN',     # South Africa
    'SINGAORGSN',   # Singapore
    'USAORGSN',     # USA
    'WWWAORGSN',    # Internet
    'OTHERAORGSN',  # Other
    'INAORGSN',     # India
}


ORG_FIELDS_REPEATABLE = {
    'ORGTEL',   # Telephone numbers for the organisation
    'ORGEMAIL', # Email addresses
    'ORGFAX',   # Fax numbers
    'ORGMOB',   # Mobile Numbers
    'ORGTELX',  # Telex Details
    'ORGURL',   # URL Details
}


ORG_FIELDS_MULTIVALUED = {
    'ORGREFN',  # Organisation now part of…
    'ORGPREVN', # Previous organisations now incorporated in the current one
    'ORGWAS',   # Org name has changed to…current record
    'AUSAORGSN',    # Australia
    'CANAORGSN',    # Canada
    'EURAORGSN',    # Europe
    'HKAORGSN',     # Hong Kong
    'UKAORGSN',     # United Kingdom
    'IRLAORGSN',    # Ireland
    'NZAORGSN',     # New Zealand
    'SAAORGSN',     # South Africa
    'SINGAORGSN',   # Singapore
    'USAORGSN',     # USA
    'WWWAORGSN',    # Internet
    'OTHERAORGSN',  # Other
    'INAORGSN',     # India

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
        if self.forename:
            self.forename = re.sub(r'([A-Z]\.)([A-Z])', r'\1 \2', self.forename)

    def __str__(self):
        s = clean('{} {} {} {} {} {}'.format(self.name['ICTBN'] or '', self.name['ICFN'] or '', self.name['ICKNP'] or '',
                                             self.name['ICKN'] or '', self.name['ICNAK'] or '', self.name['ICKNS'] or ''))
        if s is None or not s: return ''
        return s

    def as_marc(self, tag_start='1'):
        if not str(self): return None
        s = re.sub(r'\b([A-Z])$', r'\1.', '{}, {}'.format(self.surname or '', self.forename or '').strip().strip(',').strip())
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

        for letter in ['I', 'P', 'W']:
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
        # print(str(len(self.alternative_formats)))
        return self.alternative_formats

    def get_related(self):
        union = self.alternative_formats
        union.add(self.isbn)
        return union


class NielsenTSVOrganisations:

    def __init__(self, csv_row, status='c'):
        self.row = csv_row
        self.status = status

        self.values = {}
        for v in ORG_FIELDS:
            try: self.values[v] = clean(self.row[v])
            except: self.values[v] = None
        for v in ORG_FIELDS_REPEATABLE:
            self.values[v] = set()
            for i in range(1, 5):
                try: val =  clean(self.row['{}{}'.format(v, str(i))])
                except: val = None
                if val: self.values[v].add(val)
        for v in ORG_FIELDS_MULTIVALUED:
            if self.values[v]:
                self.values[v] = set([clean(val) for val in self.values[v].split(';') if clean(val)])
            else: self.values[v] = set()

    def sql_values(self):
        if not self.values['ORGID']: return None
        org_address = ', '.join(v for v in [self.values['ORGAL1'], self.values['ORGAL2'], self.values['ORGAL3'],
                                            self.values['ORGAL4'], self.values['ORGAT'], self.values['ORGACOS'],
                                            self.values['ORGCTRY'], self.values['ORGAPC']] if v)
        org_email = ';'.join(self.values['ORGEMAIL']) or None
        org_url = ';'.join(self.values['ORGURL']) or None
        return self.values['ORGID'], self.values['ORGN'], org_address, org_email, org_url

    def marc(self):

        record = Record(leader='     {}z  a22     o  4500'.format(self.status))

        # 001 - Control Number (NR)
        if self.values['ORGID']:
            record.add_field(Field(tag='001', data=self.values['ORGID'] or '[NO ORGANISATION IDENTIFIER]'))

        # 003 - Control Number Identifier (NR)
        record.add_field(Field(tag='003', data='UK-WkNB'))

        # 005 - Date and Time of Latest Transaction (NR)
        record.add_field(Field(tag='005', data='{}.0'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))

        # 008 - Fixed-Length Data Elements (NR)

        # 00-05 - Date entered on file
        data = datetime.datetime.now().strftime('%y%m%d')
        # 06 - Direct or indirect geographic subdivision
        data += 'n'
        # 07 - Romanization scheme
        data += 'n'
        # 08 - Language of catalog
        data += 'e'
        # 09 - Kind of record
        data += 'b'
        # 10 - Descriptive cataloging rules
        data += 'n'
        # 11 - Subject heading system/thesaurus
        data += 'n'
        # 12 - Type of series
        data += 'n'
        # 13 - Numbered or unnumbered series
        data += 'n'
        # 14 - Heading use-main or added entry
        data += 'b'
        # 15 - Heading use-subject added entry
        data += 'b'
        # 16 - Heading use-series added entry
        data += 'b'
        # 17 - Type of subject subdivision
        data += 'n'
        # 18-27 - Undefined character positions
        data += '          '
        # 28 - Type of government agency
        data += ' '
        # 29 - Reference evaluation
        data += 'b'
        # 30 - Undefined character position
        data += ' '
        # 31 - Record update in process
        data += '|'
        # 32 - Undifferentiated personal name
        data += '|'
        # 33 - Level of establishment
        data += 'n'
        # 34-37 - Undefined character positions
        data += '    '
        # 38 - Modified record
        data += '|'
        # 39 - Cataloging source
        data += ' '
        record.add_field(Field(tag='008', data=data))

        # 024 - Other Standard Identifier (R)
        if self.values['ORGPREF']:
            for v in sorted(set(re.sub(r'[^0-9X ]', '', self.values['ORGPREF'].upper()).split(' '))):
                record.add_field(Field('024', ['7', ' '], ['a', re.sub(r'^978', '', v), '2', 'isbnre']))

        # 035 - System Control Number (R)
        if self.values['ORGID']:
            record.add_field(Field('035', [' ', ' '], ['a', '(UK-WkNB){}'.format(self.values['ORGID'])]))

        # 040 - Cataloging Source (NR)
        record.add_field(Field('040', [' ', ' '], ['a', 'UK-WkNB', 'b', 'eng', 'c', 'Uk']))

        # 075 - Type of Entity (R)
        record.add_field(Field('075', [' ', ' '], ['a', 'Publisher']))

        # 110 - Heading - Corporate Name (NR)
        if self.values['ORGN']:
            record.add_field(Field('110', ['2', ' '], ['a', self.values['ORGN']]))

        # 368 - Other Attributes of Person or Corporate Body (R)
        subfields = ['a', 'Publisher']
        if self.values['ORGCP'] == 'Y' and self.values['ORGCGD']:
            subfields.extend(['t', self.values['ORGCGD']])
        record.add_field(Field('368', [' ', ' '], subfields))

        # 370 - Associated Place (R)
        subfields = []
        if self.values['ORGCTRY']:
            subfields.extend(['c', self.values['ORGCTRY']])
        if self.values['ORGAT']:
            subfields.extend(['e', self.values['ORGAT']])
        if subfields:
            record.add_field(Field('370', [' ', ' '], subfields))

        # 371 - Address (R)
        subfields = []
        for i in range(1, 4):
            if self.values['ORGAL{}'.format(str(i))]:
                subfields.extend(['a', self.values['ORGAL{}'.format(str(i))]])
        if self.values['ORGAT']:
            subfields.extend(['b', self.values['ORGAT']])
        if self.values['ORGACOS']:
            subfields.extend(['c', self.values['ORGACOS']])
        if self.values['ORGCTRY']:
            subfields.extend(['d', self.values['ORGCTRY']])
        if self.values['ORGAPC']:
            subfields.extend(['e', self.values['ORGAPC']])
        for v in self.values['ORGEMAIL']:
            subfields.extend(['m', v])
        if self.values['ORGGA'] == 'Y' and self.values['ORGCGD']:
            subfields.extend(['t', self.values['ORGCGD']])
            subfields.extend(['z', 'Organisation not at this address since {}.'.format(self.values['ORGCGD'])])
            if self.values['ORGCGN']:
                subfields.extend(['z', self.values['ORGCGN']])
        if subfields:
            record.add_field(Field('371', [' ', ' '], subfields))

        # 372 - Field of Activity (R)
        subfields = ['a', 'Publishing']
        if self.values['ORGCP'] == 'Y' and self.values['ORGCGD']:
            subfields.extend(['t', self.values['ORGCGD']])
        record.add_field(Field('372', [' ', ' '], subfields))

        # 410 - See From Tracing-Corporate Name (R)
        for v in self.values['ORGPREVN']:
            record.add_field(Field('410', ['2', ' '], ['w', 'i', 'i', 'Organisation subsumes' 'a', v]))
        for v in self.values['ORGWAS']:
            record.add_field(Field('410', ['2', ' '], ['w', 'a', 'a', v]))

        # 510 - See Also From Tracing-Corporate Name (R)
        for v in self.values['ORGREFN']:
            record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Organisation now part of' 'a', v]))
        for c in DISTRIBUTION_AREAS:
            for v in self.values['{}AORGSN'.format(c)]:
                record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Distributor in {}'.format(DISTRIBUTION_AREAS[c][0]), 'a', v]))
        for v in self.values['OTHERAORGSN']:
            record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Other distributor', 'a', v]))
        for v in self.values['WWWAORGSN']:
            record.add_field(Field('510', ['2', ' '], ['w', 'i', 'i', 'Internet distributor', 'a', v]))

        # 678 - Biographical or Historical Data(R)
        if self.values['ORGCP'] == 'Y':
            record.add_field(Field('678', [' ', ' '], ['a', 'Publisher has ceased publishing']))
        if self.values['ORGGA'] == 'Y':
            record.add_field(Field('678', [' ', ' '], ['a', 'Organisation is no longer at the stated address']))
        if self.values['ORGCGN']:
            record.add_field(Field('678', ['1', ' '], ['a', self.values['ORGCGN']]))
        if self.values['ORGPA'] == 'Y':
            record.add_field(Field('678', [' ', ' '], ['a', 'Member of Publisher Association']))
        for c in ['ORGVAT', 'ORGGIRO', 'ORGEDI']:
            if self.values[c]:
                record.add_field(Field('678', [' ', ' '], ['a', '{} number: {}'.format(c.replace('ORG', ''), self.values[c])]))
        for c in ['ORGTEL', 'ORGFAX', 'ORGMOB', 'ORGTELX']:
            for v in self.values[c]:
                record.add_field(Field('678', [' ', ' '],
                                       ['a', '{} number: {}'.format('Telephone' if c == 'ORGTEL' else 'Fax' if c == 'ORGFAX' else 'Mobile' if c == 'ORGMOB' else 'Telex', v)]))

        # 856 - Electronic Location and Access (R)
        for v in self.values['ORGURL']:
            record.add_field(Field('856', ['4', ' '], ['u', v]))

        return record


class NielsenTSVProducts:

    def __init__(self, csv_row, status):
        self.row = csv_row
        self.status = status
        self.UK = False
        self.multimedia, self.ebook, self.audio = False, False, False

        self.values = {}
        for v in ['CBMCCODE', 'CIS', 'COP', 'CY', 'FICGH', 'IA', 'ILL', 'IMPID', 'ISBN13', 'KEYWORDS', 'PFC', 'PFCT',
                  'PPTCT', 'PRODCT', 'PSF', 'PUBID', 'PUBPD', 'RA', 'REISD', 'RSS', 'USGCT', 'GBPCCPRC', 'GBPCCPRRRP']:
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

    def sql_values(self):
        if not self.values['ISBN13']: return None
        return self.values['ISBN13'], self.values['IMPID'], self.values['PUBID'], self.row['PUBSC'], \
               self.row['UKNBDPAC'], self.row['UKNBDEAD']

    def marc(self):

        # Leader (NR)
        try: p6 = ONIX_PRODUCT_CONTENT_TYPE_MAP[clean(self.row['PCTC1'])].leader_06
        except:
            try: p6 = ONIX_PRODUCT_FORM[self.values['PFC']][4]
            except: p6 = 'a'
        if p6 == 'a': self.material_type = 'BK'
        leader = '     {}{}m a22     2  4500'.format(self.status, p6)

        record = Record(leader=leader)

        # 001 - Control Number
        record.add_field(Field(tag='001', data=self.values['ISBN13']))

        # 003 - Control Number Identifier (NR)
        record.add_field(Field(tag='003', data='Uk'))

        # 005 - Date and Time of Latest Transaction (NR)
        record.add_field(Field(tag='005', data='{}.0'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))

        # 007 - Physical Description Fixed Field-General Information (R)
        # Field 007 depends on the material type
        try: data = ONIX_PRODUCT_FORM[self.values['PFC']][5]
        except: data = None
        if data: record.add_field(Field(tag='007', data=data))

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
            test_string_2 = ''
            test_string_2 += 'a' if 'autobiography' in test_string else ''
            test_string_2 += 'b' if 'biography' in test_string else ''
            test_string_2 += 'd' if '|drama' in test_string else ''
            test_string_2 += 'e' if ('|essays' in test_string or '/ essays' in test_string) else ''
            test_string_2 += 'k' if 'comedy' in test_string else ''
            test_string_2 += 'm' if ('|memoir' in test_string or '/ memoir' in test_string) else ''
            test_string_2 += 'o' if ('folk tale' in test_string or 'folklore' in test_string or 'fairy tale' in test_string) else ''
            test_string_2 += 'p' if '|poetry' in test_string else ''
            test_string_2 += 'f' if ('|fiction' in test_string or ' fiction' in test_string) else ''
            test_string_2 += '||'
            data += test_string_2[:2]
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
            if self.values['ILL']:
                data += (''.join(ILLUSTRATIONS[x] for x in ILLUSTRATIONS if x in self.values['ILL'].lower()).strip() + '    ')[:4]
            else: data += '    '
            # 22 - Target audience
            # NAC*  Nielsen BookData Audience level: Code
            # OAC*  ONIX Audience level: Code
            data += self.values['NAC']
            # 23 - Form of item
            # PFC   Product Form: Code
            try: data += (ONIX_PRODUCT_FORM[self.values['PFC']][0] + '|')[:1]
            except: data += '|'
            # 24-27 - Nature of contents
            # PFCT      Product Form :Text Description
            # PCTCT*    Product Content: Text Description
            test_string = self.values['PFCT'] or ''
            test_string += '|' + (self.values['ILL'] or '')
            try: test_string += '|' + '|'.join(self.row['PCTCT{}'.format(i)] for i in range(1, 10))
            except: pass
            data += (''.join(RE_NATURE_OF_CONTENTS[x] for x in RE_NATURE_OF_CONTENTS if re.search(x, test_string)).strip() + '||||')[:4]
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
            for s in ['PFC', 'PFCT']:
                if self.values[s]: test_string += '|' + self.values[s].lower()
            test_string = test_string.lower()
            data += 'd' if '|drama' in test_string \
                else 'e' if ('|essays' in test_string or '/ essays' in test_string) \
                else 'i' if '/ letters' in test_string \
                else 'j' if ('|short stories' in test_string or '/ short stories' in test_string) \
                else 'm' if 'mixed media' in test_string \
                else 'p' if '|poetry' in test_string \
                else '1' if any(s in test_string for s in ['|fiction', ' fiction', 'narrative theme']) \
                else '0' if any(s in test_string for s in ['nonfiction', 'non-fiction', '|reference', '/ general', ' general issues', 'history & criticism', 'historical & comparative', 'foreign language study']) \
                else '|'
                # Ony include 'general' in non-fiction line if it comes after fiction
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
                    if self.values['GBPCCPRC'] == 'GBP' and self.values['GBPCCPRRRP'] \
                            and re.match(r'[0-9]+\.[0-9][0-9]', self.values['GBPCCPRRRP']):
                        subfields.extend(['c', '£{}'.format(self.values['GBPCCPRRRP'].lstrip('0'))])
                record.add_field(Field('020', [' ', ' '], subfields))
                w = isbn13_convert(v)
                if w:
                    subfields_2 = ['a' if c == 'ISBN13' else 'z', w]
                    subfields_2.extend(subfields[2:])
                    record.add_field(Field('020', [' ', ' '], subfields_2))

        # 024 - Other Standard Identifier (R)
        for c in ['EAN', 'ISMN', 'DOI']:
            try: v = self.row[c].strip()
            except: continue
            if v == '' or not v: continue
            test = set([s for f in record.get_fields('020') for s in f.get_subfields('a')])
            if v in test: continue
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
        record.add_field(Field('040', [' ', ' '], ['a', 'UK-WkNB', 'b', 'eng', 'c', 'UK-WkNB', 'd', 'Uk']))

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
        if len(languages) + len(translations) > 1 or len(translations) > 0 \
                or (len(languages) == 1 and 'eng' not in languages):
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
        if len(others) > 0: resp += ' ; ' + ' ; '.join(others)

        if resp and resp != '': resp = clean(resp)
        if resp and resp != '': resp += '.'

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
                d = '[distributor] ' + ' :|[distributor] '.join(d)
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
            # Try to round up and convert to cm
            try: HMM = str(math.ceil(int(HMM) / 10)) + ' cm'
            except: HMM += ' mm'
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
            try: content_types.add((ONIX_PRODUCT_CONTENT_TYPE_MAP[self.row['PCTC{}'.format(str(i))]]).rda_text)
            except: pass
        for v in content_types:
            if v:
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

                if c == 'UK' and CCPRRRP:
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
        # EMBD      Embargo Date
        # PUBSC     ONIX Publishing Status - Code
        # PUBST     ONIX Publishing Status – Text Description
        # MOPD      Date the system was informed that the record is no longer available
        # PUBPD     Date of Publication: as supplied by Publisher or approved source
        # UKNBDLPD  Date of Publication: as supplied by Publisher or approved source
        try: EMBD = clean(re.sub(r'[^0-9]', '', self.row['EMBD']))
        except: EMBD = None
        try: PUBSC = clean(self.row['PUBSC'])
        except: PUBSC = None
        try: PUBST = clean(self.row['PUBST'])
        except: PUBST = None
        try: MOPD = clean(self.row['MOPD'])
        except: MOPD = None
        subfields = []
        try: PUBPD = re.sub(r'[^0-9]', '', clean(self.row['PUBPD']))
        except:
            try: PUBPD = re.sub(r'[^0-9]', '', clean(self.row['UKLPUBD']))
            except:
                try: PUBPD = re.sub(r'[^0-9]', '', clean(self.row['UKNBDLPD']))
                except: PUBPD = None
        if PUBPD and len(PUBPD) >= 4:
            subfields.extend(['b', (PUBPD + '--------')[:8]])
        if PUBSC:
            if MOPD: PUBSC += ' ' + MOPD
            subfields.extend(['c', PUBSC])
        if EMBD: subfields.extend(['d', EMBD])
        if PUBST: subfields.extend(['e', PUBST])
        if PUBSC: subfields.extend(['2', 'onixpubst'])
        if subfields: record.add_field(Field('366', [' ', ' '], subfields))

        for c in DISTRIBUTION_AREAS:
            # xxxNBDEAD     Availability Date
            # xxxNBDPAC     ONIX Product Availability – Code
            try: NBDEAD = clean(re.sub(r'[^0-9]', '', self.row['{}NBDEAD'.format(c)]))
            except: NBDEAD = None
            try: NBDPAC = clean(self.row['{}NBDPAC'.format(c)])
            except: NBDPAC = None
            try: NBDPAT = clean(self.row['{}NBDPAT'.format(c)])
            except: NBDPAT = None
            if NBDEAD:
                if c == 'UK': self.UK = True
                subfields = ['b', NBDEAD]
                if NBDPAC: subfields.extend(['c', NBDPAC])
                if NBDPAT: subfields.extend(['e', NBDPAT])
                subfields.extend(['j', c])
                if c != 'EUR': subfields.extend(['k', DISTRIBUTION_AREAS[c][2]])
                if NBDPAC: subfields.extend(['2', 'onixas'])
                record.add_field(Field('366', [' ', ' '], subfields))

        for i in range(1, 10):
            try: NBDAA = clean(self.row['OTHERNBDAA{}'.format(str(i))])
            except: NBDAA = None
            try: NBDEAD = clean(re.sub(r'[^0-9]', '', self.row['OTHERNBDEAD{}'.format(str(i))]))
            except: NBDEAD = None
            try: NBDPAC = clean(self.row['OTHERNBDPAC{}'.format(str(i))])
            except: NBDPAC = None
            try: NBDPAT = clean(self.row['OTHERNBDPAT{}'.format(str(i))])
            except: NBDPAT = None
            if NBDAA and NBDEAD:
                subfields = ['b', NBDEAD]
                if NBDPAC: subfields.extend(['c', NBDPAC])
                if NBDPAT: subfields.extend(['e', NBDPAT])
                subfields.extend(['j', NBDAA])
                if NBDPAC: subfields.extend(['2', 'onixas'])
                record.add_field(Field('366', [' ', ' '], subfields))

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
        translations = set()
        for i in range(1, 5):
            try: l = clean(self.row['TFT{}'.format(str(i))])
            except: l = None
            if l: translations.add(l)
        TF = ', '.join(translations)
        try: TS = clean(self.row['TS'])
        except: TS = None
        if LS or TF or TS:
            for l in LANGUAGE_REPLACEMENTS:
                if LS: LS = LS.replace(l, LANGUAGE_REPLACEMENTS[l])
                if TF: TF = TF.replace(l, LANGUAGE_REPLACEMENTS[l])
                if TS: TS = TS.replace(l, LANGUAGE_REPLACEMENTS[l])
            text = 'In {}{}'.format(rreplace(LS, ', ', ' and '), '; ' if TF or TS else '.') if LS else ''
            if TS: text += '{}ranslated from {}.'.format('t' if LS else 'T', rreplace(TS, ', ', ' and '))
            elif TF: text += '{}ranslated from {}.'.format('t' if LS else 'T', rreplace(TF, ', ', ' and '))
            record.add_field(Field('546', [' ', ' '], ['a', text]))

        # 586 - Awards Note (R)
        # PSF   Structured Prize details for all Prizes combined
        if self.values['PSF']: record.add_field(Field('586', [' ', ' '], ['a', '{}.'.format(self.values['PSF'])]))

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

        if self.material_type:
            record.add_field(Field('FMT', [' ', ' '], ['a', self.material_type]))

        record.add_field(Field('SRC', [' ', ' '], ['a', 'Record converted from Nielsen TSV data to MARC21 by Collection Metadata.']))

        return record


# ====================
#     Function for
#    file handling
# ====================


def new_files(FILES, WRITERS, conversion_type, output_path, status, file_count, today, text_output=False):
    if file_count == 0:
        for f in ('int', 'uk', 'dup', 'text'):
            FILES[f] = {}
            WRITERS[f] = {}
    else:
        for f in ('int', 'uk', 'text'):
            try: FILES[f][status].close()
            except: pass
    file_count += 1
    FILES['int'][status] = open(os.path.join(output_path, '{n:03d}_{c}_{s}_{t}.lex'.format(n=file_count, c=conversion_type, s=status, t=today)), mode='wb')
    if conversion_type == 'product':
        FILES['uk'][status] = open(os.path.join(output_path, 'UK', '{n:03d}_{c}_{s}_{t}_UK.lex'.format(n=file_count, c=conversion_type, s=status, t=today)), mode='wb')
    if text_output:
        FILES['text'][status] = open(os.path.join(output_path, '{n:03d}_{c}_{s}_{t}.txt'.format(n=file_count, c=conversion_type, s=status, t=today)), mode='w', encoding='utf-8', errors='replace')
    if file_count == 1:
        FILES['dup'][status] = open(os.path.join(output_path, '_duplicates_{}_{}_{}.txt'.format(conversion_type, status, today)), mode='w', encoding='utf-8', errors='replace')
    WRITERS['int'][status] = MARCWriter(FILES['int'][status])
    if conversion_type == 'product':
        WRITERS['uk'][status] = MARCWriter(FILES['uk'][status])
    return FILES, WRITERS, file_count