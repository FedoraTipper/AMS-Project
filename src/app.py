from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import handlers.api as APIHandler

def make_app():
  urls = [("/api/auth/", APIHandler.Authenticate),
          ("/api/register/", APIHandler.Register),
          ("/api/user", APIHandler.User),
          ("/api/node", APIHandler.Node),
          ("/api/link", APIHandler.Link),
          ("/api/label", APIHandler.Label),
          ("/api/metadata", APIHandler.Metadata)]
  return Application(urls, debug=True)
  
if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    IOLoop.instance().start()

