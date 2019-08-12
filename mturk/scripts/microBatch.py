#!/home/dave/anaconda2/bin/python

from createHit import PostHits

import sys

sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')

from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import boto.mturk.qualification as mtqu
from dateutil.parser import *

targetAssignments = sys.argv[1:]

if not targetAssignments or len(targetAssignments) > 1:
	print 'Usage: TargetAssignmentNumber'
	sys.exit(1)


targetAssignments = int(targetAssignments[0])

HOST = 'mechanicalturk.sandbox.amazonaws.com' # Use this to post to the sandbox instead
#HOST = 'mechanicalturk.amazonaws.com'

pay = '1.5'
max_assignments = 9
lifetime = 2 * 24 * 60 * 60 # days, hours, mins, seconds

exp = 'exp3'

batches = targetAssignments / 9

if targetAssignments % 9:
	batches += 1

hit_id_container = []

for batch in range(batches):
	if batch == range(batches)[-1]:
		max_assignments = targetAssignments % 9
	hit_id_container.append(PostHits(pay, lifetime, max_assignments, exp))

f = open('hit_id.txt', 'w')

for hit_id in hit_id_container:
	f.write(hit_id + '\n')

f.close()

