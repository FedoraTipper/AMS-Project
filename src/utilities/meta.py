import handlers.mysqldb as DBHandler
import utilities.sql as SQLUtil
conn = DBHandler.create_connection()

TABLE = "links"