import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.link as LinkUtil

class Link(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"link_id":0}
        link_dict = ErrorUtil.check_fields(self.request.arguments, body_categories, self)

        if link_dict == False:
            self.write(LinkUtil.get_links())
            return None

        if "link_id" in link_dict:
            self.write(LinkUtil.get_link(link_dict["link_id"]))

    def post(self):
        #User level privilege
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"node_id_1": 1, "node_id_2": 1, "view_id": 1, "relationship_id":0}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        link_id = LinkUtil.create_link(link_dict, self)
        if link_dict == False or  link_id == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "links", 
                                                                LinkUtil.get_link_id(link_dict["node_id_1"], link_dict["node_id_2"]),
                                                                link_dict)

        try:
            LoggerHandler.log_message("add", formatted_message)
        except:
            pass

        self.write({"message":"Success", "payload":link_id})

    def put(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"link_id": 1, "view_id": 0, "node_id_1": 0, "node_id_2": 0, "relationship_id":0}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        print(link_dict)

        if link_dict == False:
            return None

        link_id = link_dict["link_id"]
        del link_dict["link_id"]

        if  LinkUtil.change_link(link_id, link_dict, self) == False:
            return None

        formatted_message = LoggerHandler.form_message_dictionary(userdata, 
                                                                "links", 
                                                                link_id,
                                                                link_dict)

        try:
            LoggerHandler.log_message("change", formatted_message)
        except:
            pass

        self.write({"message":"Success"})

    def delete(self):
        if JWTHandler.authorize_action(self, 1) == False:
            return None

        userdata = JWTHandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"link_id": 1}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if link_dict == False or LinkUtil.delete_link(link_dict["link_id"], self) == False:
            return None

        formatted_message = LoggerHandler.form_delete_message_dictionary(userdata, 
                                                                "link", 
                                                                link_dict["link_id"])

        try:
            LoggerHandler.log_message("delete", formatted_message)
        except:
            pass

        self.write({"message":"Success"})