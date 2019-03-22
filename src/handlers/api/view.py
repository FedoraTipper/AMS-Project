import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders

import utilities.error as errorutil
import utilities.view as viewutil

class View(SetDefaultHeaders):
    """
    Class to handle view API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get views or a single view record
        Inputs: Tornado web request
        Output: View data
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"view_id":0}
        view_dict = errorutil.check_fields(self.request.arguments, body_categories, self)
        
        if view_dict == False:
            self.write(viewutil.get_views())
            return None

        if "view_id" in view_dict:
            self.write(viewutil.get_view(view_dict["view_id"]))

    def post(self):
        """
        Function to create a view record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"name": 1}
        view_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if view_dict == False or viewutil.create_view(view_dict, self) == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "views", 
                                                                viewutil.get_view_id(view_dict["name"]),
                                                                view_dict)


        loggerhandler.log_message("add", formatted_message)

        self.write({"message": "Success"})

    def put(self):
        """
        Function to change a view record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"view_id": 1, "name": 1}
        view_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if view_dict == False:
            return None

        view_id = view_dict["view_id"]
        del view_dict["view_id"]

        if viewutil.change_view(view_id, view_dict, self) == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "views", 
                                                                view_id,
                                                                view_dict)

        loggerhandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self):
        """
        Function to delete a view record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """ 
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"view_id":1}
        view_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if view_dict == False or viewutil.delete_view(view_dict["view_id"], self) == False:
            return None

        formatted_message = loggerhandler.form_delete_message_dictionary(userdata, 
                                                                "views", 
                                                                view_dict["view_id"])

        loggerhandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})