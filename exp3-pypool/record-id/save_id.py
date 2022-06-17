#!/bin/python


import cgi, os, sys
sys.stderr = sys.stdout

try:
  fs = cgi.FieldStorage()

  path = '../dissertation/publish/experiments/production/scenarios/check-id/code_list.txt'
  
  if fs['data'].value:
    if not os.path.exists(path):
      f = open(path,'w')
      f.write(fs['data'].value)
      f.close()
    else:
      existing_ids = []
      f = open(path,'r')
      for line in f:
        existing_ids.append(line.strip())
      f.close()
      existing_ids.append(fs['data'].value)
      f = open(path, 'w')
      for line in existing_ids:
        f.write(line + '\n')
      f.close()



  

  print("Status: 200 OK")
  print("Content-type: text/plain")
  print()


except Exception as e:
  ## tell jquery something went wrong
  print("Status: 400 Bad Request")
  print("Content-type: text/plain")
  print()
  print(str(e))