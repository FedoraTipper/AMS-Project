import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import utilities.label as LabelUtil

conn = DBHandler.create_connection()

_table_ = "nodes"

"""
Function to create a node in the database
Inputs: Dictionary of node data, Tornado object to write data
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node type already exists
"""
def create_node(node_dict, torn):
	if node_exists(node_dict["type"]):
		torn.write({'message': "Node type exists"})
		return None
	conn.execute(SQLUtil.build_insert_statement(_table_, node_dict))
	return True

"""
Function to determine if a node exists
Inputs: Node type string
Output: Boolean value - (True if the node type exists)
Caveats: None
"""
def node_exists(node_type):
	return int(conn.execute("SELECT COUNT(node_id) FROM %s WHERE type = '%s';" %(_table_, node_type)).fetchall()[0][0]) != 0

"""
Function to determine if the node ID exists
Inputs: Node ID int
Output: Boolean value - (True if the node id exists)
Caveats: None
"""
def node_id_exists(node_id):
	return int(conn.execute("SELECT COUNT(node_id) FROM %s WHERE node_id = %d;" %(_table_, int(node_id))).fetchall()[0][0]) != 0

"""
Function to return all nodes from the database
Inputs: None
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_nodes():
	nodes = conn.execute("SELECT node_id, type, label_id, icon FROM %s" % (_table_))
	return {'data': [dict(zip(tuple (nodes.keys()) ,i)) for i in nodes.cursor]}

"""
Function to get a single node's data from the database
Inputs: Node ID in int format
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_node(node_id):
	node = conn.execute("SELECT node_id, type, label_id, icon FROM %s WHERE node_id = %d" % (_table_, int(node_id)))
	return {'data': [dict(zip(tuple (node.keys()) ,i)) for i in node.cursor]}

"""
Function to return a node type's ID
Inputs: Node type string
Output: Node ID in int format
Caveats: None
"""
def get_node_id(node_type):
	return(conn.execute("SELECT node_id FROM {} WHERE type = '{}'".format(_table_, node_type)).fetchall()[0][0])

"""
Function to change a node's information that is stored in the database
Inputs: Node ID; Dictionary of columns and values that will be ammended to the record; Tornado object
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node and any FK objects exists
"""
def change_node(node_id, node_dict, torn):
	if node_id_exists(node_id) == False:
		torn.write({'message': "Node does not exist"})
		return None
	if "type" in node_dict:
		if node_exists(node_dict["type"]):
			torn.write({"message": "New node type already exists"})
			return None
	if "label_id" in node_dict:
		if LabelUtil.label_id_exists(node_dict["label_id"]) == False:
			torn.write({"message": "Label id does not exist"})
			return None

	statement = SQLUtil.build_update_statement(_table_, node_dict) + " WHERE node_id = %d;" % node_id
	conn.execute(statement)
	return True

"""
Function to delete a node record from the database table
Inputs: Node ID; Tornado object to write any messages
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node id already exists
"""
def delete_node(node_id, torn):
	if node_id_exists(node_id) == False:
		torn.write({"message":"Node does not exist"})
		return 
	#Import module in function. Not allowed to cross reference
	import utilities.link as LinkUtil
	#Delete all links that contain the node id
	LinkUtil.delete_link_with_node(node_id)
	import utilities.metadata as MetaUtil
	MetaUtil.delete_metadata_with_node(node_id)
	#Delete the node
	conn.execute("DELETE FROM {} WHERE node_id = {}".format(_table_, int(node_id)))
	return True