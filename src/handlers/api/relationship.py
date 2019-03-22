import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders

import utilities.error as errorutil
import utilities.relationship as relationshiputil

class Relationship(SetDefaultHeaders):
    """
    Class to handle relationship API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get relationships or a single relationship record
        Inputs: Tornado web request
        Output: Relationship data
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"relationship_id": 0}
        relationship_dict = errorutil.check_fields(self.request.arguments, body_categories, self)

        if relationship_dict == False:
            self.write(relationshiputil.get_relationships())
            return None

        if "relationship_id" in relationship_dict:
            self.write(relationshiputil.get_relationships(relationship_dict["relationship_id"])) 

    def post(self):
        """
        Function to create a relationship record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"message": 1}
        relationship_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if relationship_dict == False:
            return None
        relationship_id = relationshiputil.create_relationship(relationship_dict, self)
        if relationship_id == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "relationship", 
                                                                relationship_id,
                                                                relationship_dict)

        loggerhandler.log_message("add", formatted_message)
        self.write({"message":"Success", "payload": int(relationship_id)})

    def put(self):
        """
        Function to change a relationship record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        body_categories = {"relationship_id": 1, "message": 1}
        relationship_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        if relationship_dict == False:
            return None

        relationship_id = relationship_dict["relationship_id"]
        del relationship_dict["relationship_id"]

        if relationshiputil.change_relationship(relationship_id, relationship_dict, self) == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "relationship", 
                                                                relationship_id,
                                                                relationship_dict)


        loggerhandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self):
        """
        Function to delete a relationship record
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 2) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"relationship_id": 1}
        relationship_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if relationship_dict == False:
            return None

        if relationshiputil.delete_relationship(relationship_dict["relationship_id"], self) == False:
            return None

        formatted_message = loggerhandler.form_delete_message_dictionary(userdata, 
                                                                        "relationship", 
                                                                        relationship_dict["relationship_id"])

        loggerhandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})