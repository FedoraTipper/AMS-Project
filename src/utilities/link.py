import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
conn = DBHandler.create_connection()

TABLE = "links"

"""
Node ids are stored in ascending order
"""
def create_link(link_dict, torn):
	link_dict = sort_node_ids(link_dict)

	if link_dict["node_id_1"] == link_dict["node_id_2"]:
		torn.write({"message":"Links from and to the same node are not allowed"})
		return None

	if relationship_exists(link_dict["node_id_1"], link_dict["node_id_2"]):
		torn.write({"message":"Link between the two nodes already exists"})
		return None

	conn.execute(SQLUtil.build_insert_statement(TABLE, link_dict))
	return ""

def link_exists(link_id):
	return int(conn.execute("SELECT COUNT(link_id) FROM {} WHERE link_id = {};".format(TABLE, int(link_id))).fetchall()[0][0]) != 0

def relationship_exists(node_id_1, node_id_2):
	return int(conn.execute("SELECT COUNT(link_id) FROM {} WHERE node_id_1 = {} AND node_id_2 = {}")) != 0

def get_links():
	links = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (links.keys()) ,i)) for i in links.cursor]}

def get_link(link_id):
	link = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s WHERE link_id = %d" % (TABLE, int(link_id)))
	return {'data': [dict(zip(tuple (link.keys()) ,i)) for i in link.cursor]}

def change_link(link_id, link_dict):
	link_dict = sort_node_ids(link_dict)
	if link_exists(link_id) == False:
		torn.write({"message":"Link does not exist"})
		return None
	if relationship_exists(link_dict["node_id_1"], link_dict["node_id_2"]):
		torn.write({"message":"Link between the two nodes already exists"})
		return None
	statement = SQLUtil.build_update_statement(TABLE, link_dict) + " WHERE link_id = %d;" % (int(link_id))
	conn.execute(statement)
	return ""

def sort_node_ids(link_dict):
	if link_dict["node_id_1"] > link_dict["node_id_2"]:
		temp = int(link_dict["node_id_1"])
		link_dict["node_id_1"] = int(link_dict["node_id_2"])
		link_dict["node_id_2"] = temp
	return link_dict

def delete_link(link_id):
	if link_exists(link_id) == False:
		torn.write({"message":"Link does not exist"})
		return None
	conn.execute("DELETE FROM {} WHERE link_id = {}".format(TABLE, int(link_id)))
	return ""