SQL_Statements = list()

SQL_Statements.append("""CREATE TABLE user
(
 user_id   int NOT NULL AUTO_INCREMENT ,
 username  text NOT NULL ,
 password  text NOT NULL ,
 privilege int NOT NULL ,
PRIMARY KEY (user_id)
);""")

SQL_Statements.append("""CREATE TABLE labels
(
 label_id   int NOT NULL AUTO_INCREMENT ,
 label_text text NOT NULL ,
PRIMARY KEY (label_id)
);""")

SQL_Statements.append("""CREATE TABLE node_type
(
 type_id int NOT NULL AUTO_INCREMENT ,
 type    text NOT NULL ,
PRIMARY KEY (type_id)
);""")

SQL_Statements.append("""CREATE TABLE views
(
 view_id int NOT NULL AUTO_INCREMENT,
 name    text NOT NULL ,
PRIMARY KEY (view_id)
);""")

SQL_Statements.append("""CREATE TABLE nodes
(
 node_id  int NOT NULL AUTO_INCREMENT ,
 view_id  int NOT NULL ,
 type_id  int NOT NULL ,
 icon     text ,
 label_id int ,
PRIMARY KEY (node_id),
KEY fkIdx_123 (label_id),
CONSTRAINT FK_123 FOREIGN KEY fkIdx_123 (label_id) REFERENCES labels (label_id),
KEY fkIdx_174 (type_id),
CONSTRAINT FK_174 FOREIGN KEY fkIdx_174 (type_id) REFERENCES node_type (type_id),
KEY fkIdx_183 (view_id),
CONSTRAINT FK_183 FOREIGN KEY fkIdx_183 (view_id) REFERENCES views (view_id)
);""")



SQL_Statements.append("""CREATE TABLE relationship
(
 relationship_id int NOT NULL AUTO_INCREMENT ,
 message         text NOT NULL ,
PRIMARY KEY (relationship_id)
);""")


SQL_Statements.append("""CREATE TABLE links
(
 link_id         int NOT NULL AUTO_INCREMENT ,
 view_id         int NOT NULL ,
 node_id_1       int NOT NULL ,
 node_id_2       int NOT NULL ,
 relationship_id int ,
PRIMARY KEY (link_id),
KEY fkIdx_106 (node_id_1),
CONSTRAINT FK_106 FOREIGN KEY fkIdx_106 (node_id_1) REFERENCES nodes (node_id),
KEY fkIdx_109 (node_id_2),
CONSTRAINT FK_109 FOREIGN KEY fkIdx_109 (node_id_2) REFERENCES nodes (node_id),
KEY fkIdx_149 (relationship_id),
CONSTRAINT FK_149 FOREIGN KEY fkIdx_149 (relationship_id) REFERENCES relationship (relationship_id),
KEY fkIdx_191 (view_id),
CONSTRAINT FK_191 FOREIGN KEY fkIdx_191 (view_id) REFERENCES views (view_id)
);""")

SQL_Statements.append("""CREATE TABLE metadata
(
 meta_id  int NOT NULL AUTO_INCREMENT ,
 category text NOT NULL ,
 data     longtext NOT NULL ,
 node_id  int ,
 link_id  int ,
PRIMARY KEY (meta_id),
KEY fkIdx_102 (node_id),
CONSTRAINT FK_102 FOREIGN KEY fkIdx_102 (node_id) REFERENCES nodes (node_id),
KEY fkIdx_208 (link_id),
CONSTRAINT FK_208 FOREIGN KEY fkIdx_208 (link_id) REFERENCES links (link_id)
);""")

SQL_Statements.append("""CREATE TABLE logs
(
 log_id  int NOT NULL AUTO_INCREMENT ,
 message longtext NOT NULL ,
PRIMARY KEY (log_id)
);""")


import handlers.mysqldb as DBHandler

conn = DBHandler.create_connection()

previous_tables = ["logs",  "metadata", "links", "relationship", "nodes",  "node_type", "views", "labels", "user"];

#Drop all current tables

for table in previous_tables:
	print("Dropping %s" % table)
	try:
		conn.execute("DROP TABLE %s;" % table)
	except:
		print("Failed to drop: %s" % table)

#Start new table
for statement in SQL_Statements:
	print("Creating new" )
	conn.execute(statement)
