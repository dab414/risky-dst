#!/home/dave/anaconda2/bin/python

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

def PostHits():
  mtc = MTurkConnection(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        host=HOST)
  
  
  q = ExternalQuestion(external_url = "https://davebraun.org/dissertation/experiments/exp1/", frame_height=675)
  keywords = ['attention', 'psychology', 'experiment', 'research']
  title = 'A Decision Making Experiment'
  experimentName = 'Decision Making Experiment' ## this is NOT what it ends up getting called on my server
  description = 'This HIT will take about 30 mins to complete.'
  pay = 1.5
  
  qualifications = mtqu.Qualifications()
  qualifications.add(mtqu.PercentAssignmentsApprovedRequirement('GreaterThanOrEqualTo', 90))
  qualifications.add(mtqu.LocaleRequirement("EqualTo", "US"))
  #qualifications.add(mtqu.Requirement("2Z046OQ1SNQQREGXAFSQPCNR1605PN"))

  theHIT = mtc.create_hit(question=q,
                          lifetime=7 * 24 * 60 * 60, # days, hours, mins, seconds
                          max_assignments=10,
                          title=title,
                          description=description,
                          keywords=keywords,
                          qualifications=qualifications,
                          reward=pay,
                          duration=120 * 60, # 120 minutes
                          approval_delay=2* 24 * 60 * 60, # the number of seconds after an assignment is submitted is it automatically approved unless explicitly rejected
                          ## the norm is to try to keep this under 7 days, many requesters approve in less than 3 days
                          annotation=experimentName)

  assert(theHIT.status == True)
  print theHIT
  hit_type_id = theHIT[0].HITId
  print hit_type_id
  #print "https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id)

  f = open('hit_id.txt', 'w')
  f.write(hit_type_id)
  f.close()

PostHits()