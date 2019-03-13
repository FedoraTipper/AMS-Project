from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__  = 'user'
	user_id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, unique=True)
	password = Column(String)
	privilege = Column(Integer)

class Log(Base):
	__tablename__ = 'logs'
	log_id = Column(Integer, primary_key=True, autoincrement=True)
	message = Column('article_text')

class NodeType(Base):
	__tablename__ = 'node_type'
	type_id = Column(Integer, primary_key=True, autoincrement=True,
					 relationship="Nodes")
	type = Column(String, unique=True)

class Nodes(Base):
	__tablename__ = 'nodes'
	node_id = Column(Integer, primary_key=True, autoincrement=True,
					 relationship="Links")
	type = Column(Integer, ForeignKey(NodeType.type_id))
	label_id = Column(Integer, ForeignKey(Label.label_id))
	view_id = Column(Integer, ForeignKey(View.view_id))
	icon = Column(String, nullable=True)

class Links(Base):
	__tablename__ = 'nodes'
	link_id = Column(Integer, primary_key=True, autoincrement=True)
	node_id_1 = Column(Integer, ForeignKey(Nodes.node_id))
	node_id_2 = Column(Integer, ForeignKey(Nodes.node_id))
	label_id = Column(Integer, ForeignKey())
	icon = Column(String, nullable=True)


class View(Base):
	__tablename__ = 'views'
	view_id = Column(Integer, primary_key=True, autoincrement=True,
					 relationship="Nodes")
	name = Column(String, unique=True)

class Relationship(Base):
	__tablename__ = 'relationship'
	relationship_id = Column(Integer, primary_key=True, autoincrement=True)
	message = Column(String, unique=True)

class Label(Base):
	__tablename__ = 'labels'
	label_id = Column(Integer, primary_key=True, autoincrement=True,
					 relationship="Nodes")
	label_text = Column(String, unique=True)
	parent = Column(Integer, nullable=True)


