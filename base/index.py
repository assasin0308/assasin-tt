# -*- coding:utf-8 -*-
# @Time: 2020/7/2 10:26
# @Author: assasin
# @Email: <assasin0308@sina.com>
# @File: index.py

import tornado.web
import tornado.ioloop
import tornado.httpserver

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("index.page")




if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/",IndexHandler),
    ],debug=True)

    # app.listen(8000)
    http_server = tornado.httpserver.HTTPServer(app)
    tornado.ioloop.IOLoop.current().start()