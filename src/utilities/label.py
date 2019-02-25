import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil

conn = DBHandler.create_connection()

TABLE = "labels"

def create_label(label_dict, torn):
	if label_exists(labels_dict["label_text"]):
		torn.write({'message': "Label exists"})
		return None
	conn.execute(SQLUtil.build_insert_statement(TABLE, label_dict))
	#Return random object that is not None
	return ""


def label_exists(label_text):
	return int(conn.execute("SELECT COUNT(label_text) FROM %s WHERE label_text = '%s';" % (TABLE, label_text)).fetchall()[0][0]) != 0

"""
Returns json string of all labels
"""
def get_labels():
	labels = conn.execute("SELECT label_id, label_text FROM %s" % (TABLE))
	return {'data': [dict(zip(tuple (labels.keys()) ,i)) for i in labels.cursor]}

def get_label(label_id):
	label = conn.execute("SELECT label_text FROM %s WHERE label_id = %d" % (TABLE, int(label_id)))
	return {'data': [dict(zip(tuple (label.keys()) ,i)) for i in label.cursor]}

def change_label(label_id, label_dict, torn):
	if label_exists(label_id) == False:
		torn.write({'message': "Label does not exist"})
		return None
	statement = SQLUtil.build_update_statement(TABLE, label_dict) + " WHERE label_id = %d;" % label_id
	conn.execute(statement)
	return ""