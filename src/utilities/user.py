import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil

conn = DBHandler.create_connection()

TABLE = "user"

def compare_password(username, password):
	return password == get_password(username)

def get_password(username):
	return conn.execute("SELECT password FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0]

def get_uid(username):
	return int(conn.execute("SELECT user_id FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0])

def get_privilege(username):
	return int(conn.execute("SELECT privilege FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0])

def user_exists(username):
	return int(conn.execute("SELECT COUNT(username) FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0]) != 0

def create_user(user_dict, torn):
	if user_exists(user_dict["username"]):
		torn.write({"message":"Username already exists"})
		return None
	if "privilege" not in user_dict:
		user_dict["privilege"] = 0
	conn.execute(SQLUtil.build_insert_statement(TABLE, user_dict))
	return ""

"""
Function that is able to change user information values besides 
"""
def change_user_fields(user_dict, torn):
	if user_exists(user_dict["username"]) == False:
		torn.write({"message":"Username does not exist"})
		return None

	conn.execute(SQLUtil.build_update_statement(TABLE, user_dict) + " WHERE user_id = {}".format(get_uid(user_dict["username"])))
	return ""

"""
Function to change user's privilege
"""

def change_user_privilege(uid, privilege):
	conn.execute("UPDATE %s SET privilege = %d WHERE user_id = %d" % (TABLE, privilege, uid))