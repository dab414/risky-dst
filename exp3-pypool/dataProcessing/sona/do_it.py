from bs4 import BeautifulSoup
import sys
import re
import pandas as pd
import pickle
import os
import copy



def process_timeslots(timeslots_path):
	doc = open(timeslots_path, 'r').read()

	names = re.findall(r'LabelStudentTimeSlot">(\w+\s.*)\s\(', doc)
	statuses = re.findall(r'LabelStudentStatus">(\w+-?\s?\w+)<?\s?\(?', doc)

	try:
		assert(len(names) == len(statuses))
	except:
		print('names: {}'.format(len(names)))
		print('\n')
		print('statuses: {}'.format(len(statuses)))
		sys.exit(1)

	return list(zip(names, statuses))



def process_modify(modify_path):
	doc = open(modify_path, 'r').read()

	emails = re.findall(r'HyperLinkEmail.*mailto:(.*)"', doc)
	names = re.findall(r'LabelParticipantName">(\w+.*)\s\(',doc)

	assert(len(names) == len(emails))

	return(list(zip(names, emails)))



def combine(names_statuses, names_emails):
	## names_statuses: [('Name', 'Credit Granted' | 'No-Show'), ...]

	d = []

	for p1 in names_statuses:
		for p2 in names_emails:
			if p1[0] == p2[0]:
				d.append((p1[0], p2[1], p1[1]))
				break

	out = []

	for e in d:
		
		name = e[0].split(' ')
		build = {'lname': name.pop(-1).lower().strip()}
		build['fname'] = ' '.join(name).lower().strip()
		build['email'] = e[1].lower().strip()
		build['username'] = e[1].split('@')[0].strip()
		build['status'] = e[2].lower().strip()
		out.append(build)

	return out

def process_department(subject_list_path):
	dept = pd.read_excel(subject_list_path)
	dept = dept.drop(dept.columns[3:], axis = 1).to_dict('records')

	dept = [{'fname': x['Fname'].lower().strip(), 'lname': x['Lname'].lower().strip(), 
	'email': x['Email'], 'username': x['Email'].split('@')[0].lower().strip()} for x in dept]

	out = []

	for i, record in enumerate(dept):
		record['id'] = i
		out.append(record)

	return out



def save_dict(subject_d, subject_s = None):
	
	has_participated = 1 if subject_s['status'] == 'credit granted' else 0
	has_not_participated = 1 if has_participated == 0 else 0


	d = {'fname': subject_d['fname'],
				'lname': subject_d['lname'],
				'email': subject_d['email'],
				'username':subject_d['username'],
				'has_participated': has_participated,
				'has_not_participated': has_not_participated,
				'id': subject_d['id']}
	return d


def cross_reference(sona, department):
	'''
	sona:
		{'lname': 'string', 'fname': 'string', 'email': 'string', 'status': 'credit granted' | 'no-show'}
	department:
		{'fname': 'string', 'lname': 'string', 'email': 'string', 'username': 'string', 'id': a unique int}
	'''


	## clear will simply be a list of dicts storing a student's info
	clear = []
	## unclear will be: [{'base': {student_dict}, 'comparisons': [student_dict, ...]}, ...]
	unclear = []
	for subject_d in department:
		unclear.append({'base': subject_d, 'comparisons': []})
		for subject_s in sona:
			tally = 0
			if subject_d['fname'] == subject_s['fname']:
				tally += 1
			if subject_d['lname'] == subject_s['lname']:
				tally += 1
			if subject_d['username'] == subject_s['username']:
				tally += 1
				
			if tally == 3:
				clear.append(save_dict(subject_d = subject_d, subject_s = subject_s))
				unclear[-1]['comparisons'] = []
				break

			if tally < 3 and tally > 0:
				unclear[-1]['comparisons'].append(subject_s)


	return clear, unclear

def user_reconcile(clear, unclear):
	## get user input to reconcile unclear cases
	unclear = [x for x in unclear if x['comparisons']]
	print('There are {} unclear students to process.\n\n'.format(len(unclear)))

	def print_base(entry):
		print('\n\n##########################')
		print('\n\n')
		print('We need to find a match for: \n')
		for key in entry['base']:
			print('{}: {}'.format(key, entry['base'][key]))

	unclear_record = copy.deepcopy(unclear)
		
	for entry in unclear:	
		print_base(entry)
		for possible_match in entry['comparisons']:
			response = ''
			while response not in ['yes', 'no']:
				print('\n\n\n')
				print('{}: {}'.format('fname', possible_match['fname']))
				print('{}: {}'.format('lname', possible_match['lname']))
				print('{}: {}'.format('email', possible_match['email']))
				print('{}: {}'.format('username', possible_match['username']))
				response = input('Is this a match: (yes/no) ')
				if response not in ['yes', 'no']:
					print('Type "yes" or "no"\n')

			if response == 'yes':
				clear.append(save_dict(subject_d = entry['base'], subject_s = possible_match))
				del unclear_record[unclear_record.index(entry)]

				break
			else:
				print_base(entry)

	with open('clear.pickle', 'wb') as file:
		pickle.dump(clear, file)
	file.close()

	return clear, unclear_record

def compile_final_list(clear, department):
	completed_ids = [x['id'] for x in clear if x['has_participated']]
	print(len(completed_ids))
	not_participated_ids = [x['id'] for x in department if x['id'] not in completed_ids]
	not_participated_ids += [x['id'] for x in clear if x['has_not_participated']]
	not_participated_ids = list(set(not_participated_ids))
	not_participated = [x for x in department if x['id'] in not_participated_ids]
	file = open('not_participated.txt', 'w')
	for student in not_participated:
		file.write('{}, '.format(student['email']))
	file.close()
	print('There were {} students who did not participate'.format(len(not_participated)))

if __name__ == '__main__':

	### this script isnt quite perfect but it seems okay
	## it was off by a few ppl

	args = sys.argv[1:]

	if len(args) < 3:
		print('Usage: script.py timeslots modify subject_list')
		sys.exit(1)

	timeslots_path, modify_path, subject_list_path = args

	names_statuses = process_timeslots(timeslots_path)
	names_emails = process_modify(modify_path)
	sona = combine(names_statuses, names_emails)
	department = process_department(subject_list_path)

	clear, unclear = cross_reference(sona, department)

	decision = ''
	if os.path.exists('clear.pickle'):
		while decision not in ['yes', 'no']:
			decision = input('There is a file called "clear.pickle" already created. Enter yes if you want to source this. No if you want to filter by hand. (yes/no) ')

	if decision == 'yes':
		with open('clear.pickle', 'rb') as file:
			clear = pickle.load(file)

	else:
		clear, unclear = user_reconcile(clear, unclear)
		unclear = [eval(x['base']) for x in unclear]
		pd.DataFrame(unclear).to_csv('unclear.csv', index = False)

	compile_final_list(clear, department)

	clear = pd.DataFrame(clear).drop(['id', 'username'], axis = 1)
	clear = clear.rename(columns={'has_participated': 'Has Participated', 'has_not_participated': "No Show/Didn't Sign Up"})
	clear.to_excel(subject_list_path.split('.')[0] + ' Completed.xlsx', index = False)
