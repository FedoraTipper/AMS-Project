import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import utilities.label as LabelUtil
conn = DBHandler.create_connection()

_table_ = "nodes"

def create_node(node_dict, torn):
	if node_exists(node_dict["type"]):
		torn.write({'message': "Node type exists"})
		return None
	conn.execute(SQLUtil.build_insert_statement(_table_, node_dict))
	return ""

def node_exists(node_type):
	return int(conn.execute("SELECT COUNT(node_id) FROM %s WHERE type = '%s';" %(_table_, node_type)).fetchall()[0][0]) != 0

def node_id_exists(node_id):
	return int(conn.execute("SELECT COUNT(node_id) FROM %s WHERE node_id = %d;" %(_table_, int(node_id))).fetchall()[0][0]) != 0

def get_nodes():
	nodes = conn.execute("SELECT node_id, type, label_id FROM %s" % (_table_))
	return {'data': [dict(zip(tuple (nodes.keys()) ,i)) for i in nodes.cursor]}

def get_node(node_id):
	node = conn.execute("SELECT node_id, type, label_id FROM %s WHERE node_id = %d" % (_table_, int(node_id)))
	return {'data': [dict(zip(tuple (node.keys()) ,i)) for i in node.cursor]}

def get_node_id(node_type):
	return(conn.execute("SELECT node_id FROM {} WHERE type = '{}'".format(_table_, node_type)).fetchall()[0][0])

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
	return ""