#! /usr/bin/evn/ python
import os 
for variable, valor in os.environ.iteritems(): 
    print "%s: %s" % (variable, valor)