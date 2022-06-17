#!/home/dave/anaconda2/bin/python

import ast
import csv
import sys
import pandas as pd
import numpy as np
import re
import os

def catchPartialData(args, fTypes):
  '''
  takes as input all file names
  returns assignmentIds that completed one or two fTypes but not three
  '''
  
  d = {}
  ids = []

  ## for each file name
  for arg in args:
    ## take out only the assignmentId and extension (ie, fType)
    try:
      l = re.search(r'^.*\/([\w]*)\.txt', arg).group(1).split('_')
    except:
      print(arg)
      sys.exit(1)

    id_string = l[0] + '_' + l[1]
    phase = l[2]

    ## if the assignment id isn't already in the dict
    if id_string not in d.keys():
      ## add it in as a list
      d[id_string] = [phase]
    else:
      ## add it on to the existing list
      d[id_string] += [phase]

  partialData = []

  for key in d:
    ## if an assignment id doesnt have the length of phase types (plus init)
    if len(d[key]) < len(fTypes):
      ## add it to partialData
      partialData.append(key)

  return partialData


def exclude_partial_data(args, partialData, proc):
  '''
  takes all file names
  returns a list of (full) file names for only those files that are not in partial data
  '''

  relArgs = []

  args = [x for x in args if proc in x]

  for arg in args:
    file_name = re.search(r'^.*\/([\w]*)\.txt', arg).group(1)
    id_string = file_name.split('_')[0] + '_' + file_name.split('_')[1]
    if id_string not in partialData:
      relArgs.append(arg)

  return relArgs



def summarize_data(args):
  '''
  takes as input all file names (each containing a subject's data)
  passes each one to a separate function to get summarized
  returns a list of lists, where each nested list is a trial
  '''
  ## run a different procedure for each portion of the experiment
  fTypes = ['pracCued','dst', 'demo', 'rapidFire']
  out = {}

  ## look for subjects that started but didn't complete all phases of the experiment
  partialData = catchPartialData(args, fTypes)

  for proc in fTypes:
    ## grab only the data we're interested in (from same phases of the experiment)
    
    ## very ugly, but it works
    ## for each x in arg, reduce it down to only the assignmentId, and make sure it isn't partial data
    
    relArgs = exclude_partial_data(args, partialData, proc)

    if relArgs:
      ## extract the headers from the first file to use for the whole dataset
      data = ast.literal_eval(open(relArgs[0],'r').read())
      headers = compute_headers(data)

      final_data = [headers]

      ## cut out inits
      relArgs = [x for x in relArgs if 'init' not in x]
      ## pass each subject to the summarize_subject function
      for subject in relArgs:
        ## this function returns a list of lists for each subject where each core list is a trial
        final_data += summarize_subject(subject)
      
      out[proc] = final_data

  return out

def compute_headers(data):
  ## make the headers equal to the first layer of keys in the data
  headers = list(data.keys())
  
  ## if it's rvts data
  if 'blockStruct' in data.keys():
    ## add on top of the existing headers all the keys from the block level and the trial level
    headers += list(data['blockStruct'][0].keys()) + list(data['blockStruct'][0]['trialStruct'][0].keys())
  ## it's it's cued data
  elif 'trialStruct' in data.keys():
    ## only add in the trial level headers
    headers += list(data['trialStruct'][0].keys())

  ## remove all the nested headers from the var names
  headers = [x for x in headers if x not in ['trialStruct', 'blockStruct']]

  return headers
  

def summarize_subject(subjectString):
  '''
  Take as input data from one subject in nested dictionary format.
  Returns a list of lists, where each nested list is one trial (or row)
  '''
  e = ast.literal_eval(open(subjectString, 'r').read())
  
  ## grab the top level data
  subjectLevel = [e[x] for x in e if x not in ['trialStruct', 'blockStruct']]

  
  ## fix userAgent
  #subjectLevel = [x.replace(',', '') if not isinstance(x, int) and ',' in x else x for x in subjectLevel]


  trials = []
  
  if 'blockStruct' in e.keys():
    for block in e['blockStruct']:
        for trial in block['trialStruct']:
            trials.append(subjectLevel + [block[x] for x in block if x not in 'trialStruct'] + [x for x in trial.values()])
              
  elif 'trialStruct' in e.keys():
    for trial in e['trialStruct']:
        trials.append(subjectLevel + list(trial.values()))
          
  else:
    trials.append(subjectLevel)
  
  return trials

def main():
  '''
  Takes as input one or more subject data files in JSON form
  json with either: [_cuedPrac, _twoChoice, _threeChoice, _demo] extensions, representing different portions of the experiment
  returns four csv datasets for all four phases

  !!NOTE:
    libreoffice automatically brings in as delimited by commas AND semicolons.. which messes up the user agent
  '''
  args = sys.argv[1:]

  ## if there are no files in a directory, '*.txt' gets brought in as a file name
  [args.remove(h) for h in args if '*.txt' in h]

  if not args:
    print('usage: file [file ...]')
    sys.exit(1)

  ## final_data is dict where keys are phase types and values are the aggregated data
  final_data = summarize_data(args)

  for entry in final_data:

    try:
      df = pd.DataFrame(final_data[entry][1:], columns = final_data[entry][0])
    except:
      print(final_data[entry][0])
      print('\n\n')
      print(pd.DataFrame(final_data[entry][1:]).head())
    
    if not os.path.exists('/home/dave/Dropbox (Lehigh University)/Research/By Project/Dissertation/experiments/analysis/exp3-pypool/data/'):
      os.mkdir('/home/dave/Dropbox (Lehigh University)/Research/By Project/Dissertation/experiments/analysis/exp3-pypool/data/')
    
    df.to_csv('/home/dave/Dropbox (Lehigh University)/Research/By Project/Dissertation/experiments/analysis/exp3-pypool/data/' + entry + '.csv', index = False)

if __name__ == '__main__':
  main()



    