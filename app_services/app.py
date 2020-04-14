import re
import time
import pymysql

URl_FUNC_DICT = dict()


def route(url):
    def set_func(func):
        URl_FUNC_DICT[url] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        return call_func

    return set_func


@route('/index.html')
def index():
    with open('./templates/index.html', encoding='utf-8') as f:
        content = f.read()

    connect = pymysql.connect(host='192.168.8.5', user='root', password="123456",
                              database='cartoondb', port=3306)
    cursor = connect.cursor()
    cursor.execute('select * from info')
    infos = cursor.fetchall()
    templates = '''
        <tr>
            <th>{0}</th>
            <th>{1}</th>
            <th>{2}</th>
            <th>{3}</th>
            <th>{4}</th>
            <th>{5}</th>
            <th>{6}</th>
            <th>{7}</th>
            <th><input type='button' value='添加' id='toAdd' name='toAdd' systemidvaule='000007'></th>
        </tr>
    '''
    html = ''
    for line_info in infos:
        html += templates.format(line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5],
                                 line_info[6], line_info[7])

    content = re.sub(r'\{%content%\}', html, content)
    return content


@route('/center.html')
def center():
    with open('./templates/center.html', encoding='utf-8') as f:
        content = f.read()

    connect = pymysql.connect(host='192.168.8.5', user='root', password="123456",
                              database='cartoondb', port=3306)
    cursor = connect.cursor()
    cursor.execute(
        'select code,short,chg,turnover,price,highs,note_info from focus left join info on focus.info_id=info.id')
    infos = cursor.fetchall()
    templates = """
        <tr>
            <th>{0}</th>
            <th>{1}</th>
            <th>{2}</th>
            <th>{3}</th>
            <th>{4}</th>
            <th>{5}</th>
            <th style="color:red">{6}</th>
            <th>修改</th>
            <th><input type='button' value='删除' id='toDel' name='toDel' systemidvaule='000007'></th>
        </tr>
    """
    html = ''
    for line_info in infos:
        html += templates.format(line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5],
                                 line_info[6])

    content = re.sub(r'\{%content%\}', html, content)
    return content


@route(r'/add/\d+\.html')
def add_focus():
    return 'add_ok'


@route(r'/add/<temp>.html')
def add_focus(temp):
    return 'add_ok1{0}'.format(temp)


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])

    filename = environ['PATH_INFO']
    # try:
    #     for url, func in URl_FUNC_DICT.items():
    #         url_split = re.match(r'/([^/]+)/\<([^/]+)\>\.html', url)
    #         print(url_split)
    #         if url_split:
    #             return func(url_split)
    #     else:
    #         print('路由错误：找不到:', filename)
    #         return '500 Server Error ' + str(filename)
    # except Exception as e:
    #     print('捕捉到了个异常：', e)
    #     # raise e
    #     return '500 Server Error<\br>%s' % str(e)

    try:
        for url, func in URl_FUNC_DICT.items():
            ret = re.match(url, filename)
            if ret:
                return func()
        else:
            print('路由错误：找不到:', filename)
            return '500 Server Error ' + str(filename) + '<h2>页面不见了。。。可能是被吃掉了</h2>'
    except Exception as e:
        print('捕捉到了个异常：', e)
        # raise e
        return '500 Server Error<\br><h2>页面不见了。。。可能是被吃掉了</h2><\br>%s' % str(e)

    # try:
    #     service = URl_FUNC_DICT[filename]
    #     return service()
    # except KeyError as e:
    #     print('路由错误：找不到:', e)
    #     return '500 Server Error '+str(e)
    # except Exception as e:
    #     print(e)
    #     # raise e
    #     return '500 Server Error<\br>%s' % str(e)

    # if filename == '/index.py':
    #     return index()
    # else:
    #     return '<h1>Hello, web!你好</h1><h2>页面不见了。。。可能是被吃掉了</h2>'
