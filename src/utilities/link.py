import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
conn = DBHandler.create_connection()

TABLE = "links"

def create_link(link_dict):
	conn.execute(SQLUtil.build_insert_statement(TABLE, link_dict))

def get_links():
	links = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (links.keys()) ,i)) for i in links.cursor]}

def get_link(link_id):
	link = conn.execute("SELECT link_id, node_id_1, node_id_2, label_id FROM %s WHERE link_id = %d" % (TABLE, int(link_id)))
	return {'data': [dict(zip(tuple (link.keys()) ,i)) for i in link.cursor]}

def change_link(link_id, link_dict):
	statement = SQLUtil.build_update_statement(TABLE, link_dict) + " WHERE link_id = %d;" % (int(link_id))
	conn.execute(statement)