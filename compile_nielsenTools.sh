#!/bin/bash
#
function pause(){
   read -p "$*"
}
python setup.py install
python setup.py py2exe
mv dist/nielsen2marc_products.exe nielsen2marc_products.exe
mv dist/nielsen2marc_organisations.exe nielsen2marc_organisations.exe
mv dist/nielsen_isbn_analysis.exe nielsen_isbn_analysis.exe
mv dist/nielsen2marc_clusters.exe nielsen2marc_clusters.exe
cp nielsen2marc_products.exe ../nielsen2marc_products.exe
cp nielsen2marc_organisations.exe ../nielsen2marc_organisations.exe
cp nielsen_isbn_analysis.exe ../nielsen_isbn_analysis.exe
cp nielsen2marc_clusters.exe ../nielsen2marc_clusters.exe
rmdir dist
rm bin/__pycache__/nielsen2marc_products.cpython-34.pyc
rm bin/__pycache__/nielsen2marc_organisations.cpython-34.pyc
rm bin/__pycache__/nielsen_isbn_analysis.cpython-34.pyc
rm bin/__pycache__/nielsen2marc_clusters.cpython-34.pyc
rmdir bin/__pycache__
rm -rf build
pause 'Press [Enter] key to continue...'