
import sys
sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')
from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key
import boto3

region_name = 'us-east-1'


HOST = 'https://mturk-requester.us-east-1.amazonaws.com'


mtc = boto3.client('mturk', endpoint_url = HOST,region_name = region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)



pay = '1.5'
keywords = 'attention, psychology, experiment, research'
title = 'A Decision Making Experiment'
experimentName = 'Decision Making Experiment' ## this is NOT what it ends up getting called on my server
description = 'This HIT will take about 30 mins to complete. All HITS in this batch are the same, and you will only be able to perform one of the HITS in this batch.'

q = ExternalQuestion(external_url = "https://davebraun.org/dissertation/experiments/production/" + exp +"/", frame_height=675)


theHit = mtc.create_hit(Question = q.get_as_xml(),LifetimeInSeconds = lifetime,MaxAssignments = max_assignments,Title = title,Description = description,Keywords = keywords,Reward = pay,AssignmentDurationInSeconds = 120 * 60, AutoApprovalDelayInSeconds = 2* 24 * 60 * 60, RequesterAnnotation = description)