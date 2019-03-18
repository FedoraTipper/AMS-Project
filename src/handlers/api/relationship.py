import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.relationship as RelationshipUtil

class Relationship(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"relationship_id": 0}
        relationship_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if relationship_dict == False:
            self.write(RelationshipUtil.get_relationships())
            return None

        if "relationship_id" in relationship_dict:
            self.write(RelationshipUtil.get_relationships(relationship_dict["relationship_id"])) 

    def post(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"message": 1}
        relationship_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if relationship_dict == False or RelationshipUtil.create_relationship(relationship_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "relationship", 
                                                                RelationshipUtil.get_relationship_id(body_categories["message"]),
                                                                relationship_dict)


        LoggerHandler.log_message("add", formatted_message)

        self.write({"message":"Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        body_categories = {"relationship_id": 1, "message": 1}
        relationship_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        if relationship_dict == False:
            return None

        relationship_id = relationship_dict["relationship_id"]
        del relationship_dict["relationship_id"]

        if RelationshipUtil.change_relationship(relationship_id, relationship_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "relationship", 
                                                                relationship_id,
                                                                relationship_dict)


        LoggerHandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"relationship_id": 1}
        relationship_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if relationship_dict == False:
            return None

        if RelationshipUtil.delete_link_with_relationship(relationship_dict["relationship_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                        "relationship", 
                                                                        relationship_dict["relationship_id"])

        LoggerHandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})