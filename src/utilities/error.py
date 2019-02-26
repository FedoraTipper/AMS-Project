import json

def check_fields(result_body, categories, torn, result_dict = {}):
	if len(result_body) == 0:
		torn.write({"message":"Missing response body"})		
		return None
	try:	
		json_results = json.loads(result_body)
	except ValueError as err:
		torn.write({"message":"Message field values"})
		return None

	for category in categories:
		if category not in json_results and categories[category] == 1:
			torn.write({"message":"Missing fields: {}".format(category)})
			return None
		elif category not in json_results and categories[category] == 0:
			pass
		else:
			result_dict[category] = json_results[category]
	return result_dict
