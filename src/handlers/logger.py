import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil

conn = DBHandler.create_connection()

_table_ = "logs"

_message_format_ = {"add":"({user_data}) added {field} {field_id}; values: {vals}",
			"change":"({user_data}) changed {field} {field_id}; Changed values: {vals}",
			"delete":"({user_data}) deleted {field} {field_id};"}

def log_message(format, message_dict):
	message = _message_format_[format]
	for key in message_dict:
		if "{" + key + "}" in message:
			message = message.replace("{" + key + "}", message_dict[key])
	statement = SQLUtil.build_insert_statement(_table_, {"message":message})
	conn.execute(statement)
	return "Success"

"""
Utility function used to help form the correct message format in other api functions
"""
def form_message_dictionary(user_data, field, field_id, vals):
	result_dict = {"user_data":"", "field":field, "field_id": str(field_id), "vals":""}

	for key in user_data:
		result_dict["user_data"] += "{}: {}, ".format(key, str(user_data[key]))
	
	result_dict["user_data"] = result_dict["user_data"][:-2]

	for key in vals:
		result_dict["vals"] += "{} = {}, ".format(key, str(vals[key]))

	result_dict["vals"] = result_dict["vals"][:-2]

	return result_dict

def form_delete_message_dictionary(user_data, field, field_id):
	result_dict = {"user_data":"", "field":field, "field_id": str(field_id)}

	for key in user_data:
		result_dict["user_data"] += "{}: {}, ".format(key, str(user_data[key]))
	
	result_dict["user_data"] = result_dict["user_data"][:-2]

	return result_dict

def get_logs():
	logs = conn.execute("SELECT message FROM %s" % (_table_))
	return {'data': [dict(zip(tuple (logs.keys()) ,i)) for i in logs.cursor]}