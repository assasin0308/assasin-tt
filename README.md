# tornado

## 十一 Tornado

```
# Tornado全称Tornado Web Server，是一个用Python语言写成的Web服务器兼Web应用框架，由FriendFeed公司在自己的网站FriendFeed中使用，被Facebook收购以后框架在2009年9月以开源软件形式开放给大众。

# 特点：

# 1. 作为Web框架，是一个轻量级的Web框架，类似于另一个Python web框架Web.py，其拥有异步非阻塞IO的处理方式。
# 2.作为Web服务器，Tornado有较为出色的抗负载能力，官方用nginx反向代理的方式部署Tornado和其它Python web应用框架进行对比，结果最大浏览量超过第二名近40%。
# 3.性能：Tornado有着优异的性能。它试图解决C10k问题，即处理大于或等于一万的并发

# Tornado框架和服务器一起组成一个WSGI的全栈替代品。单独在WSGI容器中使用tornado网络框架或者tornaod http服务器，有一定的局限性，为了最大化的利用tornado的性能，推荐同时使用tornaod的网络框架和HTTP服务器

# Tornado与Django
# Django是走大而全的方向，注重的是高效开发，它最出名的是其全自动化的管理后台：只需要使用起ORM，做简单的对象定义，它就能自动生成数据库结构、以及全功能的管理后台。

# Django提供的方便，也意味着Django内置的ORM跟框架内的其他模块耦合程度高，应用程序必须使用Django内置的ORM，否则就不能享受到框架内提供的种种基于其ORM的便利。

# session功能
# 后台管理
# ORM

# Tornado走的是少而精的方向，注重的是性能优越，它最出名的是异步非阻塞的设计方式。

# HTTP服务器
# 异步编程
# WebSockets
```

### 177. 安装

```
#  pip install tornado
```

### 178. Hello Wrold

```
import tornado.web
  import tornado.ioloop

  class IndexHandler(tornado.web.RequestHandler):
      """主路由处理类"""
      def post(self):  # 我们修改了这里
          """对应http的post请求方式"""
          self.write("Hello Wrold!")

  if __name__ == "__main__":
      app = tornado.web.Application([
          (r"/", IndexHandler),
      ])
      app.listen(8000)
      tornado.ioloop.IOLoop.current().start()
        
# 代码讲解:
# 1. tornado.web
# tornado的基础web框架模块
# RequestHandler 封装了对应一个请求的所有信息和方法，write(响应信息)就是写响应信息的一个方法；对应每一种http请求方式（get、post等），把对应的处理逻辑写进同名的成员方法中（如对应get请求方式，就将对应的处理逻辑写在get()方法中），当没有对应请求方式的成员方法时，会返回“405: Method Not Allowed”错误。
# Application Tornado Web框架的核心应用类，是与服务器对接的接口，里面保存了路由信息表，其初始化接收的第一个参数就是一个路由信息映射元组的列表；其listen(端口)方法用来创建一个http服务器实例，并绑定到给定端口（注意：此时服务器并未开启监听）。

# 2. tornado.ioloop
# tornado的核心io循环模块，封装了Linux的epoll和BSD的kqueue，tornado高性能的基石。
# IOLoop.current()  返回当前线程的IOLoop实例。
# IOLoop.start() 启动IOLoop实例的I/O循环,同时服务器监听被打开。

# 思路总结:
# 创建web应用实例对象，第一个初始化参数为路由映射列表。
# 定义实现路由映射列表中的handler类。
# 创建服务器实例，绑定服务器端口。
# 启动当前线程的IOLoop。
```

### 179. httpserver

```
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver # 新引入httpserver模块

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    # ------------------------------
    # 我们修改这个部分
    # app.listen(8000)
    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(8000)
    # ------------------------------
    tornado.ioloop.IOLoop.current().start()

# 引入了tornado.httpserver模块，顾名思义，它就是tornado的HTTP服务器实现。

# 我们创建了一个HTTP服务器实例http_server，因为服务器要服务于我们刚刚建立的web应用，将接收到的客户端请求通过web应用中的路由映射表引导到对应的handler中，所以在构建http_server对象的时候需要传出web应用对象app。http_server.listen(8000)将服务器绑定到8000端口。

# 实际上一版代码中app.listen(8000)正是对这一过程的简写    
    
```

### 180. 单进程与多进程

```
# 一次启动多个进程，修改上面的代码如下：
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver 

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app) 
    # -----------修改----------------
    http_server.bind(8000)
    http_server.start(0)
    # ------------------------------
    tornado.ioloop.IOLoop.current().start()
    
# http_server.bind(port)方法是将服务器绑定到指定端口。

# http_server.start(num_processes=1)方法指定开启几个进程，参数num_processes默认值为1，即默认仅开启一个进程；如果num_processes为None或者<=0，则自动根据机器硬件的cpu核芯数创建同等数目的子进程；如果num_processes>0，则创建num_processes个子进程。 

# 说明:
# 1.关于app.listen()
# app.listen()这个方法只能在单进程模式中使用。

# 对于app.listen()与手动创建HTTPServer实例

http_server = tornado.httpserver.HTTPServer(app) 
http_server.listen(8000)

# 这两种方式，建议使用后者即创建HTTPServer实例的方式，因为其对于理解tornado web应用工作流程的完整性有帮助，便于大家记忆tornado开发的模块组成和程序结构；在熟练使用后，可以改为简写。

# 2.关于多进程
# 虽然tornado提供了一次开启多个进程的方法，但是由于：
# 每个子进程都会从父进程中复制一份IOLoop实例，如过在创建子进程前我们的代码动了IOLoop实例，那么会影响到每一个子进程，势必会干扰到子进程IOLoop的工作；
# 所有进程是由一个命令一次开启的，也就无法做到在不停服务的情况下更新代码；
# 所有进程共享同一个端口，想要分别单独监控每一个进程就很困难。
# 不建议使用这种多进程的方式，而是手动开启多个进程，并且绑定不同的端口。
```

### 181. options

```
# tornado.options模块——全局参数定义、存储、转换。
tornado.options.define()
# 用来定义options选项变量的方法，定义的变量可以在全局的tornado.options.options中获取使用，传入参数：

#	name 选项变量名，须保证全局唯一性，否则会报“Option 'xxx' already defined in ...”的错误；
#	default　选项变量的默认值，如不传默认为None；
#	type 选项变量的类型，从命令行或配置文件导入参数的时候tornado会根据这个类型转换输入的值，转换不成功时会报错，可以是str、float、int、datetime、timedelta中的某个，若未设置则根据default的值自动推断，若default也未设置，那么不再进行转换。可以通过利用设置type类型字段来过滤不正确的输入。
#	multiple 选项变量的值是否可以为多个，布尔类型，默认值为False，如果multiple为True，那么设置选项变量时值与值之间用英文逗号分隔，而选项变量则是一个list列表（若默认值和输入均未设置，则为空列表[]）。
#	help 选项变量的帮助提示信息，在命令行启动tornado时，通过加入命令行参数 --help　可以查看所有选项变量的信息（注意，代码中需要加入tornado.options.parse_command_line()）。

tornado.options.options
# 全局的options对象，所有定义的选项变量都会作为该对象的属性。

tornado.options.parse_command_line()
# 转换命令行参数，并将转换后的值对应的设置到全局options对象相关属性上。追加命令行参数的方式是--myoption=myvalue

# opt.py
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options # 新导入的options模块

tornado.options.define("port", default=8000, type=int, help="run server on the given port.") # 定义服务器监听端口选项
tornado.options.define("itcast", default=[], type=str, multiple=True, help="itcast subjects.") # 无意义，演示多值情况

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    print tornado.options.options.itcast # 输出多值选项
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
    
# 开启程序： 
python opt.py --port=9000 --itcast=python,c++,java,php,ios

tornado.options.parse_config_file(path)
# 从配置文件导入option，配置文件中的选项格式如下：
myoption = "myvalue"
myotheroption = "myothervalue"

# 新建配置文件config，注意字符串和列表按照python的语法格式：
port = 8000
itcast = ["python","c++","java","php","ios"]

# 修改opt.py文件：
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options # 新导入的options模块

tornado.options.define("port", default=8000, type=int, help="run server on the given port.") # 定义服务器监听端口选项
tornado.options.define("itcast", default=[], type=str, multiple=True, help="itcast subjects.") # 无意义，演示多值情况

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    tornado.options.parse_config_file("./config") # 仅仅修改了此处
    print tornado.options.options.itcast # 输出多值选项
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
    
    
# 说明:
# 1. 日志
# 在代码中调用parse_command_line()或者parse_config_file()的方法时，tornado会默认为我们配置标准logging模块，即默认开启了日志功能，并向标准输出（屏幕）打印日志信息。
# 关闭tornado默认的日志功能，可以在命令行中添加--logging=none 或者在代码中执行如下操作:
from tornado.options import options, parse_command_line
options.logging = None
parse_command_line()

# 2. 配置文件
# 在使用prase_config_file()的时候，配置文件的书写格式仍需要按照python的语法要求，其优势是可以直接将配置文件的参数转换设置到全局对象tornado.options.options中；然而，其不方便的地方在于需要在代码中调用tornado.options.define()来定义选项，而且不支持字典类型，故而在实际应用中大都不使用这种方法。

# 在使用配置文件的时候，通常会新建一个python文件（如config.py），然后在里面直接定义python类型的变量（可以是字典类型）；在需要配置文件参数的地方，将config.py作为模块导入，并使用其中的变量参数。

# config.py文件：
# conding:utf-8

# Redis配置
redis_options = {
    'redis_host':'127.0.0.1',
    'redis_port':6379,
    'redis_pass':'',
}

# Tornado app配置
settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret':'0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies':False,
    'login_url':'/login',
    'debug':True,
}

# 日志
log_path = os.path.join(os.path.dirname(__file__), 'logs/log')

# 使用config.py的模块中导入config，如下：
# conding:utf-8

import tornado.web
import config

if __name__ = "__main__":
    app = tornado.web.Application([], **config.settings)
...
```

### 182. Application

```
# settings
# debug，设置tornado是否工作在调试模式，默认为False即工作在生产模式。当设置debug=True 后，tornado会工作在调试/开发模式，在此种模式下，tornado为方便我们开发而提供了几种特性：

#	自动重启，tornado应用会监控我们的源代码文件，当有改动保存后便会重启程序，这可以减少我们手动重启程序的次数。需要注意的是，一旦我们保存的更改有错误，自动重启会导致程序报错而退出，从而需要我们保存修正错误后手动启动程序。这一特性也可单独通过autoreload=True设置；
#	取消缓存编译的模板，可以单独通过compiled_template_cache=False来设置；
#	取消缓存静态文件hash值，可以单独通过static_hash_cache=False来设置；
#	提供追踪信息，当RequestHandler或者其子类抛出一个异常而未被捕获后，会生成一个包含追踪信息的页面，可以单独通过serve_traceback=True来设置。

# 使用debug参数的方法：

import tornado.web
app = tornado.web.Application([], debug=True)



# 路由映射
# 在构建路由映射列表的时候，使用的是二元元组，如：
[(r"/", IndexHandler),]
# 对于这个映射列表中的路由，实际上还可以传入多个信息，如：
[
    (r"/", Indexhandler),
    (r"/cpp", ItcastHandler, {"subject":"c++"}),
    url(r"/python", ItcastHandler, {"subject":"python"}, name="python_url")
]
# 对于路由中的字典，会传入到对应的RequestHandler的initialize()方法中：
from tornado.web import RequestHandler
class ItcastHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)
        
# 对于路由中的name字段，注意此时不能再使用元组，而应使用tornado.web.url来构建。name是给该路由起一个名字，可以通过调用RequestHandler.reverse_url(name)来获取该名子对应的url。
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def get(self):
        python_url = self.reverse_url("python_url")
        self.write('<a href="%s">itcast</a>' %
                   python_url)

class ItcastHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", Indexhandler),
            (r"/cpp", ItcastHandler, {"subject":"c++"}),
            url(r"/python", ItcastHandler, {"subject":"python"}, name="python_url")
        ],
        debug = True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

### 183. 输入

```
# HTTP协议向服务器传参有以下几种途径:
# 查询字符串（query string)，形如key1=value1&key2=value2；
# 请求体（body）中发送的数据，比如表单数据、json、xml；
# 提取uri的特定部分，如/blogs/2016/09/0001，可以在服务器端的路由中用正则表达式截取；
# 在http报文的头（header）中增加自定义字段，如X-XSRFToken=hello。

# 1. 获取查询字符串参数
get_query_argument(name, default=_ARG_DEFAULT, strip=True)
# 从请求的查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
# default为设值未传name参数时返回的默认值，如若default也未设置，则会抛出tornado.web.MissingArgumentError异常。
# strip表示是否过滤掉左右两边的空白字符，默认为过滤。
get_query_arguments(name, strip=True)
# 从请求的查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。
# strip同前，不再赘述。

# 2. 获取请求体参数
get_body_argument(name, default=_ARG_DEFAULT, strip=True)
# 从请求体中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
# default与strip同前，不再赘述。
get_body_arguments(name, strip=True)
# 从请求体中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。
# strip同前，不再赘述。
# 说明:
# 对于请求体中的数据要求为字符串，且格式为表单编码格式（与url中的请求字符串格式相同），即key1=value1&key2=value2，HTTP报文头Header中的"Content-Type"为application/x-www-form-urlencoded 或 multipart/form-data。对于请求体数据为json或xml的，无法通过这两个方法获取。

# 3. 前两类方法的整合
get_argument(name, default=_ARG_DEFAULT, strip=True)
# 从请求体和查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
# default与strip同前，不再赘述。
get_arguments(name, strip=True)
# 从请求体和查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。
# strip同前，不再赘述。
# 说明:
# 对于请求体中数据的要求同前。 这两个方法最常用。
# 代码示例:
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def post(self):
        query_arg = self.get_query_argument("a")
        query_args = self.get_query_arguments("a")
        body_arg = self.get_body_argument("a")
        body_args = self.get_body_arguments("a", strip=False)
        arg = self.get_argument("a")
        args = self.get_arguments("a")

        default_arg = self.get_argument("b", "itcast")
        default_args = self.get_arguments("b")

        try:
            missing_arg = self.get_argument("c")
        except MissingArgumentError as e:
            missing_arg = "We catched the MissingArgumentError!"
            print e
        missing_args = self.get_arguments("c")

        rep = "query_arg:%s<br/>" % query_arg
        rep += "query_args:%s<br/>" % query_args 
        rep += "body_arg:%s<br/>"  % body_arg
        rep += "body_args:%s<br/>" % body_args
        rep += "arg:%s<br/>"  % arg
        rep += "args:%s<br/>" % args 
        rep += "default_arg:%s<br/>" % default_arg 
        rep += "default_args:%s<br/>" % default_args 
        rep += "missing_arg:%s<br/>" % missing_arg
        rep += "missing_args:%s<br/>" % missing_args

        self.write(rep)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

    
# 4. 关于请求的其他信息 
# RequestHandler.request 对象存储了关于请求的相关信息，具体属性有：
#	method HTTP的请求方式，如GET或POST;
#	host 被请求的主机名；
#	uri 请求的完整资源标示，包括路径和查询字符串；
#	path 请求的路径部分；
#	query 请求的查询字符串部分；
#	version 使用的HTTP版本；
#	headers 请求的协议头，是类字典型的对象，支持关键字索引的方式获取特定协议头信息，例如：request.headers["Content-Type"]
#	body 请求体数据；
#	remote_ip 客户端的IP地址；
#	files 用户上传的文件，为字典类型，型如：
{
  "form_filename1":[<tornado.httputil.HTTPFile>, <tornado.httputil.HTTPFile>],
  "form_filename2":[<tornado.httputil.HTTPFile>,],
  ... 
}

# tornado.httputil.HTTPFile是接收到的文件对象，它有三个属性：
#	filename 文件的实际名字，与form_filename1不同，字典中的键名代表的是表单对应项的名字；
#	body 文件的数据实体；
#	content_type 文件的类型。 这三个对象属性可以像字典一样支持关键字索引，如request.files["form_filename1"][0]["body"]。

# 实现一个上传文件并保存在服务器本地的小程序upload.py：
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def get(self):
        self.write("hello itcast.")

class UploadHandler(RequestHandler): 
    def post(self):
        files = self.request.files
        img_files = files.get('img')
        if img_files:
            img_file = img_files[0]["body"]
            file = open("./itcast", 'w+')
            file.write(img_file)
            file.close()
        self.write("OK")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/upload", UploadHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
    
# 5. 正则提取uri
# tornado中对于路由映射也支持正则提取uri，提取出来的参数会作为RequestHandler中对应请求方式的成员方法参数。若在正则表达式中定义了名字，则参数按名传递；若未定义名字，则参数按顺序传递。提取出来的参数会作为对应请求方式的成员方法的参数。
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def get(self):
        self.write("hello itcast.")

class SubjectCityHandler(RequestHandler):
    def get(self, subject, city):
        self.write(("Subject: %s<br/>City: %s" % (subject, city)))

class SubjectDateHandler(RequestHandler):
    def get(self, date, subject):
        self.write(("Date: %s<br/>Subject: %s" % (date, subject)))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/sub-city/(.+)/([a-z]+)", SubjectCityHandler), # 无名方式
        (r"/sub-date/(?P<subject>.+)/(?P<date>\d+)", SubjectDateHandler), #　命名方式
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
# 建议：提取多个值时最好用命名方式。    
```

### 184. 输出

```
# 1. write(chunk) 将chunk数据写到输出缓冲区。
class IndexHandler(RequestHandler):
    def get(self):
        self.write("hello world!")
# 利用write方法写json数据:
import json

class IndexHandler(RequestHandler):
    def get(self):
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
        
# 不用自己手动去做json序列化，当write方法检测到我们传入的chunk参数是字典类型后，会自动帮我们转换为json字符串。
class IndexHandler(RequestHandler):
    def get(self):
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        self.write(stu)
        
# 两种方式差异？
# 对比两种方式的响应头header中Content-Type字段，自己手动序列化时为Content-Type:text/html; charset=UTF-8，而采用write方法时为Content-Type:application/json; charset=UTF-8。

# write方法除了将字典转换为json字符串之外，还帮我们将Content-Type设置为application/json; charset=UTF-8。


# 2. set_header(name, value)
# 利用set_header(name, value)方法，可以手动设置一个名为name、值为value的响应头header字段。
# 用set_header方法来完成上面write所做的工作。
import json

class IndexHandler(RequestHandler):
    def get(self):
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        

# 3. set_default_headers()
# 该方法会在进入HTTP处理方法前先被调用，可以重写此方法来预先设置默认的headers。注意：在HTTP处理方法中使用set_header()方法会覆盖掉在set_default_headers()方法中设置的同名header。
class IndexHandler(RequestHandler):
    def set_default_headers(self):
        print "执行了set_default_headers()"
        # 设置get与post方式的默认响应体格式为json
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        # 设置一个名为itcast、值为python的header
        self.set_header("itcast", "python")

    def get(self):
        print "执行了get()"
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
        self.set_header("itcast", "i love python") # 注意此处重写了header中的itcast字段

    def post(self):
        print "执行了post()"
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
  


# 4. set_status(status_code, reason=None)   为响应设置状态码。
# 参数说明：
#	status_code int类型，状态码，若reason为None，则状态码必须为下表中的。
#	reason string类型，描述状态码的词组，若为None，则会被自动填充为下表中的内容。
class Err404Handler(RequestHandler):
    """对应/err/404"""
    def get(self):
        self.write("hello itcast")
        self.set_status(404) # 标准状态码，不用设置reason

class Err210Handler(RequestHandler):
    """对应/err/210"""
    def get(self):
        self.write("hello itcast")
        self.set_status(210, "itcast error") # 非标准状态码，设置了reason

class Err211Handler(RequestHandler):
    """对应/err/211"""
    def get(self):
        self.write("hello itcast")
        self.set_status(211) # 非标准状态码，未设置reason，错误
        
        
# 5. redirect(url)  告知浏览器跳转到url。
class IndexHandler(RequestHandler):
    """对应/"""
    def get(self):
        self.write("主页")

class LoginHandler(RequestHandler):
    """对应/login"""
    def get(self):
        self.write('<form method="post"><input type="submit" value="登陆"></form>')

    def post(self):
        self.redirect("/")
  

# 6. send_error(status_code=500, **kwargs)
# 抛出HTTP错误状态码status_code，默认为500，kwargs为可变命名参数。使用send_error抛出错误后tornado会调用write_error()方法进行处理，并返回给浏览器处理后的错误页面。
class IndexHandler(RequestHandler):
    def get(self):
        self.write("主页")
        self.send_error(404, content="出现404错误")
# 注意：默认的write\_error()方法不会处理send\_error抛出的kwargs参数，即上面的代码中content="出现404错误"是没有意义的。
# 示例代码:
class IndexHandler(RequestHandler):
    def get(self):
        self.write("主页")
        self.send_error(404, content="出现404错误")
        self.write("结束") # 我们在send_error再次向输出缓冲区写内容
# 注意：使用send_error()方法后就不要再向输出缓冲区写内容了！


# 7. write_error(status_code, **kwargs)
# 用来处理send_error抛出的错误信息并返回给浏览器错误信息页面。可以重写此方法来定制自己的错误显示页面。
class IndexHandler(RequestHandler):
    def get(self):
        err_code = self.get_argument("code", None) # 注意返回的是unicode字符串，下同
        err_title = self.get_argument("title", "")
        err_content = self.get_argument("content", "")
        if err_code:
            self.send_error(err_code, title=err_title, content=err_content)
        else:
            self.write("主页")

    def write_error(self, status_code, **kwargs):
        self.write(u"<h1>出错了，程序员GG正在赶过来！</h1>")
        self.write(u"<p>错误名：%s</p>" % kwargs["title"])
        self.write(u"<p>错误详情：%s</p>" % kwargs["content"])
        
        
```

### 185. 接口与调用顺序

```
# 1. initialize()
# 对应每个请求的处理类Handler在构造一个实例后首先执行initialize()方法。在讲输入时提到，路由映射中的第三个字典型参数会作为该方法的命名参数传递，如：
class ProfileHandler(RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self):
        ...

app = Application([
    (r'/user/(.*)', ProfileHandler, dict(database=database)),
    ])
# 此方法通常用来初始化参数（对象属性），很少使用。


# 2. prepare()
# 预处理，即在执行对应请求方式的HTTP方法（如get、post等）前先执行，注意：不论以何种HTTP方式请求，都会执行prepare()方法。
# 以预处理请求体中的json数据为例：
import json

class IndexHandler(RequestHandler):
    def prepare(self):
        if self.request.headers.get("Content-Type").startswith("application/json"):
            self.json_dict = json.loads(self.request.body)
        else:
            self.json_dict = None

    def post(self):
        if self.json_dict:
            for key, value in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (key, value))

    def put(self):
        if self.json_dict:
            for key, value in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (key, value))

                
# 3. HTTP方法
# get:请求指定的页面信息，并返回实体主体。
# head:类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头
# post:向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。
# delete:请求服务器删除指定的内容。
# patch:请求修改局部数据。
# put:从客户端向服务器传送的数据取代指定的文档的内容。
# options:返回给定URL支持的所有HTTP方法。

# 4. on_finish()
# 在请求处理结束后调用，即在调用HTTP方法后调用。通常该方法用来进行资源清理释放或处理日志等。注意：请尽量不要在此方法中进行响应输出。

# 5. set_default_headers()
# 6. write_error()
# 7. 调用顺序
class IndexHandler(RequestHandler):

    def initialize(self):
        print "调用了initialize()"

    def prepare(self):
        print "调用了prepare()"

    def set_default_headers(self):
        print "调用了set_default_headers()"

    def write_error(self, status_code, **kwargs):
        print "调用了write_error()"

    def get(self):
        print "调用了get()"

    def post(self):
        print "调用了post()"
        self.send_error(200)  # 注意此出抛出了错误

    def on_finish(self):
        print "调用了on_finish()"
        
        
# 在正常情况未抛出错误时，调用顺序为：
# 1. set_defautl_headers()
# 2. initialize()
# 3. prepare()
# 4. HTTP方法
# 5. on_finish()

# 在有错误抛出时，调用顺序为：
# 1.  set_default_headers()
# 2.  initialize()
# 3.  prepare()
# 4.  HTTP方法
# 5.  set_default_headers()
# 6.  write_error()
# 7.  on_finish()
```

### 186. 静态文件

```
#  static_path
# 可以通过向web.Application类的构造函数传递一个名为static_path的参数来告诉Tornado从文件系统的一个特定位置提供静态文件，如：
app = tornado.web.Application(
    [(r'/', IndexHandler)],
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
)
# 在这里，设置了一个当前应用目录下名为statics的子目录作为static_path的参数。现在应用将以读取statics目录下的filename.ext来响应诸如/static/filename.ext的请求，并在响应的主体中返回。

# 对于静态文件目录的命名，为了便于部署，建议使用static
# 对于静态文件资源，可以通过http://127.0.0.1/static/html/index.html来访问。而且在index.html中引用的静态资源文件，我们给定的路径也符合/static/...的格式，故页面可以正常浏览。
<link href="/static/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet">
<link href="/static/plugins/font-awesome/css/font-awesome.min.css" rel="stylesheet">
<link href="/static/css/reset.css" rel="stylesheet">
<link href="/static/css/main.css" rel="stylesheet">
<link href="/static/css/index.css" rel="stylesheet">

<script src="/static/js/jquery.min.js"></script>
<script src="/static/plugins/bootstrap/js/bootstrap.min.js"></script>
<script src="/static/js/index.js"></script>


# StaticFileHandler
# tornado.web.StaticFileHandler来自由映射静态文件与其访问路径url。
# tornado.web.StaticFileHandler是tornado预置的用来提供静态资源文件的handler。
import os

current_path = os.path.dirname(__file__)
app = tornado.web.Application(
    [
        (r'^/()$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html"), "default_filename":"index.html"}),
        (r'^/view/(.*)$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html")}),
    ],
    static_path=os.path.join(current_path, "statics"),
)

# path 用来指明提供静态文件的根路径，并在此目录中寻找在路由中用正则表达式提取的文件名。
# default_filename 用来指定访问路由中未指明文件名时，默认提供的文件。


# 现在，对于静态文件statics/html/index.html，可以通过三种方式进行访问：

# 1. http://127.0.0.1/static/html/index.html
# 2. http://127.0.0.1/
# 3. http://127.0.0.1/view/index.html
```

### 187. 使用模板

```
# 1. 路径与渲染
# 使用模板，需要仿照静态文件路径设置一样，向web.Application类的构造函数传递一个名为template_path的参数来告诉Tornado从文件系统的一个特定位置提供模板文件，如：
app = tornado.web.Application(
    [(r'/', IndexHandler)],
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)
# 在这里，设置了一个当前应用目录下名为templates的子目录作为template_path的参数。在handler中使用的模板将在此目录中寻找。
# 现在将静态文件目录statics/html中的index.html复制一份到templates目录中，此时文件目录结构为：
.
├── statics
│   ├── css
│   │   ├── index.css
│   │   ├── main.css
│   │   └── reset.css
│   ├── html
│   │   └── index.html
│   ├── images
│   │   ├── home01.jpg
│   │   ├── home02.jpg
│   │   ├── home03.jpg
│   │   └── landlord01.jpg
│   ├── js
│   │   ├── index.js
│   │   └── jquery.min.js
│   └── plugins
│       ├── bootstrap
│       │   └─...
│       └── font-awesome
│           └─...
├── templates
│   └── index.html
└── test.py

# 在handler中使用render()方法来渲染模板并返回给客户端。
class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html") # 渲染主页模板，并返回给客户端。



current_path = os.path.dirname(__file__)
app = tornado.web.Application(
    [
        (r'^/$', IndexHandler),
        (r'^/view/(.*)$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html")}),
    ],
    static_path=os.path.join(current_path, "statics"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)


# 2. 模板语法
# 2-1 变量与表达式
# 在tornado的模板中使用{{}}作为变量或表达式的占位符，使用render渲染后占位符{{}}会被替换为相应的结果值。
# 将index.html中的一条房源信息记录:
<li class="house-item">
    <a href=""><img src="/static/images/home01.jpg"></a>
    <div class="house-desc">
        <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
        <div class="house-price">￥<span>398</span>/晚</div>
        <div class="house-intro">
            <span class="house-title">宽窄巷子+160平大空间+文化保护区双地铁</span>
            <em>整套出租 - 5分/6点评 - 北京市丰台区六里桥地铁</em>
        </div>
    </div>
</li>

# 改为模板：
<li class="house-item">
    <a href=""><img src="/static/images/home01.jpg"></a>
    <div class="house-desc">
        <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
        <div class="house-price">￥<span>{{price}}</span>/晚</div>
        <div class="house-intro">
            <span class="house-title">{{title}}</span>
            <em>整套出租 - {{score}}分/{{comments}}点评 - {{position}}</em>
        </div>
    </div>
</li>
# 渲染方式如下：
class IndexHandler(RequestHandler):
    def get(self):
        house_info = {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }
        self.render("index.html", **house_info)
        
# {{}}不仅可以包含变量，还可以是表达式，如：
<li class="house-item">
    <a href=""><img src="/static/images/home01.jpg"></a>
    <div class="house-desc">
        <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
        <div class="house-price">￥<span>{{p1 + p2}}</span>/晚</div>
        <div class="house-intro">
            <span class="house-title">{{"+".join(titles)}}</span>
            <em>整套出租 - {{score}}分/{{comments}}点评 - {{position}}</em>
        </div>
    </div>
</li>

class IndexHandler(RequestHandler):
    def get(self):
        house_info = {
            "p1": 198,
            "p2": 200,
            "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }
        self.render("index.html", **house_info)
        
        
# 2-2 控制语句
# 可以在Tornado模板中使用Python条件和循环语句。控制语句以{\%和\%}包围，并以类似下面的形式被使用：
{% if page is None %}
# 或
{% if len(entries) == 3 %}
# 控制语句的大部分就像对应的Python语句一样工作，支持if、for、while，注意end:
{% if ... %} ... {% elif ... %} ... {% else ... %} ... {% end %}
{% for ... in ... %} ... {% end %}
{% while ... %} ... {% end %}

# 修改index.html:
<ul class="house-list">
    {% if len(houses) > 0 %}
        {% for house in houses %}
        <li class="house-item">
            <a href=""><img src="/static/images/home01.jpg"></a>
            <div class="house-desc">
                <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
                <div class="house-price">￥<span>{{house["price"]}}</span>/晚</div>
                <div class="house-intro">
                    <span class="house-title">{{house["title"]}}</span>
                    <em>整套出租 - {{house["score"]}}分/{{house["comments"]}}点评 - {{house["position"]}}</em>
                </div>
            </div>
        </li>
        {% end %}
    {% else %}
        对不起，暂时没有房源。
    {% end %}
</ul>
# python中渲染语句为：
class IndexHandler(RequestHandler):
    def get(self):
        houses = [
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }]
        self.render("index.html", houses=houses)
        

# 2-3 函数
# static_url()  生成静态文件目录下文件的URL
<link rel="stylesheet" href="{{ static_url("style.css") }}">
# 优点：
#	static_url函数创建了一个基于文件内容的hash值，并将其添加到URL末尾（查询字符串的参数v）。这个hash值确保浏览器总是加载一个文件的最新版而不是之前的缓存版本。无论是在你应用的开发阶段，还是在部署到生产环境使用时，都非常有用，因为你的用户不必再为了看到你的静态内容而清除浏览器缓存了。
#	另一个好处是你可以改变你应用URL的结构，而不需要改变模板中的代码。例如，可以通过设置static_url_prefix来更改Tornado的默认静态路径前缀/static。如果使用static_url而不是硬编码的话，代码不需要改变。

# 转义
# 新建一个表单页面new.html:
<!DOCTYPE html>
<html>
    <head>
        <title>新建房源</title>
    </head>
    <body>
        <form method="post">
            <textarea name="text"></textarea>
            <input type="submit" value="提交">
        </form>
        {{text}}
    </body>
</html>
# 对应的handler为：
class NewHandler(RequestHandler):

    def get(self):
        self.render("new.html", text="")

    def post(self):
        text = self.get_argument("text", "") 
        print text
        self.render("new.html", text=text)
# 当我们在表单中填入如下内容时,写入的js程序并没有运行，而是显示出来了：：
<script>alert("hello!");</script>
# 查看页面源代码，发现<、>、"等被转换为对应的html字符。
&lt;script&gt;alert(&quot;hello!&quot;);&lt;/script&gt;
# 是因为tornado中默认开启了模板自动转义功能，防止网站受到恶意攻击。
# 可以通过raw语句来输出不被转义的原始格式，如：
{% raw text %}
# 注意：在Firefox浏览器中会直接弹出alert窗口，而在Chrome浏览器中，需要set_header("X-XSS-Protection", 0)
# 若要关闭自动转义，一种方法是在Application构造函数中传递autoescape=None，另一种方法是在每页模板中修改自动转义行为，添加如下语句：
{% autoescape None %}

# escape()
# 关闭自动转义后，可以使用escape()函数来对特定变量进行转义，如：
{{ escape(text) }}

# 自定义函数
# 在模板中还可以使用一个自己编写的函数，只需要将函数名作为模板的参数传递即可，就像其他变量一样。
# 修改后端如下：
def house_title_join(titles):
    return "+".join(titles)

class IndexHandler(RequestHandler):
    def get(self):
        house_list = [
        {
            "price": 398,
            "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }]
        self.render("index.html", houses=house_list, title_join = house_title_join)
        
        
# 前端模板我们修改为：  
<ul class="house-list">
    {% if len(houses) > 0 %}
        {% for house in houses %}
        <li class="house-item">
            <a href=""><img src="/static/images/home01.jpg"></a>
            <div class="house-desc">
                <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
                <div class="house-price">￥<span>{{house["price"]}}</span>/晚</div>
                <div class="house-intro">
                    <span class="house-title">{{title_join(house["titles"])}}</span>
                    <em>整套出租 - {{house["score"]}}分/{{house["comments"]}}点评 - {{house["position"]}}</em>
                </div>
            </div>
        </li>
        {% end %}
    {% else %}
        对不起，暂时没有房源。
    {% end %}
</ul>


# 2-4 块 可以使用块来复用模板，块语法如下：
{% block block_name %} {% end %}
# 对模板index.html进行抽象，抽离出父模板base.html如下：
<!DOCTYPE html>
<html>
<head> 
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    {% block page_title %}{% end %}
    <link href="{{static_url('plugins/bootstrap/css/bootstrap.min.css')}}" rel="stylesheet">
    <link href="{{static_url('plugins/font-awesome/css/font-awesome.min.css')}}" rel="stylesheet">
    <link href="{{static_url('css/reset.css')}}" rel="stylesheet">
    <link href="{{static_url('css/main.css')}}" rel="stylesheet">
    {% block css_files %}{% end %}
</head>
<body>
    <div class="container">
        <div class="top-bar">
            {% block header %}{% end %}
        </div>
        {% block body %}{% end %}
        <div class="footer">
            {% block footer %}{% end %}
        </div>
    </div>

    <script src="{{static_url('js/jquery.min.js')}}"></script>
    <script src="{{static_url('plugins/bootstrap/js/bootstrap.min.js')}}"></script>
    {% block js_files %}{% end %}
</body>
</html>

# 而子模板index.html使用extends来使用父模板base.html，如下：
{% extends "base.html" %}

{% block page_title %}
    <title>爱家-房源</title>
{% end %}

{% block css_files %}
    <link href="{{static_url('css/index.css')}}" rel="stylesheet">
{% end %} 

{% block js_files %}
    <script src="{{static_url('js/index.js')}}"></script>
{% end %}

{% block header %}
    <div class="nav-bar">
        <h3 class="page-title">房 源</h3>
    </div>
{% end %}

{% block body %}
    <ul class="house-list">
    {% if len(houses) > 0 %}
        {% for house in houses %}
        <li class="house-item">
            <a href=""><img src="/static/images/home01.jpg"></a>
            <div class="house-desc">
                <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
                <div class="house-price">￥<span>{{house["price"]}}</span>/晚</div>
                <div class="house-intro">
                    <span class="house-title">{{title_join(house["titles"])}}</span>
                    <em>整套出租 - {{house["score"]}}分/{{house["comments"]}}点评 - {{house["position"]}}</em>
                </div>
            </div>
        </li>
        {% end %}
    {% else %}
        对不起，暂时没有房源。
    {% end %}
    </ul>
{% end %}

{% block footer %}
    <p><span><i class="fa fa-copyright"></i></span>爱家租房&nbsp;&nbsp;享受家的温馨</p>
{% end %}
```

### 188. 数据库

```
# 在Tornado3.0版本以前提供tornado.database模块用来操作MySQL数据库，而从3.0版本开始，此模块就被独立出来，作为torndb包单独提供。torndb只是对MySQLdb的简单封装，不支持Python 3。
# torndb安装:
pip install torndb

# 连接初始化:
# 需要在应用启动时创建一个数据库连接实例，供各个RequestHandler使用。我们可以在构造Application的时候创建一个数据库实例并作为其属性，而RequestHandler可以通过self.application获取其属性，进而操作数据库实例。
import torndb

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "statics"),
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # 创建一个全局mysql连接实例供handler使用
        self.db = torndb.Connection(
            host="127.0.0.1",
            database="pachong",
            user="root",
            password="mysql"
        )

# 使用数据库:
# 1. 执行语句
# execute(query, parameters, *kwparameters) 返回影响的最后一条自增字段值
# execute_rowcount(query, parameters, *kwparameters) 返回影响的行数
# query为要执行的sql语句，parameters与kwparameters为要绑定的参数，如：
db.execute("insert into houses(title, position, price, score, comments) values(%s, %s, %s, %s, %s)", "独立装修小别墅", "紧邻文津街", 280, 5, 128)
或
db.execute("insert into houses(title, position, price, score, comments) values(%(title)s, %(position)s, %(price)s, %(score)s, %(comments)s)", title="独立装修小别墅", position="紧邻文津街", price=280, score=5, comments=128)
# 执行语句主要用来执行非查询语句。
class InsertHandler(RequestHandler):
    def post(self):
        title = self.get_argument("title")
        position = self.get_argument("position")
        price = self.get_argument("price")
        score = self.get_argument("score")
        comments = self.get_argument("comments")
        try:
            ret = self.application.db.execute("insert into houses(title, position, price, score, comments) values(%s, %s, %s, %s, %s)", title, position, price, score, comments)
        except Exception as e:
            self.write("DB error:%s" % e)
        else:
            self.write("OK %d" % ret)

# 2. 查询语句
# get(query, parameters, *kwparameters) 返回单行结果或None，若出现多行则报错。返回值为torndb.Row类型，是一个类字典的对象，即同时支持字典的关键字索引和对象的属相访问。
# query(query, parameters, *kwparameters) 返回多行结果，torndb.Row的列表。

# 修改一下index.html模板，将
<span class="house-title">{{title_join(house["titles"])}}</span>
# 改为
<span class="house-title">{{house["title"]}}</span>
# 添加两个新的handler：
class GetHandler(RequestHandler):
    def get(self):
        """访问方式为http://127.0.0.1/get?id=111"""
        hid = self.get_argument("id")
        try:
            ret = self.application.db.get("select title,position,price,score,comments from houses where id=%s", hid)
        except Exception as e:
            self.write("DB error:%s" % e)
        else:
            print type(ret)
            print ret
            print ret.title
            print ret['title']
            self.render("index.html", houses=[ret])


class QueryHandler(RequestHandler):
    def get(self):
        """访问方式为http://127.0.0.1/query"""
        try:
            ret = self.application.db.query("select title,position,price,score,comments from houses limit 10")
        except Exception as e:
            self.write("DB error:%s" % e)
        else:
            self.render("index.html", houses=ret)
```

### 189. 安全应用

```
# 设置
set_cookie(name, value, domain=None, expires=None, path='/', expires_days=None)
# 参数说明：
# name:cookie名
# value:cookie值
# domain:提交cookie时匹配的域名
# path:提交cookie时匹配的路径
# expires:cookie的有效期，可以是时间戳整数、时间元组或者datetime类型，为UTC时间
# expires_days:cookie的有效期，天数，优先级低于expires

# 示例:
import datetime

class IndexHandler(RequestHandler):
    def get(self):
        self.set_cookie("n1", "v1")
        self.set_cookie("n2", "v2", path="/new", expires=time.strptime("2016-11-11 23:59:59","%Y-%m-%d %H:%M:%S"))
        self.set_cookie("n3", "v3", expires_days=20)
        # 利用time.mktime将本地时间转换为UTC标准时间
        self.set_cookie("n4", "v4", expires=time.mktime(time.strptime("2016-11-11 23:59:59","%Y-%m-%d %H:%M:%S")))
        self.write("OK")

# 原理
# 设置cookie实际就是通过设置header的Set-Cookie来实现的。  
# 获取
get_cookie(name, default=None)
# 获取名为name的cookie，可以设置默认值。
class IndexHandler(RequestHandler):
    def get(self):
        n3 = self.get_cookie("n3")
        self.write(n3)
# 清除
clear_cookie(name, path='/', domain=None)

# 删除名为name，并同时匹配domain和path的cookie。

clear_all_cookies(path='/', domain=None)

# 删除同时匹配domain和path的所有cookie。
# 示例:
class ClearOneCookieHandler(RequestHandler):
    def get(self):
        self.clear_cookie("n3")
        self.write("OK")

class ClearAllCookieHandler(RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.write("OK")
#   注意：执行清除cookie操作后，并不是立即删除了浏览器中的cookie，而是给cookie值置空，并改变其有效期使其失效。真正的删除cookie是由浏览器去清理的。  


# 安全Cookie
# Cookie是存储在客户端浏览器中的，很容易被篡改。Tornado提供了一种对Cookie进行简易加密签名的方法来防止Cookie被恶意篡改。

# 使用安全Cookie需要为应用配置一个用来给Cookie进行混淆的秘钥cookie_secret，将其传递给Application的构造函数。我们可以使用如下方法来生成一个随机字符串作为cookie_secret的值。
>>> import base64, uuid
>>> base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
'2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A='

# Base64是一种基于64个可打印字符来表示二进制数据的表示方法。由于2的6次方等于64，所以每6个比特为一个单元，对应某个可打印字符。三个字节有24个比特，对应于4个Base64单元，即3个字节需要用4个可打印字符来表示。

# uuid, 通用唯一识别码（英语：Universally Unique Identifier，简称UUID），是由一组32个16进制数字所构成（两个16进制数是一个字节，总共16字节），因此UUID理论上的总数为16^32=2^128，约等于3.4 x 10^38。也就是说若每纳秒产生1兆个UUID，要花100亿年才会将所有UUID用完。

# uuid模块的uuid4()函数可以随机产生一个uuid码，bytes属性将此uuid码作为16字节字符串。

# 将生成的cookie_secret传入Application构造函数：
app = tornado.web.Application(
    [(r"/", IndexHandler),],
    cookie_secret = "2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A="
)

# 获取和设置
set_secure_cookie(name, value, expires_days=30)
# 设置一个带签名和时间戳的cookie，防止cookie被伪造。
get_secure_cookie(name, value=None, max_age_days=31)
# 如果cookie存在且验证通过，返回cookie的值，否则返回None。max_age_day不同于expires_days，expires_days是设置浏览器中cookie的有效期，而max_age_day是过滤安全cookie的时间戳。

class IndexHandler(RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1
        self.set_secure_cookie("count", str(count))
        self.write(
            '<html><head><title>Cookie计数器</title></head>'
            '<body><h1>您已访问本页%d次。</h1>' % count + 
            '</body></html>'
        )
# 签名后的cookie值：
"2|1:0|10:1476412069|5:count|4:NQ==|cb5fc1d4434971de6abf87270ac33381c686e4ec8c6f7e62130a0f8cbe5b7609"


# 字段说明：
# 安全cookie的版本，默认使用版本2，不带长度说明前缀
# 默认为0
# 时间戳
# cookie名
# base64编码的cookie值
# 签名值，不带长度说明前缀

# 注意：Tornado的安全cookie只是一定程度的安全，仅仅是增加了恶意修改的难度。Tornado的安全cookies仍然容易被窃听，而cookie值是签名不是加密，攻击者能够读取已存储的cookie值，并且可以传输他们的数据到任意服务器，或者通过发送没有修改的数据给应用伪造请求。因此，避免在浏览器cookie中存储敏感的用户数据是非常重要的。
```

### 190. XSRF 跨站请求伪造

```
# 先建立一个网站127.0.0.1:8000，使用上一节中的Cookie计数器：
class IndexHandler(RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1
        self.set_secure_cookie("count", str(count))
        self.write(
            '<html><head><title>Cookie计数器</title></head>'
            '<body><h1>您已访问本页%d次。</h1>' % count +
            '</body></html>'
        )
# 再建立一个网站127.0.0.1:9000，
class IndexHandler(RequestHandler):
    def get(self):
        self.write('<html><head><title>被攻击的网站</title></head>'
        '<body><h1>此网站的图片链接被修改了</h1>'
        '<img alt="这应该是图片" src="http://127.0.0.1:8000/?f=9000/">'
        '</body></html>'
        )
# 在9000网站模拟攻击者修改了图片源地址为8000网站的Cookie计数器页面网址。当我们访问9000网站的时候，在我们不知道、未授权的情况下8000网站的Cookie被使用了，以至于让8000网址认为是我们自己调用了8000网站的逻辑。这就是CSRF（Cross-site request forgery）跨站请求伪造（跨站攻击或跨域攻击的一种），通常缩写为CSRF或者XSRF。

# 刚刚使用的是GET方式模拟的攻击，为了防范这种方式的攻击，任何会产生副作用的HTTP请求，比如点击购买按钮、编辑账户设置、改变密码或删除文档，都应该使用HTTP POST方法（或PUT、DELETE）。但是，这并不足够：一个恶意站点可能会通过其他手段来模拟发送POST请求，保护POST请求需要额外的策略。


# XSRF保护
# 浏览器有一个很重要的概念——同源策略(Same-Origin Policy)。 所谓同源是指，域名，协议，端口相同。 不同源的客户端脚本(javascript、ActionScript)在没明确授权的情况下，不能读写对方的资源。
# 由于第三方站点没有访问cookie数据的权限（同源策略），所以我们可以要求每个请求包括一个特定的参数值作为令牌来匹配存储在cookie中的对应值，如果两者匹配，我们的应用认定请求有效。而第三方站点无法在请求中包含令牌cookie值，这就有效地防止了不可信网站发送未授权的请求。

# 开启XSRF保护
# 要开启XSRF保护，需要在Application的构造函数中添加xsrf_cookies参数：
app = tornado.web.Application(
    [(r"/", IndexHandler),],
    cookie_secret = "2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
    xsrf_cookies = True
)
# 当这个参数被设置时，Tornado将拒绝请求参数中不包含正确的_xsrf值的POST、PUT和DELETE请求。
class IndexHandler(RequestHandler):
    def post(self):
        self.write("hello itcast")
# 用不带_xsrf的post请求时，报出了HTTP 403: Forbidden ('_xsrf' argument missing from POST)的错误。


# 模板应用
# 在模板中使用XSRF保护，只需在模板中添加
{% module xsrf_form_html() %}
# 新建一个模板index.html
<!DOCTYPE html>
<html>
<head>
    <title>测试XSRF</title>
</head>
<body>
    <form method="post">
      {% module xsrf_form_html() %}
      <input type="text" name="message"/>
      <input type="submit" value="Post"/>
    </form>
</body>
</html>
# 后端
class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        self.write("hello itcast")
# 作用:
# 为浏览器设置了_xsrf的Cookie（注意此Cookie浏览器关闭时就会失效）
# 为模板的表单中添加了一个隐藏的输入名为_xsrf，其值为_xsrf的Cookie值 
# 渲染后的页面原码如下：
<!DOCTYPE html>
<html>
    <head>
        <title>测试XSRF</title>
    </head>
    <body>
        <form method="post">
            <input type="hidden" name="_xsrf" value="2|543c2206|a056ff9e49df23eaffde0a694cde2b02|1476443353"/>
            <input type="text" name="message"/>
            <input type="submit" value="Post"/>
        </form>
    </body>
</html>



# 非模板应用
# 对于不使用模板的应用来说，首先要设置_xsrf的Cookie值，可以在任意的Handler中通过获取self.xsrf_token的值来生成_xsrf并设置Cookie。
# 下面两种方式都可以起到设置_xsrf Cookie的作用。
class XSRFTokenHandler(RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""
    def get(self):
        self.xsrf_token
        self.write("Ok")

class StaticFileHandler(tornado.web.StaticFileHandler):
    """重写StaticFileHandler，构造时触发设置_xsrf Cookie"""
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
# 对于请求携带_xsrf参数，有两种方式：
# 若请求体是表单编码格式的，可以在请求体中添加_xsrf参数
# 若请求体是其他格式的（如json或xml等），可以通过设置HTTP头X-XSRFToken来传递_xsrf值
# 1. 请求体携带_xsrf参数
# 新建一个页面xsrf.html：
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>测试XSRF</title>
</head>
<body>
    <a href="javascript:;" onclick="xsrfPost()">发送POST请求</a>
    <script src="http://cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
    <script type="text/javascript">
        //获取指定Cookie的函数
        function getCookie(name) {
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
        }
        //AJAX发送post请求，表单格式数据
        function xsrfPost() {
            var xsrf = getCookie("_xsrf");
            $.post("/new", "_xsrf="+xsrf+"&key1=value1", function(data) {
                alert("OK");
            });
        }
    </script>
</body>
</html>

# 2. HTTP头X-XSRFToken
# 新建一个页面json.html：
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>测试XSRF</title>
</head>
<body>
    <a href="javascript:;" onclick="xsrfPost()">发送POST请求</a>
    <script src="http://cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
    <script type="text/javascript">
        //获取指定Cookie的函数
        function getCookie(name) {
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
        }
        //AJAX发送post请求，json格式数据
        function xsrfPost() {
            var xsrf = getCookie("_xsrf");
            var data = {
                key1:1,
                key1:2
            };
            var json_data = JSON.stringify(data);
            $.ajax({
                url: "/new",
                method: "POST",
                headers: {
                    "X-XSRFToken":xsrf,
                },
                data:json_data,
                success:function(data) {
                    alert("OK");
                }
            })
        }
    </script>
</body>
</html>
```

### 191. 用户验证

```
# 用户验证是指在收到用户请求后进行处理前先判断用户的认证状态（如登陆状态），若通过验证则正常处理，否则强制用户跳转至认证页面（如登陆页面）。

# authenticated装饰器
# 为了使用Tornado的认证功能，我们需要对登录用户标记具体的处理函数。我们可以使用@tornado.web.authenticated装饰器完成它。当我们使用这个装饰器包裹一个处理方法时，Tornado将确保这个方法的主体只有在合法的用户被发现时才会调用。
class ProfileHandler(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("这是我的个人主页。")
# get_current_user()方法
# 装饰器@tornado.web.authenticated的判断执行依赖于请求处理类中的self.current_user属性，如果current_user值为假（None、False、0、""等），任何GET或HEAD请求都将把访客重定向到应用设置中login_url指定的URL，而非法用户的POST请求将返回一个带有403（Forbidden）状态的HTTP响应。
# 在获取self.current_user属性的时候，tornado会调用get_current_user()方法来返回current_user的值。也就是说，我们验证用户的逻辑应写在get_current_user()方法中，若该方法返回非假值则验证通过，否则验证失败。
class ProfileHandler(RequestHandler):
    def get_current_user(self):
        """在此完成用户的认证逻辑"""
        user_name = self.get_argument("name", None)
        return user_name 

    @tornado.web.authenticated
    def get(self):
        self.write("这是我的个人主页。")
        
# login_url设置
# 当用户验证失败时，将用户重定向到login_url上，所以我们还需要在Application中配置login_url。
class LoginHandler(RequestHandler):
    def get(self):
        """在此返回登陆页面"""
        self.write("登陆页面")

app = tornado.web.Application(
    [
        (r"/", IndexHandler),
        (r"/profile", ProfileHandler),
        (r"/login", LoginHandler),
    ],
    "login_url":"/login"
)

# 在login_url后面补充的next参数就是记录的跳转至登录页面前的所在位置，所以我们可以使用next参数来完成登陆后的跳转。
# 修改登陆逻辑：
class LoginHandler(RequestHandler):
    def get(self):
        """登陆处理，完成登陆后跳转回前一页面"""
        next = self.get_argument("next", "/")
        self.redirect(next+"?name=logined")
        
```

### 192. 认识异步

```
# 1. 同步
# 模拟两个客户端请求，并依次进行处理：
# coding:utf-8

def req_a():
    """模拟请求a"""
    print '开始处理请求req_a'
    print '完成处理请求req_a'

def req_b():
    """模拟请求b"""
    print '开始处理请求req_b'
    print '完成处理请求req_b'

def main():
    """模拟tornado框架，处理两个请求"""
    req_a()
    req_b()

if __name__ == "__main__":
    main()
    
    
#执行结果：

# 开始处理请求req_a
# 完成处理请求req_a
# 开始处理请求req_b
# 完成处理请求req_b

# 同步是按部就班的依次执行，始终按照同一个步调执行，上一个步骤未执行完不会执行下一步。
# 如果在处理请求req_a时需要执行一个耗时的工作（如IO），其执行过程:
import time

def long_io():
    """模拟耗时IO操作"""
    print "开始执行IO操作"
    time.sleep(5)
    print "完成IO操作"
    return "io result"

def req_a():
    print "开始处理请求req_a"
    ret = long_io()
    print "ret: %s" % ret
    print "完成处理请求req_a"

def req_b():
    print "开始处理请求req_b"
    print "完成处理请求req_b"

def main():
    req_a()
    req_b()

if __name__=="__main__":
    main()

# 执行过程：
# 开始处理请求req_a
# 开始执行IO操作
# 完成IO操作
# 完成处理请求req_a
# 开始处理请求req_b
# 完成处理请求req_b    
    

# 2. 异步
# 对于耗时的过程，我们将其交给别人（如其另外一个线程）去执行，而我们继续往下处理，当别人执行完耗时操作后再将结果反馈给我们，这就是我们所说的异步。
# 使用线程机制来实现异步。

# 2.1 回调写法实现原理
import time
import thread

def long_io(callback):
    """将耗时的操作交给另一线程来处理"""
    def fun(cb): # 回调函数作为参数
        """耗时操作"""
        print "开始执行IO操作"
        time.sleep(5)
        print "完成IO操作，并执行回调函数"
        cb("io result")  # 执行回调函数
    thread.start_new_thread(fun, (callback,))  # 开启线程执行耗时操作

def on_finish(ret):
    """回调函数"""
    print "开始执行回调函数on_finish"
    print "ret: %s" % ret
    print "完成执行回调函数on_finish"

def req_a():
    print "开始处理请求req_a" 
    long_io(on_finish)
    print "离开处理请求req_a"

def req_b():
    print "开始处理请求req_b"
    time.sleep(2) # 添加此句来突出显示程序执行的过程
    print "完成处理请求req_b"

def main():
    req_a()
    req_b()
    while 1: # 添加此句防止程序退出，保证线程可以执行完
        pass

if __name__ == '__main__':
    main()
    
    
# 执行过程:
# 开始处理请求req_a
# 离开处理请求req_a
# 开始处理请求req_b
# 开始执行IO操作
# 完成处理请求req_b
# 完成IO操作，并执行回调函数
# 开始执行回调函数on_finish
# ret: io result
# 完成执行回调函数on_finish

# 异步的特点是程序存在多个步调，即本属于同一个过程的代码可能在不同的步调上同时执行。


# 2.2 协程写法实现原理
# 在使用回调函数写异步程序时，需将本属于一个执行逻辑（处理请求a）的代码拆分成两个函数req_a和on_finish，这与同步程序的写法相差很大。而同步程序更便于理解业务逻辑，所以能否用同步代码的写法来编写异步程序？
# 初始版本
# coding:utf-8

import time
import thread

gen = None # 全局生成器，供long_io使用

def long_io():
    def fun():
        print "开始执行IO操作"
        global gen
        time.sleep(5)
        try:
            print "完成IO操作，并send结果唤醒挂起程序继续执行"
            gen.send("io result")  # 使用send返回结果并唤醒程序继续执行
        except StopIteration: # 捕获生成器完成迭代，防止程序退出
            pass
    thread.start_new_thread(fun, ())

def req_a():
    print "开始处理请求req_a"
    ret = yield long_io()
    print "ret: %s" % ret
    print "完成处理请求req_a"

def req_b():
    print "开始处理请求req_b"
    time.sleep(2)
    print "完成处理请求req_b"

def main():
    global gen
    gen = req_a()
    gen.next() # 开启生成器req_a的执行
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()
    
# 执行过程：
# 开始处理请求req_a
# 开始处理请求req_b
# 开始执行IO操作
# 完成处理请求req_b
# 完成IO操作，并send结果唤醒挂起程序继续执行
# ret: io result
# 完成处理请求req_a
    
# 升级版本
# 上面编写出的版本虽然req_a的编写方式很类似与同步代码，但是在main中调用req_a的时候却不能将其简单的视为普通函数，而是需要作为生成器对待。
# 现在，试图尝试修改，让req_a与main的编写都类似与同步代码。
# coding:utf-8

import time
import thread

gen = None # 全局生成器，供long_io使用

def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        global gen
        gen = f()
        gen.next()
    return wrapper

def long_io():
    def fun():
        print "开始执行IO操作"
        global gen
        time.sleep(5)
        try:
            print "完成IO操作，并send结果唤醒挂起程序继续执行"
            gen.send("io result")  # 使用send返回结果并唤醒程序继续执行
        except StopIteration: # 捕获生成器完成迭代，防止程序退出
            pass
    thread.start_new_thread(fun, ())

@gen_coroutine
def req_a():
    print "开始处理请求req_a"
    ret = yield long_io()
    print "ret: %s" % ret
    print "完成处理请求req_a"

def req_b():
    print "开始处理请求req_b"
    time.sleep(2)
    print "完成处理请求req_b"

def main():
    req_a()
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()
    
    
# 执行过程：
# 开始处理请求req_a
# 开始处理请求req_b
# 开始执行IO操作
# 完成处理请求req_b
# 完成IO操作，并send结果唤醒挂起程序继续执行
# ret: io result
# 完成处理请求req_a


# 最终版本
# 刚刚完成的版本依然不理想，因为存在一个全局变量gen来供long_io使用。我们现在再次改写程序，消除全局变量gen。
# coding:utf-8

import time
import thread

def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        gen_f = f()  # gen_f为生成器req_a
        r = gen_f.next()  # r为生成器long_io
        def fun(g):
            ret = g.next() # 执行生成器long_io
            try:
                gen_f.send(ret) # 将结果返回给req_a并使其继续执行
            except StopIteration:
                pass
        thread.start_new_thread(fun, (r,))
    return wrapper

def long_io():
    print "开始执行IO操作"
    time.sleep(5)
    print "完成IO操作，yield回操作结果"
    yield "io result"

@gen_coroutine
def req_a():
    print "开始处理请求req_a"
    ret = yield long_io()
    print "ret: %s" % ret
    print "完成处理请求req_a"

def req_b():
    print "开始处理请求req_b"
    time.sleep(2)
    print "完成处理请求req_b"

def main():
    req_a()
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()
    
# 执行过程：
# 开始处理请求req_a
# 开始处理请求req_b
# 开始执行IO操作
# 完成处理请求req_b
# 完成IO操作，yield回操作结果
# ret: io result
# 完成处理请求req_a

# 最终版本就是理解Tornado异步编程原理的最简易模型，但是，Tornado实现异步的机制不是线程，而是epoll，即将异步过程交给epoll执行并进行监视回调。

# 需要注意的一点是，实现的版本严格意义上来说不能算是协程，因为两个程序的挂起与唤醒是在两个线程上实现的，而Tornado利用epoll来实现异步，程序的挂起与唤醒始终在一个线程上，由Tornado自己来调度，属于真正意义上的协程。虽如此，并不妨碍理解Tornado异步编程的原理。
```

### 193. Tornado异步

```
# 因为epoll主要是用来解决网络IO的并发问题，所以Tornado的异步编程也主要体现在网络IO的异步上，即异步Web请求。

# 1. tornado.httpclient.AsyncHTTPClient
# Tornado提供了一个异步Web请求客户端tornado.httpclient.AsyncHTTPClient用来进行异步Web请求。
# fetch(request, callback=None)
# 用于执行一个web请求request，并异步返回一个tornado.httpclient.HTTPResponse响应。

# request可以是一个url，也可以是一个tornado.httpclient.HTTPRequest对象。如果是url，fetch会自己构造一个HTTPRequest对象。

# HTTPRequest
# HTTP请求类，HTTPRequest的构造函数可以接收众多构造参数，最常用的如下：
#	url (string) – 要访问的url，此参数必传，除此之外均为可选参数
#	method (string) – HTTP访问方式，如“GET”或“POST”，默认为GET方式
#	headers (HTTPHeaders or dict) – 附加的HTTP协议头
#	body – HTTP请求的请求体


# HTTPResponse
# HTTP响应类，其常用属性如下：
#	code: HTTP状态码，如 200 或 404
#	reason: 状态码描述信息
#	body: 响应体字符串
#	error: 异常（可有可无）

# 2. 测试接口
# 新浪IP地址库
#	接口说明
#	1.请求接口（GET）：
http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=[ip地址字串]
#	2.响应信息：
#	（json格式的）国家 、省（自治区或直辖市）、市（县）、运营商
#	3.返回数据格式：
{"ret":1,"start":-1,"end":-1,"country":"\u4e2d\u56fd","province":"\u5317\u4eac","city":"\u5317\u4eac","district":"","isp":"","type":"","desc":""}


# 3. 回调异步
class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body)
            if 1 == data["ret"]:
                self.write(u"国家：%s 省份: %s 城市: %s" % (data["country"], data["province"], data["city"]))
            else:
                self.write("查询IP信息错误")
        self.finish() # 发送响应信息，结束请求处理


# tornado.web.asynchronous
# 此装饰器用于回调形式的异步方法，并且应该仅用于HTTP的方法上（如get、post等）。

# 此装饰器不会让被装饰的方法变为异步，而只是告诉框架被装饰的方法是异步的，当方法返回时响应尚未完成。只有在request handler调用了finish方法后，才会结束本次请求处理，发送响应。

# 不带此装饰器的请求在get、post等方法返回时自动完成结束请求处理。


# 4. 协程异步
# 上一节中封装的装饰器get_coroutine在Tornado中对应的是tornado.gen.coroutine。
class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24")
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body)
            if 1 == data["ret"]:
                self.write(u"国家：%s 省份: %s 城市: %s" % (data["country"], data["province"], data["city"]))
            else:
                self.write("查询IP信息错误")
                
# 也可以将异步Web请求单独出来：
class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        rep = yield self.get_ip_info("14.130.112.24")
        if 1 == rep["ret"]:
            self.write(u"国家：%s 省份: %s 城市: %s" % (rep["country"], rep["province"], rep["city"]))
        else:
            self.write("查询IP信息错误")

    @tornado.gen.coroutine
    def get_ip_info(self, ip):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip)
        if response.error:
            rep = {"ret:0"}
        else:
            rep = json.loads(response.body)
        raise tornado.gen.Return(rep)  # 此处需要注意
        
# 代码中我们需要注意的地方是get_ip_info返回值的方式，在python 2中，使用了yield的生成器可以使用不返回任何值的return，但不能return value，因此Tornado为我们封装了用于在生成器中返回值的特殊异常tornado.gen.Return，并用raise来返回此返回值。


# 并行协程
# Tornado可以同时执行多个异步，并发的异步可以使用列表或字典，如下：
class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        ips = ["14.130.112.24",
            "15.130.112.24",
            "16.130.112.24",
            "17.130.112.24"]
        rep1, rep2 = yield [self.get_ip_info(ips[0]), self.get_ip_info(ips[1])]
        rep34_dict = yield dict(rep3=self.get_ip_info(ips[2]), rep4=self.get_ip_info(ips[3]))
        self.write_response(ips[0], rep1) 
        self.write_response(ips[1], rep2) 
        self.write_response(ips[2], rep34_dict['rep3']) 
        self.write_response(ips[3], rep34_dict['rep4']) 

    def write_response(self, ip, response):
        self.write(ip) 
        self.write(":<br/>") 
        if 1 == response["ret"]:
            self.write(u"国家：%s 省份: %s 城市: %s<br/>" % (response["country"], response["province"], response["city"]))
        else:
            self.write("查询IP信息错误<br/>")

    @tornado.gen.coroutine
    def get_ip_info(self, ip):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip)
        if response.error:
            rep = {"ret:1"}
        else:
            rep = json.loads(response.body)
        raise tornado.gen.Return(rep)
        
# 5. 关于数据库的异步说明
# 网站基本都会有数据库操作，而Tornado是单线程的，这意味着如果数据库查询返回过慢，整个服务器响应会被堵塞。

# 数据库查询，实质上也是远程的网络调用；理想情况下，是将这些操作也封装成为异步的；但Tornado对此并没有提供任何支持。

# 这是Tornado的设计，而不是缺陷。

# 一个系统，要满足高流量；是必须解决数据库查询速度问题的！

# 数据库若存在查询性能问题，整个系统无论如何优化，数据库都会是瓶颈，拖慢整个系统！

# 异步并不能从本质上提到系统的性能；它仅仅是避免多余的网络响应等待，以及切换线程的CPU耗费。

# 如果数据库查询响应太慢，需要解决的是数据库的性能问题；而不是调用数据库的前端Web应用。

# 对于实时返回的数据查询，理想情况下需要确保所有数据都在内存中，数据库硬盘IO应该为0；这样的查询才能足够快；而如果数据库查询足够快，那么前端web应用也就无将数据查询封装为异步的必要。

# 就算是使用协程，异步程序对于同步程序始终还是会提高复杂性；需要衡量的是处理这些额外复杂性是否值得。

# 如果后端有查询实在是太慢，无法绕过，Tornaod的建议是将这些查询在后端封装独立封装成为HTTP接口，然后使用Tornado内置的异步HTTP客户端进行调用。
        
```

### 194. WebSocket

```
# WebSocket是HTML5规范中新提出的客户端-服务器通讯协议，协议本身使用新的ws://URL格式。

# WebSocket 是独立的、创建在 TCP 上的协议，和 HTTP 的唯一关联是使用 HTTP 协议的101状态码进行协议切换，使用的 TCP 端口是80，可以用于绕过大多数防火墙的限制。

# WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端直接向客户端推送数据而不需要客户端进行请求，两者之间可以创建持久性的连接，并允许数据进行双向传送。

# 目前常见的浏览器如 Chrome、IE、Firefox、Safari、Opera 等都支持 WebSocket，同时需要服务端程序支持 WebSocket。


# 1. Tornado的WebSocket模块
# ornado提供支持WebSocket的模块是tornado.websocket，其中提供了一个WebSocketHandler类用来处理通讯。
WebSocketHandler.open()  # 当一个WebSocket连接建立后被调用。
WebSocketHandler.on_message(message)  # 当客户端发送消息message过来时被调用，注意此方法必须被重写。
WebSocketHandler.on_close()  #  当WebSocket连接关闭后被调用。
WebSocketHandler.write_message(message, binary=False) # 向客户端发送消息messagea，message可以是字符串或字典（字典会被转为json字符串）。若binary为False，则message以utf8编码发送；二进制模式（binary=True）时，可发送任何字节码。
WebSocketHandler.close()  # 关闭WebSocket连接。
WebSocketHandler.check_origin(origin)  # 判断源origin，对于符合条件（返回判断结果为True）的请求源origin允许其连接，否则返回403。可以重写此方法来解决WebSocket的跨域请求（如始终return True）。


# 2. 前端JavaScript编写
# 在前端JS中使用WebSocket与服务器通讯的常用方法如下：
var ws = new WebSocket("ws://127.0.0.1:8888/websocket"); // 新建一个ws连接
ws.onopen = function() {  // 连接建立好后的回调
   ws.send("Hello, world");  // 向建立的连接发送消息
};
ws.onmessage = function (evt) {  // 收到服务器发送的消息后执行的回调
   alert(evt.data);  // 接收的消息内容在事件参数evt的data属性中
};

#  3. 在线聊天室的小Demo
# 后端代码 server.py
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=8000, type=int)

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
# 前端代码index.html

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>聊天室</title>
</head>
<body>
    <div id="contents" style="height:500px;overflow:auto;"></div>
    <div>
        <textarea id="msg"></textarea>
        <a href="javascript:;" onclick="sendMsg()">发送</a>
    </div>
    <script src="{{static_url('js/jquery.min.js')}}"></script>
    <script type="text/javascript">
        var ws = new WebSocket("ws://192.168.114.177:8000/chat");
        ws.onmessage = function(e) {
            $("#contents").append("<p>" + e.data + "</p>");
        }
        function sendMsg() {
            var msg = $("#msg").val();
            ws.send(msg);
            $("#msg").val("");
        }
    </script>
</body>
</html>
```

### 195. 部署Tornado

```
# 为了充分利用多核CPU，并且为了减少同步代码中的阻塞影响，在部署Tornado的时候需要开启多个进程（最好为每个CPU核心开启一个进程）

# 因为Tornado自带的服务器性能很高，所以我们只需开启多个Tornado进程。为了对外有统一的接口，并且可以分发用户的请求到不同的Tornado进程上，用Nginx来进行代理。

# 1. supervisor
# 为了统一管理Tornado的多个进程，可以借助supervisor工具。

# 安装
sudo pip install supervisor

# 配置
# 运行echo_supervisord_conf命令输出默认的配置项，可以如下操作将默认配置保存到文件中
echo_supervisord_conf > supervisord.conf

# 打开编辑supervisord.conf文件，修改
[include]
files = relative/directory/*.ini
# 为:
[include]
files = /etc/supervisor/*.conf

# include选项指明包含的其他配置文件。
# 将编辑后的supervisord.conf文件复制到/etc/目录下
sudo cp supervisord.conf /etc/

# 然后在/etc目录下新建子目录supervisor（与配置文件里的选项相同），并在/etc/supervisor/中新建tornado管理的配置文件tornado.conf。
[group:tornadoes]
programs=tornado-8000,tornado-8001,tornado-8002,tornado-8003

[program:tornado-8000]
command=/home/python/.virtualenvs/tornado_py2/bin/python /home/python/Documents/demo/chat/server.py --port=8000
directory=/home/python/Documents/demo/chat
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/home/python/tornado.log
loglevel=info

[program:tornado-8001]
command=/home/python/.virtualenvs/tornado_py2/bin/python /home/python/Documents/demo/chat/server.py --port=8001
directory=/home/python/Documents/demo/chat
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/home/python/tornado.log
loglevel=info

[program:tornado-8002]
command=/home/python/.virtualenvs/tornado_py2/bin/python /home/python/Documents/demo/chat/server.py --port=8002
directory=/home/python/Documents/demo/chat
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/home/python/tornado.log
loglevel=info

[program:tornado-8003]
command=/home/python/.virtualenvs/tornado_py2/bin/python /home/python/Documents/demo/chat/server.py --port=8003
directory=/home/python/Documents/demo/chat
user=python
autorestart=true
redirect_stderr=true
stdout_logfile=/home/python/tornado.log
loglevel=info


# 启动
supervisord -c /etc/supervisord.conf
# 查看 supervisord 是否在运行：
ps aux | grep supervisord


# supervisorctl
# 可以利用supervisorctl来管理supervisor。
supervisorctl

> status    # 查看程序状态
> stop tornadoes:*   # 关闭 tornadoes组 程序
> start tornadoes:*  # 启动 tornadoes组 程序
> restart tornadoes:*    # 重启 tornadoes组 程序
> update    ＃ 重启配置文件修改过的程序

# 执行status命令时，显示如下信息说明tornado程序运行正常：
supervisor> status
tornadoes:tornado-8000 RUNNING pid 32091, uptime 00:00:02
tornadoes:tornado-8001 RUNNING pid 32092, uptime 00:00:02
tornadoes:tornado-8002 RUNNING pid 32093, uptime 00:00:02
tornadoes:tornado-8003 RUNNING pid 32094, uptime 00:00:02
            

            
# 2. nginx
# 对于使用ubuntu apt-get 安装nginx，其配置文件位于/etc/nginx/sites-available中，修改default文件如下：
upstream tornadoes {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

upstream websocket {
    server 127.0.0.1:8000;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    location /static/ {
        root /home/python/Documents/demo/chat;
        if ($query_string) {
            expires max;
        }
    }

    location /chat {
        proxy_pass http://websocket/chat;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;  # 协议 http https
        proxy_pass http://tornadoes;
    }
}

# 启动nginx
service nginx start   # 启动
service nginx stop    # 停止
service nginx restart # 重启


# 源码安装版本
启动：sudo sbin/nginx
停止：sudo sbin/nginx -s stop
重启：sudo sbin/nginx -s reload
```

## 