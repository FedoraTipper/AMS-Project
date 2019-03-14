import handlers.mysqldb as DBHandler
from sqlalchemy import update, delete

session = DBHandler.create_session()

"""
Function to get a single relationship record from the database
Inputs: Relationship ID of the record wanted
Output: JSON formatted string of relationship record
Caveats: None
"""
def get_relationship(relationship_id):
	entries = session.query(TableEntities.Relationship)
	.filter(TableEntities.Relationship.relationship_id == int(relationship_id)).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to get all relationship records
Inputs: None
Output: JSON Formatted string of all relationship records
Caveats: None
"""
def get_relationships():
	entries = session.query(TableEntities.Relationship).all()
	return {'data': [entry.as_dict() for entry in entries]}

"""
Function to return a relationship ID given it's message
Inputs: Message string
Output: Relationship ID
Caveats: None
"""
def get_relationship_id(message):
	return  (session.query(TableEntities.Relationship).filter(
			(TableEntities.Relationship.message == message))
			.one().meta_id)

"""
Function to create a relationship
Inputs: Relationship dictionary; Tornado Object
Output: True if operation was successful, False if the operation was not
Caveats: Check if relationship message already exists
"""
def create_relationship(relationship_dict, torn):
	if relationship_exists(relationship_dict["message"]):
		torn.write({"message":"Relationship message already exists"})
		return False
	session.add(TableEntities.Relationship(message=relationship_dict["message"]))
	session.commit()
	return True

"""
Function to see whether a relationship exists given its message
Inputs: Message string
Output: Boolean value - (True if the relationship exists)
Caveats: None
"""
def relationship_exists(message):
	return int(session.query(TableEntities.Relationship).filter(
				TableEntities.Relationship.message == message)
				.count()) != 0

"""
Function to see whether a relationship id exists
Inputs: Relationship ID
Output: Boolean value - (True if the relationship ID exists)
Caveats: None
"""
def relationship_id_exists(relationship_id):
	return  (session.query(TableEntities.Relationship).filter(TableEntities.Relationship.relationship_id == int(relationship_id))
			.one().relationship_id)

"""
Function to change link record data
Inputs: Link ID; Dictionary of link data to be ammended; Tornado object to write messages
Output: True if operation was successful, False if the operation was not
Caveats: Determine if node and other FK objects needed to be changed exist; Determine if link relation already exists
"""
def change_relationship(relationship_id, relationship_dict, torn):
	if relationship_id_exists(relationship_id) == False:
		torn.write({"message":"Relationship does not exists"})
		return False

	if relationship_exists(relationship_dict["message"]):
		torn.write({"message":"New relationship message exists"})
		return False

	try:
		session.execute(
			update(TableEntities.Relationship).where(TableEntities.Relationship.relationship_id == int(relationship_id))
			.values(relationship_dict)
			)	
		session.commit()
	except:
		print("Something went wrong. <Relationship Update>")
		return False

	return True

"""
Function to delete relationship
Inputs: Relationship ID
Output: True if operation was successful, False if the operation was not
Caveats: Nullify relation ID columns in other tables 
"""
def delete_relationship(relationship_id, torn):
	if relationship_id_exists(relationship_id) == False:
		torn.write({"message": "Relationship id does not exist"})
		return False

	null_dict = {"relationship_id": False}
	#Create SQL statements to set relationship ID in FK _table_s to NULL
	try:
		#Nullify relationship id's in links table
		session.execute(
				update(TableEntities.Links).where(TableEntities.Links.relationship_id == int(relationship_id))
				.values(null_dict)
				)	
		session.commit()
		#Delete relationship
		session.execute(
			delete(TableEntities.Relationship).where(TableEntities.Relationship.relationship_id == int(relationship_id))
			)
		session.commit()
	except:
		print("Something went wrong. <Relationship Delete>")
		return False

	return True