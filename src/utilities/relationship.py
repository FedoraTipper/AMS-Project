import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil

conn = DBHandler.create_connection()

_table_ = "relationship"

"""
Function to get a single relationship record from the database
Inputs: Relationship ID of the record wanted
Output: JSON formatted string of relationship record
Caveats: None
"""
def get_relationship(relationship_id):
	relationship = conn.execute("SELECT relationship_id, message FROM {} WHERE relationship_id = {}" % (_table_, int(relationship_id)))
	return {'data': [dict(zip(tuple (relationships.keys()) ,i)) for i in relationships.cursor]}

"""
Function to get all relationship records
Inputs: None
Output: JSON Formatted string of all relationship records
Caveats: None
"""
def get_relationships():
	relationships = conn.execute("SELECT relationship_id, message FROM %s" % (_table_))
	return {'data': [dict(zip(tuple (relationships.keys()) ,i)) for i in relationships.cursor]}

"""
Function to return a relationship ID given it's message
Inputs: Message string
Output: Relationship ID
Caveats: None
"""
def get_relationship_id(message):
	return conn.execute("SELECT relationship_id FROM {} WHERE message = {}".format(_table_, message)).fetchall()[0][0]

"""
Function to create a relationship
Inputs: Relationship dictionary; Tornado Object
Output: True if operation was successful, False if the operation was not
Caveats: Check if relationship message already exists
"""
def create_relationship(relationship_dict, torn):
	if relationship_exists(relationship_dict["message"]):
		torn.write({"message":"Relationship message already exists"})
		return False
	conn.execute(SQLUtil.build_insert_statement(_table_, relationship_dict))
	return True

"""
Function to see whether a relationship exists given its message
Inputs: Message string
Output: Boolean value - (True if the relationship exists)
Caveats: None
"""
def relationship_exists(message):
	return int(conn.execute("SELECT COUNT(relationship_id) FROM {} WHERE message = '{}';".format(_table_, message)).fetchall()[0][0]) != 0

"""
Function to see whether a relationship id exists
Inputs: Relationship ID
Output: Boolean value - (True if the relationship ID exists)
Caveats: None
"""
def relationship_id_exists(relationship_id):
	return int(conn.execute("SELECT COUNT(relationship_id) FROM {} WHERE relationship_id = {};".format(_table_, int(relationship_id))).fetchall()[0][0]) != 0

"""
Function to change link record data
Inputs: Link ID; Dictionary of link data to be ammended; Tornado object to write messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine if node and other FK objects needed to be changed exist; Determine if link relation already exists
"""
def change_relationship(relationship_id, relationship_dict, torn):
	if relationship_id_exists(relationship_id) == False:
		torn.write({"message":"Relationship does not exists"})
		return False

	if relationship_exists(relationship_dict["message"]):
		torn.write({"message":"New relationship message exists"})
		return False

	conn.execute(SQL.build_update_statement(_table_, relationship_dict) + " WHERE relationship_id = {}".format(int(relationship_id)))

"""
Function to delete relationship
Inputs: Relationship ID
Output: True if operation was successful, False if the operation was not
Caveats: Nullify relation ID columns in other tables 
"""
def delete_relationship(relationship_id, torn):
	if relationship_id_exists(relationship_id) == False:
		torn.write({"message": "Relationship id does not exist"})
		return False
	_table_ = {"links"}
	null_dict = {"relationship_id": False}
	#Create SQL statements to set relationship ID in FK _table_s to NULL
	statements = SQLUtil.build_nullify_statements(_table_, null_dict)
	statements.append("DELETE FROM {}".format(_table_))
	
	for sql_statement in statements:
		conn.execute(sql_statement + " WHERE relationship_id = {};".format(int(relationship_id)))

	return True