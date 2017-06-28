#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from http.client import HTTPConnection
# from pandas import DataFrame
from urllib.request import urlopen
import sys
import lxml.html as html
import mysql.connector as c
from datetime import datetime as dt

defaultDbConfig = {
    'user': 'test',
    'password': 'test',
    'host': '127.0.0.1',
    'database': 'test',
    'raise_on_warnings': True,
}
tables = {
    'goods': 'goods',
    'prices': 'prices',
    'emails': 'emails', """ todo """
    'shops': 'shops',
    'categories': 'categories',
}
db = None


class Http:

    def __init__(self):
        pass

    def get(self, filename: str, offset: int = -1, maxlen: int = -1):
        ret = urlopen(filename)
        charset = ret.headers.get_content_charset()
        ret = ret.read()
        if offset > 0:
            ret = ret[offset:]
        if maxlen > 0:
            ret = ret[:maxlen]
        return ret.decode(charset)


class File:

    def __init__(self):
        pass

    def get(self, filename: str, offset: int = -1, maxlen: int = -1):
        fp = open(filename, 'rb')
        try:
            if offset > 0:
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret
        finally:
            fp.close()


class Parser:

    html = ''
    url = ''

    def __init__(self, url: str):
        self.url = url

    def find(self, selector):
        if len(self.html) < 1:
            if self.url.find('://') > 0:
                http = Http()
                content = http.get(self.url)
            else:
                file = File()
                content = file.get(self.url)
            self.html = html.document_fromstring(content)

        return self.html.cssselect(selector)

    def getAttr(self, element, attr: str):
        """
        :param element:
        :param attr:
        :return:
        """
        if attr in self.getKeys(element):
            return element.get(attr)
        return ''

    def getKeys(self, element):
        return element.keys()


class Db:

    connector = None
    cursor = None

    def __init__(self, config: dict):
        self.connector = c.connect(**config)

    def execute(self, query: str, args: dict = ()):
        self.cursor.execute(query, args)
        return self

    def query(self, query: str, args: dict = ()):
        self.cursor = self.connector.cursor()
        self.execute(query, args)
        return self

    def fetch(self, size: int = 10):
        return self.cursor.fetchmany(size)

    def close(self):
        self.cursor.close()
        self.connector.close()


def _create_connection():
    global db
    if type(db) == type(None):
        db = get_db(defaultDbConfig)
    return db


def get_parser(url: str):
    return Parser(url)


def get_db(config):
    return Db(config)


def insert_price(product_id: int, price: float):
    db = _create_connection()
    q = db.query('SELECT count(1) as c WHERE price=%s AND DATE(good_id)=%s AND date=DATE(%s)', (price, product_id, dt.now(),))
    result = q.fetch(1)
    if hasattr(result, 'c') and result['c'] > 0:
        return
    db.execute('INSERT INTO prices (price, good_id, date) VALUES (%s, %s, %s)', (price, product_id, dt.now(),))


def insert_product(product_id: int, shop_id: int):
    db = _create_connection()
    q = db.query('SELECT count(1) as c WHERE price=%s AND DATE(good_id)=%s AND date=DATE(%s)', (price, product_id, dt.now(),))
    result = q.fetch(1)
    if hasattr(result, 'c') and result['c'] > 0:
        return
    db.execute('INSERT INTO prices (price, good_id, date) VALUES (%s, %s, %s)', (price, product_id, dt.now(),))


if __name__ == '__main__':

    # print(dt.now(), .2 + .1 - .2 - .1)

    exit(0)

    db = Db(defaultDbConfig)
    db.query('SELECT * FROM users WHERE id > %s', ('0',))
    print(db.cursor.fetchmany(2))

    exit(0)

    url = 'https://ya.ru/'
    if len(sys.argv) > 1 and sys.argv[1].find('://') > 0:
        url = sys.argv[1]
    parser = Parser(url)
    element = parser.find('.personal.i-bem')#.text_content()
    for e in element:
        # list = []
        # for i in dir(e):
        #     if callable(getattr(e, i)):
        #         list.append(i)
        # print(list)
        # print(e.get('data-bem'))
        # print(e.text_content())
        pass
