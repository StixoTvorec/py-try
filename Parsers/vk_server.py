#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import time
# import mysql.connector as mysqlConnector
import logging
from wsrpc import WebSocketRoute, WebSocket

project_root = os.getcwd()
options = {
    'port': 81,
    'listen': '0.0.0.0'
}
# db_url = os.environ.get('CLEARDB_DATABASE_URL', '')
# if db_url == '':
#     defaultDbConfig = {
#         'user': 'test',
#         'password': 'test',
#         'host': 'localhost',
#         'database': 'shop',
#         'raise_on_warnings': True,
#     }
# else:
#     defaultDbConfig = {
#         'user': 'test',
#         'password': 'test',
#         'host': 'localhost',
#         'database': 'shop',
#         'raise_on_warnings': True,
#     }

list = {}
log = logging.getLogger("wsrpc.handler")


# class Db:
# 
#     connector = None
#     cursor = None
# 
#     def __init__(self, config: dict):
#         self.connector = mysqlConnector.connect(**config)
# 
#     def execute(self, query: str, args: tuple = tuple()):
#         self.cursor = self.connector.cursor(buffered=True)
#         self.cursor.execute(query, args)
#         return self
# 
#     def query(self, query: str, args: tuple = tuple()):
#         self.cursor = self.connector.cursor(buffered=True)
#         self.execute(query, args)
#         return self
# 
#     def fetch(self, size: int = 10):
#         if size == 1:
#             return self.cursor.fetchone()
#         if size == 0:
#             return self.cursor.fetchall()
#         return self.cursor.fetchmany(size)
# 
#     def close(self):
#         global db
#         db = None
#         self.connector.commit()
#         self.cursor.close()
#         self.connector.close()
# 
#     def insert_id(self):
#         return self.cursor.lastrowid


# db = Db(defaultDbConfig)


class MyWebSocket(WebSocket):
    _list = []
    userId = 1

    def on_close(self):
        self._list.pop({self.id: self.userId})
        super().on_close()

    def open(self):
        super().open()
        self.userId += 1
        self._list[self.id] = self.userId

    def clients_list(self):
        return self._CLIENTS


class MessagesClass(WebSocketRoute):
    list = []

    def init(self, **kwargs):
        print(123)
        return self.socket.call('whoAreYou', callback=self._handle_user_agent)

    def send(self, **kwargs):
        if 'message' in kwargs:
            # self.list.extend([self.socket.id])
            for u in MyWebSocket().clients_list():
                u.call('incoming', {'text': kwargs['message'], 'from'})


# WebSocket.ROUTES['test'] = ExampleClassBasedRoute
MyWebSocket.ROUTES['messages'] = MessagesClass
MyWebSocket.ROUTES['getTime'] = lambda t: time.time()

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(tornado.web.Application((
        (r"/ws/", MyWebSocket),
        (r'/(.*)', tornado.web.StaticFileHandler, {
             'path': os.path.join(project_root, 'static'),
             'default_filename': 'index.html'
        }),
    ), cookie_secret='eE6bwD2$Qr8Qvz*aZZ0VE&XSz5i@a9%tNzFwacNdO99^W*4#Xiwdyww'))

    print('Starting server: {}:{}'.format(options['listen'], options['port'],))

    http_server.listen(options['port'], address=options['listen'])
    # WebSocket.cleanup_worker()
    tornado.ioloop.IOLoop.instance().start()
