#!/usr/bin/python 

import sys

datei = open(sys.argv[0],"rU")
for zeile in datei:
 print(zeile, end=''),

datei.close()
sys.exit(0)