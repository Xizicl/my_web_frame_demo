import re
import time

URl_FUNC_DICT = dict()


def route(url):
    def set_func(func):
        URl_FUNC_DICT[url] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        return call_func

    return set_func


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])

    filename = environ['PATH_INFO']
    try:
        service = URl_FUNC_DICT[filename]
        return service()
    except KeyError as e:
        print('路由错误：找不到:', e)
        return '500 Server Error'
    except Exception as e:
        print(e)
        return '500 Server Error<\br>%s' % str(e)

    # if filename == '/index.py':
    #     return index()
    # else:
    #     return '<h1>Hello, web!你好</h1><h2>页面不见了。。。可能是被吃掉了</h2>'


@route('/index.py')
def index():
    with open('./templates/index.html', encoding='utf-8') as f:
        content = f.read()
    my_stock_info = 'POWER by Xizicl '
    content = re.sub(r'\{%content%\}', (my_stock_info + time.ctime()), content)
    return content


@route('/center.py')
def center():
    with open('./templates/center.html', encoding='utf-8') as f:
        content = f.read()
    my_stock_info = 'POWER by Xizicl '
    content = re.sub(r'\{%content%\}', (my_stock_info + time.ctime()), content)
    return content
