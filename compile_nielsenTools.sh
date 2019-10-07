python setup.py install
pyinstaller bin/nielsen_isbn_analysis.py -F
pyinstaller bin/nielsen2marc_clusters.py -F
pyinstaller bin/nielsen2marc_organisations.py -F
pyinstaller bin/nielsen2marc_products.py -F
read -p "Press [Enter]"
rm -rf bin/__pycache__
mv dist/nielsen_isbn_analysis.exe nielsen_isbn_analysis.exe
mv dist/nielsen2marc_clusters.exe nielsen2marc_clusters.exe
mv dist/nielsen2marc_organisations.exe nielsen2marc_organisations.exe
mv dist/nielsen2marc_products.exe nielsen2marc_products.exe
rmdir dist
rm -rf __pycache__
rm -rf build
rm nielsen_isbn_analysis.spec
rm nielsen2marc_clusters.spec
rm nielsen2marc_organisations.spec
rm nielsen2marc_products.spec
read -p "Press [Enter]"