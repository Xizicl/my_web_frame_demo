import time


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])

    filename = environ['PATH_INFO']
    if filename == '/index.py':
        return index()
    else:
        return '<h1>Hello, web!你好</h1><h2>页面不见了。。。可能是被吃掉了</h2>'


def index():
    return 'welcome my website' + time.ctime()
