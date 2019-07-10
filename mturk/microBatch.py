#!/home/dave/anaconda2/bin/python

from createHit import PostHits

import sys

sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')

from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key

#!/usr/bin/python
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import boto.mturk.qualification as mtqu
from dateutil.parser import *

HOST = 'mechanicalturk.sandbox.amazonaws.com' # Use this to post to the sandbox instead
#HOST = 'mechanicalturk.amazonaws.com'

pay = 1.5
max_assignments = 9
lifetime = 14 * 24 * 60 * 60 # days, hours, mins, seconds

exp = 'exp1'
batches = 3

hit_id_container = []

for batch in range(batches):
	hit_id_container.append(PostHits(pay, lifetime, max_assignments, exp))

f = open('hit_id.txt', 'w')

for hit_id in hit_id_container:
	f.write(hit_id + '\n')

f.close()

