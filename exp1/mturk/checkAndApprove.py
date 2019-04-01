import sys, re, os
from boto.mturk.connection import MTurkConnection
from KEYS import aws_access_key_id
from KEYS import aws_secret_access_key


def extract_ids():
	args = sys.argv[1:]

	if not args:
		print 'usage: file.txt [file.txt ...]'
		sys.exit(1)

	clean_ids = [os.path.split(x)[1].split('.')[0] for x in args]

	return clean_ids



def main():

	'''
	This script takes as input all files in 'build rvts/subject_data'. The script only parses the file names (which should be the assignment ids).
	This script will automatically approve all assignment IDs that are present in the subject_data folder.
	If the IDs aren't in the folder (but are in the mturk database), flag these cases in `bad_assignments.txt` for further review.
	'''

	HOST = 'mechanicalturk.sandbox.amazonaws.com'
	#HOST = 'mechanicalturk.amazonaws.com'

	mtc = MTurkConnection(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, host = HOST)

	## read the HIT ID, remember there's only ONE of these for each study
	## this is NOT assignment ID
	hitId = open('hit_id.txt', 'r').read()

	## get all target assignment ids that submitted the HIT from mturk
	target_ids = list(mtc.get_assignments(hitId))
	target_ids = [x.AssignmentId for x in target_ids]

	## get all reference assignment ids who have data on the server
	reference_ids = extract_ids()

	

	## for each id from mturk, check to see whether or not it's already approved
	## if it is, check whether their data is on my server
	## if so, approve the hit
	## if not, flag them for closer inspection and save the report to file
		## !!! note that this report writing will overwrite any existing reports on file !!! #####

	bad_assignments = []

	for assignment_id in target_ids:
		if mtc.get_assignment(assignment_id)[0].AssignmentStatus != 'Approved':
			if assignment_id in reference_ids:
				mtc.approve_assignment(assignment_id)
			else:
				print 'Assignment ID: ' + assignment_id + ' submitted a HIT but their data is not on mturk. \n'
				print 'Saving ID to local file.'
				bad_assignments.append(assignment_id)

	if bad_assignments:
		f = open('bad_assignments.txt', 'w')
		for entry in bad_assignments:
			f.write(entry + '\n')
		f.close()	
		
if __name__ == '__main__':
	main()
