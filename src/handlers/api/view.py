import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.view as ViewUtil

class View(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"view_id":0}
        view_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)
        
        if view_dict == False:
            self.write(ViewUtil.get_views())
            return None

        if "view_id" in view_dict:
            self.write(ViewUtil.get_view(view_dict["view_id"]))

    def post(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"name": 1}
        view_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if view_dict == False or ViewUtil.create_view(view_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "views", 
                                                                ViewUtil.get_view_id(view_dict["name"]),
                                                                view_dict)


        LoggerHandler.log_message("add", formatted_message)

        self.write({"message": "Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"view_id": 1, "name": 1}
        view_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if view_dict == False:
            return None

        view_id = view_dict["view_id"]
        del view_dict["view_id"]

        if ViewUtil.change_view(view_id, view_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "views", 
                                                                view_id,
                                                                view_dict)

        LoggerHandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self): 
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"view_id":1}
        view_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if view_dict == False or ViewUtil.delete_view(view_dict["view_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "views", 
                                                                view_dict["view_id"])

        LoggerHandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})