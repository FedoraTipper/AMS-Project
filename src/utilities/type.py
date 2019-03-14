import handlers.mysqldb as DBHandler
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as FLHandler

session = DBHandler.create_session()


def create_type(type_dict, torn):
	if type_exists(type_dict["type"]):
		torn.set_status(400)
		torn.write({'message': "Node type already exists"})
		return False
	
	try:
		session.add(TableEntities.NodeType(type=type_dict["type"]))
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False

	return True

def type_exists(type):
	return int(session.query(TableEntities.NodeType).filter(
			TableEntities.NodeType.type == type).count()) != 0

def type_id_exists(type_id):
	return int(session.query(TableEntities.NodeType).filter(
			TableEntities.NodeType.type_id == type_id).count()) != 0

def get_types():
	entries = session.query(TableEntities.NodeType).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_type(type_id):
	entries = session.query(TableEntities.NodeType).filter(TableEntities.NodeType.type_id == int(type_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_type_id(type):
	return  session.query(TableEntities.NodeType).filter(TableEntities.NodeType.type == type).one().type_id

def change_type(type_id, type_dict, torn):
	if type_id_exists(type_id) == False:
		torn.set_status(404)
		torn.write({"message": "Node Type does not exist"})
		return False

	if (type_dict["type"] is None):
		torn.set_status(400)
		torn.write({"message": "Empty update statement"})
		return False
	
	if (type_exists(type_dict["type"])):
			torn.set_status(400)
			torn.write({"message": "New node type already exists"})
			return False

	try:
		session.execute(
			update(TableEntities.NodeType).where(TableEntities.NodeType.type_id == int(type_id))
			.values(type_dict)
			)	
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False
	return True

def delete_type(type_id, torn):
	if type_id_exists(type_id) == False:
		torn.set_status(404)
		torn.write({"message": "Node type ID does not exist"})
		return False

	try:
		import utilities.node as NodeUtil
		#Delete all objects dependant on the node type that will be deleted
		#Deleting a node will remove the link and metadata as well
		NodeUtil.delete_node_with_type(type_id)
		#Delete the label
		session.execute(
			delete(TableEntities.NodeType).where(TableEntities.NodeType.type_id == int(type_id))
			)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False
		
	return True