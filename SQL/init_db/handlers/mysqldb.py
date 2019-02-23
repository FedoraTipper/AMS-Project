from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import handlers.config as ConfigHandlers

def create_connection():
	db_cfg_list = ConfigHandlers.get_keys("DATABASE")
	engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s" % (
															db_cfg_list[3], db_cfg_list[4],
															db_cfg_list[0], db_cfg_list[1],
															db_cfg_list[2]) 
															)
	return engine.connect()

	