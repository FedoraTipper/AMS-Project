import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil

conn = DBHandler.create_connection()


TABLE = "relationship"

def get_relationship(relationship_id):
	relationship = conn.execute("SELECT relationship_id, message FROM {} WHERE relationship_id = {}" % (TABLE, int(relationship_id)))
	return {'data': [dict(zip(tuple (relationships.keys()) ,i)) for i in relationships.cursor]}

def get_relationships():
	relationships = conn.execute("SELECT relationship_id, message FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (relationships.keys()) ,i)) for i in relationships.cursor]}

def create_relationship(relationship_dict, torn):
	if relationship_exists(relationship_dict["message"]):
		torn.write({"message":"Relationship message already exists"})
		return None
	conn.execute(SQLUtil.build_insert_statement(TABLE, relationship_dict))
	return ""

def relationship_exists(message):
	return int(conn.execute("SELECT COUNT(relationship_id) FROM {} WHERE message = '{}';".format(TABLE, message)).fetchall()[0][0]) != 0

def relationship_id_exists(relationship_id):
	return int(conn.execute("SELECT COUNT(relationship_id) FROM {} WHERE relationship_id = {};".format(TABLE, int(relationship_id))).fetchall()[0][0]) != 0

def change_relationship(relationship_id, relationship_dict, torn):
	if relationship_id_exists(relationship_id) == False:
		torn.write({"message":"Relationship does not exists"})
		return None

	if relationship_exists(relationship_dict["message"]):
		torn.write({"message":"New relationship message exists"})
		return None

	conn.execute(SQL.build_update_statement(TABLE, relationship_dict) + " WHERE relationship_id = {}".format(int(relationship_id)))

def delete_relationship(relationship_id, torn):
	if relationship_id_exists(relationship_id) == False:
		torn.write({"message": "Relationship id does not exist"})
		return None
	tables = {"links"}
	null_dict = {"relationship_id": None}
	#Create SQL statements to set relationship ID in FK tables to NULL
	statements = SQLUtil.build_nullify_statements(tables, null_dict)
	statements.append("DELETE FROM {}".format(TABLE))
	
	for sql_statement in statements:
		conn.execute(sql_statement + " WHERE relationship_id = {};".format(int(relationship_id)))

	return ""