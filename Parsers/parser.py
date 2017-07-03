#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from http.client import HTTPConnection
# from pandas import DataFrame
# from urllib.request import urlopen
from requests import get as get_request
from datetime import datetime as dt
import sys
import lxml.html as html
import mysql.connector as c
# from math import ceil
# from random import random

defaultDbConfig = {
    'user': 'test',
    'password': 'test',
    'host': 'localhost',
    'database': 'shop',
    'raise_on_warnings': True,
}
tables = {
    'goods': 'goods',
    'prices': 'prices',
    'emails': 'emails',
    'shops': 'shops',
    'categories': 'categories',
    'vendors': 'vendors',
}
db = None


class Http:

    def __init__(self):
        pass

    def get(self, filename: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None):
        if not headers:
            headers = {}
        if not cookies:
            cookies = ()
        response = get_request(filename, headers=headers, cookies=cookies)
        ret = response.text
        if offset > 0:
            ret = ret[offset:]
        if maxlen > 0:
            ret = ret[:maxlen]
        return ret


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

    def find(self, selector, _html: str = '', cookies: dict = None, headers: dict = None):
        if len(_html) < 1 and len(self.html) < 1:
            if self.url.find('://') > 0:
                http = Http()
                content = http.get(self.url, cookies=cookies, headers=headers)
            else:
                file = File()
                content = file.get(self.url)
            self.html = html.document_fromstring(content)

        if len(_html) > 0:
            _html = html.document_fromstring(_html)
        else:
            _html = self.html

        return _html.cssselect(selector)

    def get_attr(self, element, attr: str):
        """
        :param element:
        :param attr:
        :return:
        """
        if attr in self.get_keys(element):
            return element.get(attr)
        return ''

    def get_keys(self, element):
        return element.keys()


class Db:

    connector = None
    cursor = None

    def __init__(self, config: dict):
        self.connector = c.connect(**config)

    def execute(self, query: str, args: tuple = tuple()):
        self.cursor = self.connector.cursor(buffered=True)
        self.cursor.execute(query, args)
        return self

    def query(self, query: str, args: tuple = tuple()):
        self.cursor = self.connector.cursor(buffered=True)
        self.execute(query, args)
        return self

    def fetch(self, size: int = 10):
        if size == 1:
            return self.cursor.fetchone()
        if size == 0:
            return self.cursor.fetchall()
        return self.cursor.fetchmany(size)

    def close(self):
        global db
        db = None
        self.connector.commit()
        self.cursor.close()
        self.connector.close()

    def insert_id(self):
        return self.cursor.lastrowid


def get_content(url: str, cookies: dict = None, headers: dict = None):
    if url.find('://') >= 0:
        return Http().get(url, cookies=cookies, headers=headers)
    return File().get(url)


def get_db(config=None):
    global db
    if not config:
        config = defaultDbConfig
    if db is None:
        db = Db(config)
    return db


def get_parser(url: str):
    return Parser(url)


# todo: переложить на модели https://docs.djangoproject.com/en/1.11/topics/db/models/

def insert_price(product_id: int, price: float):
    db = get_db()
    q = db.query('SELECT id FROM ' + tables.get('prices') + ' WHERE good_id=%s AND DATE(good_id)=DATE(%s)', (product_id, dt.now(),)).fetch(1)
    if isinstance(q, tuple):
        id = q[0]
    else:
        id = db.execute(
            'INSERT INTO ' + tables.get('prices') + ' (price, good_id, date) VALUES (%s, %s, %s)'
            , (price, product_id, dt.now(),)
        ).insert_id()
    db.close()
    return id


def insert_product(product_id: int, shop_id: int, name: str, vendor_id: int, category_id: int):
    db = get_db()
    q = db.query('SELECT id FROM ' + tables.get('goods') + ' WHERE good_id=%s AND shop_id=%s', (product_id, shop_id,)).fetch(1)
    print(q)
    if isinstance(q, tuple):
        id = q[0]
    else:
        id = db.execute(
        'INSERT INTO %s (price, good_id, date) VALUES (%s, %s, %s, %s, %s, %s)'
        , (tables.get('goods'), product_id, dt.now(), name, vendor_id, category_id,)
    ).insert_id()
    db.close()
    return id


def insert_category(name: str, url: str, shop_id: int):
    db = get_db()
    q = db.query('SELECT id FROM ' + tables.get('categories') + ' WHERE url=%s AND shop_id=%s', (url, shop_id,)).fetch(1)
    if isinstance(q, tuple):
        id = q[0]
    else:
        id = db.execute(
            'INSERT INTO ' + tables.get('categories') + ' (name, url, date, shop_id) VALUES (%s, %s, %s, %s)'
            , (name, url, dt.now(), shop_id,)
        ).insert_id()
    db.close()
    return id


def insert_vendor(name: str):
    db = get_db()
    q = db.query('SELECT id FROM ' + tables.get('vendors') + ' WHERE name=%s', (name,)).fetch(1)
    if isinstance(q, tuple):
        id = q[0]
    else:
        id = db.execute(
            'INSERT INTO ' + tables.get('vendors') + ' (name) VALUES (%s)'
            , (name,)
        ).insert_id()
    db.close()
    return id


def insert_store(name: str, url: str):
    db = get_db()
    q = db.query('SELECT id FROM ' + tables.get('shops') + ' WHERE url=%s', (url,)).fetch(1)
    if isinstance(q, tuple):
        id = q[0]
    else:
        id = db.execute(
            'INSERT INTO ' + tables.get('shops') + ' (name, url) VALUES (%s, %s)'
            , (name, url,)
        ).insert_id()
    db.close()
    return id


if __name__ == '__main__':

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
