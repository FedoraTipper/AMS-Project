import handlers.mysqldb as DBHandler
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete

session = DBHandler.create_session()


def create_view(view_dict, torn):
	if view_exists(view_dict["name"]):
		torn.write({'message': "View name already exists"})
		return False
	
	try:
		session.add(TableEntities.View(name=view_dict["name"]))
		session.commit()
	except:
		print("Something went wrong. <View Create>")
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
		torn.write({"message": "View does not exist"})
		return False

	if (view_dict["name"] is None):
		torn.write({"message": "Empty update statement"})
		return False
	else:
		if (view_exists(view_dict["name"])):
			torn.write({"message": "New view name already exists"})
			return False
	try:
		session.execute(
			update(TableEntities.View).where(TableEntities.View.view_id == int(view_id)).values(view_dict)
			)	
		session.commit()
	except:
		print("Something went wrong. <View Update>")
		return False
	return True

def delete_view(view_id, torn):
	if label_id_exists(view_id) == False:
		torn.write({"message": "View does not exist"})
		return False

	null_dict = {"view_id": None}
	entities = [TableEntities.Links, TableEntities.Nodes]
	try:
		#Nullify label_ids in other tables
		for entity in entities:			
			session.execute(	
				update(entity).where(entity.view_id == int(view_id)).values(null_dict)
				)
		session.commit()
		#Delete the label
		session.execute(
			delete(TableEntities.View).where(TableEntities.View.view_id == int(view_id))
			)
		session.commit()
	except:
		print("Something went wrong. <View Delete>")
		return False
		
	return True