from tornado.web import RequestHandler
import json

import handlers.mysqldb as DBHandler
import handlers.logger as LoggerHandler
import handlers.config as ConfigHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.user as UserUtil
import utilities.label as LabelUtil
import utilities.node as NodeUtil
import utilities.link as LinkUtil
import utilities.meta as MetadataUtil
import utilities.error as ErrorUtil
import utilities.meta as MetaUtil
import utilities.relationship as RelationshipUtil

class Authenticate(SetDefaultHeaders):
    def post(self):        
        body_categories = {"username": 1, "password": 1}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict is None:
            return None

        if UserUtil.user_exists(user_dict["username"]) == False:
            self.write({"message":"Authentication failed"})
            return None

        if(UserUtil.compare_password(user_dict["username"], user_dict["password"]) == False):
            self.write({"message":"Authentication failed"})
            return None

        username = user_dict["username"].lower()
        token = JWTHandler.create_token(UserUtil.get_uid(username), username,  (UserUtil.get_privilege(username) + 1))

        self.add_header("Authorization", token)
        self.write({"message":"Authenticated"})

class Register(SetDefaultHeaders):
    def post(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"username": 1, "password": 1, "privilege": 0}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict is None or UserUtil.create_user(user_dict, self) is None:
            return None

        username = user_dict["username"]

        token = JWTHandler.create_token(UserUtil.get_uid(username), username,  UserUtil.get_privilege(username) + 1)
        self.add_header("token", token)

        #sanitise password for logs
        del user_dict["password"]

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                        "user", 
                                                        UserUtil.get_uid(username),
                                                        user_dict)
        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            print("A")
            pass

        self.write({'message': "Success"})

class User(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        body_categories = {"username": 1}
        user_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if user_dict is None:
            return None

        self.write({"user_id": UserUtil.get_uid(user_dict["username"])})

    """
    Change user information
    Come back
    """
    def put(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        body_categories = {"username": 1, "password": 0, "admin": 0}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict is None:
            return None

        if UserUtil.change_user_fields(user_dict, self) is None:
            return None

        self.write({'message': "Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

class Label(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"label_id":0}
        label_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if label_dict is None:
            self.write(LabelUtil.get_labels())
            return None

        if "label_id" in label_dict:
            self.write(LabelUtil.get_label(label_dict["label_id"]))

    """
    Only admins may create new labels/collections
    """
    def post(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None
        
        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_text": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict is None:
            return None

        if LabelUtil.create_label(label_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "label", 
                                                                LabelUtil.get_label_id(label_dict["label_text"]),
                                                                label_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message": "Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_id": 1, "label_text": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict is None:
            return None

        label_id = label_dict["label_id"]
        del label_dict["label_id"]
        if LabelUtil.change_label(label_id, label_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "label", 
                                                                label_id,
                                                                label_dict)
        try:
            LoggerHandler.log_message("change", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_id": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict is None:
            return None

        if LabelUtil.delete_label(label_dict["label_id"], self) is None:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "label", 
                                                                label_dict["label_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

class Node(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"node_id":0}
        node_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        if node_dict is None:
            self.write(NodeUtil.get_nodes())
            return None

        if "node_id" in node_dict:
            self.write(NodeUtil.get_node(node_dict["node_id"]))

    def post(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type": 1, "label_id": 0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)
        
        if node_dict is None:
            return None

        if NodeUtil.create_node(node_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "node", 
                                                                NodeUtil.get_node_id(node_dict["type"]),
                                                                node_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message": "Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type": 0, "node_id": 1, "label_id": 0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if node_dict is None:
            return None

        node_id = node_dict["node_id"]
        del node_dict["node_id"]

        if NodeUtil.change_node(node_id, node_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "node", 
                                                                node_id,
                                                                node_dict)
        try:
            LoggerHandler.log_message("change", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self): 
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"node_id":1}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if node_dict is None or NodeUtil.delete_node(node_dict["node_id"], self) is None:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "nodes", 
                                                                node_dict["node_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})
  
class Link(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"link_id":0}
        link_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if link_dict is None:
            self.write(LinkUtil.get_links())
            return None

        if "link_id" in link_dict:
            self.write(LinkUtil.get_link(link_dict["link_id"]))

    def post(self):
        #User level privilege
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"node_id_1": 1, "node_id_2": 1, "label_id":0, "relationship_id":0}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if link_dict is None or LinkUtil.create_link(link_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "links", 
                                                                LinkUtil.get_link_id(link_dict["node_id_1"], link_dict["node_id_2"]),
                                                                link_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"link_id": 1, "node_id_1": 0, "node_id_2": 0, "label_id": 0, "relationship_id":0}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if link_dict is None:
            return None

        link_id = link_dict["link_id"]
        del link_dict["link_id"]

        if LinkUtil.change_link(link_id, link_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "links", 
                                                                link_id,
                                                                link_dict)

        try:
            LoggerHandler.log_message("change", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"link_id": 1}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if link_dict is None or LinkUtil.delete_link(link_dict["link_id"], self) is None:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "link", 
                                                                link_dict["link_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

class Metadata(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"node_id":0}
        metadata_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        if metadata_dict is None:
            self.write(MetaUtil.get_all_metadata())
            return None

        if "node_id" in metadata_dict:
            self.write(MetadataUtil.get_metadata(metadata_dict["node_id"]))

    def post(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"node_id": 1,  "category" : 1, "metadata": 1}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])
        
        if metadata_dict is None or MetaUtil.create_category(metadata_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "metadata", 
                                                                int(MetaUtil.get_metadata_id(metadata_dict["category"],metadata_dict["node_id"])),
                                                                metadata_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"meta_id": 1, "node_id": 0,  "category" : 0, "metadata": 0}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        metadata_id = metadata_dict["meta_id"]

        if metadata_dict is None or MetaUtil.change_metadata(metadata_id, metadata_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "metadata", 
                                                                metadata_id,
                                                                metadata_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"meta_id": 1}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if metadata_dict is None or MetaUtil.delete_metadata(metadata_dict["meta_id"], self) is None:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "link", 
                                                                metadata_dict["meta_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

class Relationship(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"relationship_id": 0}
        relationship_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if relationship_dict is None:
            self.write(RelationshipUtil.get_relationships())
            return None

        if "relationship_id" in relationship_dict:
            self.write(RelationshipUtil.get_relationships(relationship_dict["relationship_id"])) 

    def post(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"message": 1}
        relationship_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if relationship_dict is None or RelationshipUtil.create_relationship(relationship_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "relationship", 
                                                                RelationshipUtil.get_relationship_id(message),
                                                                relationship_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        body_categories = {"relationship_id": 1, "message": 1}
        relationship_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        if relationship_dict is None:
            return None

        relationship_id = relationship_dict["relationship_id"]
        del relationship_dict["relationship_id"]

        if RelationshipUtil.change_relationship(relationship_id, relationship_dict, self) is None:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "relationship", 
                                                                relationship_id,
                                                                relationship_dict)

        try:
            LoggerHandler.log_message("change", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"relationship_id": 1}
        relationship_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if relationship_dict is None:
            return None

        if RelationshipUtil.delete_link(relationship_dict["relationship_id"], self) is None:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                        "relationship", 
                                                                        relationship_dict["relationship_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

class Log(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        self.write(LoggerHandler.get_logs())