SQL_Statements = list()

SQL_Statements.append("""CREATE TABLE user
(
 user_id   int NOT NULL AUTO_INCREMENT ,
 username  varchar(150) NOT NULL ,
 password  varchar(255) NOT NULL ,
 privilege int NOT NULL ,
PRIMARY KEY (user_id)
);""")

SQL_Statements.append("""CREATE TABLE labels
(
 label_id   int NOT NULL AUTO_INCREMENT ,
 label_text varchar(255) NOT NULL ,
 parent     int ,
PRIMARY KEY (label_id),
KEY fkIdx_155 (parent),
CONSTRAINT FK_155 FOREIGN KEY fkIdx_155 (parent) REFERENCES labels (label_id)
);""")

SQL_Statements.append("""CREATE TABLE nodes
(
 node_id  int NOT NULL AUTO_INCREMENT ,
 type     varchar(255) NOT NULL ,
 label_id int ,
 icon     varchar(500) ,
PRIMARY KEY (node_id),
KEY fkIdx_123 (label_id),
CONSTRAINT FK_123 FOREIGN KEY fkIdx_123 (label_id) REFERENCES labels (label_id)
);""")

SQL_Statements.append("""CREATE TABLE metadata
(
 meta_id  int NOT NULL AUTO_INCREMENT ,
 category   varchar(350) NOT NULL ,
 metadata varchar(350) NOT NULL ,
 node_id  int NOT NULL ,
PRIMARY KEY (meta_id),
KEY fkIdx_102 (node_id),
CONSTRAINT FK_102 FOREIGN KEY fkIdx_102 (node_id) REFERENCES nodes (node_id)
);""")

SQL_Statements.append("""CREATE TABLE relationship
(
 relationship_id int NOT NULL AUTO_INCREMENT,
 message         varchar(255) NOT NULL ,
PRIMARY KEY (relationship_id)
);""")


SQL_Statements.append("""CREATE TABLE links
(
 link_id         int NOT NULL AUTO_INCREMENT ,
 node_id_1       int NOT NULL ,
 node_id_2       int NOT NULL ,
 label_id        int ,
 relationship_id int ,
PRIMARY KEY (link_id),
KEY fkIdx_106 (node_id_1),
CONSTRAINT FK_106 FOREIGN KEY fkIdx_106 (node_id_1) REFERENCES nodes (node_id),
KEY fkIdx_109 (node_id_2),
CONSTRAINT FK_109 FOREIGN KEY fkIdx_109 (node_id_2) REFERENCES nodes (node_id),
KEY fkIdx_120 (label_id),
CONSTRAINT FK_120 FOREIGN KEY fkIdx_120 (label_id) REFERENCES labels (label_id),
KEY fkIdx_149 (relationship_id),
CONSTRAINT FK_149 FOREIGN KEY fkIdx_149 (relationship_id) REFERENCES relationship (relationship_id)
);""")



SQL_Statements.append("""CREATE TABLE messages
(
 message_id int NOT NULL AUTO_INCREMENT,
 text       varchar(2000) NOT NULL ,
PRIMARY KEY (message_id)
);""")


SQL_Statements.append("""CREATE TABLE logs
(
 log_id     int NOT NULL AUTO_INCREMENT ,
 user_id    int NOT NULL ,
 node_id    int ,
 link_id    int ,
 meta_id    int ,
 label_id   int ,
 message_id int NOT NULL ,
PRIMARY KEY (log_id),
KEY fkIdx_128 (meta_id),
CONSTRAINT FK_128 FOREIGN KEY fkIdx_128 (meta_id) REFERENCES metadata (meta_id),
KEY fkIdx_131 (label_id),
CONSTRAINT FK_131 FOREIGN KEY fkIdx_131 (label_id) REFERENCES labels (label_id),
KEY fkIdx_139 (message_id),
CONSTRAINT FK_139 FOREIGN KEY fkIdx_139 (message_id) REFERENCES messages (message_id),
KEY fkIdx_66 (user_id),
CONSTRAINT FK_66 FOREIGN KEY fkIdx_66 (user_id) REFERENCES user (user_id),
KEY fkIdx_69 (node_id),
CONSTRAINT FK_69 FOREIGN KEY fkIdx_69 (node_id) REFERENCES nodes (node_id),
KEY fkIdx_95 (link_id),
CONSTRAINT FK_95 FOREIGN KEY fkIdx_95 (link_id) REFERENCES links (link_id)
);
""")


import handlers.mysqldb as DBHandler

conn = DBHandler.create_connection()

previous_tables = ["logs","messages", "metadata", "relationship", "links", "nodes", "labels", "user"];

#Drop all current tables

for table in previous_tables:
	print("Dropping %s" % table)
	try:
		conn.execute("DROP TABLE %s;" % table)
	except:
		pass

#Start new table
for statement in SQL_Statements:
	print("Creating new" )
	conn.execute(statement)








