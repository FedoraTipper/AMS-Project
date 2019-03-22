import handlers.mysqldb as dbhandler
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as flhandler


session = dbhandler.create_session()

def create_view(view_dict, torn):
	"""
	Function to create a view in the database
	Inputs: Dictionary of view data, Tornado object to write data
	Output: True if operation was successful, False if the operation was not
	Caveats: Check if the view name already exists
	"""
	if view_exists(view_dict["name"]):
		torn.set_status(400)
		torn.write({'message': "View name already exists"})
		return False
	
	try:
		session.add(TableEntities.View(name=view_dict["name"]))
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False

	return True

def view_exists(name):
	"""
	Function to determine if the view exists by the name
	Inputs: Name
	Output: Boolean value - (True if the view name exists)
	Caveats: None
	"""
	return int(session.query(TableEntities.View).filter(
			TableEntities.View.name == name).count()) != 0

def view_id_exists(view_id):
	"""
	Function to determine if the view ID exists
	Inputs: view ID int
	Output: Boolean value - (True if the view id exists)
	Caveats: None
	"""
	return int(session.query(TableEntities.View).filter(
			TableEntities.View.view_id == int(view_id)).count()) != 0

def get_views():
	"""
	Function to return all views from the database
	Inputs: None
	Output: JSON formatted string of column names and respective values
	Caveats: None
	"""
	entries = session.query(TableEntities.View).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_view(view_id):
	"""
	Function to return a view from the database
	Inputs: None
	Output: JSON formatted string of column names and respective values
	Caveats: None
	"""
	entries = session.query(TableEntities.View).filter(TableEntities.View.view_id == int(view_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_view_id(name):
	"""
	Function to return a view name's ID
	Inputs: View name
	Output: View ID in int format
	Caveats: None
	"""
	return  session.query(TableEntities.View).filter(TableEntities.View.name == name).one().view_id

def change_view(view_id, view_dict, torn):
	"""
	Function to change a view's information
	Inputs: View ID; Dictionary of columns and values that will be ammended to the record; Tornado object
	Output: True if operation was successful, False if the operation was not
	Caveats: Check if the the view name already exists
	"""
	if view_id_exists(view_id) == False:
		torn.set_status(404)
		torn.write({"message": "View does not exist"})
		return False

	if (view_dict["name"] is None):
		torn.write({"message": "Empty update statement"})
		return False
	else:
		if (view_exists(view_dict["name"])):
			torn.set_status(400)
			torn.write({"message": "New view name already exists"})
			return False
	try:
		session.execute(
			update(TableEntities.View).where(TableEntities.View.view_id == int(view_id)).values(view_dict)
			)	
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False
	return True

def delete_view(view_id, torn):
	"""
	Function to delete a view record from the database table
	Inputs: View ID; Tornado object to write any messages
	Output: True if operation was successful, False if the operation was not
	Caveats: This will delete all dependancy's to the view as well
	"""
	if view_id_exists(view_id) == False:
		torn.set_status(404)
		torn.write({"message": "View does not exist"})
		return False

	try:
		import utilities.node as nodeutil
		#Delete all objects dependant on the view that will be deleted
		#Deleting a node will remove the link and the metadata as well
		nodeutil.delete_node_with_view(view_id, torn)

		#Delete the view itself
		session.execute(
			delete(TableEntities.View).where(TableEntities.View.view_id == int(view_id))
			)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False
	return True