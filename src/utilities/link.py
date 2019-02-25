import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import utilities.node as NodeUtil
import utilities.label as LabelUtil
conn = DBHandler.create_connection()


TABLE = "links"

"""
Node ids are stored in ascending order
"""
def create_link(link_dict, torn):

	if check_nodes_exist(link_dict["node_id_1"], link_dict["node_id_2"]) == False:
		torn.write({"message":"One of nodes in the the link does not exist"})
		return None

	link_dict = sort_node_ids(link_dict)

	if link_dict["node_id_1"] == link_dict["node_id_2"]:
		torn.write({"message":"Links from and to the same node are not allowed"})
		return None

	if relationship_exists(link_dict["node_id_1"], link_dict["node_id_2"]):
		torn.write({"message":"Link between the two nodes already exists"})
		return None

	if "label_id" in link_dict:
		if LabelUtil.label_id_exists(link_dict["label_id"]) == False:
			torn.write({"message":"Label does not exist"})
			return None

	conn.execute(SQLUtil.build_insert_statement(TABLE, link_dict))
	return ""

def link_exists(link_id):
	return int(conn.execute("SELECT COUNT(link_id) FROM {} WHERE link_id = {};".format(TABLE, int(link_id))).fetchall()[0][0]) != 0

def relationship_exists(node_id_1, node_id_2):
	return int(conn.execute("SELECT COUNT(link_id) FROM {} WHERE node_id_1 = {} AND node_id_2 = {}".format(TABLE, node_id_1, node_id_2)).fetchall()[0][0]) != 0

def get_links():
	links = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (links.keys()) ,i)) for i in links.cursor]}

def get_link(link_id):
	link = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s WHERE link_id = %d" % (TABLE, int(link_id)))
	return {'data': [dict(zip(tuple (link.keys()) ,i)) for i in link.cursor]}

def change_link(link_id, link_dict, torn):

	if link_exists(link_id) == False:
		torn.write({"message":"Link does not exist"})
		return None

	check = True
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
		return None

	if link_dict["node_id_1"] == link_dict["node_id_2"]:
		torn.write({"message":"Links from and to the same node are not allowed"})
		return None

	link_dict = sort_node_ids(link_dict)

	if relationship_exists(link_dict["node_id_1"], link_dict["node_id_2"]):
		torn.write({"message":"Link between the two nodes already exists"})
		return None
	conn.execute(SQLUtil.build_update_statement(TABLE, link_dict) + " WHERE link_id = %d;" % (int(link_id)))
	return ""

def sort_node_ids(link_dict):
	if link_dict["node_id_1"] > link_dict["node_id_2"]:
		temp = int(link_dict["node_id_1"])
		link_dict["node_id_1"] = int(link_dict["node_id_2"])
		link_dict["node_id_2"] = temp
	return link_dict

def delete_link(link_id, torn):
	if link_exists(link_id) == False:
		torn.write({"message":"Link does not exist"})
		return None
	conn.execute("DELETE FROM {} WHERE link_id = {}".format(TABLE, int(link_id)))
	return ""

def check_nodes_exist(node_id_1, node_id_2):
	if NodeUtil.node_id_exists(node_id_1) == False or NodeUtil.node_id_exists(node_id_2) == False:
		return False
	return True

def get_node_ids_in_link(link_id):
	return conn.execute("SELECT node_id_1, node_id_2 FROM {} WHERE link_id = {}".format(TABLE, int(link_id))).fetchall()[0]