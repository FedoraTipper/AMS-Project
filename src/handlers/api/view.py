from tornado.web import RequestHandler

import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil
import utilities.view as ViewUtil

class View(SetDefaultHeaders):
    def get(self):
        return None