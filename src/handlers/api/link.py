import handlers.logger as loggerhandler
import handlers.jwt as  jwthandler
from handlers.headers import SetDefaultHeaders

import utilities.error as errorutil
import utilities.link as linkutil

class Link(SetDefaultHeaders):
    """
    Class to handle link API requests
    Functions: get, post, put, delete
    """
    def get(self):
        """
        Function to get links or a single link
        Inputs: Tornado web request
        Output: Link data
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        body_categories = {"link_id":0}
        link_dict = errorutil.check_fields(self.request.arguments, body_categories, self)

        if link_dict == False:
            self.write(linkutil.get_links())
            return None

        if "link_id" in link_dict:
            self.write(linkutil.get_link(link_dict["link_id"]))

    def post(self):
        """
        Function to create a link
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"node_id_1": 1, "node_id_2": 1, "view_id": 1, "relationship_id":0}
        link_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        link_id = linkutil.create_link(link_dict, self)
        if link_dict == False or  link_id == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "links", 
                                                                linkutil.get_link_id(link_dict["node_id_1"], link_dict["node_id_2"]),
                                                                link_dict)


        loggerhandler.log_message("add", formatted_message)

        self.write({"message":"Success", "payload":link_id})

    def put(self):
        """
        Function to change a link
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"link_id": 1, "view_id": 0, "node_id_1": 0, "node_id_2": 0, "relationship_id":0}
        link_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        print(link_dict)

        if link_dict == False:
            return None

        link_id = link_dict["link_id"]
        del link_dict["link_id"]

        if  linkutil.change_link(link_id, link_dict, self) == False:
            return None

        formatted_message = loggerhandler.form_message_dictionary(userdata, 
                                                                "links", 
                                                                link_id,
                                                                link_dict)


        loggerhandler.log_message("change", formatted_message)

        self.write({"message":"Success"})

    def delete(self):
        """
        Function to delete a link
        Inputs: Tornado web request
        Output: Success message
        Caveats: Authentication needs to be passed
        """
        if jwthandler.authorize_action(self, 1) == False:
            return None

        userdata = jwthandler.decode_userdata(self.request.headers["Authorization"])

        body_categories = {"link_id": 1}
        link_dict = errorutil.check_fields(self.request.body.decode(), body_categories, self)

        if link_dict == False or linkutil.delete_link(link_dict["link_id"], self) == False:
            return None

        formatted_message = loggerhandler.form_delete_message_dictionary(userdata, 
                                                                "link", 
                                                                link_dict["link_id"])


        loggerhandler.log_message("delete", formatted_message)

        self.write({"message":"Success"})