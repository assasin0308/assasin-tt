# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop

class IndexHandler(tornado.web.RequestHandler):
    """主页处理类"""
    def get(self):
        """GET请求方式"""
        self.write("this is index page")







if __name__ == '__main__':
    app = tornado.web.Application(
    [
        (r"/",IndexHandler),
    ],
    debug=True
    )
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

