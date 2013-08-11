#!/usr/bin/python

import sys
import socket

if len(sys.argv) > 1:
 host = sys.argv[1]
 port = int(sys.argv[2])

else:
 print "usage: ", sys.argv[0], "host port"
 sys.exit(0)


sock = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host,port))


datei = open(sys.argv[0],"rU")

for zeile in datei:
 write = sock.send(zeile) 

datei.close()

sys.exit(0)
