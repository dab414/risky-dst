#!/home/dave/anaconda2/bin/python
import sys
sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')
import pandas as pd
import numpy as np
import os
from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key
import boto3

args = sys.argv[1:]

if len(args) > 1 or not args or args[0] not in ['exp1', 'exp2']:
	print 'Usage: [exp1 / exp2]'
	sys.exit(1)

exp = args[0]


identitiesAndRejections = '/home/dave/OneDrive/Research/By Project/Dissertation/experiments/analysis/' + exp + '/scripts/identitiesAndRejections/'

region_name = 'us-east-1'


HOST = 'https://mturk-requester.us-east-1.amazonaws.com'


mtc = boto3.client('mturk', endpoint_url = HOST,region_name = region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)


rejectedListExists = 1

try:
	## import csv of all assignments that have already been rejected
	rejected = pd.read_csv(identitiesAndRejections + 'rejectedAssignments.csv')

	## select out the assignment ids to cross reference
	rejectedList = np.array(rejected['curId'])

except:
	rejectedListExists = 0

## import csv containing all assignments from *whole experiment* that deserve to be rejected based on rejection criterion
inputReject = pd.read_csv(identitiesAndRejections + 'rejectList.csv')

## see which out of all of the people who need to be rejected havent already been rejected
## those are the ones that we want to reject now
if rejectedListExists:
	inputReject = inputReject[~inputReject['curId'].isin(rejectedList)]

message = "The instructions of this HIT were clear in that you needed to maintain an accuracy of at least 75% for your work to be accepted. Your work fell below this threshold, and it will be rejected for this reason."

if not inputReject.empty:

	if rejectedListExists:
		totalRejected = pd.concat([rejected, inputReject])
	else:
		totalRejected = inputReject

	inputReject.to_csv(identitiesAndRejections + 'assignmentsToReject.csv', index = False)
	totalRejected.to_csv(identitiesAndRejections + 'rejectedAssignments.csv', index = False)

	print '\n'
	print '###############'
	print 'DATA QUALITY ASSESSMENT'
	print '\n'
	print 'There are ' + str(len(np.array(inputReject['curId']))) + ' assignments that need to be rejected.'
	print '################'
	print '\n'

else:
	print '\n'
	print '###############'
	print 'DATA QUALITY ASSESSMENT'
	print '\n'
	print 'No additional bots need to be rejected'
	print '################'
	print '\n'
	x = pd.DataFrame(['Nothing to Reject'], columns = ['CurId'])
	x.to_csv(identitiesAndRejections + 'assignmentsToReject.csv', index = False)
	