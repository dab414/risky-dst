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
  
hit_id = open('hit_id.txt', 'r').read()

mtc.expire_hit(hit_id)
mtc.dispose_hit(hit_id)
print mtc.get_hit(hit_id)