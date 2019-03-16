from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT

Base = declarative_base()

"""
Description of file.

We import in sqlalchemy's functions where we are able to create 
a theoretical mapping of our choosing. If incorrect settings are applied
SQLAlchemy will complaign, and it doesn't preemptively check with the database  
"""

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
	view_id = Column(Integer, ForeignKey(View.view_id), nullable=False)
	relationship_id = Column(Integer, ForeignKey(Relationship.relationship_id), nullable=True)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Metadata(Base):
	__tablename__ = 'metadata'
	meta_id = Column(Integer, primary_key=True, autoincrement=True)
	category = Column(String, nullable=False)
	data = Column(LONGTEXT, nullable=False)
	node_id = Column(Integer, ForeignKey(Nodes.node_id), nullable=True)
	link_id = Column(Integer, ForeignKey(Links.link_id), nullable=True)
	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}
