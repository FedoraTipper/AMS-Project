import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
import handlers.classes.TableEntities as TableEntities
from sqlachemy import update, delete

session = DBHandler.create_session()

"""
Function to create a label record
Inputs: Dictionary of label data, Tornado object to write data
Output: True if operation was successful, False if the operation was not
Caveats: Check if the label text already exists
"""
def create_label(label_dict, torn):
	if label_exists(label_dict["label_text"]):
		torn.write({'message': "Label text already exists"})
		return False
	
	try:
		session.add(TableEntities.Label(label_text=label_dict["label_text"]))
		session.commit()
	except:
		print("Something went wrong. <Label Create>")
		return False

	return True

"""
Function to determine if a label exists
Inputs: Label text
Output: Boolean value - (True if the label text exists)
Caveats: None
"""
def label_exists(label_text):
	return int(session.query(TableEntities.Label).filter(
			TableEntities.Label.label_text == label_text).count()) != 0

"""
Function to determine if the label ID exists
Inputs: Label ID int
Output: Boolean value - (True if the label id exists)
Caveats: None
"""
def label_id_exists(label_id):
	return int(session.query(TableEntities.Label).filter(
			TableEntities.Label.label_id == label_id).count()) != 0

"""
Function to return all label records from the database
Inputs: None
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_labels():
	entries = session.query(TableEntities.Label).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to get a single node's data from the database
Inputs: Label ID in int format
Output: JSON formatted string of column names and respective values
Caveats: None
"""
def get_label(label_id):
	entries = session.query(TableEntities.Label)
	.filter(TableEntities.Label.label_id == int(label_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to return a label's id give the label text
Inputs: Label text
Output: Label ID
Caveats: None
"""
def get_label_id(label_text):
	return  session.query(TableEntities.Label).filter(TableEntities.Label.label_text == label_text) 
			.one().label_id

"""
Function to change a label record's data
Inputs: Label ID; Dictionary of label values; Tornado object
Output: True if operation was successful, False if the operation was not
Caveats: Determine if the label ID exists and whether the text exists as well as parent label
"""
def change_label(label_id, label_dict, torn):
	if label_id_exists(label_id) == False:
		torn.write({"message": "Label does not exist"})
		return False
	if (label_dict["label_text"] is not None):
		if (label_exists(label_dict["label_text"])):
			torn.write({"message": "New label text already exists"})
			return False
	try:
		session.execute(
			update(TableEntities.Label).where(TableEntities.Label.label_id == int(label_id))
			.values(label_dict)
			)	
		session.commit()
	except:
		print("Something went wrong. <Label Update>")
		return False
	return True

"""
Function to delete a label record from the database
Inputs: Label ID; Tornado object to write any messages
Output: True if operation was successful, False if the operation was not
Caveats: Check if the label id exists. Nullify label ID in any other tables
"""
def delete_label(label_id, torn):
	if label_id_exists(label_id) == False:
		torn.write({"message": "Label does not exist"})
		return False

	null_dict = {"label_id": None}
	entities = [TableEntities.Links, TableEntities.Nodes]
	try:
		#Nullify label_ids in other tables
		for entity in entities:			
			session.execute(	
				update(entity).where(entity.label_id == int(label_id))
				.values(null_dict)
				)
		session.commit()
		#Delete the label
		session.execute(
			delete(TableEntities.Label).where(TableEntities.Label.label_id == int(label_id))
			)
		session.commit()
	except:
		print("Something went wrong. <Relationship Delete>")
		return False
		
	return True