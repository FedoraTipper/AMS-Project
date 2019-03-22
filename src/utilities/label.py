import handlers.mysqldb as dbhandler
import utilities.sql as sqlutil
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as flhandler

session = dbhandler.create_session()

def create_label(label_dict, torn):
    """
    Function to create a label record
    Inputs: Dictionary of label data, Tornado object to write data
    Output: True if operation was successful, False if the operation was not
    Caveats: Check if the label text already exists
    """
    if label_exists(label_dict["label_text"]):
        torn.set_status(400)
        torn.write({'message': "Label text already exists"})
        return False

    try:
        session.add(TableEntities.Label(label_text=label_dict["label_text"]))
        session.commit()
    except exc.SQLAlchemyError as Error:
        flhandler.log_error_to_file(Error)
        torn.set_status(500)
        return False

    return True

def label_exists(label_text):
    """
    Function to determine if a label exists
    Inputs: Label text
    Output: Boolean value - (True if the label text exists)
    Caveats: None
    """
    return int(session.query(TableEntities.Label).filter(
        TableEntities.Label.label_text == label_text).count()) != 0

def label_id_exists(label_id):
    """
    Function to determine if the label ID exists
    Inputs: Label ID int
    Output: Boolean value - (True if the label id exists)
    Caveats: None
    """
    return int(session.query(TableEntities.Label).filter(
        TableEntities.Label.label_id == label_id).count()) != 0

def get_labels():
    """
    Function to return all label records from the database
    Inputs: None
    Output: JSON formatted string of column names and respective values
    Caveats: None
    """
    entries = session.query(TableEntities.Label).all()
    return {'data': [entry.as_dict() for entry in entries]}

def get_label(label_id):
    """
    Function to get a single node's data from the database
    Inputs: Label ID in int format
    Output: JSON formatted string of column names and respective values
    Caveats: None
    """
    entries = session.query(TableEntities.Label).filter(
        TableEntities.Label.label_id == int(label_id)).all()
    return {'data': [entry.as_dict() for entry in entries]}

def get_label_id(label_text):
    """
    Function to return a label's id give the label text
    Inputs: Label text
    Output: Label ID
    Caveats: None
    """
    return session.query(TableEntities.Label).filter(TableEntities.Label.label_text == label_text).one().label_id

def change_label(label_id, label_dict, torn):
    """
    Function to change a label record's data
    Inputs: Label ID; Dictionary of label values; Tornado object
    Output: True if operation was successful, False if the operation was not
    Caveats: Determine if the label ID exists and whether the text exists as well as parent label
    """
    if label_id_exists(label_id) == False:
        torn.set_status(404)
        torn.write({"message": "Label does not exist"})
        return False
    if (label_dict["label_text"] is not None):
        if (label_exists(label_dict["label_text"])):
            torn.set_status(404)
            torn.write({"message": "New label text already exists"})
            return False
    try:
        session.execute(
            update(TableEntities.Label).where(
                TableEntities.Label.label_id == int(label_id)).values(label_dict)
        )
        session.commit()
    except exc.SQLAlchemyError as Error:
        flhandler.log_error_to_file(Error)
        torn.set_status(500)
        return False
    return True

def delete_label(label_id, torn):
    """
    Function to delete a label record from the database
    Inputs: Label ID; Tornado object to write any messages
    Output: True if operation was successful, False if the operation was not
    Caveats: Check if the label id exists. Nullify label ID in any other tables
    """
    if label_id_exists(label_id) == False:
        torn.set_status(404)
        torn.write({"message": "Label does not exist"})
        return False

    null_dict = {"label_id": None}
    try:
        # Nullify label_ids in other tables
        session.execute(
                update(TableEntities.Nodes).where(TableEntities.Nodes.label_id ==
                                     int(label_id)).values(null_dict)
            )
        session.commit()
        # Delete the label
        session.execute(
            delete(TableEntities.Label).where(
                TableEntities.Label.label_id == int(label_id))
        )
        session.commit()
    except exc.SQLAlchemyError as Error:
        torn.set_status(500)
        flhandler.log_error_to_file(Error)
        return False

    return True
