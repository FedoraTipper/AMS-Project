import handlers.mysqldb as DBHandler
import utilities.node as NodeUtil
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as FLHandler

session = DBHandler.create_session()


"""
Function to create metadata category for a specified node
Inputs: Dictionary of metadata; Tornado object to write messages
Output: True if insert operation was successful, False if the operation was not
Caveats: Check if the node and if the category for that node already exists
"""
def create_category(metadata_dict, torn):
	if NodeUtil.node_id_exists(metadata_dict["node_id"]) == False:
		torn.set_status(404)
		torn.write({"message": "Node does not exist"})
		return False

	if category_exists(metadata_dict["category"], metadata_dict["node_id"]):
		torn.set_status(400)
		torn.write({"message": "Metadata category for the specified node already exists"})
		return False

	try:
		session.add(TableEntities.Metadata(node_id=int(metadata_dict["node_id"]), category=metadata_dict["category"],
					data=metadata_dict["data"]))
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False
	return True

"""
Function to determine if a metadata category for a node already exists
Inputs: Category string; Node ID int
Output: Boolean value - (True indicates category for the node exists)
Caveats: None
"""
def category_exists(category, node_id):
	return int(session.query(TableEntities.Metadata).filter(
							(TableEntities.Metadata.category == category) & 
							(TableEntities.Metadata.node_id == int(node_id))).count()) != 0

"""
Function to determine if a metadata record exists in the database
Inputs: Metadata ID int format
Output: Boolean value - (True indicates that the id exists)
Caveats: None
"""
def metadata_exists(metadata_id):
	return int(session.query(TableEntities.Metadata).filter(
							TableEntities.Metadata.meta_id == int(metadata_id)).count()) != 0

"""
Function to get all metadata records from the database
Inputs: None
Output: JSON formatted string of all metadata records
Caveats: None
"""
def get_all_metadata():
	entries = session.query(TableEntities.Metadata).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to get a single metadata record from the database
Inputs: Node ID
Output: JSON formatted string of metadata records for specified node
Caveats: None
"""
def get_metadata(node_id):
	entries = session.query(TableEntities.Metadata).filter(TableEntities.Metadata.node_id == int(node_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to retrieve a metadata's id given the node ID and category
Inputs: Category string; Node ID
Output: Metadata id int 
Caveats: None
"""
def get_metadata_id(category, node_id):
	return  (session.query(TableEntities.Metadata).filter((TableEntities.Metadata.category == category) & 
			(TableEntities.Metadata.node_id == int(node_id))).one().meta_id)

"""
Function to change a metadata record in the database
Inputs: Metadata ID; Metadata Dictionary of all values that will be changed; Tornado object for writing messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine the existance of metadata record, node id and category before change
"""
def change_metadata(metadata_id, metadata_dict, torn):
	if metadata_exists(metadata_id) == False:
		torn.set_status(404)
		torn.write({"message": "Metadata ID does not exist"})
		return False

	if "node_id" in metadata_dict:
		if NodeUtil.node_id_exists(metadata_dict["node_id"]) == False:
			torn.set_status(404)
			torn.write({"message": "Node does not exist"})
			return False

	if "category" in metadata_dict:
		if category_exists(metadata_dict["category"], metadata_dict["node_id"]):
			torn.set_status(400)
			torn.write({"message": "Metadata category already exists"})
			return False
	try:
		session.execute(
			update(TableEntities.Metadata).where(TableEntities.Metadata.metadata_id == int(metadata_id)).values(metadata_dict)
			)	
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False
	return True

"""
Function to delete a metadata record from the database
Inputs: Metadata ID; Tornado object to write messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine the existance of metadata record
"""
def delete_metadata(metadata_id, torn):
	if metadata_exists(metadata_id) == False:
		torn.set_status(404)
		torn.write({"message": "Node does not exist"})
		return False
	try:
		session.execute(
			delete(TableEntities.Metadata).where(TableEntities.Metadata.metadata_id == int(metadata_id))
			)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False
	return True

"""
Function to delete all metadata records that belong to a single node
Inputs: Node ID
Output: None
Caveats: Returns none as this function is seen as "best effort"
"""
def delete_metadata_with_node(node_id):
	try:
		session.execute(
			delete(TableEntities.Metadata).where(TableEntities.Metadata.node_id == int(node_id))
			)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False