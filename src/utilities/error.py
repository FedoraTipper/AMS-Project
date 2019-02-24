def check_fields(result_body, categories, torn, result_dict = {}):
	for category in categories:
		if category not in result_body and categories[category] == 1:
			torn.write({"message":"Missing fields: {}".format(category)})
			return None
		elif category not in result_body and categories[category] == 0:
			pass
		else:
			result_dict[category] = result_body[category]
	return result_dict

