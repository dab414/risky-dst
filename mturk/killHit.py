#!/home/dave/anaconda2/bin/python

import sys

sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')

from boto.mturk.connection import MTurkConnection

from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key

HOST = 'mechanicalturk.sandbox.amazonaws.com' # Use this to post to the sandbox instead

mtc = MTurkConnection(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        host=HOST)
  
hit_ids = []

for h in mtc.get_all_hits():
	hit_ids.append(h.HITId)

for h in hit_ids:
	mtc.disable_hit(h)
	print mtc.get_hit(h)[0].HITId + ': ' + mtc.get_hit(h)[0].HITStatus

