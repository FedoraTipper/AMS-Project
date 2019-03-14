from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT

Base = declarative_base()

class User(Base):
	__tablename__  = 'user'
	user_id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	privilege = Column(Integer, nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Log(Base):
	__tablename__ = 'logs'
	log_id = Column(Integer, primary_key=True, autoincrement=True)
	message = Column(LONGTEXT, nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Label(Base):
	__tablename__ = 'labels'
	label_id = Column(Integer, primary_key=True, autoincrement=True)
	label_text = Column(String, unique=True, nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class View(Base):
	__tablename__ = 'views'
	view_id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, unique=True, nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class NodeType(Base):
	__tablename__ = 'node_type'
	type_id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(String, unique=True, nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Nodes(Base):
	__tablename__ = 'nodes'
	node_id = Column(Integer, primary_key=True, autoincrement=True)
	type_id = Column(Integer, ForeignKey(NodeType.type_id), nullable=False)
	label_id = Column(Integer, ForeignKey(Label.label_id), nullable=True)
	view_id = Column(Integer, ForeignKey(View.view_id), nullable=False)
	icon = Column(String, nullable=True)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Relationship(Base):
	__tablename__ = 'relationship'
	relationship_id = Column(Integer, primary_key=True, autoincrement=True)
	message = Column(String, unique=True, nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Links(Base):
	__table_args__ = {"extend_existing":True}
	__tablename__ = 'links'
	link_id = Column(Integer, primary_key=True, autoincrement=True)
	node_id_1 = Column(Integer, ForeignKey(Nodes.node_id), nullable=False)
	node_id_2 = Column(Integer, ForeignKey(Nodes.node_id), nullable=False)
	label_id = Column(Integer, ForeignKey(Label.label_id), nullable=True)
	view_id = Column(Integer, ForeignKey(View.view_id), nullable=False)
	relationship_id = Column(Integer, ForeignKey(Relationship.relationship_id), nullable=True)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Metadata(Base):
	__tablename__ = 'metadata'
	meta_id = Column(Integer, primary_key=True, autoincrement=True)
	category = Column(String, nullable=False)
	data = Column(LONGTEXT, nullable=False)
	node_id = Column(Integer, ForeignKey(Nodes.node_id), nullable=False)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

engine = create_engine("mysql+pymysql://apirunner:ZJJFt7rqeg8eMPreru69NX9W9yMfhyechc8Yzz4ogtdEfUB@139.59.172.124:3306/project1")
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = Session
session._model_changes = {}


#print(session.query(Nodes).all())

# session.add(NodeType(type="Developer"))
# session.commit()
# session.add(View(name="Countercept"))
# session.commit()
# node = Nodes(type_id=2,view_id=1)
# node.icon = "hello"
# session.add(node)
# session.commit()
# print(session.query(View).all())
# entries = session.query(Nodes).all()

# for entry in entries:
# 	print("node_id: %d" % entry.node_id)
# 	print("view_id: %d" % entry.view_id)
# 	print("type_id: %d" % entry.type_id)
# 	print("")


# session.add(Relationship(message="owns"))
# session.commit()

# session.add(Links(node_id_1=2, node_id_2=1, view_id=1, relationship_id=1))
# session.commit()
# print(session.query(Links).one().link_id)
# print(session.query(Nodes).all().node_id)

# session.add(User(username="hello", password="world", privilege=1))
# session.commit()
# user_dict = {"username":"usertest123"}
# session.execute(update(User).where(User.user_id == 1).values(user_dict))
# session.commit()

# connection = engine.connect()
# sqldata = connection.execute("SELECT * FROM user;")

# entries = session.query(User).all()

# dict_list = list()
# json = "{'data': ["

# print({'data': [entry.as_dict() for entry in entries]})
	

# print({'data': [dict(zip(tuple (sqldata.keys()) ,i)) for i in sqldata.cursor]})


# def link_relation_exists(node_id_1, node_id_2):
# 	return int(session.query(Nodes).filter((
# 			(Links.node_id_1 == int(node_id_1)) & 
# 			(Links.node_id_2 == int(node_id_2))) | (
# 			(Links.node_id_2 == int(node_id_1)) & 
# 			(Links.node_id_1 == int(node_id_2))))
# 			.count()) != 0

# print(link_relation_exists(1, 2))
