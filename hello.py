#!/usr/bin/python 

import sys

if len(sys.argv) > 1:
 for name in sys.argv[1:]:
  print "Hi", name

else:
  print "Hi Christopher"

