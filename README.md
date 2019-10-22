# nielsenTools
Tools for working with data feeds from Nielsen 

## Requirements

Requires the regex module from https://bitbucket.org/mrabarnett/mrab-regex. The built-in re module is not sufficient.

Also requires the pyperclip module (https://pypi.org/project/pyperclip/), sqlite3 and csv.

PyInstaller (https://pypi.org/project/PyInstaller/) is required to create stand-alone executable files.

## Installation

From GitHub:

    git clone https://github.com/victoriamorris/nielsenTools
    cd nielsenTools

To install as a Python package:

    python setup.py install
    
To create stand-alone executable (.exe) files for individual scripts:

    pyinstaller bin/nielsen_isbn_analysis.py -F
    pyinstaller bin/nielsen2marc_clusters.py -F
    pyinstaller bin/nielsen2marc_organisations.py -F
    pyinstaller bin/nielsen2marc_products.py -F 
    
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
      
Input files must be **tab-delimited** files; the file names should end .add, .upd, or .del.

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
        --help  Show help message and exit.

Input files must be **tab-delimited** files; the file names should end .add, .upd, or .del.

##### NOTE:

Records for products contain ORGIDs, to link them to organisations (see above). 
However, the ORGID is **not** a permanent or persistent identifier, and may change; 
therefore this number should be used as a *current* link, not a *permanent* one.

#### nielsen2marc_clusters

Converts Nielsen CSV files for **clusters** to MARC 21 (Bibliographic) format.

    Usage: nielsen2marc_clusters.exe -i <input_path> -o <output_path>

        -i    path to FOLDER containing Input files
        -o    path to FOLDER to contain Output files
    If not specified, input path will be /Input/Products
    If not specified, output path will be /Output/Products

    Options:
        --help  Show help message and exit.

Input files must be **tab-delimited** files; the file names should end .add, .upd, or .del.

#### nielsen_isbn_analysis

Various options allow for the identification of clusters of related ISBNs.

The database file **isbns.db** must be present in the folder in which the script is run.

##### Option 1: to add data from Nielsen files to the database:

    Usage: nielsen_isbn_analysis.exe -i <input_path> (-n|-o|-p)
    
        -i    path to FOLDER containing Nielsen input files
        
        -n    input files are Nielsen Cluster files
        -o    input files are Nielsen Organisation files
        -p    input files are Nielsen Product files
                        
    If not specified, input path will be /Input/Nielsen
    
##### Option 2: search for information about a list of ISBNs

    Usage: nielsen_isbn_analysis.exe -i <input_path> -s
    
        -i    path to FOLDER containing lists of ISBNs to search for.
    If not specified, input path will be /Input/Search_lists
    Input files must be text (.txt) files, with one ISBN per line.

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
* Valid? - either True or False, to indicate whether the ISBN is structurally valid.
* Related ISBNs - a semi-colon-separated list.
* Publication status.
* Availability status.
* Availability date.
* Publisher ID.
* Publisher name.
* Publisher address. 
* Publisher email. 
* Publisher URL.
* Imprint ID.
* Imprint name.
* Imprint address.
* Imprint email.
* Imprint URL.
    
##### Notes

If the format of an ISBN cannot be determined from the source data, the Google Books API may be invoked,
via the URL https://www.googleapis.com/books/v1/. 
If the option -c is specified, the user will be given the option to check ISBN formats manually, where a format conflict arises.
The user will be prompted to enter a format code for a specific ISBN, which will be copied to the clipboard to facilitate catalogue/online searching.

In all cases, information about related ISBNs will be stored/retrieved from the ISBN database named isbns.db;
it is essential that this database file is present in the folder in which the script is run.
