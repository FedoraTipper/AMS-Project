"""
Functions to build base SQL statements. Conditions of statements are left out,
and added on, outside of functions.
"""

"""
Function to build SQL update statements for any table in the database
Inputs: table name; dictionary of all respective cols and values that need to be appended
Output: Half-built sql statement for updating a table.
Caveats: Conditions are added externally
"""
def build_update_statement(table, statement_dict):
	query = "UPDATE %s SET" % table
	for key in statement_dict:
		if isinstance(statement_dict[key], str):
			query += " {} = '{}',".format(key, statement_dict[key])
		elif statement_dict[key] is None:
			query += " {} = NULL,".format(key)
		else:
			query += " {} = {},".format(key, statement_dict[key])
	return query[:-1]

"""
Function to build SQL insert statements for any table in the database
Inputs: table name; dictionary of all respective cols and values that need to be added to the table row
Output: Half-built sql statement for inserting a record to a table.
Caveats: Conditions are added externally
"""
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


"""
Function to set any fields to NULL in a predefined list of tables
Inputs: list of tables; dictionary of all respective cols that will be set to NULL
Output: Half-built sql statement to set fields to NULL
Caveats: Conditions are added externally
"""
def build_nullify_statements(tables, statement_dict):
	statement_list = list()
	for table in tables:
		for key in statement_dict:
			statement_list.append(build_update_statement(table, statement_dict))
	return statement_list