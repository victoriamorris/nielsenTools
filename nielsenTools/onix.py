#  -*- coding: utf-8 -*-

"""Information relating to ONIX data used within nielsenTools."""

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#     Constants
# ====================


ONIX_AUDIENCE_CODES = {
    '01':   'g',    # General
    '02':	'j',    # Children / Juvenile
    '03':	'd',    # Teenage / Young adult
    '04':	'f',    # Educational: Primary & Secondary
    '05':	'f',    # Tertiary & Higher Education
    '06':	'f',    # Professional & Vocational
    '07':	'f',    # ELT General
    '08':	'f',    # Adult education
    '09':	'f',    # Second language teaching
}

# List 164  Work relation
ONIX_WORK_RELATION = {
    '01':	'Manifestation of',
    '02':	'Derived from',
    '03':	'Related work is derived from this',
    '04':	'Other work in same collection',
    '05':	'Other work by same contributor',
}

# List 51	Product relation
ONIX_PRODUCT_RELATION = {
    '00':	'Unspecified',
    '01':	'Includes',
    '02':	'Is part of',
    '03':	'Replaces',
    '05':	'Replaced by',
    '06':	'Alternative format',
    '07':	'Has ancillary product',
    '08':	'Is ancillary to',
    '09':	'Is remaindered as',
    '10':	'Is remainder of',
    '11':	'Is other-language version of',
    '12':	'Publisher’s suggested alternative',
    '13':	'Epublication based on (print product)',
    '16':	'POD replacement for',
    '17':	'Replaced by POD',
    '18':	'Is special edition of',
    '19':	'Has special edition',
    '20':	'Is prebound edition of',
    '21':	'Is original of prebound edition',
    '22':	'Product by same author',
    '23':	'Similar product',
    '24':	'Is facsimile of',
    '25':	'Is original of facsimile',
    '26':	'Is license for',
    '27':	'Electronic version available as',
    '28':	'Enhanced version available as',
    '29':	'Basic version available as',
    '30':	'Product in same collection',
    '31':	'Has alternative in a different market sector',
    '32':	'Has equivalent intended for a different market',
    '33':	'Has alternative intended for different market',
    '34':	'Cites',
    '35':	'Is cited by',
    '37':	'Is signed version of',
    '38':	'Has signed version',
    '39':	'Has related student material',
    '40':	'Has related teacher material',
    '41':	'Some content shared with',
    '42':	'Is later edition of first edition',
    '43':	'Adapted from',
    '44':	'Adapted as',
}


# List 150	Product form
# ONIX product form code:   (008/23)
ONIX_PRODUCT_FORM = {
    '00':	['', 'unspecified', 'unspecified', 'unspecified'],  # Undefined
    'AA':	['', 'spoken word', 'audio', 'unspecified', 'i'],        # Audio                    ########## MUSIC ##########
    'AB':	['', 'spoken word', 'audio', 'audiocassette', 'i'],      # Audio cassette           #
    'AC':	['', 'spoken word', 'audio', 'audio disc', 'i'],         # CD-Audio                 #
    'AD':	['', 'spoken word', 'audio', 'other', 'i'],              # DAT                      #
    'AE':	['', 'spoken word', 'audio', 'audio disc', 'i'],         # Audio disc               #
    'AF':	['', 'spoken word', 'audio', 'audiotape reel', 'i'],     # Audio tape               #
    'AG':	['', 'spoken word', 'audio', 'audio disc', 'i'],         # MiniDisc                 #
    'AH':	['', 'spoken word', 'audio', 'audio disc', 'i'],         # CD-Extra                 #
    'AI':	['', 'spoken word', 'audio', 'audio disc', 'i'],         # DVD Audio                #
    'AJ':	['', 'spoken word', 'audio', 'online resource', 'i'],    # Downloadable audio file  #
    'AK':	['', 'spoken word', 'unmediated', 'other', 'i'],         # Pre-recorded digital audio player
    'AL':	['', 'spoken word', 'audio', 'computer card', 'i'],      # Pre-recorded SD card     #
    'AM':	['', 'spoken word', 'audio', 'audio disc', 'i'],         # LP                       #
    'AN':	['', 'spoken word', 'audio', 'online resource', 'i'],    # Downloadable and online audio file
    'AO':	['', 'spoken word', 'audio', 'online resource', 'i'],    # Online audio file        #
    'AZ':	['', 'spoken word', 'audio', 'other', 'i'],              # Other audio format       ########## MUSIC ##########
    'BA':	['r', 'text', 'unmediated', 'volume', 'a'],  # Book                    ########## BOOK ##########
    'BB':	['r', 'text', 'unmediated', 'volume', 'a'],  # Hardback                #
    'BC':	['r', 'text', 'unmediated', 'volume', 'a'],  # Paperback / softback    #
    'BD':	['r', 'text', 'unmediated', 'sheet', 'a'],   # Loose-leaf              #
    'BE':	['r', 'text', 'unmediated', 'volume', 'a'],  # Spiral bound            #
    'BF':	['r', 'text', 'unmediated', 'volume', 'a'],  # Pamphlet                #
    'BG':	['r', 'text', 'unmediated', 'volume', 'a'],  # Leather / fine binding  #
    'BH':	['r', 'text', 'unmediated', 'volume', 'a'],  # Board book              #
    'BI':	['r', 'text', 'unmediated', 'volume', 'a'],  # Rag book                #
    'BJ':	['r', 'text', 'unmediated', 'volume', 'a'],  # Bath book               #
    'BK':	['r', 'text', 'unmediated', 'volume', 'a'],  # Novelty book            #
    'BL':	['r', 'text', 'unmediated', 'volume', 'a'],  # Slide bound             #
    'BM':	['r', 'text', 'unmediated', 'volume', 'a'],  # Big book                #
    'BN':	['r', 'text', 'unmediated', 'volume', 'a'],  # Part-work (fascículo)   #
    'BO':	['r', 'text', 'unmediated', 'volume', 'a'],  # Fold-out book or chart  #
    'BP':	['r', 'text', 'unmediated', 'volume', 'a'],  # Foam book               #
    'BZ':	['r', 'text', 'unmediated', 'volume', 'a'],  # Other book format       ########## BOOK ##########
    'CA':	['a', 'cartographic image', 'unmediated', 'sheet', 'e'],     # Sheet map                ########## MAP ##########
    'CB':	['a', 'cartographic image', 'unmediated', 'sheet', 'e'],     # Sheet map, folded        #
    'CC':	['a', 'cartographic image', 'unmediated', 'sheet', 'e'],     # Sheet map, flat          #
    'CD':	['a', 'cartographic image', 'unmediated', 'roll', 'e'],      # Sheet map, rolled        #
    'CE':	['d', 'cartographic three-dimensional form', 'unmediated', 'object', 'e'],  # Globe     #
    'CZ':	['u', 'unspecified', 'unspecified', 'unspecified', 'e'],     # Other cartographic       ########## MAP ##########
    'DA':	['', 'computer dataset', 'computer', 'unspecified', 'm'],        # Digital (on physical carrier)     ########## COMPUTER FILE ##########
    'DB':	['', 'computer dataset', 'computer', 'computer disc', 'm'],      # CD-ROM                            #
    'DC':	['', 'computer dataset', 'computer', 'computer disc', 'm'],      # CD-I                              #
    'DE':	['', 'computer program', 'computer', 'other', 'm'],              # Game cartridge                    #
    'DF':	['', 'computer dataset', 'computer', 'computer disc', 'm'],      # Diskette                          #
    'DI':	['', 'computer dataset', 'computer', 'computer disc', 'm'],      # DVD-ROM                           #
    'DJ':	['', 'computer dataset', 'computer', 'computer card', 'm'],      # Secure Digital (SD) Memory Card   #
    'DK':	['', 'computer dataset', 'computer', 'computer card', 'm'],      # Compact Flash Memory Card         #
    'DL':	['', 'computer dataset', 'computer', 'computer card', 'm'],      # Memory Stick Memory Card          #
    'DM':	['', 'computer dataset', 'computer', 'other', 'm'],              # USB Flash Drive                   #
    'DN':	['', 'computer dataset', 'computer', 'computer disc', 'm'],      # Double-sided CD/DVD               #
    'DZ':	['', 'computer dataset', 'computer', 'other', 'm'],              # Other digital carrier             ########## COMPUTER FILE ##########
    'EA':	['', 'computer dataset', 'computer', 'unspecified', 'm'],        # Digital (delivered electronically)#
    'EB':	['', 'computer dataset', 'computer', 'online resource', 'm'],    # Digital download and online       #
    'EC':	['', 'computer dataset', 'computer', 'online resource', 'm'],    # Digital online                    #
    'ED':	['', 'computer dataset', 'computer', 'online resource', 'm'],    # Digital download                  ########## COMPUTER FILE ##########
    'FA':	['t', 'still image', 'projected', 'unspecified', 'g'],           # Film or transparency              ########## VISUAL ##########
    'FC':	['s', 'still image', 'projected', 'slide', 'g'],                 # Slides                            #
    'FD':	['t', 'still image', 'projected', 'overhead transparency', 'g'], # OHP transparencies                #
    'FE':	['f', 'still image', 'projected', 'filmstrip', 'g'],             # Filmstrip                         #
    'FF':	['f', 'still image', 'projected', 'unspecified', 'g'],           # Film                              #
    'FZ':	['t', 'still image', 'projected', 'unspecified', 'g'],           # Other film or transparency format ########## VISUAL ##########
    'LA':	['', 'computer dataset', 'computer', 'unspecified', 'm'],        # Digital product license           ########## COMPUTER FILE ##########
    'LB':	['', 'computer dataset', 'computer', 'unspecified', 'm'],        # Digital product license key       #
    'LC':	['', 'computer dataset', 'computer', 'unspecified', 'm'],        # Digital product license code      ########## COMPUTER FILE ##########
    'MA':	['a', 'text', 'microform', 'unspecified', 'a'],                  # Microform                ########## BOOK ##########
    'MB':	['b', 'text', 'microform', 'microfiche', 'a'],                   # Microfiche               #
    'MC':	['a', 'text', 'microform', 'microfilm reel', 'a'],               # Microfilm                #
    'MZ':	['a', 'text', 'microform', 'unspecified', 'a'],                  # Other microform          ########## BOOK ##########
    'PA':	['r', 'text', 'unmediated', 'unspecified', 'a'],                 # Miscellaneous print      ########## BOOK ##########
    'PB':	['r', 'text', 'unmediated', 'volume', 'a'],                      # Address book             #
    'PC':	['r', 'text', 'unmediated', 'other', 'a'],                       # Calendar                 #
    'PD':	['r', 'text', 'unmediated', 'card', 'a'],                        # Cards                    #
    'PE':	['r', 'text', 'unmediated', 'other', 'a'],                       # Copymasters              #
    'PF':	['r', 'text', 'unmediated', 'volume', 'a'],                      # Diary                    ########## BOOK ##########
    'PG':	['i', 'still image', 'unmediated', 'sheet', 'k'],                # Frieze                   ########## VISUAL ##########
    'PH':	['b', 'three-dimensional form', 'unmediated', 'object', 'o'],    # Kit                      ########## VISUAL ##########
    'PI':	['', 'notated music', 'unmediated', 'volume', 'c'],              # Sheet music              ########## MUSIC ##########
    'PJ':	['i', 'still image', 'unmediated', 'card', 'k'],                 # Postcard book or pack    ########## VISUAL ##########
    'PK':	['i', 'still image', 'unmediated', 'sheet', 'k'],                # Poster                   ########## VISUAL ##########
    'PL':	['r', 'text', 'unmediated', 'volume', 'a'],                      # Record book              ########## BOOK ##########
    'PM':	['z', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Wallet or folder         ########## VISUAL ##########
    'PN':	['i', 'still image', 'unmediated', 'sheet', 'k'],                # Pictures or photographs  #
    'PO':	['i', 'still image', 'unmediated', 'sheet', 'k'],                # Wallchart                #
    'PP':	['z', 'still image', 'unmediated', 'other', 'k'],                # Stickers                 #
    'PQ':	['z', 'still image', 'unmediated', 'other', 'k'],                # Plate (lámina)           ########## VISUAL ##########
    'PR':	['r', 'text', 'unmediated', 'volume', 'a'],                      # Notebook / blank book    ########## BOOK ##########
    'PS':	['r', 'text', 'unmediated', 'volume', 'a'],                      # Organizer                ########## BOOK ##########
    'PT':	['r', 'text', 'unmediated', 'other', 'a'],                       # Bookmark                 ########## VISUAL ##########
    'PU':	['r', 'text', 'unmediated', 'sheet', 'a'],                       # Leaflet                  ########## BOOK ##########
    'PZ':	['r', 'text', 'unmediated', 'unspecified', 'a'],                 # Other printed item       ########## BOOK ##########
    'SA':	['', 'unspecified', 'unspecified', 'unspecified'],          # Multiple-component retail product
    'SB':	['', 'unspecified', 'unspecified', 'unspecified'],          # Multiple-component retail product, boxed
    'SC':	['', 'unspecified', 'unspecified', 'unspecified'],          # Multiple-component retail product, slip-cased
    'SD':	['', 'unspecified', 'unspecified', 'unspecified'],          # Multiple-component retail product, shrink-wrapped
    'SE':	['', 'unspecified', 'unspecified', 'unspecified'],          # Multiple-component retail product, loose
    'SF':	['', 'unspecified', 'unspecified', 'unspecified'],          # Multiple-component retail product, part(s) enclosed
    'VA':	['v', 'three-dimensional moving image', 'video', 'unspecified'],    # Video                    ########## VISUAL ##########
    'VF':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # Videodisc                #
    'VI':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # DVD video                #
    'VJ':	['v', 'three-dimensional moving image', 'video', 'videocassette'],  # VHS video                #
    'VK':	['v', 'three-dimensional moving image', 'video', 'videocassette'],  # Betamax video            #
    'VL':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # VCD                      #
    'VM':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # SVCD                     #
    'VN':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # HD DVD                   #
    'VO':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # Blu-ray                  #
    'VP':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # UMD Video                #
    'VQ':	['v', 'three-dimensional moving image', 'video', 'videodisc'],      # CBHD                     #
    'VZ':	['v', 'three-dimensional moving image', 'video', 'unspecified'],    # Other video format       ########## VISUAL ##########
    'XA':	['', 'unspecified', 'unspecified', 'unspecified'],                  # Trade-only material
    'XB':	['', 'unspecified', 'unmediated', 'object', 'r'],                # Dumpbin – empty
    'XC':	['', 'unspecified', 'unmediated', 'object', 'r'],                # Dumpbin – filled
    'XD':	['', 'unspecified', 'unmediated', 'object', 'r'],                # Counterpack – empty
    'XE':	['', 'unspecified', 'unmediated', 'object', 'r'],                # Counterpack – filled
    'XF':	['i', 'still image', 'unmediated', 'sheet', 'r'],                # Poster, promotional
    'XG':	['', 'unspecified', 'unmediated', 'unspecified'],           # Shelf strip
    'XH':	['', 'unspecified', 'unmediated', 'unspecified'],           # Window piece
    'XI':	['', 'unspecified', 'unmediated', 'unspecified'],           # Streamer
    'XJ':	['', 'unspecified', 'unmediated', 'unspecified'],           # Spinner
    'XK':	['', 'unspecified', 'unmediated', 'object'],                # Large book display
    'XL':	['', 'unspecified', 'unmediated', 'unspecified'],           # Shrink-wrapped pack
    'XM':	['', 'unspecified', 'unmediated', 'unspecified'],           # Boxed pack
    'XZ':	['', 'unspecified', 'unspecified', 'unspecified'],          # Other point of sale
    'ZA':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # General merchandise
    'ZB':	['w', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Doll
    'ZC':	['w', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Soft toy
    'ZD':	['w', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Toy
    'ZE':	['g', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Game
    'ZF':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # T-shirt
    'ZG':	['', 'computer program', 'unmediated', 'object', 'm'],           # E-book reader
    'ZH':	['', 'computer program', 'unmediated', 'object', 'm'],           # Tablet computer
    'ZI':	['', 'computer program', 'unmediated', 'object', 'm'],           # Audiobook player
    'ZJ':	['w', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Jigsaw
    'ZK':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Mug
    'ZL':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Tote bag
    'ZM':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Tableware
    'ZN':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Umbrella
    'ZY':	['r', 'three-dimensional form', 'unmediated', 'object', 'r'],    # Other apparel
    'ZZ':	['r', 'three-dimensional form', 'unmediated', 'unspecified', 'r'],  # Other merchandise
}

# List 81   Product content type
# ONIX code:    ONIX value, RDA content term, RDA code, LDR/06 code
ONIX_PRODUCT_CONTENT_TYPE = {
    '10':	['Text (eye-readable)', 'text', 'txt', 'a'],
    '15':	'Extensive links between internal content',
    '14':	'Extensive links to external content',
    '16':	['Additional eye-readable text not part of main work', 'text', 'txt', 'a'],
    '41':	'Additional eye-readable links to external content',
    '17':	['Promotional text for other book product', 'text', 'txt', 'a'],
    '11':	['Musical notation', 'notated music', 'ntm', 'c'],
    '07':	['Still images / graphics', 'still image', 'sti', 'k'],
    '18':	['Photographs', 'still image', 'sti', 'k'],
    '19':	['Figures, diagrams, charts, graphs', 'still image', 'sti', 'k'],
    '20':	['Additional images / graphics not part of main work', 'still image', 'sti', 'k'],
    '12':	['Maps and/or other cartographic content', 'cartographic image', 'cri', 'e',],
    '42':	'Assessment material',
    '01':	['Audiobook', 'spoken word', 'spw', 'i'],
    '02':	['Performance – spoken word', 'spoken word', 'spw', 'i'],
    '13':	['Other speech content', 'spoken word', 'spw', 'i'],
    '03':	['Music recording', 'performed music', 'prm', 'j'],
    '04':	['Other audio', 'sounds', 'snd', 'i'],
    '21':	['Partial performance – spoken word', 'spoken word', 'spw', 'i'],
    '22':	['Additional audio content not part of main work', 'sounds', 'snd', 'i'],
    '23':	['Promotional audio for other book product', 'spoken word', 'spw', 'i'],
    '06':	['Video', 'two-dimensional moving image', 'tdi', 'g'],
    '26':	['Video recording of a reading', 'two-dimensional moving image', 'tdi', 'g'],
    '27':	['Performance – visual', 'two-dimensional moving image', 'tdi', 'g'],
    '24':	['Animated / interactive illustrations', 'two-dimensional moving image', 'tdi', 'g'],
    '25':	['Narrative animation', 'two-dimensional moving image', 'tdi', 'g'],
    '28':	['Other video', 'two-dimensional moving image', 'tdi', 'g'],
    '29':	['Partial performance – video', 'two-dimensional moving image', 'tdi', 'g'],
    '30':	['Additional video content not part of main work', 'two-dimensional moving image', 'tdi', 'g'],
    '31':	['Promotional video for other book product', 'two-dimensional moving image', 'tdi', 'g'],
    '05':	['Game / Puzzle', 'tactile three-dimensional form', 'tcf', 'r'],
    '32':	'Contest',
    '08':	['Software', 'computer program', 'cop', 'm'],
    '09':	['Data', 'computer dataset', 'cod', 'm'],
    '33':	['Data set plus software', 'computer dataset', 'cod', 'm'],
    '34':	'Blank pages or spaces',
    '35':	'Advertising content',
    '37':	'Advertising – first party',
    '36':	'Advertising – coupons',
    '38':	'Advertising – third party display',
    '39':	'Advertising – third party textual',
    '40':	'Scripting',
}


class OnixProductContentType:
    def __init__(self, onix_code, mappings):
        self.onix_code = onix_code
        if len(mappings) > 1:
            self.onix_text = mappings[0]
            self.rda_text = mappings[1]
            self.rda_code = mappings[2]
            self.leader_06 = mappings[3]
        else:
            self.onix_text = mappings
            self.rda_text = None
            self.rda_code = None
            self.leader_06 = None


for c in ONIX_PRODUCT_CONTENT_TYPE:
    ONIX_PRODUCT_CONTENT_TYPE[c] = OnixProductContentType(c, ONIX_PRODUCT_CONTENT_TYPE[c])


ONIX_CONTRIBUTOR_ROLES = {
    'A01':	'author',	        # By (author)
    'A02':	'contributor',	    # With
    'A03':	'screenwriter',	    # Screenplay by
    'A04':	'librettist',	    # Libretto by
    'A05':	'lyricist',	        # Lyrics by
    'A06':	'composer',	        # By (composer)
    'A07':	'artist',	        # By (artist)
    'A08':	'photographer',	    # By (photographer)
    'A09':	'creator',	        # Created by
    'A10':	'contributor',	    # From an idea by
    'A11':	'designer',	        # Designed by
    'A12':	'illustrator',	    # Illustrated by
    'A13':	'illustrator',	    # Photographs by
    'A14':	'writer of added text',	                        # Text by
    'A15':	'writer of preface',	                        # Preface by
    'A16':	'writer of supplementary textual content',	    # Prologue by
    'A17':	'writer of supplementary textual content',	    # Summary by
    'A18':	'writer of supplementary textual content',	    # Supplement by
    'A19':	'writer of supplementary textual content',	    # Afterword by
    'A20':	'writer of supplementary textual content',	    # Notes by
    'A21':	'writer of added commentary',	                # Commentaries by
    'A22':	'writer of supplementary textual content',	    # Epilogue by
    'A23':	'writer of supplementary textual content',	    # Foreword by
    'A24':	'writer of introduction',	                    # Introduction by
    'A25':	'writer of supplementary textual content',	    # Footnotes by
    'A26':	'contributor',	                                # Memoir by
    'A27':	'contributor',	                                # Experiments by
    'A29':	'writer of supplementary textual content',	    # Introduction and notes by
    'A30':	'contributor',	    # Software written by
    'A31':	'lyricist',	        # Book and lyrics by
    'A32':	'contributor',	    # Contributions by
    'A33':	'contributor',	    # Appendix by
    'A34':	'contributor',	    # Index by
    'A35':	'illustrator',	    # Drawings by
    'A36':	'illustrator',	    # Cover design or artwork by
    'A37':	'originator',	    # Preliminary work by
    'A38':	'originator',	    # Original author
    'A39':	'cartographer',	    # Maps by
    'A40':	'illustrator',	    # Inked or colored by
    'A41':	'illustrator',	    # Paper engineering by
    'A42':	'contributor',	    # Continued by
    'A43':	'interviewer',	    # Interviewer
    'A44':	'interviewee',	    # Interviewee
    'A45':	'writer of added text',	    # Comic script by
    'A46':	'illustrator',	    # Inker
    'A47':	'illustrator',	    # Colorist
    'A48':	'illustrator',	    # Letterer
    'A51':	'contributor',	    # Research by
    'A99':	'creator',	        # Other primary creator
    'B01':	'editor',	        # Edited by
    'B02':	'editor',	        # Revised by
    'B03':	'author',	        # Retold by
    'B04':	'abridger',	        # Abridged by
    'B05':	'author',	        # Adapted by
    'B06':	'translator',	    # Translated by
    'B07':	'author',	        # As told by
    'B08':	'translator',	    # Translated with commentary by
    'B09':	'editor',	        # Series edited by
    'B10':	'editor',	        # Edited and translated by
    'B11':	'editor',	        # Editor-in-chief
    'B12':	'editor',	        # Guest editor
    'B13':	'editor',	        # Volume editor
    'B14':	'editor',	        # Editorial board member
    'B15':	'editor',	        # Editorial coordination by
    'B16':	'editor',	        # Managing editor
    'B17':	'editor',	        # Founded by
    'B18':	'editor',	        # Prepared for publication by
    'B19':	'editor',	        # Associate editor
    'B20':	'editor',	        # Consultant editor
    'B21':	'editor',	        # General editor
    'B22':	'author',	        # Dramatized by
    'B23':	'editor',	        # General rapporteur
    'B24':	'editor',	        # Literary editor
    'B25':	'arranger of music',	    # Arranged by (music)
    'B26':	'editor',	                # Technical editor
    'B27':	'degree supervisor',	    # Thesis advisor or supervisor
    'B28':	'degree supervisor',	    # Thesis examiner
    'B29':	'editor',	        # Scientific editor
    'B30':	'contributor',	    # Historical advisor
    'B31':	'editor',	        # Original editor
    'B99':	'adaptor',	        # Other adaptation by
    'C01':	'editor',	        # Compiled by
    'C02':	'compiler',	        # Selected by
    'C03':	'compiler',	        # Non-text material selected by
    'C04':	'curator',	        # Curated by
    'C99':	'editor',	        # Other compilation by
    'D01':	'producer',	        # Producer
    'D02':	'director',	        # Director
    'D03':	'conductor',	    # Conductor
    'D04':	'choreographer',	# Choreographer
    'D99':	'director',	        # Other direction by
    'E01':	'actor',	        # Actor
    'E02':	'dancer',	        # Dancer
    'E03':	'narrator',	        # Narrator
    'E04':	'commentator',	    # Commentator
    'E05':	'singer',	        # Vocal soloist
    'E06':	'instrumentalist',  # Instrumental soloist
    'E07':	'narrator',	        # Read by
    'E08':	'performer',	    # Performed by (orchestra, band, ensemble)
    'E09':	'speaker',	        # Speaker
    'E10':	'narrator',	        # Presenter
    'E99':	'performer',	    # Performed by
    'F01':	'director of photography',	        # Filmed/photographed by
    'F02':	'editor of moving image work',	    # Editor (film or video)
    'F99':	'recordist',	    # Other recording by
    'Z01':	'contributor',	    # Assisted by
    'Z02':	'dedicatee',	    # Honored/dedicated to
    # Z98 Various roles
    # Z99 Other
}
