import handlers.mysqldb as DBHandler
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as FLHandler


session = DBHandler.create_session()


def create_view(view_dict, torn):
	if view_exists(view_dict["name"]):
		torn.set_status(400)
		torn.write({'message': "View name already exists"})
		return False
	
	try:
		session.add(TableEntities.View(name=view_dict["name"]))
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False

	return True

def view_exists(name):
	return int(session.query(TableEntities.View).filter(
			TableEntities.View.name == name).count()) != 0

def view_id_exists(view_id):
	return int(session.query(TableEntities.View).filter(
			TableEntities.View.view_id == int(view_id)).count()) != 0

def get_views():
	entries = session.query(TableEntities.View).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_view(view_id):
	entries = session.query(TableEntities.View).filter(TableEntities.View.view_id == int(view_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

def get_view_id(name):
	return  session.query(TableEntities.View).filter(TableEntities.View.name == name).one().view_id

def change_view(view_id, view_dict, torn):
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
		FLHandler.log_error_to_file(Error)
		return False
	return True

def delete_view(view_id, torn):
	if view_id_exists(view_id) == False:
		torn.set_status(404)
		torn.write({"message": "View does not exist"})
		return False

	try:
		import utilities.node as NodeUtil
		#Delete all objects dependant on the view that will be deleted
		#Deleting a node will remove the link and the metadata as well
		NodeUtil.delete_node_with_view(view_id)

		#Delete the view itself
		session.execute(
			delete(TableEntities.View).where(TableEntities.View.view_id == int(view_id))
			)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		FLHandler.log_error_to_file(Error)
		return False
	return True