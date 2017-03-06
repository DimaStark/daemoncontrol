

class MainHandler(tornado.web.RequestHandler):
    """ / Handler"""
    def initialize(self, daemon):
        self.daemon = daemon

    def get(self):
        self.render("html/layout.html",
                    state=STATE,
                    status=self.daemon.status)
