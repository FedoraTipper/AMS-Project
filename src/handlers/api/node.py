from tornado.web import RequestHandler

import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.node as NodeUtil

class Node(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"node_id":0}
        node_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        if node_dict == False:
            self.write(NodeUtil.get_nodes())
            return None

        if "node_id" in node_dict:
            self.write(NodeUtil.get_node(node_dict["node_id"]))

    def post(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type": 1, "label_id": 0, "icon":0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if node_dict == False or NodeUtil.create_node(node_dict, self) == False:
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
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type": 0, "node_id": 1, "label_id": 0, "icon":0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if node_dict == False:
            return None

        node_id = node_dict["node_id"]
        del node_dict["node_id"]

        if NodeUtil.change_node(node_id, node_dict, self) == False:
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
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"node_id":1}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if node_dict == False or NodeUtil.delete_node(node_dict["node_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "nodes", 
                                                                node_dict["node_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})