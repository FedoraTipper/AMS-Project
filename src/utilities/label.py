import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil

conn = DBHandler.create_connection()

_table_ = "labels"

"""
Function to create a label record
Inputs: Dictionary of label data, Tornado object to write data
Output: True if operation was successful, False if the operation was not
Caveats: Check if the label text already exists
"""
def create_label(label_dict, torn):
	if label_exists(label_dict["label_text"]):
		torn.write({'message': "Label exists"})
		return False
	conn.execute(SQLUtil.build_insert_statement(_table_, label_dict))
	return True

"""
Function to determine if a label exists
Inputs: Label text
Output: Boolean value - (True if the label text exists)
Caveats: None
"""
def label_exists(label_text):
	return int(conn.execute("SELECT COUNT(label_text) FROM %s WHERE label_text = '%s';" % (_table_, label_text)).fetchall()[0][0]) != 0

"""
Function to determine if the label ID exists
Inputs: Label ID int
Output: Boolean value - (True if the label id exists)
Caveats: None
"""
def label_id_exists(label_id):
	return int(conn.execute("SELECT COUNT(label_id) FROM %s WHERE label_id = %d;" % (_table_, int(label_id))).fetchall()[0][0]) != 0

"""
Function to return all label records from the database
Inputs: None
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_labels():
	labels = conn.execute("SELECT label_id, label_text FROM %s" % (_table_))
	return {'data': [dict(zip(tuple (labels.keys()) ,i)) for i in labels.cursor]}

"""
Function to get a single node's data from the database
Inputs: Label ID in int format
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_label(label_id):
	label = conn.execute("SELECT label_text FROM %s WHERE label_id = %d" % (_table_, int(label_id)))
	return {'data': [dict(zip(tuple (label.keys()) ,i)) for i in label.cursor]}

"""
Function to return a label's id give the label text
Inputs: Label text
Output: Label ID
Caveats: None
"""
def get_label_id(label_text):
	return(conn.execute("SELECT label_id FROM {} WHERE label_text = '{}'".format(_table_, label_text)).fetchall()[0][0])

"""
Function to change a label record's data
Inputs: Label ID; Dictionary of label values; Tornado object
Output: True if operation was successful, False if the operation was not
Caveats: Determine if the label ID exists and whether the text exists
"""
def change_label(label_id, label_dict, torn):
	if label_id_exists(label_id) == False:
		torn.write({"message": "Label does not exist"})
		return False
	if label_exists(label_dict["label_text"]):
		torn.write({"message": "New label text already exists"})
		return False
	statement = SQLUtil.build_update_statement(_table_, label_dict) + " WHERE label_id = %d;" % int(label_id)
	conn.execute(statement)
	return True

"""
Function to delete a label record from the database
Inputs: Label ID; Tornado object to write any messages
Output: True if operation was successful, False if the operation was not
Caveats: Check if the label id exists. Nullify label ID in any other tables
"""
def delete_label(label_id, torn):
	if label_id_exists(label_id) == False:
		torn.write({"message": "Label does not exist"})
		return False
	_table_s = {"links", "nodes"}
	null_dict = {"label_id": False}
	statements = SQLUtil.build_nullify_statements(_table_, null_dict)
	statements.append("DELETE FROM {}".format(_table_))
	
	for sql_statement in statements:
		conn.execute(sql_statement + " WHERE label_id = {};".format(int(label_id)))

	return true