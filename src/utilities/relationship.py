import handlers.mysqldb as DBHandler
from sqlalchemy import update, delete, exc
import handlers.filelogger as FLHandler
import handlers.classes.TableEntities as TableEntities

session = DBHandler.create_session()

def get_relationship(relationship_id):
    """
    Function to get a single relationship record from the database
    Inputs: Relationship ID of the record wanted
    Output: JSON formatted string of relationship record
    Caveats: None
    """
    entries = session.query(TableEntities.Relationship).filter(
        TableEntities.Relationship.relationship_id == int(relationship_id)).all()
    return {'data': [entry.as_dict() for entry in entries]}

def get_relationships():
    """
    Function to get all relationship records
    Inputs: None
    Output: JSON Formatted string of all relationship records
    Caveats: None
    """
    entries = session.query(TableEntities.Relationship).all()
    return {'data': [entry.as_dict() for entry in entries]}

def get_relationship_id(message):
    """
    Function to return a relationship ID given it's message
    Inputs: Message string
    Output: Relationship ID
    Caveats: None
    """
    return (session.query(TableEntities.Relationship).filter(
        (TableEntities.Relationship.message == message)).one().meta_id)

def create_relationship(relationship_dict, torn):
    """
    Function to create a relationship
    Inputs: Relationship dictionary; Tornado Object
    Output: True if operation was successful, False if the operation was not
    Caveats: Check if relationship message already exists
    """
    if relationship_exists(relationship_dict["message"]):
        torn.set_status(400)
        torn.write({"message": "Relationship message already exists"})
        return False
    try:
        session.add(TableEntities.Relationship(
            message=relationship_dict["message"]))
        session.commit()
    except exc.SQLAlchemyError as Error:
        torn.set_status(500)
        FLHandler.log_error_to_file(Error)
        return False
    return True

def relationship_exists(message):
    """
    Function to see whether a relationship exists given its message
    Inputs: Message string
    Output: Boolean value - (True if the relationship exists)
    Caveats: None
    """
    return int(session.query(TableEntities.Relationship).filter(
        TableEntities.Relationship.message == message).count()) != 0

def relationship_id_exists(relationship_id):
    """
    Function to see whether a relationship id exists
    Inputs: Relationship ID
    Output: Boolean value - (True if the relationship ID exists)
    Caveats: None
    """
    return (session.query(TableEntities.Relationship).filter(TableEntities.Relationship.relationship_id == int(relationship_id)).one().relationship_id)

def change_relationship(relationship_id, relationship_dict, torn):
    """
    Function to change link record data
    Inputs: Link ID; Dictionary of link data to be ammended; Tornado object to write messages
    Output: True if operation was successful, False if the operation was not
    Caveats: Determine if node and other FK objects needed to be changed exist; Determine if link relation already exists
    """
    if relationship_id_exists(relationship_id) == False:
        torn.set_status(404)
        torn.write({"message": "Relationship does not exists"})
        return False

    if relationship_exists(relationship_dict["message"]):
        torn.set_status(400)
        torn.write({"message": "New relationship message exists"})
        return False

    try:
        session.execute(
            update(TableEntities.Relationship).where(
                TableEntities.Relationship.relationship_id == int(relationship_id))
            .values(relationship_dict)
        )
        session.commit()
    except exc.SQLAlchemyError as Error:
        FLHandler.log_error_to_file(Error)
        return False

    return True

def delete_relationship(relationship_id, torn):
    """
    Function to delete relationship
    Inputs: Relationship ID
    Output: True if operation was successful, False if the operation was not
    Caveats: Nullify relation ID columns in other tables 
    """
    if relationship_id_exists(relationship_id) == False:
        torn.set_status(404)
        torn.write({"message": "Relationship id does not exist"})
        return False

    null_dict = {"relationship_id": False}
    # Create SQL statements to set relationship ID in FK _table_s to NULL
    try:
        # Nullify relationship id's in links table
        session.execute(
            update(TableEntities.Links).where(
                TableEntities.Links.relationship_id == int(relationship_id))
            .values(null_dict)
        )
        session.commit()
        # Delete relationship
        session.execute(
            delete(TableEntities.Relationship).where(
                TableEntities.Relationship.relationship_id == int(relationship_id))
        )
        session.commit()
    except exc.SQLAlchemyError as Error:
        torn.set_status(500)
        FLHandler.log_error_to_file(Error)
        return False

    return True
