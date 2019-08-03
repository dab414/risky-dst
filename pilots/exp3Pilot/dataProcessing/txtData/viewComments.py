#!/home/dave/anaconda2/bin/python

import sys

args = sys.argv[1:]

if not args:
	print 'Usage: file [files . . . ]'
	sys.exit(1)


for file in args:
	d = eval(open(file, 'r').read())
	print d['curId']
	print d['comments']
	print '\n'


