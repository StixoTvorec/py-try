#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser as p


sqlConfig = {
  'user': 'test',
  'password': 'test',
  'host': '127.0.0.1',
  'database': 'test',
  'raise_on_warnings': True,
}
mainMenuClass = '.b-dropdown__body__h > .b-dropdown__body__h > ul'


def menu_links(element, only_up_level:bool = False):
    list = []
    if only_up_level:
        links = element.cssselect('a[href]')
    else:
        links = element.cssselect('a[href]')
    for i in links:
        e = i.get('href')
        if e.find('/catalog') == 0 and e.find('c') == 1:
            # print(e)
            list.append(i)
    return list


if __name__ == '__main__':
    # _ = p.get_parser('https://ulmart.ru/')
    _ = p.get_parser('/tmp/view-source_https___www.ulmart.ru.html')
    menu = _.find(mainMenuClass)
    if len(menu) < 1:
        exit(1)
    menu = menu[0]
    menu_links(menu)
    # print()
