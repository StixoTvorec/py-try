#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from lxml import html
# from lxml import etree
# from pandas import DataFrame
# from pprint import pprint
# # from StringIO import StringIO
# from urllib.request import urlopen
#
# domain = 'http://www.ulmart.ru'
#
# file = urlopen(domain + '/goods/4000284')
# # source = file.read()
# # file.close()
#
# source = '<html><head></head><body><div class=\'asd\'>' \
#          '<div class="panel-group_theme_normal">' \
#          '<div class="asda1ed1241">' \
#          '<div class="">ccczzz</div>' \
#          '<div class="b-price__num">123312312312312</div>' \
#          '</div>' \
#          '</div></body></html>'
#
# page = html.fromstring(source)
# source = html.tostring(page)
#
# pprint(etree.parse(file))
# # pprint(etree.parse(StringIO(source)))
#
# exit(1)
#
# e = page.getroot(). \
#     cssselect('.panel-group_theme_normal .b-price__num').\
#     pop()
#
#
# pprint(e)
