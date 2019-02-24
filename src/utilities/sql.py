"""
Functions to build base SQL statements. Conditions of statements are left out,
and added on outside of the function.
"""

def build_update_statement(table, statement_dict):
	query = "UPDATE %s SET" % table
	for key in statement_dict:
		if isinstance(statement_dict[key], str):
			query += " {} = '{}',".format(key, statement_dict[key])
		else:
			query += " {} = {},".format(key, statement_dict[key])
	return query[:-1]

def build_insert_statement(table, statement_dict):
	query = "INSERT INTO %s (" % table

	for key in statement_dict:
		query += "%s, " % key

	query = query[:-2] + ") VALUES ("

	for key in statement_dict:
		if isinstance(statement_dict[key], str):
			query += "'{}', ".format(statement_dict[key])
		else:
			query += "{}, ".format(statement_dict[key])

	return (query[:-2] + ");")
