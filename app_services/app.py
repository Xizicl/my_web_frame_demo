import re
import time


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])

    filename = environ['PATH_INFO']

    service = URl_FUNC_DICT[filename]
    return service()
    # if filename == '/index.py':
    #     return index()
    # else:
    #     return '<h1>Hello, web!你好</h1><h2>页面不见了。。。可能是被吃掉了</h2>'


def index():
    with open('./templates/index.html', encoding='utf-8') as f:
        content = f.read()
    my_stock_info = 'POWER by Xizicl '
    content = re.sub(r'\{%content%\}', (my_stock_info + time.ctime()), content)
    return content


def center():
    with open('./templates/center.html', encoding='utf-8') as f:
        content = f.read()
    my_stock_info = 'POWER by Xizicl '
    content = re.sub(r'\{%content%\}', (my_stock_info + time.ctime()), content)
    return content


URl_FUNC_DICT = {
    '/index.py': index,
    '/center.py': center
}
