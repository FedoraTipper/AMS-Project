import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders
import handlers.filelogger as flhandler

import utilities.error as errorutil
import utilities.user as userutil

class Authenticate(SetDefaultHeaders):
    """
    Class to handle Authentication API requests
    Functions: post
    """
    def post(self):
        """
        Function to authenticate a user
        Inputs: Tornado web request
        Output: Success message; Encrypted JWT token and user payload data
        Caveats: Authentication needs to be passed
        """
        body_categories = {"username": 1, "password": 1}
        user_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict == False or userutil.user_exists(user_dict["username"]) == False:
            statement = "Failed login attempt %s : %s", (user_dict["username"], user_dict["password"])
            flhandler.log_debug_to_file(statement)
            self.set_status(401)
            self.write({"message":"Authentication failed"})
            return None
        if(userutil.compare_password(user_dict["username"], user_dict["password"]) == False):
            statement = "Failed login attempt %s : %s", (user_dict["username"], user_dict["password"])
            flhandler.log_debug_to_file(statement)
            self.set_status(401)
            self.write({"message":"Authentication failed"})
            return None

        username = user_dict["username"].lower()
        token = jwthandler.create_token(userutil.get_uid(username), username,  (userutil.get_privilege(username) + 1))

        self.add_header("Authorization", token)
        self.write({"message":"Authenticated", "payload":{"User": username, "privilege": (userutil.get_privilege(username) + 1) >= 2}})

class Register(SetDefaultHeaders):
    """
    Class to handle registration API requests
    Functions: post
    """
    def post(self):
        """
        Function to register a new password
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 0) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"username": 1, "password": 1, "privilege": 0}
        user_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict == False or userutil.create_user(user_dict, self) == False:
            return None

        username = user_dict["username"]

        token = jwthandler.create_token(userutil.get_uid(username), username,  userutil.get_privilege(username) + 1)
        self.add_header("token", token)

        #sanitise password for logs
        del user_dict["password"]

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                        "user", 
                                                        userutil.get_uid(username),
                                                        user_dict)
    
        loggerhandler.log_message("add", formatted_message)


        self.write({'message': "Success"})

class Password(SetDefaultHeaders):
    """
    Class to handle password API requests
    Functions: put
    """
    def put(self):
        """
        Function to change a user password
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        user_data = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"old_password": 1, "new_password": 1}
        password_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)
        print(userutil.compare_password(user_data["username"], password_dict["old_password"]))
        if userutil.compare_password(user_data["username"], password_dict["old_password"]):
            user_id = user_data["uid"]
            if userutil.change_password(user_id, password_dict["new_password"]):
                self.write({"message":"Success"})
            else:
                self.set_status(500)
                self.write({"message":"Failed to change password"})
                return None
        else:
            self.write({"message":"Failed to change password"})
            return None

        formatted_message = loggerhandler.form_message_dictionary(user_data, 
                                                        "user", 
                                                        user_data["uid"],
                                                        {"old_password":"", "new_password":""})
    
        loggerhandler.log_message("add", formatted_message)
        return None

class User(SetDefaultHeaders):
    """
    Class to handle password API requests
    Functions: get, put
    """
    def get(self):
        """
        Function to get user data
        Inputs: Tornado web request
        Output: User ID
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        body_categories = {"username": 1}
        user_dict = errorutil.check_fields(self.request.arguments, body_categories, self)

        if user_dict == False:
            return None

        self.write({"user_id": userutil.get_uid(user_dict["username"])})

    def put(self):
        """
        Function to change user data
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        body_categories = {"username": 1, "password": 0, "admin": 0}
        user_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict == False or userutil.change_user_fields(user_dict, self) == False:
            return None

        self.write({'message': "Success"})