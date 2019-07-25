#!/home/dave/anaconda2/bin/python

import sys
import pandas as pd
import numpy as np
import os
from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key
import boto3


sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')

identitiesAndRejections = '/home/dave/OneDrive/Research/By Project/Dissertation/experiments/analysis/exp1/scripts/identitiesAndRejections/'

region_name = 'us-east-1'


HOST = 'https://mturk-requester.us-east-1.amazonaws.com'


mtc = boto3.client('mturk', endpoint_url = HOST,region_name = region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)


## import csv of all assignments that have already been rejected
rejected = pd.read_csv(identitiesAndRejections + 'rejectedAssignments.csv')

## select out the assignment ids to cross reference
rejectedList = np.array(rejected['curId'])

## import csv containing all assignments from *whole experiment* that deserve to be rejected based on rejection criterion
inputReject = pd.read_csv(identitiesAndRejections + 'rejectList.csv')

## see which out of all of the people who need to be rejected havent already been rejected
## those are the ones that we want to reject now
toReject = inputReject[~inputReject['curId'].isin(rejectedList)]

message = "The instructions of this HIT were clear in that you needed to maintain an accuracy of at least 75% for your work to be accepted. Your work fell below this threshold, and it will be rejected for this reason."

if not toReject.empty:

	toReject = np.array(toReject['curId'])

	for a in toReject:
		print 'Rejecting assignment: ' + a + '\n'
		mtc.reject_assignment(AssignmentId = a, feedback = message)

	rejectedList = pd.concat([rejected, inputReject[inputReject['curId'].isin(toReject)]])

	rejectedList.to_csv(identitiesAndRejections + 'rejectedAssignments.csv')

else:
	print 'No additional bots were rejected'