#!/home/dave/anaconda2/bin/python

import sys
import pandas as pd
import numpy as np
import os


sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')

identitiesAndRejections = '/home/dave/OneDrive/Research/By Project/Dissertation/experiments/analysis/exp1/scripts/identitiesAndRejections/'

from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key

#!/usr/bin/python
from boto.mturk.connection import MTurkConnection

HOST = 'mechanicalturk.amazonaws.com'

mtc = MTurkConnection(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,host=HOST)

rejected = pd.read_csv(identitiesAndRejections + 'rejectedAssignments.csv')

rejectedList = np.array(rejected['curId'])

inputReject = pd.read_csv(identitiesAndRejections + 'rejectList.csv')

toReject = inputReject[~inputReject['curId'].isin(rejectedList)]

message = "The instructions of this HIT were clear in that you needed to maintain an accuracy of at least 75% for your work to be accepted. Your work fell below this threshold, and it will be rejected."

if not toReject.empty:

	toReject = np.array(toReject['curId'])

	for aid in toReject:
		print 'Rejecting assignment: ' + aid + '\n'
		mtc.reject_assignment(aid, feedback = message)

	rejectedList = pd.concat([rejected, inputReject[inputReject['curId'].isin(toReject)]])

	rejectedList.to_csv(identitiesAndRejections + 'rejectedAssignments.csv')

else:
	print 'No additional bots were rejected'