import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.label as LabelUtil

class Label(SetDefaultHeaders):
    """
    Class to handle label API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get all labels or a single label record
        Inputs: Tornado web request
        Output: Label data
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"label_id":0}
        label_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if label_dict == False:
            self.write(LabelUtil.get_labels())
            return None

        if "label_id" in label_dict:
            self.write(LabelUtil.get_label(label_dict["label_id"]))

    def post(self):
        """
        Function to create a new label
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 2) == False:
            return None
        
        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_text": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False or LabelUtil.create_label(label_dict, self) == False:
            return None

        label_id = LabelUtil.get_label_id(label_dict["label_text"])

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "label", 
                                                                label_id,
                                                                label_dict)


        LoggerHandler.log_message("add", formatted_message)

        self.write({"message": "Success", "payload":label_id})

    def put(self):
        """
        Function to change a label
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_id": 1, "label_text": 0, "parent": 0}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False:
            return None

        label_id = label_dict["label_id"]
        del label_dict["label_id"]

        if LabelUtil.change_label(label_id, label_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "label", 
                                                                label_id,
                                                                label_dict)

        LoggerHandler.log_message("change", formatted_message)


        self.write({"message":"Success"})

    def delete(self):
        """
        Function to delete a label
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_id": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False or LabelUtil.delete_label(label_dict["label_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "label", 
                                                                label_dict["label_id"])


        LoggerHandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})