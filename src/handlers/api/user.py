import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders
import handlers.filelogger as FLHandler

import utilities.error as ErrorUtil
import utilities.user as UserUtil

class Authenticate(SetDefaultHeaders):
    def post(self):
        body_categories = {"username": 1, "password": 1}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict == False or UserUtil.user_exists(user_dict["username"]) == False:
            statement = "Failed login attempt %s : %s", (user_dict["username"], user_dict["password"])
            FLHandler.log_debug_to_file(statement)
            self.set_status(401)
            self.write({"message":"Authentication failed"})
            return None
        if(UserUtil.compare_password(user_dict["username"], user_dict["password"]) == False):
            statement = "Failed login attempt %s : %s", (user_dict["username"], user_dict["password"])
            FLHandler.log_debug_to_file(statement)
            self.set_status(401)
            self.write({"message":"Authentication failed"})
            return None

        username = user_dict["username"].lower()
        token = JWTHandler.create_token(UserUtil.get_uid(username), username,  (UserUtil.get_privilege(username) + 1))

        self.add_header("Authorization", token)
        self.write({"message":"Authenticated", "payload":{"User": username, "privilege": (UserUtil.get_privilege(username) + 1) >= 2}})

class Register(SetDefaultHeaders):
    def post(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"username": 1, "password": 1, "privilege": 0}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict == False or UserUtil.create_user(user_dict, self) == False:
            return None

        username = user_dict["username"]

        token = JWTHandler.create_token(UserUtil.get_uid(username), username,  UserUtil.get_privilege(username) + 1)
        self.add_header("token", token)

        #sanitise password for logs
        del user_dict["password"]

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                        "user", 
                                                        UserUtil.get_uid(username),
                                                        user_dict)
    
        LoggerHandler.log_message("add", formatted_message)


        self.write({'message': "Success"})

class Password(SetDefaultHeaders):
    def put(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        user_data = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"old_password": 1, "new_password": 1}
        password_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)
        print(UserUtil.compare_password(user_data["username"], password_dict["old_password"]))
        if UserUtil.compare_password(user_data["username"], password_dict["old_password"]):
            user_id = user_data["uid"]
            if UserUtil.change_password(user_id, password_dict["new_password"]):
                self.write({"message":"Success"})
            else:
                self.set_status(500)
                self.write({"message":"Failed to change password"})
                return None
        else:
            self.write({"message":"Failed to change password"})
            return None

        formatted_message = LoggerHandler.form_message_dictionary(user_data, 
                                                        "user", 
                                                        user_data["uid"],
                                                        {"old_password":"", "new_password":""})
    
        LoggerHandler.log_message("add", formatted_message)
        return None

class User(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        body_categories = {"username": 1}
        user_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if user_dict == False:
            return None

        self.write({"user_id": UserUtil.get_uid(user_dict["username"])})

    def put(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        body_categories = {"username": 1, "password": 0, "admin": 0}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict == False or UserUtil.change_user_fields(user_dict, self) == False:
            return None

        self.write({'message': "Success"})