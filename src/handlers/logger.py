import handlers.mysqldb as dbhandler
import utilities.sql as sqlutil
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import exc

session = dbhandler.create_session()

_message_format_ = {"add":"({user_data}) added {field} {field_id}; values: {vals}",
			"change":"({user_data}) changed {field} {field_id}; Changed values: {vals}",
			"delete":"({user_data}) deleted {field} {field_id};"}

def log_message(format, message_dict):
	"""
	Function to log a message to the database
	Inputs: message format, dictionary of message variables
	Output: Success message
	Caveats: Variables replace {} areas within message formats
	"""
	message = _message_format_[format]
	for key in message_dict:
		if "{" + key + "}" in message:
			message = message.replace("{" + key + "}", message_dict[key])
	try:
		session.add(TableEntities.Log(message=message))
		session.commit()
	except exc.SQLAlchemyError as Error:
		print(Error)
		print("Something went wrong. <Log add>")
		return False
	return "Success"

def form_message_dictionary(user_data, field, field_id, vals):
	"""
	Function to help form a message dictionary to log to the database
	Inputs: User data, field, field id, dictionary of values 
	Output: Dictionary which can be used for log_message
	Caveats: Used for add and updating API calls
	"""
	result_dict = {"user_data":"", "field":field, "field_id": str(field_id), "vals":""}

	for key in user_data:
		result_dict["user_data"] += "{}: {}, ".format(key, str(user_data[key]))
	
	result_dict["user_data"] = result_dict["user_data"][:-2]
	for key in vals:
		result_dict["vals"] += "{} = {}, ".format(key, str(vals[key]))

	result_dict["vals"] = result_dict["vals"][:-2]

	return result_dict

def form_delete_message_dictionary(user_data, field, field_id):
	"""
	Function to help form a message dictionary to log to the database
	Inputs: User data, field, field id
	Output: Dictionary which can be used for log_message
	Caveats: Used for delete API calls only
	"""
	result_dict = {"user_data":"", "field":field, "field_id": str(field_id)}

	for key in user_data:
		result_dict["user_data"] += "{}: {}, ".format(key, str(user_data[key]))
	
	result_dict["user_data"] = result_dict["user_data"][:-2]

	return result_dict

def get_logs():
	"""
	Function to return all rows from table logs in the database
	Inputs: None
	Output: Dictionary of log messages
	Caveats: None
	"""
	entries = session.query(TableEntities.Log).all()
	return {'data': [entry.as_dict() for entry in entries]}

