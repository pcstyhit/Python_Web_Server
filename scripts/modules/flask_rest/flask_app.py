from functools import wraps
import threading
from flask import Flask, render_template
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from scripts.libs import CONFIGS, get_abs_path
from .easy_restful import api_handle
from .websocket import webSocket_handle

app = Flask(__name__)
PORT = CONFIGS['default_web_port']
HOST = '0.0.0.0'


def init_app():
    '''
    初始化flask app
    template_folder: 用于指定模板文件的文件夹路径。模板文件通常包含 HTML 或其他模板引擎支持的标记,用于构建动态生成的网页。
    static_url_path: 这是一个可选参数,指定静态文件的URL路径。默认情况下,静态文件的URL路径是/static/,但你可以通过这个参数进行自定义。
    static_folder: 用于指定包含静态文件(如样式表、JavaScript文件等)的文件夹路径。
    '''
    template_folder = get_abs_path('example_path')
    static_url_path = ""
    static_folder = get_abs_path('example_dependencies_path')


    app = Flask(__name__,
                template_folder=template_folder,
                static_url_path=static_url_path,
                static_folder=static_folder)
    # 允许跨域
    CORS(app, supports_credentials=True)

    # 声明restful api
    api = Api(app)
    api_handle(api)

    # 挂载静态网页的路由
    @app.route('/')
    def index():
        return render_template('index.html')


def run_in_threading(func):
    '''语法糖,将全部函数运行在一个线程内'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()

    return wrapper

@run_in_threading
def run_default_app():
    init_app()
    app.run(host=HOST, port=PORT)

@run_in_threading
def run_socket_app():
    init_app()
    # 创建为websocket服务
    socketio = SocketIO(app, cors_allowed_origins='*')
    webSocket_handle(socketio)
    socketio.run(app, host=HOST, port=PORT)

@run_in_threading
def run_defaut_ssl_app():
    init_app()
    certfile = get_abs_path('cert_path','server.crt')
    keyfile = get_abs_path('cert_path','server.key')
    app.run(host=HOST, port=PORT, ssl_context=(certfile, keyfile))


@run_in_threading
def run_socket_ssl_app():
    pass
