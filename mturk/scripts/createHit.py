#!/home/dave/anaconda2/bin/python

import sys
sys.path.append('/home/dave/OneDrive/Research/By Project/Dissertation/experiments/private/')
from awsKeys import aws_access_key_id
from awsKeys import aws_secret_access_key
import boto3
from boto.mturk.question import ExternalQuestion

#HOST = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com' # Use this to post to the sandbox instead
HOST = 'https://mturk-requester.us-east-1.amazonaws.com'

pay = '1.5'
max_assignments = 9
lifetime = 2 * 24 * 60 * 60 # days, hours, mins, seconds

exp = 'exp3'

def PostHits(pay, lifetime, max_assignments, exp):

	region_name = 'us-east-1'

	keywords = 'attention, psychology, experiment, research'
	title = 'A Decision Making Experiment'
	experimentName = 'Decision Making Experiment' ## this is NOT what it ends up getting called on my server
	description = 'This HIT will take about 30 mins to complete. All HITS in this batch are the same, and you will only be able to perform one of the HITS in this batch.'


  ## PRODUCTION LINK
	q = ExternalQuestion(external_url = "https://davebraun.org/dissertation/experiments/production/" + exp +"/", frame_height=675)

	## MAKE UP HIT LINK
	#q = ExternalQuestion(external_url = "https://davebraun.org/dissertation/experiments/production/makeupHit", frame_height=675)

	## EXP 3 PILOT
	#q = ExternalQuestion(external_url = "https://davebraun.org/dissertation/experiments/production/pilots/exp3Pilot/", frame_height=675)

	qr = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [90],
    'RequiredToPreview': True,
	}]

	qr.append({
		'QualificationTypeId': '00000000000000000071',
		'Comparator': 'EqualTo',
		'LocaleValues': [{'Country': 'US'}],
		'RequiredToPreview': True
		})

	
	## Make up hit qualification
	'''
	qr.append({
		'QualificationTypeId': '39G8RJBXZVGXWGOFKKWZFWUS2DYSFD',
		'Comparator': 'Exists',
		'ActionsGuarded': 'PreviewAndAccept'
		})
	'''
	

	mtc = boto3.client('mturk', endpoint_url = HOST,region_name = region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)

	theHit = mtc.create_hit(Question = q.get_as_xml(),
													LifetimeInSeconds = lifetime,
													MaxAssignments = max_assignments,
													Title = title,
													Description = description,
													Keywords = keywords,
													Reward = pay,
													AssignmentDurationInSeconds = 60 * 60, # 60 minutes
													AutoApprovalDelayInSeconds = 2* 24 * 60 * 60, # the number of seconds after an assignment is submitted is it automatically approved unless explicitly rejected
	                        ## the norm is to try to keep this under 7 days, many requesters approve in less than 3 days
	                        RequesterAnnotation = description,
	                        QualificationRequirements = qr)

	print theHit['HIT']['HITId']


if __name__ == '__main__':
	PostHits(pay, lifetime, max_assignments, exp)