import handlers.mysqldb as DBHandler
import utilities.label as LabelUtil
import utilities.view as ViewUtil
import utilities.type as TypeUtil
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as FLHandler

session = DBHandler.create_session()

"""
Function to create a node in the database
Inputs: Dictionary of node data, Tornado object to write data
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node type already exists
"""
def create_node(node_dict, torn):
	if TypeUtil.type_id_exists(node_dict["type_id"]) == False:
		torn.set_status(404)
		torn.write({'message': "Type ID does not exist"})
		return False

	if ViewUtil.view_id_exists(node_dict["view_id"]) == False:
		torn.set_status(404)
		torn.write({'message': "View ID does not exist"})
		return False

	node = TableEntities.Nodes(type_id=node_dict["type_id"], view_id=node_dict["view_id"])
	
	if "label_id" in node_dict:
		if LabelUtil.label_id_exists(node_dict["label_id"]) == False:
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
		FLHandler.log_error_to_file(Error)
		return False

	node_id = session.query(TableEntities.Nodes).order_by(TableEntities.Nodes.node_id.desc()).first()
	#create metadata category for type of node
	type_name = TypeUtil.get_type(node_dict["type_id"])["data"][0]["type"]
	import utilities.meta as MetadataUtil
	metadata_dict = {"node_id": int(node_id.node_id), "category":"Type", "data": type_name}
	MetadataUtil.create_type_category(metadata_dict)
	return node_id.node_id

"""
Function to determine if the node ID exists
Inputs: Node ID int
Output: Boolean value - (True if the node id exists)
Caveats: None
"""
def node_id_exists(node_id):
	return int(session.query(TableEntities.Nodes).filter(
			TableEntities.Nodes.node_id == int(node_id)).count()) != 0

"""
Function to return all nodes from the database
Inputs: None
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_nodes():
	entries = session.query(TableEntities.Nodes).all()
	return {'data': [entry.as_dict() for entry in entries]}
"""
Function to get a single node's data from the database
Inputs: Node ID in int format
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_node(node_id):
	entries = session.query(TableEntities.Nodes).filter(TableEntities.Nodes.node_id == int(node_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to return a node's ID
Inputs: Node type string
Output: Node ID in int format
Caveats: None
"""
def get_node_id(node_type):
	return  session.query(TableEntities.Nodes).filter(TableEntities.Nodes.node_type == node_type).one().node_id

"""
Function to change a node's information that is stored in the database
Inputs: Node ID; Dictionary of columns and values that will be ammended to the record; Tornado object
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node and any FK objects exists
"""
def change_node(node_id, node_dict, torn):
	if node_id_exists(node_id) == False:
		torn.set_status(404)
		torn.write({'message': "Node does not exist"})
		return False

	if "type" in node_dict:
		if TypeUtil.type_id_exists(node_dict["type"]) == False:
			torn.set_status(404)
			torn.write({'message': "Type ID does not exist"})
			return False

	if "label_id" in node_dict:
		if LabelUtil.label_id_exists(node_dict["label_id"]) == False:
			torn.set_status(404)
			torn.write({"message": "Label id does not exist"})
			return False

	if "view_id" in node_dict:
		if ViewUtil.view_id_exists(node_dict["view_id"]) == False:
			torn.set_status(404)
			torn.write({'message': "View ID does not exist"})
			return False

	try:
		session.execute(
			update(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node_id)).values(node_dict)
			)	
		session.commit()

		type_name = TypeUtil.get_type(node_dict["type_id"])["data"][0]["type"]
		import utilities.meta as MetadataUtil
		metadata_id = MetadataUtil.get_metadata_id("Type", node_id)
		metadata_dict = {"node_id": node_id, "category":"Type", "data": type_name}
		MetadataUtil.change_metadata_internal(metadata_id, metadata_dict)
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False

	return True

"""
Function to delete a node record from the database table
Inputs: Node ID; Tornado object to write any messages
Output: True if operation was successful, False if the operation was not
Caveats: Check if the node id already exists
"""
def delete_node(node_id, torn):
	if node_id_exists(node_id) == False:
		torn.set_status(404)
		torn.write({"message":"Node does not exist"})
		return False
	#Import module in function. Not allowed to cross reference
	import utilities.link as LinkUtil
	#Delete all links that contain the node id
	LinkUtil.delete_link_with_node(node_id)
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
		FLHandler.log_error_to_file(Error)
		return False

	return True

"""
Function to delete a node which depends on a view
Inputs: View_ID; Tornado object to write any messages
Output: True if operation was successful, False if the operation was not
Caveats: Delete links and metadata alongside
"""
def delete_node_with_view(view_id, torn):
	node_entries = session.query(TableEntities.Nodes).filter(TableEntities.Nodes.view_id == int(view_id)).all()
	#Import module in function. Not allowed to cross reference
	import utilities.link as LinkUtil
	import utilities.meta as MetaUtil

	for node in node_entries:
		LinkUtil.delete_link_with_node(node.node_id)
		MetaUtil.delete_metadata_with_node(node.node_id)
		try:
			session.execute(
				delete(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node.node_id))
				)
			session.commit()
		except exc.SQLAlchemyError as Error:
			torn.set_status(500)
			FLHandler.log_error_to_file(Error)
			return False
	return True

"""
Function to delete a node which depends on a node type
Inputs: type; Tornado object to write any messages
Output: True if operation was successful, False if the operation was not
Caveats: Delete links and metadata alongside
"""
def delete_node_with_type(type_id, torn):
	node_entries = session.query(TableEntities.Nodes).filter(TableEntities.Nodes.type_id == int(type_id)).all()
	#Import module in function. Not allowed to cross reference
	import utilities.link as LinkUtil
	import utilities.meta as MetaUtil

	for node in node_entries:
		LinkUtil.delete_link_with_node(node.node_id)
		MetaUtil.delete_metadata_with_node(node.node_id)
		try:
			session.execute(
				delete(TableEntities.Nodes).where(TableEntities.Nodes.node_id == int(node.node_id))
				)
			session.commit()
		except exc.SQLAlchemyError as Error:
			torn.set_status(500)
			FLHandler.log_error_to_file(Error)
			return False
	return True
