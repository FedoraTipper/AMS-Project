import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.node as NodeUtil

class Node(SetDefaultHeaders):
    """
    Class to handle node API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get nodes or a single node record
        Inputs: Tornado web request
        Output: Node data
        Caveats: Authentication needs to be passed
        """
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
        """
        Function to create a node record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type_id": 1, "view_id": 1, "label_id": 0, "icon":0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        node_id = NodeUtil.create_node(node_dict, self)
        if node_dict == False or node_id == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "node", 
                                                                node_id,
                                                                node_dict)

        LoggerHandler.log_message("add", formatted_message)

        self.write({"message": "Success", "payload":node_id})

    def put(self):
        """
        Function to change a node record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"node_id": 1, "type_id": 0, "view_id": 0, "label_id": 0, "icon":0}
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
        """
        Function to delete a node record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """ 
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