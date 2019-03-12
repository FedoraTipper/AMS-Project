import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import utilities.node as NodeUtil
conn = DBHandler.create_connection()

_table_ = "metadata"

def create_category(metadata_dict, torn):
	if NodeUtil.node_id_exists(metadata_dict["node_id"]) == False:
		torn.write({"message": "Node does not exist"})
		return False

	if category_exists(metadata_dict["category"], metadata_dict["node_id"]):
		torn.write({"message": "Metadata category for the specified node already exists"})
		return False

	conn.execute(SQLUtil.build_insert_statement(_table_, metadata_dict))
	return ""

def category_exists(category, node_id):
	return int(conn.execute("SELECT COUNT(meta_id) FROM %s WHERE category = '%s' AND node_id = %d;" %(_table_, category, int(node_id))).fetchall()[0][0]) != 0

def metadata_exists(metadata_id):
	return int(conn.execute("SELECT COUNT(meta_id) FROM %s WHERE meta_id = %d;" % (_table_, int(metadata_id))).fetchall()[0][0]) != 0

def get_all_metadata():
	metadata = conn.execute("SELECT meta_id, category, metadata, node_id FROM %s;" % (_table_))
	return {'data': [dict(zip(tuple (metadata.keys()) ,i)) for i in metadata.cursor]}

def get_metadata(node_id):
	metadata = conn.execute("SELECT meta_id, category, metadata, node_id FROM %s WHERE node_id = %d;" % (_table_, int(node_id)))
	return {'data': [dict(zip(tuple (metadata.keys()) ,i)) for i in metadata.cursor]}

def get_metadata_id(category, node_id):
	return(conn.execute("SELECT meta_id FROM {} WHERE node_id = {} AND category = '{}';".format(_table_, int(node_id), category)).fetchall()[0][0])

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

	return ""

def delete_metadata(metadata_id, torn):
	if metadata_exists(metadata_id) == False:
		torn.write({"message": "Node does not exist"})
		return False
	conn.execute("DELETE FROM {} WHERE meta_id = {}".format(_table_, metadata_id))
	return False

def delete_metadata_with_node(node_id):
	conn.execute("DELETE FROM {} WHERE node_id = {}".format(_table_, int(node_id)))