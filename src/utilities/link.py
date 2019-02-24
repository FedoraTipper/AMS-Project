import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
conn = DBHandler.create_connection()
TABLE = "links"

def create_link(node_dict):
	query = SQLUtil.build_insert_statement(TABLE, node_dict)
	print(query)
	conn.execute(query)

def get_links():
	links = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (links.keys()) ,i)) for i in links.cursor]}

def get_link(link_id):
	link = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s WHERE link_id = %d" % (TABLE, int(link_id)))
	return {'data': [dict(zip(tuple (link.keys()) ,i)) for i in link.cursor]}