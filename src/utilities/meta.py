import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import utilities.node as NodeUtil
conn = DBHandler.create_connection()

_table_ = "metadata"

"""
Function to create metadata category for a specified node
Inputs: Dictionary of metadata; Tornado object to write messages
Output: True if insert operation was successful, False if the operation was not
Caveats: Check if the node and if the category for that node already exists
"""
def create_category(metadata_dict, torn):
	if NodeUtil.node_id_exists(metadata_dict["node_id"]) == False:
		torn.write({"message": "Node does not exist"})
		return False

	if category_exists(metadata_dict["category"], metadata_dict["node_id"]):
		torn.write({"message": "Metadata category for the specified node already exists"})
		return False

	conn.execute(SQLUtil.build_insert_statement(_table_, metadata_dict))
	return True

"""
Function to determine if a metadata category for a node already exists
Inputs: Category string; Node ID int
Output: Boolean value - (True indicates category for the node exists)
Caveats: None
"""
def category_exists(category, node_id):
	return int(conn.execute("SELECT COUNT(meta_id) FROM %s WHERE category = '%s' AND node_id = %d;" %(_table_, category, int(node_id))).fetchall()[0][0]) != 0

"""
Function to determine if a metadata record exists in the database
Inputs: Metadata ID int format
Output: Boolean value - (True indicates that the id exists)
Caveats: None
"""
def metadata_exists(metadata_id):
	return int(conn.execute("SELECT COUNT(meta_id) FROM %s WHERE meta_id = %d;" % (_table_, int(metadata_id))).fetchall()[0][0]) != 0

"""
Function to get all metadata records from the database
Inputs: None
Output: JSON formatted string of all metadata records
Caveats: None
"""
def get_all_metadata():
	metadata = conn.execute("SELECT meta_id, category, metadata, node_id FROM %s;" % (_table_))
	return {'data': [dict(zip(tuple (metadata.keys()) ,i)) for i in metadata.cursor]}

"""
Function to get a single metadata record from the database
Inputs: Node ID
Output: JSON formatted string of metadata records for specified node
Caveats: None
"""
def get_metadata(node_id):
	metadata = conn.execute("SELECT meta_id, category, metadata, node_id FROM %s WHERE node_id = %d;" % (_table_, int(node_id)))
	return {'data': [dict(zip(tuple (metadata.keys()) ,i)) for i in metadata.cursor]}

"""
Function to retrieve a metadata's id given the node ID and category
Inputs: Category string; Node ID
Output: Metadata id int 
Caveats: None
"""
def get_metadata_id(category, node_id):
	return(conn.execute("SELECT meta_id FROM {} WHERE node_id = {} AND category = '{}';".format(_table_, int(node_id), category)).fetchall()[0][0])

"""
Function to change a metadata record in the database
Inputs: Metadata ID; Metadata Dictionary of all values that will be changed; Tornado object for writing messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine the existance of metadata record, node id and category before change
"""
def change_metadata(metadata_id, metadata_dict, torn):
	if metadata_exists(metadata_id) == False:
		torn.write({"message": "Metadata ID does not exist"})
		return False

	if "node_id" in metadata_dict:
		if NodeUtil.node_id_exists(metadata_dict["node_id"]) == False:
			torn.write({"message": "Node does not exist"})
			return False

	if "category" in metadata_dict:
		if category_exists(metadata_dict["category"], metadata_dict["node_id"]):
			torn.write({"message": "Metadata category already exists"})
			return False

	statement = SQLUtil.build_update_statement(_table_, metadata_dict) + " WHERE meta_id = %d;" % metadata_id
	conn.execute(statement)

	return True

"""
Function to delete a metadata record from the database
Inputs: Metadata ID; Tornado object to write messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine the existance of metadata record
"""
def delete_metadata(metadata_id, torn):
	if metadata_exists(metadata_id) == False:
		torn.write({"message": "Node does not exist"})
		return False
	conn.execute("DELETE FROM {} WHERE meta_id = {}".format(_table_, metadata_id))
	return True

"""
Function to delete all metadata records that belong to a single node
Inputs: Node ID
Output: None
Caveats: Returns none as this function is seen as "best effort"
"""
def delete_metadata_with_node(node_id):
	conn.execute("DELETE FROM {} WHERE node_id = {}".format(_table_, int(node_id)))