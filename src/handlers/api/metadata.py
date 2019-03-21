import handlers.logger as LoggerHandler
import handlers.jwt as JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.meta as MetadataUtil

class Metadata(SetDefaultHeaders):
    """
    Class to handle metadata API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get metadata or a single metadata record
        Inputs: Tornado web request
        Output: Metadata data
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"node_id":0, "link_id":0}
        metadata_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        if metadata_dict == False:
            self.set_status(400)
            self.write({"message":"Empty get request"})
            return None

        if "node_id" in metadata_dict:
            self.write(MetadataUtil.get_node_metadata(metadata_dict["node_id"]))
        else:
            self.write(MetadataUtil.get_link_metadata(metadata_dict["link_id"]))

    def post(self):
        """
        Function to create a metadata record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"node_id": 0, "link_id": 0,  "category" : 1, "data": 1}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        if metadata_dict == False:
            return None
        meta_id = 0
        if ("node_id" not in metadata_dict and "link_id" not in metadata_dict):
            self.set_status(400, "Empty object create request")
            self.write({"message": "Missing link_id or node_id field"})
            return None            
        else:
            meta_id = MetadataUtil.create_category(metadata_dict, self)
            if meta_id == False:
                return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                 "metadata", 
                                                                 meta_id,
                                                                 metadata_dict)

        LoggerHandler.log_message("add", formatted_message)

        self.write({"message":"Success", "payload":meta_id})

    def put(self):
        """
        Function to change a metadata record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"meta_id": 1, "node_id": 0, "link_id": 0,"category" : 0, "metadata": 0}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if "node_id" in metadata_dict and "link_id" in metadata_dict:
            self.set_status(400)
            self.write({"message": "Too many object id fields. Either use node_id or link_id"})
            return None  

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        metadata_id = metadata_dict["meta_id"]

        if metadata_dict == False or MetadataUtil.change_metadata(metadata_id, metadata_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "metadata", 
                                                                metadata_id,
                                                                metadata_dict)

        LoggerHandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self):
        """
        Function to delete a metadata record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"meta_id": 1}
        metadata_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if metadata_dict == False or MetadataUtil.delete_metadata(metadata_dict["meta_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "metadata", 
                                                                metadata_dict["meta_id"])

        LoggerHandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})