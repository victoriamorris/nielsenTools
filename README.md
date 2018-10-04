# nielsenTools
Tools for working with data feeds from Nielsen 

## Requirements

Requires the regex module from https://bitbucket.org/mrabarnett/mrab-regex. The built-in re module is not sufficient.
Also required the pyperclip module (https://pypi.org/project/pyperclip/).

## Installation

To install as a Python package:

    python setup.py install
    
To create stand-alone executable (.exe) files for individual scripts:

    python setup.py py2exe 
    
Executable files will be created in the folder \dist, and should be copied to an executable path.

Both of the above commands can be carried out by running the shell script:

    compile_nielsenTools.sh

## Usage

### Running scripts

The following scripts can be run from anywhere, once the package is installed:

#### nielsen2marc_organisations

Converts Nielsen records for **organisations** (publishers, imprints and distributors) to MARC Authority format.
    
    Usage: nielsen2marc_organisations.exe -i <input_path> -o <output_path>
    
        -i    path to FOLDER containing Input files
        -o    path to FOLDER to contain Output files
    If not specified, input path will be /Input/Organisations
    If not specified, output path will be /Output/Organisations

    Options:
        --help    Show help message and exit.
      
Input files must be **tagged** files; the file names should begin 31_ and end .upd.

##### Example tagged record:

    $
    *a
    ORGID 198352
    ORGN Lickle Publishing, Inc
    ORGAL1 568 Island Drive
    ORGAT Palm Beach
    ORGACOS FL
    ORGAPC 33480
    ORGCTRY United States of America
    ORGPREF 09650308 1890674
    ORGTEL1 +1  561 881 0450
    ORGEMAIL1 wlickle@licklepub.com
    ORGFAX1 +1   561 881 0818
    ORGURL1 www.licklepub.com

##### NOTE:

The ORGID field can be used to link organisations to product records. 
However, the ORGID is **not** a permanent or persistent identifier, and may change; 
therefore this number should be used as a *current* link, not a *permanent* one, for identifying an organisation.  

#### nielsen2marc_products

Converts Nielsen records for **products** (books, etc.) to MARC Bibliographic format.
    
    Usage: nielsen2marc_products.exe -i <input_path> -o <output_path>
    
        -i    path to FOLDER containing Input files
        -o    path to FOLDER to contain Output files
    If not specified, input path will be /Input/Products
    If not specified, output path will be /Output/Products
    
    Options:
        --help    Show help message and exit.

Input files must be **tab-delimited** files; the file names should end .add, .upd, or .del.

As records are parsed, information about related ISBNs and Nielsen Work IDs will be added to the ISBN database in \Database\isbns.db;
it is essential that this database file is present, in the location specified.

##### NOTE:

Records for products contain ORGIDs, to link them to organisations (see above). 
However, the ORGID is **not** a permanent or persistent identifier, and may change; 
therefore this number should be used as a *current* link, not a *permanent* one.

#### nielsen_isbn_analysis

Various options allow for the identification of clusters of related ISBNs.

##### Option 1: to add ISBNs from Nielsen data feeds to the database:

    Usage: nielsen_isbn_analysis.exe -n <input_path>
    
        -n    path to FOLDER containing Nielsen Input files
    If no options are specified, -n is assumed, with input folder Input\ISBNs
    
##### Option 2: to add ISBNs from MARC (.lex) files to the database:

    Usage: nielsen_isbn_analysis.exe -m <input_path>
    
        -m    path to FOLDER containing MARC Input files

##### Option 3: search for information about a list of ISBNs

    Usage: nielsen_isbn_analysis.exe -s <search_list>
    
        -s    path to FILE containing list of ISBNs to search for.
        This must be a text (.txt) file, with one ISBN per line.

Search results will be written to a file with the name of the form <search_list>_out.txt, in the same folder as the input file.
The output file will include the following columns:
* Input ISBN
* 13-digit ISBN - the ISBN converted to 13-digit form, where possible
* Prefix - the publisher's prefix
* Format - a code denoting the format of the publication to which the ISBN belongs:
    * U - unknown
    * P - print book
    * E - e-book
    * A - audio-book
    * C - collective
    * O - other
    * X - contradiction 
* Valid? - either True or False, to indicate whether the ISBN is strucurally valid.
* Nielsen Work ID - Nielsen ID for the work of which the publication is a manifestation, if known.
* Related ISBNs - a semi-colon-separated list.
    
##### Notes

If the format of an ISBN cannot be determined from the source data, the Google Books API may be invoked,
via the URL https://www.googleapis.com/books/v1/. 
If the option -c is specified, the user will be given the option to check ISBN formats manually, where a format conflict arises.
The user will be prompted to enter a format code for a specific ISBN, which will be copied to the clipboard to facilitate catalogue/online searching.

In all cases, information about related ISBNs and Nielsen Work IDs will be stored/retrieved from the ISBN database in \Database\isbns.db;
it is essential that this database file is present, in the location specified.
