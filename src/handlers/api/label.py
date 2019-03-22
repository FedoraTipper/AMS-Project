import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders

import utilities.error as errorutil
import utilities.label as labelutil

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
        if jwthandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"label_id":0}
        label_dict = errorutil.check_fields(self.request.arguments, body_categories, self)

        if label_dict == False:
            self.write(labelutil.get_labels())
            return None

        if "label_id" in label_dict:
            self.write(labelutil.get_label(label_dict["label_id"]))

    def post(self):
        """
        Function to create a new label
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None
        
        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_text": 1}
        label_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False or labelutil.create_label(label_dict, self) == False:
            return None

        label_id = labelutil.get_label_id(label_dict["label_text"])

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "label", 
                                                                label_id,
                                                                label_dict)


        loggerhandler.log_message("add", formatted_message)

        self.write({"message": "Success", "payload":label_id})

    def put(self):
        """
        Function to change a label
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_id": 1, "label_text": 0, "parent": 0}
        label_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False:
            return None

        label_id = label_dict["label_id"]
        del label_dict["label_id"]

        if labelutil.change_label(label_id, label_dict, self) == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "label", 
                                                                label_id,
                                                                label_dict)

        loggerhandler.log_message("change", formatted_message)


        self.write({"message":"Success"})

    def delete(self):
        """
        Function to delete a label
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"label_id": 1}
        label_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict == False or labelutil.delete_label(label_dict["label_id"], self) == False:
            return None

        formatted_message = loggerhandler.form_delete_message_dictionary(userdata, 
                                                                "label", 
                                                                label_dict["label_id"])


        loggerhandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})