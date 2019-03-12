import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import utilities.node as NodeUtil
import utilities.label as LabelUtil
import utilities.relationship as RelationshipUtil
conn = DBHandler.create_connection()


_table_ = "links"

"""
Function to create a link
Inputs: Link dictionary; Tornado Object
Output: True if operation was successful, False if the operation was not
Caveats: Check if both nodes and any FK objects exists, links already exists and if the link is to and from the same node
"""
def create_link(link_dict, torn):
	if check_nodes_exist(link_dict["node_id_1"], link_dict["node_id_2"]) == False:
		torn.write({"message":"One of nodes in the the link does not exist"})
		return False

	if link_dict["node_id_1"] == link_dict["node_id_2"]:
		torn.write({"message":"Links from and to the same node are not allowed"})
		return False

	if link_relation_exists(link_dict["node_id_1"], link_dict["node_id_2"]):
		torn.write({"message":"Link between the two nodes already exists"})
		return False

	if "label_id" in link_dict:
		if LabelUtil.label_id_exists(link_dict["label_id"]) == False:
			torn.write({"message":"Label does not exist"})
			return False

	if "relationship_id" in link_dict:
		if RelationshipUtil.relationship_id_exists(link_dict["relationship_id"]) == False:
			torn.write({"message":"Relationship does not exist"})
			return False

	conn.execute(SQLUtil.build_insert_statement(_table_, link_dict))
	return True

"""
Function to determine if a link exists
Inputs: Link ID
Output: Boolean value - (True if the link exists)
Caveats: None
"""
def link_exists(link_id):
	return int(conn.execute("SELECT COUNT(link_id) FROM {} WHERE link_id = {};".format(_table_, int(link_id))).fetchall()[0][0]) != 0

"""
Function to determine if a link between two nodes already exist
Inputs: Node ID 1; Node ID 2
Output: True if link already exists
Caveats: None
"""
def link_relation_exists(node_id_1, node_id_2):
	return int(conn.execute("SELECT COUNT(link_id) FROM {0} WHERE (node_id_1 = {1} AND node_id_2 = {2}) AND (node_id_1 = {2} AND node_id_2 = {1});".format(_table_, int(node_id_1), int(node_id_2))).fetchall()[0][0]) != 0

"""
Function to get all link records from the database
Inputs: None
Output: JSON Formatted string of all link records
Caveats: None
"""
def get_links():
	links = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id, relationship_id FROM %s" % (_table_))
	return {'data': [dict(zip(tuple (links.keys()) ,i)) for i in links.cursor]}

"""
Function to get a single link record from the database
Inputs: Link ID of the record wanted
Output: JSON formatted string of link record
Caveats: None
"""
def get_link(link_id):
	link = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id, relationship_id FROM %s WHERE link_id = %d" % (_table_, int(link_id)))
	return {'data': [dict(zip(tuple (link.keys()) ,i)) for i in link.cursor]}

"""
Function to return a Link ID given the nodes in it
Inputs: Node ID 1; Node ID 2
Output: Link ID int
Caveats: None
"""
def get_link_id(node_id_1, node_id_2):
	return conn.execute("SELECT link_id FROM {} WHERE node_id_1 = {} AND node_id_2 = {}".format(_table_, int(node_id_1), int(node_id_2))).fetchall()[0][0]

"""
Function to change link record data
Inputs: Link ID; Dictionary of link data to be ammended; Tornado object to write messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine if node and other FK objects needed to be changed exist; Determine if link relation already exists
"""
def change_link(link_id, link_dict, torn):

	if link_exists(link_id) == False:
		torn.write({"message":"Link does not exist"})
		return False

	check = True
	if "node_id_1" in link_dict or "node_id_2" in link_dict:
		if "node_id_1" in link_dict and "node_id_2" not in link_dict:
			node_ids = get_node_ids_in_link(link_id)
			link_dict["node_id_2"] = int(node_ids[1])
		elif "node_id_2" in link_dict and "node_id_1" not in link_dict:
			node_ids = get_node_ids_in_link(link_id)
			link_dict["node_id_1"] = int(node_ids[0])
		else:
			check = False

		if check == True and check_nodes_exist(link_dict["node_id_1"], link_dict["node_id_2"]) == False:
			torn.write({"message":"One of nodes in the the link does not exist"})
			return False

		if link_dict["node_id_1"] == link_dict["node_id_2"]:
			torn.write({"message":"Links from and to the same node are not allowed"})
			return False

		if link_relation_exists(link_dict["node_id_1"], link_dict["node_id_2"]):
			torn.write({"message":"Link between the two nodes already exists"})
			return False
	conn.execute(SQLUtil.build_update_statement(_table_, link_dict) + " WHERE link_id = %d;" % (int(link_id)))
	return True

"""
Deprecated
"""
def sort_node_ids(link_dict):
	if link_dict["node_id_1"] > link_dict["node_id_2"]:
		temp = int(link_dict["node_id_1"])
		link_dict["node_id_1"] = int(link_dict["node_id_2"])
		link_dict["node_id_2"] = temp
	return link_dict

"""
Function to delete a link from the database
Inputs: Link ID; Tornado object
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node and any FK objects exists
"""
def delete_link(link_id, torn):
	if link_exists(link_id) == False:
		torn.write({"message":"Link does not exist"})
		return False
	conn.execute("DELETE FROM {} WHERE link_id = {}".format(_table_, int(link_id)))
	return True

#Internal function
def delete_link_with_node(node_id):
	conn.execute("DELETE FROM {0} WHERE node_id_1 = {1} or node_id_2 = {1}".format(_table_, int(node_id)))

"""
Function to check if two nodes exist
Inputs: Node ID 1; Node ID 2
Output: True if both nodes exist
Caveats: None
"""
def check_nodes_exist(node_id_1, node_id_2):
	if NodeUtil.node_id_exists(node_id_1) == False or NodeUtil.node_id_exists(node_id_2) == False:
		return False
	return True

"""
Function to retrieve node IDs in a link
Inputs: Link ID
Output: List of two node IDs
Caveats: None
"""
def get_node_ids_in_link(link_id):
	return conn.execute("SELECT node_id_1, node_id_2 FROM {} WHERE link_id = {}".format(_table_, int(link_id))).fetchall()[0]