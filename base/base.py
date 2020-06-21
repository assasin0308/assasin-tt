# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

from tornado.options import define,options
from tornado.web import RequestHandler,url


tornado.options.define("port",type=int,default=8000,help="服务器监听端口")


class Indexhandler(RequestHandler):
    """主页处理类"""
    def  get(self):
        self.write(" index page ")
        # self.write("<a href= ' " + self.reverse_url("cpp_url") + " '>cpp</a>")
        # subject = self.get_argument("subject")
        # query_data = self.get_arguments("q")
        # query_body = self.get_body_argument("q")
        # query_body = self.get_body_arguments("q")
        # self.write(query_data)

class SubjectHandler(RequestHandler):
    def initialize(self,subject):
        self.subject = subject

    def  get(self):
        self.write(self.subject)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        [
            (r"/",Indexhandler),
            (r"/python",SubjectHandler,{"subject":"python"}),
            url(r"/cpp",SubjectHandler,{"subject":"cpp"},name="cpp_url"),
        ],
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
