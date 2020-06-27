# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json


from tornado.options import define,options
from tornado.web import RequestHandler,url


define("port",type=int,default=8000,help="服务器监听端口")


class Indexhandler(RequestHandler):
    """主页处理类"""
    def  get(self):
        # self.write(chunk)
        # self.write(" index page 1 ")
        # self.write(" index page 2 ")
        # self.write(" index page 3 ")
        # 输出json数据
        stu = {
            "name":"zhangsan",
            "age":25,
            "gender":1
        }
        # self.write(json.dumps(stu))
        # self.set_header("Content-Type", "application/json; charset=UTF-8")
        # 不用自己手动去做json序列化，当write方法检测到传入的chunk参数是字典类型后，
        # 会自动帮我们转换为json字符串。
        self.write(stu)

    def post(self):
        files = self.request.files
        img_files = files.get('img')
        if img_files:
            img_file = img_files[0]['body']
            # print(img_file)
            file = open('./itcast','w+')
            file.write(img_file)
            file.close()
        self.write('OK')

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



