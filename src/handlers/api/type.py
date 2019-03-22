import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders

import utilities.error as errorutil
import utilities.type as typeutil


class NodeType(SetDefaultHeaders):
    """
    Class to handle node type API requests
    Functions: get, post, put, delete (Typical )
    """
    def get(self):
        """
        Function to get types or a single type record
        Inputs: Tornado web request
        Output: Type data
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"type_id":0}
        type_dict = errorutil.check_fields(self.request.arguments, body_categories, self)
        
        if type_dict == False:
            self.write(typeutil.get_types())
            return None

        if "type_id" in type_dict:
            self.write(typeutil.get_type(type_dict["type_id"]))

    def post(self):
        """
        Function to create a type record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type": 1}
        type_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if type_dict == False or typeutil.create_type(type_dict, self) == False:
            return None
        
        type_id = typeutil.get_type_id(type_dict["type"])

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "node_type", 
                                                                type_id,
                                                                type_dict)

        loggerhandler.log_message("add", formatted_message)

        self.write({"message": "Success","payload":type_id})

    def put(self):
        """
        Function to change a type record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type_id": 1, "type": 1}
        type_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if type_dict == False:
            return None

        type_id = type_dict["type_id"]
        del type_dict["type_id"]

        if typeutil.change_type(type_id, type_dict, self) == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "node_type", 
                                                                type_id,
                                                                type_dict)

        loggerhandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self): 
        """
        Function to delete a type record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type_id":1}
        type_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if type_dict == False or typeutil.delete_type(type_dict["type_id"], self) == False:
            return None

        formatted_message = loggerhandler.form_delete_message_dictionary(userdata, 
                                                                "node_type", 
                                                                type_dict["type_id"])

        loggerhandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})