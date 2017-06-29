#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser as p


storeUrl = '/tmp/view-source_https___www.ulmart.ru.html'
# storeUrl = 'https://ulmart.ru'
mainMenuClass = 'li.b-list__item.b-dropdown.b-dropdown_catalog-menu.dropdown.dropdown_catalog-menu > a'
shopId = 0


def product_process(url: str, params: dict):
    pass


def page_process(url: str, params: dict):
    pass


if __name__ == '__main__':

    shopId = p.insert_store(name='Ulmart', url=storeUrl)

    _ = p.get_parser('/tmp/view-source_https___www.ulmart.ru.html')
    menu = _.find(mainMenuClass, cookies={'sity': '281'})
    if len(menu) < 1:
        print('err')
        exit(1)
    for i in menu:
        print(i.get('href'))
        # if 'href' in i.keys() and i.get('href').find('/catalog/') == 0:
        #     print(i.get('href'))
