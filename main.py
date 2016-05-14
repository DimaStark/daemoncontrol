#!/usr/bin/python3
#coding: utf-8
"""Main entry of the server"""
import tornado.ioloop
import tornado.web
from daemon import Daemon
from os.path import exists


STATE = False


class MainHandler(tornado.web.RequestHandler):
    """ / Handler"""
    def initialize(self, daemon):
        self.daemon = daemon

    def get(self):
        self.render("html/index.html", 
                    state=STATE,
                    status=self.daemon.status)


class StartHandler(tornado.web.RequestHandler):
    """ /start Handler"""
    def initialize(self, daemon):
        self.daemon = daemon

    def get(self):
        if STATE:
            self.daemon.start()
            self.render("html/answer.html", answer="Daemon start")
        else:
            self.render("html/answer.html", answer="Service is disabled")


class StopHandler(tornado.web.RequestHandler):
    """ /stop Handler"""
    def initialize(self, daemon):
        self.daemon = daemon

    def get(self):
        if STATE:
            self.daemon.stop()
            self.render("html/answer.html", 
                        answer="Daemon stop")
        else:
            self.render("html/answer.html", answer="Service is disabled")


class RestartHandler(tornado.web.RequestHandler):
    """ /restart Handler"""
    def initialize(self, daemon):
        self.daemon = daemon

    def get(self):
        if STATE:
            self.daemon.restart()
            self.render("html/answer.html", 
                        answer="Daemon restart")
        else:
            self.render("html/answer.html", answer="Service is disabled")


class SwitchHandler(tornado.web.RequestHandler):
    """ /switch Handler"""
    def get(self):
        global STATE
        STATE = not STATE
        self.render("html/answer.html", answer="Switched")


def get_state_value():
    """Get saved value from file (if exists)"""
    if exists("state"):
        with open("state") as state:
            return state.read() == "1"
    else:
        return STATE


def make_app():
    """Make tornado app"""
    global STATE
    STATE = get_state_value()
    dct = {"daemon": Daemon("apache2")}
    return tornado.web.Application([
        (r"/", MainHandler, dct),
        (r"/switch", SwitchHandler),
        (r"/start", StartHandler, dct),
        (r"/stop", StopHandler, dct),
        (r"/restart", RestartHandler, dct),
    ])


if __name__ == "__main__":
    try:
        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    finally:
        with open("state", mode="w") as state:
            state.write("1" if STATE else "0")