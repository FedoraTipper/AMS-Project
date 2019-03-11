import json


"""
Function to check/validate response body or uri parameters of an API request
Inputs: response body or uri parameters; dictionary of categories that need to be checked; tornado object to write any messages
Output: None if there is an user error; Dictionary of all fields and corresponding values
Caveats: 
	Fields not listed in categories will be ignored. 
	Fields with dict value of 0 will be included if it was given in the response body
	Fields with dict value of 1 is required in the response body
"""

def check_fields(result_body, categories, torn):
	result_dict = {}

	if isinstance(result_body, dict) and (len(result_body) == 0):
		return None
	elif len(result_body) == 0:
		torn.write({"message":"Missing response body"})
		return None

	if isinstance(result_body, dict):
		json_results = result_body
	else:
		try:
			json_results = json.loads(result_body)
		except ValueError as err:
			torn.write({"message":"Missing field values"})
			return None

	for category in categories:
		if category not in json_results and categories[category] == 1:
			torn.write({"message":"Missing fields: {}".format(category)})
			return None
		elif category not in json_results and categories[category] == 0:
			pass
		else:
			if isinstance(json_results[category], list):
				if json_results[category][0] != b'':
					result_dict[category] = str(json_results[category][0])[-2:-1]
				else:
					return None
			else:
				if(not isinstance(json_results[category], int) and len(json_results[category]) != 0): 
					result_dict[category] = json_results[category]
				elif(isinstance(json_results[category], int)):
					result_dict[category] = json_results[category]
				else:
					torn.write({"message":"Empty values for field {}".format(category)})
					return None
	return result_dict