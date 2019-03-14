from tornado.web import RequestHandler

import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.type as TypeUtil

class NodeType(SetDefaultHeaders):
    def get(self):
        return None