from tornado.web import RequestHandler

import utilities.error as ErrorUtil
import handlers.logger as LoggerHandler
import handlers.jwt as  JWTHandler
from handlers.headers import SetDefaultHeaders

import utilities.error as ErrorUtil

class Log(SetDefaultHeaders):
    def get(self):
        if JWTHandler.authorize_action(self, 2) == False:
            return None

        self.write(LoggerHandler.get_logs())