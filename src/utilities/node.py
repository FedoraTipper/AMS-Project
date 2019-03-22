import handlers.mysqldb as dbhandler
import utilities.label as labelutil
import utilities.view as viewutil
import utilities.type as typeutil
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as flhandler

session = dbhandler.create_session()

def create_node(node_dict, torn):
	"""
	Function to create a node in the database
	Inputs: Dictionary of node data, Tornado object to write data
	Output: True if operation was successful, False if the operation was not
	Caveats: Check if the node type already exists
	"""
	if typeutil.type_id_exists(node_dict["type_id"]) == False:
		torn.set_status(404)
		torn.write({'message': "Type ID does not exist"})
		return False

	if viewutil.view_id_exists(node_dict["view_id"]) == False:
		torn.set_status(404)
		torn.write({'message': "View ID does not exist"})
		return False

	node = TableEntities.Nodes(type_id=node_dict["type_id"], view_id=node_dict["view_id"])
	
	if "label_id" in node_dict:
		if labelutil.label_id_exists(node_dict["label_id"]) == False:
			torn.set_status(404)
			torn.write({"message": "Label ID does not exist"})
			return False
		else: 
			node.label_id = int(node_dict["label_id"])

	if "icon" in node_dict:
		node.icon = node_dict["icon"]

	try:
		session.add(node)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False

	node_id = session.query(TableEntities.Nodes).order_by(TableEntities.Nodes.node_id.desc()).first()
	#create metadata category for type of node
	type_name = typeutil.get_type(node_dict["type_id"])["data"][0]["type"]
	import utilities.meta as metadatautil
	metadata_dict = {"node_id": int(node_id.node_id), "category":"Type", "data": type_name}
	metadatautil.create_type_category(metadata_dict)
	return node_id.node_id

def node_id_exists(node_id):
	"""
	Function to determine if the node ID exists
	Inputs: Node ID int
	Output: Boolean value - (True if the node id exists)
	Caveats: None
	"""
	return int(session.query(TableEntities.Nodes).filter(
			TableEntities.Nodes.node_id == int(node_id)).count()) != 0

def get_nodes():
	"""
	Function to return all nodes from the database
	Inputs: None
	Output: JSON formatted string of column names and respective values
	Caveats: None
	"""
	entries = session.query(TableEntities.Nodes).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_node(node_id):
	"""
	Function to get a single node's data from the database
	Inputs: Node ID in int format
	Output: JSON formatted string of column names and respective values
	Caveats: None
	"""
	entries = session.query(TableEntities.Nodes).filter(TableEntities.Nodes.node_id == int(node_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_node_id(node_type):
	"""
	Function to return a node's ID
	Inputs: Node type string
	Output: Node ID in int format
	Caveats: None
	"""
	return  session.query(TableEntities.Nodes).filter(TableEntities.Nodes.node_type == node_type).one().node_id

def change_node(node_id, node_dict, torn):
	"""
	Function to change a node's information that is stored in the database
	Inputs: Node ID; Dictionary of columns and values that will be ammended to the record; Tornado object
	Output: True if operation was successful, False if the operation was not
	Caveats: Check if the node and any FK objects exists
	"""
	if node_id_exists(node_id) == False:
		torn.set_status(404)
		torn.write({'message': "Node does not exist"})
		return False

	if "type" in node_dict:
		if typeutil.type_id_exists(node_dict["type"]) == False:
			torn.set_status(404)
			torn.write({'message': "Type ID does not exist"})
			return False

	if "label_id" in node_dict:
		if labelutil.label_id_exists(node_dict["label_id"]) == False:
			torn.set_status(404)
			torn.write({"message": "Label id does not exist"})
			return False

	if "view_id" in node_dict:
		if viewutil.view_id_exists(node_dict["view_id"]) == False:
			torn.set_status(404)
			torn.write({'message': "View ID does not exist"})
			return False

	try:
		session.execute(
			update(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node_id)).values(node_dict)
			)	
		session.commit()
		if("type_id" in node_dict):
			type_name = typeutil.get_type(node_dict["type_id"])["data"][0]["type"]
			import utilities.meta as metadatautil
			metadata_id = metadatautil.get_metadata_id("Type", node_id)
			metadata_dict = {"node_id": node_id, "category":"Type", "data": type_name}
			metadatautil.change_metadata_internal(metadata_id, metadata_dict)
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False

	return True

def delete_node(node_id, torn):
	"""
	Function to delete a node record from the database table
	Inputs: Node ID; Tornado object to write any messages
	Output: True if operation was successful, False if the operation was not
	Caveats: Check if the node id already exists
	"""
	if node_id_exists(node_id) == False:
		torn.set_status(404)
		torn.write({"message":"Node does not exist"})
		return False
	#Import module in function. Not allowed to cross reference
	import utilities.link as linkutil
	#Delete all links that contain the node id
	linkutil.delete_link_with_node(node_id)
	import utilities.meta as MetaUtil
	MetaUtil.delete_metadata_with_node(node_id)
	#Delete the node
	try:
		session.execute(
			delete(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node_id))
			)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False

	return True

def delete_node_with_view(view_id, torn):
	"""
	Function to delete a node which depends on a view
	Inputs: View_ID; Tornado object to write any messages
	Output: True if operation was successful, False if the operation was not
	Caveats: Delete links and metadata alongside
	"""
	node_entries = session.query(TableEntities.Nodes).filter(TableEntities.Nodes.view_id == int(view_id)).all()
	#Import module in function. Not allowed to cross reference
	import utilities.link as linkutil
	import utilities.meta as MetaUtil

	for node in node_entries:
		linkutil.delete_link_with_node(node.node_id)
		MetaUtil.delete_metadata_with_node(node.node_id)
		try:
			session.execute(
				delete(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node.node_id))
				)
			session.commit()
		except exc.SQLAlchemyError as Error:
			torn.set_status(500)
			flhandler.log_error_to_file(Error)
			return False
	return True

def delete_node_with_type(type_id, torn):
	"""
	Function to delete a node which depends on a node type
	Inputs: type; Tornado object to write any messages
	Output: True if operation was successful, False if the operation was not
	Caveats: Delete links and metadata alongside
	"""
	node_entries = session.query(TableEntities.Nodes).filter(TableEntities.Nodes.type_id == int(type_id)).all()
	#Import module in function. Not allowed to cross reference
	import utilities.link as linkutil
	import utilities.meta as MetaUtil

	for node in node_entries:
		linkutil.delete_link_with_node(node.node_id)
		MetaUtil.delete_metadata_with_node(node.node_id)
		try:
			session.execute(
				delete(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node.node_id))
				)
			session.commit()
		except exc.SQLAlchemyError as Error:
			torn.set_status(500)
			flhandler.log_error_to_file(Error)
			return False
	return True
