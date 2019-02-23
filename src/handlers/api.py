from tornado.web import RequestHandler
import handlers.mysqldb as DBHandler
import handlers.logger as LoggerHandler
import handlers.config as ConfigHandler
import utilities.user as UserUtil
import utilities.label as LabelUtil
import utilities.node as NodeUtil
import utilities.jwt as  JWTUtil
import json

Logger = LoggerHandler.Logger()


class Authenticate(RequestHandler):
    def post(self):        
        body = self.request.body.decode()
        json_body = json.loads(body)
        username = json_body["username"]
        password = json_body["password"]

        if len(password) == 0 and len(username) == 0:
            self.write({'message': "Empty strings"})
            return None

        if(UserUtil.compare_password(username, password) == False):
            self.write({"message":"Authentication failed"})

        token = JWTUtil.create_token(UserUtil.get_uid(username), username,  UserUtil.get_privilege(username))

        self.add_header("Authorization", token)
        self.write({"message":"Authenticated"})



class Register(RequestHandler):
    def post(self):
        body = self.request.body.decode()
        json_body = json.loads(body)
        username = json_body["username"]
        password = json_body["password"]
        admin = int(json_body["admin"]) if json_body["admin"] == "1" else 0

        if len(password) == 0 and len(username) == 0:
            self.write({'message': "Empty username/password"})
            return None

        if UserUtil.user_exists(username):
            self.write({'message': "Username exists"})
            return None

        UserUtil.create_user(username, password, admin)

        token = JWTUtil.create_token(UserUtil.get_uid(username), username,  UserUtil.get_privilege(username))
        self.add_header("token", token)
        self.write({'message': "Success"})

class User(RequestHandler):
    def get(self):

        encoded_token = self.request.headers["Authorization"] if "Authorization" in self.request.headers else ""

        if JWTUtil.determine_privilege(encoded_token) == 0:
            self.write({"message":"Authorization failed"})
            self.add_header("Authorization", "")
            return None

        body = self.request.body.decode()
        json_body = json.loads(body)
        username = json_body["username"]

        if len(username) == 0:
            self.write({'message': "Empty strings"})
            return None

        user_id = UserUtil.get_uid(username)

        self.write({"user_id": user_id})

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

        encoded_token = self.request.headers["Authorization"] if "Authorization" in self.request.headers else ""

        if JWTUtil.determine_privilege(encoded_token) == 0:
            self.write({"message":"Authorization failed"})
            self.add_header("Authorization", "")
            return None

        body = self.request.body.decode()
        json_body = json.loads(body)

        uid = UserUtil.get_uid(JWTUtil.decode_token(encoded_token)["username"])
        label_text = json_body["label_text"]

        if len(label_text) == 0:
            self.write({'message': "Empty label text/type"})
            return None

        if LabelUtil.label_exists(label_text):
            self.write({'message': "Label exists"})
            return None

        LabelUtil.create_label(label_text, uid)
        self.write({"message": "Success"})

    def put(self):
        decoded_token = JWTUtil.authorize_action(self)
        if decoded_token == None:
            return None

        body = self.request.body.decode()
        json_body = json.loads(body)

        body_categories = {"label_id": 1, "label_text": 1}
        label_dict = {}

        for category in body_categories:
            if category not in json_body and body_categories[category] == 1:
                self.write({"message":"Missing fields"})
                return None
            elif category not in json_body and body_categories[category] == 0:
                pass
            else:
                label_dict[category] = json_body[category]

        label_id = json_body["label_id"]
        del label_dict["label_id"]
        LabelUtil.change_label(label_id, label_dict)
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
        encoded_token = self.request.headers["Authorization"] if "Authorization" in self.request.headers else ""

        decoded_token = JWTUtil.decode_token(encoded_token) if encoded_token != "" else 0
        print(decoded_token)
        if decoded_token["privilege"] == 0:
            self.write({"message":"Authorization failed"})
            self.add_header("Authorization", "")
            return None

        body = self.request.body.decode()
        json_body = json.loads(body)
        uid = decoded_token["uid"]
        node_type = json_body["type"]

        if len(node_type) == 0:
            self.write({'message': "Empty node type"})
            return None

        if NodeUtil.node_exists(node_type):
            self.write({'message': "Node exists"})
            return None        

        NodeUtil.create_node(node_type, uid)
        self.write({"message": "Success"})


    def put(self):
        decoded_token = JWTUtil.authorize_action(self)
        if decoded_token == None:
            return None

        body = self.request.body.decode()
        json_body = json.loads(body)

        body_categories = {"type": 0, "node_id": 1, "label_id": 0}
        node_dict = {}

        for category in body_categories:
            if category not in json_body and body_categories[category] == 1:
                self.write({"message":"Missing fields"})
                return None
            elif category not in json_body and body_categories[category] == 0:
                pass
            else:
                node_dict[category] = json_body[category]

        node_id = json_body["node_id"]
        del node_dict["node_id"]
        NodeUtil.change_node(node_id, node_dict)
        self.write({"message":"Success"})

    def delete(self):  
        return None
  
class Link(RequestHandler):
    def get(self):
        return None

    def post(self):
        #Handle user authorisation
        decoded_token = JWTUtil.authorize_action(self)
        if decoded_token == None:
            return None

        body = self.request.body.decode()
        json_body = json.loads(body)

        body_categories = {"node_id_1": 1, "node_id_2": 1, "label_id": 0}
        node_dict = {}

        for category in body_categories:
            if category not in json_body and body_categories[category] == 1:
                self.write({"message":"Missing fields: {}".format(category)})
                return None
            elif category not in json_body and body_categories[category] == 0:
                pass
            else:
                node_dict[category] = json_body[category]

        uid = decoded_token["uid"]
        

    def put(self):
        return None

    def delete(self):
        return None

class Metadata(RequestHandler):
    def get(self):
        return None

    def post(self):
        return None

    def put(self):
        return None

    def delete(self):
        return None


