#!/usr/bin/python3
# -*- coding: utf-8 -*-


def my_func(n):
    return {'func': (lambda z: n+z), 'pow': n*n}

Sum = my_func(100)
print(Sum['func'](110))
print(Sum['pow'])
