import handlers.logger as LoggerHandler
import handlers.jwt as JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.meta as MetadataUtil

class Metadata(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"node_id":0}
        metadata_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        if metadata_dict == False:
            self.write(MetaUtil.get_all_metadata())
            return None

        if "node_id" in metadata_dict:
            self.write(MetadataUtil.get_metadata(metadata_dict["node_id"]))

    def post(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"node_id": 1,  "category" : 1, "data": 1}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])
        
        if metadata_dict == False or MetaUtil.create_category(metadata_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "metadata", 
                                                                int(MetaUtil.get_metadata_id(metadata_dict["category"],metadata_dict["node_id"])),
                                                                metadata_dict)

        LoggerHandler.log_message("add", formatted_message)

        self.write({"message":"Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"meta_id": 1, "node_id": 0,  "category" : 0, "metadata": 0}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        metadata_id = metadata_dict["meta_id"]

        if metadata_dict == False or MetaUtil.change_metadata(metadata_id, metadata_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "metadata", 
                                                                metadata_id,
                                                                metadata_dict)

        LoggerHandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"meta_id": 1}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if metadata_dict == False or MetaUtil.delete_metadata(metadata_dict["meta_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "link", 
                                                                metadata_dict["meta_id"])

        LoggerHandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})