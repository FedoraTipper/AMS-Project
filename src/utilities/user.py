import handlers.mysqldb as DBHandler

conn = DBHandler.create_connection()

TABLE = "user"

def compare_password(username, password):
	return password == get_password(username)

def get_password(username):
	return conn.execute("SELECT password FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0]

def get_uid(username):
	return int(conn.execute("SELECT user_id FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0])

def get_privilege(username):
	return int(conn.execute("SELECT admin FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0])

def user_exists(username):
	return int(conn.execute("SELECT COUNT(username) FROM %s WHERE username = '%s';" % (TABLE, username)).fetchall()[0][0]) != 0

def create_user(username, password, admin):
	conn.execute("INSERT INTO %s (username, password, admin) VALUES ('%s', '%s', %d);" % (TABLE, username, password, 0))

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


