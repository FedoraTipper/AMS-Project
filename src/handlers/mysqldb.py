from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import handlers.config as ConfigHandlers


"""
Function to create SQLAlchemy session objects
Inputs: None
Output: SQLAlchemy session object
Caveats: Predefined config variables
"""
def create_session():
	db_cfg_list = db_cfg_list = ConfigHandlers.get_keys("DATABASE")
	engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s" % (
															db_cfg_list[3], db_cfg_list[4],
															db_cfg_list[0], db_cfg_list[1],
															db_cfg_list[2]) 
															)
	Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	session = Session
	session._model_changes = {}
	return session
