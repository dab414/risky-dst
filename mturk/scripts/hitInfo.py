#!/home/dave/anaconda2/bin/python


import sys
sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')
from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key
import boto3

region_name = 'us-east-1'

#HOST = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
HOST = 'https://mturk-requester.us-east-1.amazonaws.com'

totalSubmitted = 0

mtc = boto3.client('mturk', endpoint_url = HOST,region_name = region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)


print '\n'

for hit in mtc.list_hits(MaxResults = 100)['HITs']:
	maxAssignments = hit['MaxAssignments']
	availableAssignments = hit['NumberOfAssignmentsAvailable']
	pendingAssignments = hit['NumberOfAssignmentsPending']

	totalSubmitted += (maxAssignments - (availableAssignments + pendingAssignments))

	print 'HIT ID: ' + hit['HITId']
	print 'Max Assignments: ' + str(maxAssignments)
	print 'Available Assignments: ' + str(availableAssignments)
	print 'Pending Assignments: ' + str(pendingAssignments)
	print 'Completed Assignments: ' + str(hit['NumberOfAssignmentsCompleted'])
	print 'HIT Status: ' + hit['HITStatus']
	print '\n\n'
	

print 'Overall, ' + str(totalSubmitted) + ' assignments have been submitted.'
print '\n\n'