from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import handlers.api as APIHandler
import os

def make_app():
  urls = [("/api/auth/", APIHandler.Authenticate),
          ("/api/register/", APIHandler.Register),
          ("/api/user/", APIHandler.User),
          ("/api/node/", APIHandler.Node),
          ("/api/link/", APIHandler.Link),
          ("/api/label/", APIHandler.Label),
          ("/api/metadata/", APIHandler.Metadata),
          ("/api/relationship/", APIHandler.Relationship),
          ("/api/logs/", APIHandler.Log)]

  return Application(urls,
  ssl_options = {
    "certfile": os.path.join("certs/server.crt"),
    "keyfile": os.path.join("certs/server.key")
  }, debug=True)
  
if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    IOLoop.instance().start()

