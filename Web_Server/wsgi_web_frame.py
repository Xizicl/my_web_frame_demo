# -*- coding: utf-8 -*-
import json
import socket
import re
import multiprocessing

try:
    from app_services import app
except Exception as e:
    print("请将app_services中放入app.py")
    raise e


class WSGIServer():
    def __init__(self, port=8888, static_path='./static'):
        # 设置默认配置

        self.port = port
        self.static_path = static_path  # 静态文件路径
        self.load_config()
        # 创建套接字

        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定套接字
        self.tcp_server_socket.bind(("", self.port))
        # 变为监听套接字
        self.tcp_server_socket.listen(128)

    def service_client(self, new_socket):
        """为这个客户端返回数据"""
        # 1.接收浏览器发过来的http请求
        # '''GET /images/trolltech-logo.png HTTP/1.1\r\n
        # Host: 127.0.0.1:7890\r\n
        # Connection: keep-alive\r\n
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\r\n
        # Accept: image/webp,image/apng,image/*,*/*;q=0.8\r\n
        # Referer: http://127.0.0.1:7890/\r\n
        # Accept-Encoding: gzip, deflate, br\r\n
        # Accept-Language: zh-CN,zh;q=0.9\r\n
        # \r\n'''
        request_ = new_socket.recv(1024).decode("utf-8")
        # request_line = request_.splitlines()
        # print('request_:'+request_)
        re_a = re.match(r"GET (.*) HTTP", request_)
        if re_a:
            filename = re_a.group(1)
            # re_a = re.match(r"[^/]+/[^ ]*",request_line[0])
            # print('{0}{1}'.format(request_.split('\r\n'),filename))
            print(filename)
            if not filename.endswith('.py'):
                # 静态资源
                if filename == "/":
                    filename = "/index.html"
                try:
                    # with open(r".\advanced\web服务器\html"+re_a,"rb") as f:
                    #         all_file= f.read()
                    # print(all_file)

                    f = open(self.static_path + filename, "rb")

                except:
                    response = "HTTP/1.1 404 NOT FOUND\r\n"
                    response += "\r\n"
                    response += "----file not found----"
                    new_socket.send(response.encode("utf-8"))
                    # new_socket.close()

                else:
                    all_file = f.read()
                    f.close()
                    response = "HTTP/1.1 200 OK\r\n"
                    response += "\r\n"

                    new_socket.send(response.encode("utf-8"))
                    new_socket.send(all_file)
                    # new_socket.close()
            else:
                # 动态资源

                env = dict()
                env['PATH_INFO'] = filename
                body = app.application(env, start_response=self.start_response)

                header = "HTTP/1.1 %s\r\n" % self.status_code
                for head in self.headers:
                    header += "%s:%s\r\n" % (head[0], head[1])
                header += "\r\n"

                response = header + body
                new_socket.send(response.encode('utf-8'))
        else:
            print('request:' + request_ + 'maybe the client is closed')
        new_socket.close()

    def start_response(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers + [('server', 'Xizi_frame')]

    def load_config(self):
        try:
            with open('./conf/config.conf') as f:
                config_list = json.load(f)
            print('config:', config_list)
            if config_list:
                static_path = config_list["static_path"]
                port = config_list["port"]

                self.port = port
                self.static_path = static_path
        except KeyError as e:
            print('配置文件错误,按默认配置运行', e)
        except Exception as e:
            raise e
        else:
            return True

    def run_forever(self):
        """用来完成整体的控制"""
        print("Server is running with:http://{0}:{1}".format(*self.tcp_server_socket.getsockname()))
        print("Server is running with:http://{0}:{1}".format('127.0.0.1', self.tcp_server_socket.getsockname()[1]))
        # http://localhost:7890/
        while True:
            # 等待新客户端的连接
            new_socket, client_addr = self.tcp_server_socket.accept()
            # 为这个客户端服务
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            # service_client(new_socket)
            p.start()
            new_socket.close()  # 多线程不需要这个


def main():
    wsgi_server = WSGIServer()
    wsgi_server.run_forever()


if __name__ == "__main__":
    print('请从根目录下main.py运行')
