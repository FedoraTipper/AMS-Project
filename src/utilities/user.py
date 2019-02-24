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

def create_user(user_dict):
	conn.execute(SQLUtil.build_insert_statement(TABLE, user_dict))

"""
Function that is able to change user information values besides 
"""
def change_user_fields(uid,user_dict):
	sql_statement = "UPDATE %s SET " % (TABLE)
	for key, value in user_dict.items():
		sql_statement += "%s = '%s', " % (key, value)
	sql_statement = sql_statement[:-2] + (" WHERE user_id = %d" % uid) + ";"
	print(sql_statement)
	conn.execute(sql_statement)

"""
Function to change user's privilege
"""

def change_user_privilege(uid, privilege):
	conn.execute("UPDATE %s SET privilege = %d WHERE user_id = %d" % (TABLE, privilege, uid))


