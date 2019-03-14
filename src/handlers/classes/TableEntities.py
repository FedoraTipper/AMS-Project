from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__  = 'user'
	user_id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	privilege = Column(Integer, nullable=False)

class Log(Base):
	__tablename__ = 'logs'
	log_id = Column(Integer, primary_key=True, autoincrement=True)
	message = Column('article_text', nullable=False)

class Label(Base):
	__tablename__ = 'labels'
	label_id = Column(Integer, primary_key=True, autoincrement=True)
	label_text = Column(String, unique=True, nullable=False)

class View(Base):
	__tablename__ = 'views'
	view_id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, unique=True, nullable=False)

class NodeType(Base):
	__tablename__ = 'node_type'
	type_id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(String, unique=True, nullable=False)

class Nodes(Base):
	__tablename__ = 'nodes'
	node_id = Column(Integer, primary_key=True, autoincrement=True)
	type_id = Column(Integer, ForeignKey(NodeType.type_id), nullable=False)
	label_id = Column(Integer, ForeignKey(Label.label_id), nullable=True)
	view_id = Column(Integer, ForeignKey(View.view_id), nullable=False)
	icon = Column(String, nullable=True)

class Relationship(Base):
	__tablename__ = 'relationship'
	relationship_id = Column(Integer, primary_key=True, autoincrement=True)
	message = Column(String, unique=True, nullable=False)

class Links(Base):
	__table_args__ = {"extend_existing":True}
	__tablename__ = 'links'
	link_id = Column(Integer, primary_key=True, autoincrement=True)
	node_id_1 = Column(Integer, ForeignKey(Nodes.node_id), nullable=False)
	node_id_2 = Column(Integer, ForeignKey(Nodes.node_id), nullable=False)
	label_id = Column(Integer, ForeignKey(Label.label_id), nullable=True)
	view_id = Column(Integer, ForeignKey(View.view_id), nullable=False)
	relationship_id = Column(Integer, ForeignKey(Relationship.relationship_id), nullable=False)

class Metadata(Base):
	__tablename__ = 'metadata'
	meta_id = Column(Integer, primary_key=True, autoincrement=True)
	category = Column(String, nullable=False)
	data = Column("article_text", nullable=False)
	node_id = Column(Integer, ForeignKey(Nodes.node_id), nullable=False)