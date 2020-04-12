import time


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])
    return '<h1>Hello, web!你好</h1>'


def login():
    return 'welcome my website' + time.ctime()
