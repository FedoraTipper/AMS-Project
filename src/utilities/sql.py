def build_update_statement(table, statement_dict):
	query = "UPDATE %s SET" % table
	for key in statement_dict:
		if isinstance(statement_dict[key], str):
			query += " {} = '{}',".format(key, statement_dict[key])
		else:
			query += " {} = {},".format(key, statement_dict[key])
	return query[:-1]