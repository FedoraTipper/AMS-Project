import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.type as TypeUtil

class NodeType(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"type_id":0}
        type_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        
        if type_dict == False:
            self.write(TypeUtil.get_types())
            return None

        if "type_id" in type_dict:
            self.write(TypeUtil.get_type(type_dict["type_id"]))

    def post(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type": 1}
        type_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if type_dict == False or TypeUtil.create_type(type_dict, self) == False:
            return None
        
        type_id = TypeUtil.get_type_id(type_dict["type"])

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "node_type", 
                                                                type_id,
                                                                type_dict)

        LoggerHandler.log_message("add", formatted_message)

        self.write({"message": "Success","payload":type_id})

    def put(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type_id": 1, "type": 1}
        type_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if type_dict == False:
            return None

        type_id = type_dict["type_id"]
        del type_dict["type_id"]

        if TypeUtil.change_type(type_id, type_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "node_type", 
                                                                type_id,
                                                                type_dict)

        LoggerHandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self): 
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"type_id":1}
        type_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if type_dict == False or TypeUtil.delete_type(type_dict["type_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "node_type", 
                                                                type_dict["type_id"])

        LoggerHandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})