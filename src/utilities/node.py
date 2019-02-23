import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
conn = DBHandler.create_connection()

TABLE = "nodes"

def create_node(node_type, user_id):
	conn.execute("INSERT INTO %s (type, user_id) VALUES ('%s', %d);" % (TABLE, node_type, int(user_id)))

def node_exists(node_type):
	return int(conn.execute("SELECT COUNT(node_id) FROM %s WHERE type = '%s';" %(TABLE, node_type)).fetchall()[0][0]) != 0

def get_nodes():
	nodes = conn.execute("SELECT node_id, type, label_id FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (nodes.keys()) ,i)) for i in nodes.cursor]}

def get_node(node_id):
	node = conn.execute("SELECT node_id, type, label_id FROM %s WHERE node_id = %d" % (TABLE, int(node_id)))
	return {'data': [dict(zip(tuple (node.keys()) ,i)) for i in node.cursor]}

def add_label(node_id, label_id):
	conn.execute("UPDATE %s SET label_id = '%s'")


def change_node(node_id, node_dict):
	statement = SQLUtil.build_update_statement(TABLE, node_dict) + " WHERE node_id = %d;" % node_id
	conn.execute(statement)