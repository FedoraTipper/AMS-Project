from tornado.web import RequestHandler

import handlers.mysqldb as DBHandler
import handlers.logger as LoggerHandler
import handlers.config as ConfigHandler
import handlers.jwt as  JWTHandler

import utilities.user as UserUtil
import utilities.label as LabelUtil
import utilities.node as NodeUtil
import utilities.link as LinkUtil
import utilities.error as ErrorUtil
import utilities.meta as MetaUtil


Logger = LoggerHandler.Logger()

class Authenticate(RequestHandler):
    def get(self):        
        body_categories = {"username": 1, "password": 1}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict is None:
            return None

        if(UserUtil.compare_password(user_dict["username"], user_dict["password"]) == False):
            self.write({"message":"Authentication failed"})
            return None

        username = user_dict["username"]
        token = JWTHandler.create_token(UserUtil.get_uid(username), username,  (UserUtil.get_privilege(username) + 1))

        self.add_header("Authorization", token)
        self.write({"message":"Authenticated"})

class Register(RequestHandler):
    def post(self):
        body_categories = {"username": 1, "password": 1, "privilege": 0}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict is None:
            return None

        if UserUtil.user_exists(user_dict["username"]):
            self.write({'message': "User does not exists"})
            return None

        UserUtil.create_user(user_dict)
        username = user_dict["username"]
        token = JWTHandler.create_token(UserUtil.get_uid(username), username,  UserUtil.get_privilege(username) + 1)
        self.add_header("token", token)
        self.write({'message': "Success"})

class User(RequestHandler):
    def get(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        body_categories = {"username": 1}
        user_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if user_dict is None:
            return None

        self.write({"user_id": UserUtil.get_uid(user_dict["username"])})

    """
    Change user information
    Come back
    """
    def put(self):
        body = self.request.body.decode()
        json_body = json.loads(body)
        username = json_body["username"]
        del json_body["username"]
        #Handle administration access
        if UserUtil.user_exists(username):
            uid = UserUtil.get_uid(username)
            UserUtil.change_user_information(uid, json_body)
        else:
            self.write({'message': "Username does not exist"})

    def delete(self):
        return None

class Label(RequestHandler):
    def get(self):
        if len(self.request.body) != 0:
            body = self.request.body.decode()
            json_body = json.loads(body)
            if "label_id" in json_body:
                self.write(LabelUtil.get_label(json_body["label_id"]))
                return None
        self.write(LabelUtil.get_labels())
    """
    Only admins may create new labels/collections
    """
    def post(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        body_categories = {"label_text": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict is None:
            return None

        if LabelUtil.create_label(label_dict, self) is None:
            return None

        self.write({"message": "Success"})

    def put(self):
        decoded_token = JWTHandler.authorize_action(self, 2)
        if decoded_token == None:
            return None

        body_categories = {"label_id": 1, "label_text": 1}
        label_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if label_dict is None:
            return None

        label_id = json_body["label_id"]
        del label_dict["label_id"]
        if LabelUtil.change_label(label_id, label_dict, self) is None:
            return None

        self.write({"message":"Success"})


    def delete(self):
        return None

class Node(RequestHandler):
    def get(self):
        if len(self.request.body) != 0:
            body = self.request.body.decode()
            json_body = json.loads(body)
            if "node_id" in json_body:
                self.write(NodeUtil.get_node(json_body["node_id"]))
                return None
        self.write(NodeUtil.get_nodes())

    def post(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"type": 1, "label_id": 0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)
        
        if node_dict is None:
            return None

        if NodeUtil.create_node(node_dict, self):
            return None

        self.write({"message": "Success"})


    def put(self):
        if JWTHandler.authorize_action(self, 2) is None:
            return None

        body_categories = {"type": 0, "node_id": 1, "label_id": 0}
        node_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if node_dict is None:
            return None

        node_id = json_body["node_id"]
        del node_dict["node_id"]

        if NodeUtil.change_node(node_id, node_dict, self) is None:
            return None

        self.write({"message":"Success"})

    def delete(self):  
        return None
  
class Link(RequestHandler):
    def get(self):
        if len(self.request.body) != 0:
            body = self.request.body.decode()
            json_body = json.loads(body)
            if "link_id" in json_body:
                self.write(LinkUtil.get_link(json_body["link_id"]))
                return None
        self.write(LinkUtil.get_links())

    def post(self):
        #User level privilege
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"node_id_1": 1, "node_id_2": 1}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)
        
        if link_dict is None:
            return None

        LinkUtil.create_link(link_dict)
        self.write({"message":"Success"})

    def put(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"link_id": 1, "node_id_1": 0, "node_id_2": 0, "label_id": 0}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)

        if link_dict is None:
            return None

        link_id = link_dict["link_id"]
        del link_dict["link_id"]

        LinkUtil.change_link(link_id, link_dict)
        self.write({"message":"Success"})

    def delete(self):
        return None

class Metadata(RequestHandler):
    def get(self):
        if len(self.request.body) != 0:
            body = self.request.body.decode()
            json_body = json.loads(body)
            if "meta_id" in json_body:
                self.write(LinkUtil.get_link(json_body["meta_id"]))
                return None
        self.write(LinkUtil.get_links())

    def post(self):
        if JWTHandler.authorize_action(self, 1) is None:
            return None

        body_categories = {"node_id_1": 1, "node_id_2": 1}
        link_dict = ErrorUtil.check_fields(self.request.body.decode(), body_categories, self)
        
        if link_dict is None:
            return None

        LinkUtil.create_link(link_dict)
        self.write({"message":"Success"})

    def put(self):
        return None

    def delete(self):
        return None


