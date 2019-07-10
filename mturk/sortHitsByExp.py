def SortHitsByExp(mtc):
	'''
	takes as input MTurkConnection object
	returns a dict with keys ['exp1', 'exp2'] and values as arrays of HIT IDs
	'''

	i = {'exp1': [], 'exp2': []}

	hit_ids = [h.HITId for h in mtc.get_all_hits()]

	for hit in hit_ids:
		if 'exp1' in mtc.get_hit(hit)[0].Question:
			i['exp1'].append(hit)
		elif 'exp2' in mtc.get_hit(hit)[0].Question:
			i['exp2'].append(hit)

	return i

