#!/usr/bin/python3
# -*- coding: utf-8 -*-


import random, os

filename = os.path.realpath(__file__) # full path
dirname = os.path.dirname(filename) # directory
filename = os.path.basename(filename) # filename

# filename without extension
split_filename = filename.split('.')[0]
# split_filename = split_filename[split_filename.__len__() - 1]

filename = str(dirname) + '/' + str(split_filename) + '.txt'


def write(name: str, data: str, new_file: bool=False):
    """
    :param name: String file name
    :param data: String
    :param new_file: Boolean
    :return: None
    """
    mode = 'a'
    if new_file or not os.path.isfile(name) or (os.path.getsize(name) > 1024*1024):
        mode = 'w'
    with open(name, mode, encoding='utf-8') as f:
        f.write(str(data) + "\n")


def read(name: str):
    """
    :param name: string file name
    :return: mixed
    """
    if not os.path.isfile(name):
        return ''
    with open(name, 'r', encoding='utf-8') as f:
        return f.read()


def write_random(name: str, length: int=10):
    """
    :param name: string file name
    :param length: int count lines for write
    :return:  None
    """
    i = 0
    while i < length:
        write(name, str(random.random()))
        i += 1


write_random(filename)

print(read(filename))

print(str(os.path.getsize(filename)) + ' b.')