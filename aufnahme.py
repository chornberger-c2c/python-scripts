#!/usr/bin/python 


import sys

datei = open(sys.argv[0],"rU")

for zeile in datei:
 print zeile,

datei.close()
 
sys.exit(0)



