#  -*- coding: utf-8 -*-

"""Functions used within nielsenTools."""

# Import required modules
import datetime
import locale
import random
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
    if conversion_type == 'Products':
        print('    --database  Add ISBN information to database')
    exit_prompt()


def date_time(message=None):
    if message:
        print('\n\n{} ...'.format(message))
        print('----------------------------------------')
    print(str(datetime.datetime.now()))


def date_time_exit():
    date_time(message='All processing complete')
    sys.exit()


def message(s) -> str:
    """Function to convert OPTIONS description to present tense"""
    if s == 'Exit program': return 'Shutting down'
    return s.replace('Parse', 'Parsing').replace('eXport', 'Exporting').replace('Search', 'Searching').replace('build',
                                                                                                               'Building').replace(
        'Index', 'index')


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
    return "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def rreplace(string, old, new, occurrence=1):
    return new.join(string.rsplit(old, occurrence))


def format_date(d):
    if not d: return None
    date = re.sub(r'[^0-9]', '', d)
    if date and len(date) >= 4: return date[:4]
    return d


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
        if case == 'lower':
            string = rx.sub(lambda m: m.group(1).lower(), string)
        elif case == 'upper':
            string = rx.sub(lambda m: m.group(1).upper(), string)
        elif case == 'caps':
            string = rx.sub(lambda m: m.group(1).capitalise(), string)
        return clean(string)
    except:
        return string


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
    string = re.sub(r', unspecified\s*$', '',
                    re.sub(r'\s*\b(b[&/]?w|black-and-white)\b\s*', ' black and white ', string))
    if string in ['0', 'total illustrations: 0']: return None
    if string == 'total illustrations: 1': return '1 illustration'
    string = re.sub(r'^total illustrations: ([0-9]+)$', r'\1 illustrations', string)
    string = clean(string)
    return string


# ====================
#    Functions for
#      having fun
# ====================

FACTS = [
    'A beaver\'s teeth never stop growing. It needs to chew on tree trunks and branches to keep them from getting too long.',
    'A chameleon\'s tongue can be as long as its body.',
    'A chameleons tongue can be as long as its body.',
    'A cheetah can go from zero to 60 miles per hour in three seconds.',
    'A cockroach will live nine days without its head, before it starves to death.',
    'A crocodile can\'t move its tongue and cannot chew. Its digestive juices are so strong that it can digest a steel nail.',
    'A crocodile can\'t stick its tongue out.',
    'A desert locust swarm can be 460 square miles in size and can consume 423 million pounds of plants in a single day.',
    'A dog was the first animal to up in space.',
    'A duck\'s quack doesn\'t echo, and no one knows why.',
    'A giraffe can clean its ears with its 21-inch tongue!',
    'A group of cats is called a clowder',
    'A group of tigers is known as an \'ambush\' or \'streak\'.',
    'A hungry tiger can eat as much as 60 pounds of meat in one meal.',
    'A male emperor moth can smell a female emperor moth up to 7 miles away.',
    'A mole can dig a tunnel 300 feet (91.44 meters) long in just one night.',
    'A Pineapple is actually a bunch of small berries fused together into a single mass',
    'A pregnant goldfish is called a twit.',
    'A rat can last longer without water than a camel.',
    'A shark can detect one part of blood in 100 million parts of water.',
    'A sheep, a duck and a rooster were the first animals to fly in a hot air balloon.',
    'A shrimp\'s heart is in its head.',
    'A snowy owl may eat up to 1,600 lemmings a year - three to five every day.',
    'A wolf can eat up to 20 pounds of meat in one sitting.',
    'African elephants have the longest pregnancy of any mammal - nearly two years long.',
    'All clownfish are born male, and will only change sex to become a dominant female.',
    'Alligators have been around for 150 million years.',
    'Almost all pufferfish contain a toxin called tetrodoxin, which is up to 1,200 times more lethal to humans than cyanide. Despite this, some pufferfish meat - called fugu - is a delicacy in Japan, where it must be prepared by a licensed chef.',
    'Also, southern elephant seals can reach depths of nearly a mile into the ocean and are able to hold their breath for two hours.',
    'An adult panda typically spends 12 hours a day eating and must consume 28 pounds of bamboo daily to fulfill its dietary needs.',
    'An ostrich is the fastest bird and can run up to 70 km/h.',
    'An ostrich\'s eye is bigger that its brain.',
    'Ancient Greek dentists used the venom from stingrays as an anesthetic.',
    'Anteaters eat 35,000 ants a day.',
    'Ants can accidentally misinterpret the chemical trails left by other ants and start walking in circles. If too many members of the colony join in, it can kill the whole colony in what is sometimes known as the \'Death Spiral\'',
    'Arabian camels rarely sweat, but are capable of drinking 30 gallons of water in less than 15 minutes.',
    'Armadillos are the only animal besides humans that can get leprosy.',
    'Around half of tiger cubs don\'t live beyond two years of age.',
    'As well as being a famous Looney Tunes character, the Tasmanian Devil is a real animal that is only found in the wild in Tasmania, Australia. ',
    'At lengths of 40 feet long - the size of a school bus - the whale shark is the largest fish in the sea, but feeds on tiny microscopic plankton.',
    'Baby giraffes can stand within half an hour of birth.',
    'Blue whales are the loudest mammals, producing low-frequency "pulses" that can be heard from more than 500 miles away.',
    'Butterflies taste with their feet.',
    'Cats\' urine glows under a black light.',
    'Cats use their whiskers to check whether a space is too small for them to fit through or not.',
    'Certain frogs can be frozen solid, then thawed, and survive.',
    'Chameleons don\'t change colours to match their surroundings, but to show emotions and specific reactions.',
    'Cows have four different stomachs.',
    'Denmark has twice as many pigs as there are people.',
    'Despite the white, fluffy appearance of Polar Bears\' fur, they actually have black skin.',
    'Dogs have a remarkable sense of smell, they are capable of differentiating odors in concentrations nearly 100 million times lower than humans can.',
    'Dogs have four toes on their hind feet, and five on their front feet.',
    'Dolphins have a super sense called electroreception. They can sense electrical impulses given off by all living things. Dolphins use this to search for fish hiding in the mud.',
    'Dominant male elephant seals collect a harem of 40 to 50 females during breeding season.',
    'During those two months, the mother will travel up to 50 miles each way to hunt, and will return to their newly-hatched chick with a belly full of food to regurgitate.',
    'Elephants are the only mammals that can\'t jump.',
    'Elephants can smell water from several miles away.',
    'Elephants use the skin folds on their backs to crush mosquitoes.',
    'Emus and kangaroos cannot walk backwards, and are on the Australian coat of arms for that reason.',
    'Even when a snake has its eyes closed, it can still see through its eyelids.',
    'Fleas can jump distances 100 times their body length.',
    'Flying fish reach speeds of 37 miles per hour to breach the water and glide up to 655 feet - more than the length of two football fields!',
    'Galapagos tortoises sleep for 16 hours a day and can go a year without food or water.',
    'Giant Arctic jellyfish have tentacles that can reach over 36 metres in length.',
    'Goats and sheep have rectangular pupils which allow them to see nearly 360 degrees around themselves.',
    'Great white sharks can detect a drop of blood in 25 gallons of water and can even sense tiny amounts of blood from three miles away.',
    'Grizzly bears have been clocked running at up to 30 miles per hour.',
    'Hippos secrete a red oily substance from their skin that acts as sunblock and a moisturizer.',
    'Horses and cows sleep while standing up.',
    'Houseflies hum in the key of F.',
    'Humans are the only primates that don\'t have pigment in the palms of their hands.',
    'Hummingbirds are so agile and have such good control that they can fly backwards.',
    'If all the females in a group of clownfish die a male will change its gender in order to keep its group alive.',
    'If NASA sent birds into space they would soon die; they need gravity to swallow.',
    'In 1386, a pig in France was executed by public hanging for murder of a child.',
    'In total there is said to be around 400 million dogs in the world.',
    'Insects such as bees, mosquitoes and cicadas make noise by rapidly moving their wings.',
    'Instead of bones, sharks have a skeleton made from cartilage.',
    'It\'s possible to lead a cow upstairs ... but not downstairs.',
    'Koalas are actually not bears - they\'re marsupials - and they sleep for 18 hours a day.',
    'Less than 10% of hunts end successfully for tigers',
    'Locusts have leg muscles that are about 1000 times more powerful than an equal weight of human muscle.',
    'Male emperor penguins will stand without eating for up to two months in the Antarctic elements while the female goes to feed.',
    'Male tarantulas also get the hell away from females after mating, because the lady tarantula often will eat the dude!',
    'Mammals are the only creatures that have flaps around their ears.',
    'Many hamsters only blink one eye at a time.',
    'Mosquitoes can be annoying insects but only the female mosquito actually bites humans.',
    'Most lipstick contains fish scales.',
    'Never get a camel angry, for he or she will spit at you.',
    'No two tigers have the exact same stripes.',
    'Once a giant clam picks a spot to live on a reef, it does not move for the rest of its life.',
    'Orcas kill sharks by torpedoing up into to shark\'s stomach from underneath, causing the shark to explode.',
    'Ostriches can cover 16 feet in a single stride, and are capable of reaching speeds of 43 miles per hour.',
    'Oysters can change gender multiple times during their life.',
    'Palm trees are part of the grass family.',
    'Peregrine falcons dive-bomb their prey and can reach dive speeds of up to 200 miles per hour.',
    'Polar bears are left handed.',
    'Polar bears have black skin under their white fur to better absorb the rays of the sun.',
    'Porcupines float in water.',
    'Queen bees also regulate the activity of a hive by releasing a chemical into the air that guides other bees\' behavior.',
    'Rare white tigers carry a gene that is only present in around 1 in every 10000 tigers.',
    'Rats and horses can\'t vomit.',
    'Rats breed so quickly that in just 18 months, 2 rats could have created over 1 million relatives.',
    'Rats can chew through wood, cement, brick, lead, cinder blocks and aluminum.',
    'Ruby-throated hummingbirds beat their wings at a rate of 53 times per second, and can fly backwards and upside down in addition to hovering.',
    'Sailfish are the fastest fish in the ocean and can leap out of the water at speeds of up to 68 miles per hour.',
    'Scientists have frozen scorpions overnight, and when thawed, the arthropod walked away unscathed.',
    'Scorpions are incredibly resilient, and are able to live on a single insect per year. ',
    'Sea cucumbers will spit out some of their internal organs via their anus as a defence mechanism.',
    'Seahorses are also the only animal on earth where the male bears the unborn young.',
    'Seahorses are monogamous and mate for life.',
    'Sharks lay the biggest eggs in the world.',
    'Snails can sleep for 3 years without eating',
    'Snow leopards can leap up to 50 feet in one jump.',
    'Some moths never eat anything as adults because they don\'t have mouths. They must live on the energy they stored as caterpillars.',
    'Some species of earthworm can have as many as 10 hearts.',
    'Starfish don\'t have brains.',
    'Subspecies of the tiger include the Sumatran Tiger, Siberian Tiger, Bengal Tiger, South China Tiger, Malayan Tiger and Indochinese Tiger.',
    'Tarantulas secrete digestive enzymes so they can liquefy their pray and drink up their remains. Yum!',
    'Technically, only males are peacocks - females are peahens, and choose their mate based on the size, quality, and colour of the male\'s feather trains.',
    'The 2-inch-long golden poison dart frog has enough venom to kill 10 adult men.',
    'The average housefly only lives for 2 or 3 weeks.',
    'The bloodhound is the only animal whose evidence is admissible in court.',
    'The blue whale can produce the loudest sound of any animal. At 188 decibels, the noise can be detected over 800 kilometres away.',
    'The blue whale\'s tongue weighs as much as an adult elephant.',
    'The Chinese soft-shelled turtle urinates through its mouth',
    'The coelacanth, a bizarre-looking fish, was thought to have gone extinct with the dinosaurs 65 million years ago, only to be rediscovered in 1938.',
    'The crocodile\'s tongue is unmovable, as it is attached to the roof of its mouth.',
    'The electric eel can deliver jolts of electricity up to 600 volts, enough to knock a fully grown horse off its feet.',
    'The fingerprints of koala bears are virtually indistinguishable from those of humans, so much so that they could be confused at a crime scene.',
    'The flying snake can glide in the air for distances up to 330 feet and can even make turns in the air.',
    'The golden eagle can dive at speeds of up to 150 miles per hour and has been known to attack fully grown deer.',
    'The horn of a rhinoceros is made from compacted hair rather than bone or another substance.',
    'The howler monkey is the loudest land animal. Its call can be heard from three miles away.',
    'The kick of an ostrich is used as a weapon and is capable of killing a lion - and yes, humans too.',
    'The king cobra has enough venom to kill an elephant.',
    'The king cobra is also the largest venomous snake at up to 18 feet long, and can rear itself up to six feet off the ground - enough to tower over many humans.',
    'The largest bald eagle nest on record was 20 feet high and weighed two tons.',
    'The largest giant squid on record was 59 feet long, and the creature\'s eyes were as big as beach balls.',
    'The leg muscle of a locust are about 1000 times more powerful than an equal weight of a humans.',
    'The length of an elephant is the same as the tongue of a blue whale.',
    'The life of a housefly is only 14 days.',
    'The lifespan of 75 percent of wild birds is 6 months.',
    'The longest-living Galapagos tortoise lived to be 152.',
    'The name "jaguar" comes from a Native American word meaning "he who kills with one leap."',
    'The narwhal has two teeth, one of which can grow into a nearly-nine-foot-long tusk in males.',
    'The oldest breed of a dog known to mankind is the \'Saluki\'.',
    'The penguin is the only bird who can swim, but not fly.',
    'The reptiles have 6,000 species crawling in their habitats; and more are discovered each year.',
    'The sailfish can swim at the speed of 109 km/h, making it the fastest swimmer.',
    'The saliva of a Komodo dragon harvests more than 50 types of bacteria. Animals bitten by the lizard typically die within 24 hours from blood poisoning - if they aren\'t eaten first.',
    'The Sea Horse is the slowest fish, drifting at approximately 0.016 km/h.',
    'The small car on the road is probably the size of the heart of a blue whale.',
    'The snapping shrimp is the loudest known living creature. It has specialized claws that shoot jets of water at up to 62 miles per hour and leaving a trail of bubbles that explode at 200 decibels - enough to stun and even kill its prey.',
    'The sperm whale eats about a ton of fish and squid every day.',
    'The spring peeper lets most of its body freeze during winter hibernation and still thaw out and survive.',
    'The Tasmanian Devil is the largest carnivorous marsupial in the world.',
    'The three-foot-long tusks of a walrus, which grow throughout their lives, are actually canine teeth.',
    'The three-toed sloth sleeps up to 20 hours a day and is so sedentary algae grows on its back.',
    'The tiger shark is nicknamed "the wastebasket of the sea" and refuse like old license plates and tires has been found in its stomach.',
    'The venomous Portuguese-man-of-war is actually an animal made up of four separate organisms, known as a siphonophore.',
    'The water boatman can make a 105-decibel noise by rubbing its penis against its belly.',
    'The world has approximately one billion cattle, of which about 200 million belong to India.',
    'There are crabs that are the size of a pea. There are known as \'Pea Crabs\'.',
    'There are more tigers held privately as pets than there are in the wild.',
    'There are over 70,000 types of spiders spinning their webs in the world.',
    'There are presently over a million animal species upon planet earth.',
    'Tiger cubs leave their mother when they are around 2 years of age.',
    'Tigers are good swimmers and can swim up to 6 kilometres.',
    'Tigers can easily jump over 5 metres in length.',
    'Tigers can reach a length of up to 3.3 metres (11 feet) and weigh as much as 300 kilograms (660 pounds).',
    'Tigers have been known to reach speeds up to 65 kph (40 mph).',
    'Tigers that breed with lions give birth to hybrids known as tigons and ligers.',
    'Tigers usually hunt alone at night time.',
    'To escape the grip of a crocodile\'s jaws, push your thumbs into its eyeballs - it will let you go instantly.',
    'Unlike humans, sheep have four stomachs, each one helps them digest the food they eat.',
    'Vampire bats feed entirely on blood, and a 100-bat colony drinks the blood of 25 cows every year.',
    'Want to known the appetite of a South American Giant Anteater? Well it eats over 30,000 ants, per day.',
    'When a queen bee dies, worker bees create a new queen by feeding a female bee "royal jelly" that makes her fertile.',
    'When anacondas mate, several competing males can form a ball around a female in a ritual that can last up to a month.',
    'When tarantulas moult, they can replace internal organs including stomach lining, female genitalia, and even lost limbs.',
    'You do not need cotton buds to clean a giraffe ears. It can do so with its own 50cm-tongue.',
    'The heart of a shrimp is located in its head.',
    'A snail can sleep for three years.',
    'Slugs have four noses.',
    'Elephants are the only animal that can\'t jump.',
    'A rhinoceros\' horn is made of hair.',
    'It is possible to hypnotize a frog by placing it on its back and gently stroking its stomach.',
    'It takes a sloth two weeks to digest its food.',
    'Nearly three percent of the ice in Antarctic glaciers is penguin urine.',
    'A cow gives nearly 200,000 glasses of milk in a lifetime.',
    'Bats always turn left when leaving a cave.',
    'Giraffes have no vocal chords.',
    'Kangaroos can\'t fart.',
    'An ostrich\'s eye is bigger than its brain.',
    'Around 50 percent of orangutans have fractured bones, due to falling out of trees on a regular basis.',
    'Frogs cannot vomit. If one absolutely has to, then it will vomit its entire stomach.',
    'The heaviest animal ever recorded was a blue whale weighing 190 tons.',
    'Pigeons in Japan were trained to discriminate between Picasso and Monet paintings in 1995.',
    'Causing a horse, donkey or pony to lose its balance and fall over is illegal in Phoenix, Arizona.',
    'In 2008, a snake in Australia that swallowed four golf balls thinking they were chicken eggs was saved by emergency surgery',
    'Around 10 million times as many sharks are killed by humans as humans killed by sharks.',
    'St Francis, the patron saint of animals, was born in 1181 or 1182 and died on the night of October 3, 1226. He was renowned for his love of animals. In many places it is still usual for churches to bless animals on October 4.',
    'Cows have best friends.',
    'Millions of trees grow every year thanks to squirrels forgetting where they put their nuts.',
    'Female insects of the genus Neotrogla have a penis and can have sex for up to 70 hours.',
    'There\'s a mammal in Australia that has sex until it disintegrates',
    'During sex, flies create a buzz that can attract predatory bats.',
    'Female komodo dragons don\'t need a male to reproduce.',
    'Bald eagles court each other in the sky. They lock talons while freefalling, then soar upward before hitting the ground',
    'Female black widow spiders sometimes kill and eat their male counterparts after mating',
    'Squirrels can\'t burp or vomit',
    'Less time separates the existence of humans and the tyrannosaurus rex than the T-rex and the stegosaurus',
    'There\'s a place on Earth where seagulls prey on right whales',
    'A group of crows is called a murder.',
    'A group of otters is called a romp.',
    'A group of parrots is known as a pandemonium.',
    'A group of porcupines is called a prickle.',
    'A group of rhinoceroses is called a crash.',
    'Animals with smaller bodies and faster metabolism see in slow motion.',
    'Azara\'s owl monkeys are more monogamous than humans.',
    'Baby dolphins have spines on the sides of their tongue. The spines zip up to make a straw so that they can drink the mother\'s milk without getting salt water in it.',
    'Baby porcupines have soft quills at birth, which harden within a few days.',
    'Barn owls are normally monogamous, but about 25 percent of mated pairs "divorce."',
    'Because beavers\' teeth never stop growing, they must constantly gnaw on objects to keep them at a manageable length. Their teeth would eventually grow into their brain if they didn\'t maintain them.',
    'Cats "headbutt" people because they make them feel safe, or they trust them.',
    'Dogs will sneeze to tell other dogs that they\'re playing, so when they\'re playing rough it doesn\'t turn into a fight.',
    'Dogs\' sense of smell is about 100,000 times stronger than humans\', but they have just one-sixth our number of taste buds.',
    'Dolphins can stay active for 15 days or more by sleeping with only one half of their brain at a time.',
    'Each of a tarsier\'s eyeballs is as big as its brain.',
    'Elephants can smell water up to 3 miles away. They are also one of the three mammals that undergo menopause, the other two being humpback whales and human females.',
    'Every year, the Peruvian town of Churin holds a Guinea Pig Festival, including an elaborate costume competition.',
    'Houseflies don\'t allow their short lifespans (14 days) to hinder their musical abilities. They always hum in the key of F.',
    'Infant Pygmy Marmosets babble to develop their language skills, similarly to the way human babies babble.',
    'Kangaroos use their tails for balance, so if you lift a kangaroo\'s tail off the ground, it can\'t hop.',
    'Koala bears almost exclusively eat only eucalyptus leaves and nothing else.',
    'Lobsters pee out of their faces.',
    'Male gentoo and Adelie penguins "propose" to females by giving them a pebble.',
    'Ostriches can run faster than horses, and the male ostriches can roar like lions.',
    'Owls don\'t have eyeballs. They have eye tubes.',
    'Some lobster species can live to be 50 years or older.',
    'Some turtles can breathe through their butts.',
    'The Chinese soft-shelled turtle can expel urea, the main waste product in urine, out of its mouth.',
    'The extinct colossus penguin stood as tall as LeBron James.',
    'The Grizzly bear\'s name comes from the word "grizzled" which means \'streaked with gray hair\'.',
    'Tigers not only have stripes on their fur, they also have them on their skin. No two tigers ever have the same stripes.',
    'To escape the grip of a crocodile\'s jaw, push your thumb into its eyeball. It will let you go instantly.',
    'Wombat feces are cube-shaped to stop them from rolling away.',
    'You can tell a turtle\'s gender by the noise it makes. Males grunt and females hiss.',
    'You can use a blue whale\'s wax earplug to work out its life history.',
]

ANIMALS = {
    'cow':
        '     ^__^\n'
        '     (oo)\\_______\n'
        '     (__)\\       )\\/\\\n'
        '         ||----w |\n'
        '         ||     ||',
    'giraffe':
        '    (\\-/)\n'
        '   (:O O:)\n'
        '    \\   /o\\\\\n'
        '     | |\\o \\\\\n'
        '     (:) \\ o\\\\\n'
        '       \\o \\--\\\\\n'
        '        ( o O\n'
        '          (  O\n',
    'owl':
        '     ,___,\n'
        '     [O.o]\n'
        '     /)__)\n'
        '     -”–”-',
    'rabbit':
        '     (\\__/)\n'
        '     (>’.\'<)\n'
        '      /   \\\n'
        '     (“)_(“)\n',
    'pig':
        '       (\\____/)\n'
        '       / @__@ \\\n'
        '      (  (oo)  )\n'   
        '       `-.~~.-\'\n'
        '        /    \\\n'
        '      @/      \\_\n'          
        '     (/ /    \\ \\)\n'
        '      WW\'----\'WW',
    'butterfly':
        '                                  _ " _\n'
        '   _ " _                         (_\\|/_)\n'
        '  (_\\|/_)  _ " _         _ " _    (/|\\)\n'
        '   (/|\\)  (_\\|/_) " _   (_\\|/_)\n'
        '           (/|\\)_\\|/_)   (/|\\)\n'
        '                (/|\\)',
    'bird':
        '          .--.\n'
        '          /  6_6\n'
        '          \\  (__\\\n'
        '         //   \\\\\n'
        '        ((     ))\n'
        '  =======""===""===============\n'
        '           |||\n'
        '           |||\n'
        '           \'|\'',
    'elephant':
        '          / \\__/ \\_____\n'
        '         /  /  \\  \\    `\\\n'
        '         )  \\\'\'/  (     |\\\n'
        '         `\\__)/__/\'_\\  / `\n'
        '            //_|_|~|_|_|\n'
        '            ^""\'"\' ""\'"\'',
    'fish':
        '    o   o'
        '                  /^^^^^7\n'
        '    \'  \'     ,oO))))))))Oo,\n'
        '           ,\'))))))))))))))), /{\n'
        '      \'  ,\'o  ))))))))))))))))={\n'
        '         >    ))))))))))))))))={\n'
        '         `,   ))))))\\ \\)))))))={\n'
        '           \',))))))))\\/)))))\' \\{\n'
        '             \'*O))))))))O*\'',
}


def magician():
    animal = random.choice(list(ANIMALS.values()))
    print('\n\n' +animal)
    fact = random.choice(FACTS)
    print('\n\nAccording to the internet ...\n{}\n'.format(fact))
    return
