import handlers.mysqldb as dbhandler
from passlib.hash import pbkdf2_sha256
import handlers.classes.TableEntities as TableEntities
from sqlalchemy import update, delete, exc
import handlers.filelogger as flhandler

session = dbhandler.create_session()

def compare_password(username, password):
	"""
	Function to compare user's given password hash instance versus hash stored in the database 
	Inputs: username, user's hashed password
	Output: Boolean value of whether the user details were correct
	Caveats: None
	"""
	stored_hash = get_password(username)
	return pbkdf2_sha256.verify(password, stored_hash)


def get_password(username):
	"""
	Function to return the password of a user found in the database
	Inputs: Username
	Output: Hashed password
	Caveats: None
	"""
	return (session.query(TableEntities.User).filter(TableEntities.User.username == username)).one().password

def get_uid(username):
	"""
	Function to get the user's id found in the database
	Inputs: Username
	Output: User's id in int fTableEntitiesat
	Caveats: None
	"""
	return session.query(TableEntities.User).filter(TableEntities.User.username == username).one().user_id

def get_privilege(username):
	"""
	Function to return the privilege level of a user
	Inputs: Username
	Output: User's privilege level in int fTableEntitiesat
	Caveats: None
	"""
	return session.query(TableEntities.User).filter(TableEntities.User.username == username).one().privilege

def user_exists(username):
	"""
	Function to determine whether the user exists in the database
	Inputs: Username
	Output: Boolean value  (True set to "they exists")
	Caveats: None
	"""
	return (int(session.query(TableEntities.User).filter(TableEntities.User.username == username).count()) != 0)

def create_user(user_dict, torn):
	"""
	Function to create a user record and to be inserted into the database
	Inputs: Dictionairy of user data; Tornado object to write messages
	Output: None if user error occured; True if the operating was successful
	Caveats: Password is hashed using pbkdf sha256 with 48k rounds and salt size of 64 bits
	"""
	if user_exists(user_dict["username"]):
		torn.set_status(400)
		torn.write({"message":"Username already exists"})
		return False
	if "privilege" not in user_dict:
		user_dict["privilege"] = 0
	user_dict["username"] = user_dict["username"].lower()
	#salt_size 64 bits
	#48k rounds
	user_dict["password"] = pbkdf2_sha256.hash(user_dict["password"], salt_size=64, rounds=48000)
	new_user = TableEntities.User(username=user_dict["username"], 
						password=user_dict["password"], 
						privilege=user_dict["privilege"])
	try:
		session.add(new_user)
		session.commit()
	except exc.SQLAlchemyError as Error:
		torn.set_status(500)
		flhandler.log_error_to_file(Error)
		return False
	#sanitize variables
	del user_dict
	return True

def change_password(user_id, new_password):
	"""
	Function to allow a user to change it's password
	Inputs: user_id; user's new password
	Output: False if user error occured; True if the operation was successful
	Caveats: Password is hashed using pbkdf sha256 with 48k rounds and salt size of 64 bits
	"""
	password = pbkdf2_sha256.hash(new_password, salt_size=64, rounds=48000)
	try:
		session.execute(
			update(TableEntities.User).where(TableEntities.User.user_id == int(user_id)).values({"password":password})
			)	
		session.commit()
		return True
	except exc.SQLAlchemyError as Error:
		flhandler.log_error_to_file(Error)
		return False
"""
Function that is able to change user infTableEntitiesation values besides 
# """
# def change_user_fields(user_dict, torn):
# 	if user_exists(user_dict["username"]) == False:
# 		torn.write({"message":"Username does not exist"})
# 		return None

# 	conn.execute(sqlutil.build_update_statement(_table_, user_dict) + " WHERE user_id = {}", (get_uid(user_dict["username"])))
# 	return ""

# """
# Function to change user's privilege
# """

# def change_user_privilege(uid, privilege):
# 	conn.execute("UPDATE %s SET privilege = %d WHERE user_id = %d" , (_table_, privilege, uid))