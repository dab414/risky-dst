#!/home/dave/anaconda2/bin/python

import sys
sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')
from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key
import boto3

region_name = 'us-east-1'

#HOST = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
HOST = 'https://mturk-requester.us-east-1.amazonaws.com'


mtc = boto3.client('mturk', endpoint_url = HOST,region_name = region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)

for e in mtc.list_hits()['HITs']:
	print e
	print '\n'