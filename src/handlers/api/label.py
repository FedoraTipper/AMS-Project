from tornado.web import RequestHandler

import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.label as LabelUtil

class Label(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"label_id":0}
        label_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if label_dict == False:
            self.write(LabelUtil.get_labels())
            return None

        if "label_id" in label_dict:
            self.write(LabelUtil.get_label(label_dict["label_id"]))

    """
    Only admins may create new labels/collections
    """
    def post(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None
        
        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_text": 1, "parent": 0}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False or LabelUtil.create_label(label_dict, self) == False:
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
        try:
            LoggerHandler.log_message("change", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self):
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

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})