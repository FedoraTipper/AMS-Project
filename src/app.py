from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import handlers.api.node as NodeHandler
import handlers.api.user as UserHandler
import handlers.api.link as LinkHandler
import handlers.api.label as LabelHandler
import handlers.api.metadata as MetadataHandler
import handlers.api.relationship as RelationshipHandler
import handlers.api.view as ViewHandler
import handlers.api.type as TypeHandler
import handlers.api.logs as LogHandler

def make_app():
  urls = [("/api/auth/", UserHandler.Authenticate),
          ("/api/register/", UserHandler.Register),
          ("/api/user/", UserHandler.User),
          ("/api/node/", NodeHandler.Node),
          ("/api/link/", LinkHandler.Link),
          ("/api/label/", LabelHandler.Label),
          ("/api/metadata/", MetadataHandler.Metadata),
          ("/api/relationship/", RelationshipHandler.Relationship),
          ("/api/logs/", LogHandler.Log),
          ("/api/view/", ViewHandler.View),
          ("/api/type/", TypeHandler.NodeType)]

  return Application(urls, debug=True)
  
if __name__ == '__main__':
    app = make_app()
    port = 5000
    app.listen(port)
    print("Starting on port %d" % port)
    IOLoop.instance().start()