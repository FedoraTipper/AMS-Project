import json
import re

def check_fields(result_body, categories, torn, result_dict = {}):
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
				result_dict[category] = json_results[category]
	return result_dict