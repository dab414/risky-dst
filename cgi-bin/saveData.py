#!/usr/local/bin/python

import cgi, os, sys
sys.stderr = sys.stdout

try:
  fs = cgi.FieldStorage()

  if not os.path.exists('../turk/data/dissertation/' + fs['experiment'].value):
    os.makedirs('../turk/data/dissertation/' + fs['experiment'].value)


  session = fs['sessionCode'].value

  f = open('../turk/data/dissertation/' + fs['experiment'].value + '/' + fs['curId'].value + '_' + session + '.txt','w')

  f.write(fs['currentData'].value)

  f.close()

  print "Status: 200 OK"
  print "Content-type: text/plain"
  print
  print fs["curId"].value + " saved."

except:
  ## tell jquery something went wrong
  print "Status: 400 Bad Request"
  print "Content-type: text/plain"
  print
  print "Error"