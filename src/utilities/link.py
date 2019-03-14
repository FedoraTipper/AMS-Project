import handlers.mysqldb as DBHandler
import utilities.node as NodeUtil
import utilities.label as LabelUtil
import utilities.view as ViewUtil
import utilities.relationship as RelationshipUtil
import handlers.classes.TableEntities as TableEntities

session = DBHandler.create_session()

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

	if ViewUtil.view_id_exists(link_dict["view_id"]) == False:
		torn.write({"message":"View ID does not exist"})

	link = TableEntities.Links(node_id_1=int(link_dict["node_id_1"]),
								node_id_2=int(link_dict["node_id_2"]),
								view_id = int(link_dict["view_id"]))

	if "label_id" in link_dict:
		if LabelUtil.label_id_exists(link_dict["label_id"]) == False:
			torn.write({"message":"Label does not exist"})
			return False
		else:
			link.label_id = int(link_dict["label_id"])

	if "relationship_id" in link_dict:
		if RelationshipUtil.relationship_id_exists(link_dict["relationship_id"]) == False:
			torn.write({"message":"Relationship does not exist"})
			return False
		else:
			link.relationship_id = int(link_dict["relationship_id"])

	try:
		session.add(link)
		session.commit()
	except:
		print("Something went wrong. <Link Add>")
		return False
	return True

"""
Function to determine if a link exists
Inputs: Link ID
Output: Boolean value - (True if the link exists)
Caveats: None
"""
def link_exists(link_id):
	return int(session.query(TableEntities.Links).filter(
			TableEntities.Links.link_id == int(link_id)).count()) != 0

"""
Function to determine if a link between two nodes already exist
Inputs: Node ID 1; Node ID 2
Output: True if link already exists
Caveats: None
"""
def link_relation_exists(node_id_1, node_id_2):
	return int(session.query(TableEntities.Nodes).filter((
			(TableEntities.Links.node_id_1 == int(node_id_1)) & 
			(TableEntities.Links.node_id_2 == int(node_id_2))) | (
			(TableEntities.Links.node_id_2 == int(node_id_1)) & 
			(TableEntities.Links.node_id_1 == int(node_id_2))))
			.count()) != 0

"""
Function to get all link records from the database
Inputs: None
Output: JSON Formatted string of all link records
Caveats: None
"""
def get_links():
	entries = session.query(TableEntities.Links).all()
	return {'data': [entry.as_dict() for entry in entries]}
"""
Function to get a single link record from the database
Inputs: Link ID of the record wanted
Output: JSON formatted string of link record
Caveats: None
"""
def get_link(link_id):
	entries = session.query(TableEntities.Links).filter(
		TableEntities.Links.link_id == int(link_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}
"""
Function to return a Link ID given the nodes in it
Inputs: Node ID 1; Node ID 2
Output: Link ID int
Caveats: None
"""
def get_link_id(node_id_1, node_id_2):
	return  (session.query(TableEntities.Links).filter((TableEntities.Links.node_id_1 == int(node_id_1)) & 
			(TableEntities.Links.node_id_2 == int(node_id_2))).one().meta_id)

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
		#Get the node id that the user didn't submit
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

	if "view_id" in link_dict:
		if ViewUtil.view_id_exists(link_dict["view_id"]) == False:
			torn.write({'message': "View ID does not exist"})
			return False

	if "relationship_id" in link_dict:
		if RelationshipUtil.relationship_id_exists(link_dict["relationship_id"]) == False:
			torn.write({'message': "Relationship ID does not exist"})
			return False

	try:
		session.execute(
			update(TableEntities.Links).where(TableEntities.Links.link_id == int(link_id))
			.values(link_dict)
			)	
		session.commit()
	except:
		print("Something went wrong. <Link Update>")
		return False

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
	try:
		session.execute(
			delete(TableEntities.Links).where(TableEntities.Links.link_id == int(link_id))
			)
		session.commit()
	except:
		print("Something went wrong. <Link Delete>")
	return True

#Internal function
def delete_link_with_node(node_id):
	try:
		session.execute(
			delete(TableEntities.Links).where((TableEntities.Links.node_id_1 == int(node_id)) | (TableEntities.Links.node_id_2 == int(node_id)))
			)
		session.commit()
	except:
		print("Something went wrong. <Link with Node Delete>")
		return False
	return True
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
	query = session.query(Links).filter(Links.link_id == 1).one()
	node_list = list()
	node_list.append(query.node_id_1)
	node_list.append(query.node_id_2)
	return node_list