import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
conn = DBHandler.create_connection()

_table_ = "metadata"

def create_metadata():
	return None