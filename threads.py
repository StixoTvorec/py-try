#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from class
from threading import Thread
import time
import os
from argparse import ArgumentParser
import sys


class Helper:
    def __init__(self):
        super().__init__()
        self.file = ''

    def read(self):
        """
        :return: mixed
        """

        if self.file == '':
            sys.exit(1)

        if not os.path.isfile(self.file):
            return ''

        with open(self.file, mode='r', encoding='utf-8') as f:
            return f.read()

    def write(self, data: str):
        """
        :param data
        :return: mixed
        """

        if self.file == '':
            sys.exit(1)

        if not os.path.isfile(self.file):
            return ''

        with open(self.file, mode='w', encoding='utf-8') as f:
            return f.write(data)

    def args(self):
        """
        Arguments parser helper
        :return: ArgumentParser
        """
        parser = ArgumentParser()

        parser.add_argument('-d', '--daemon', action='store_const', const=True, default=False, help='Run as daemon mode')
        parser.add_argument('-f', '--file', default='debug_output.log', help='Output file (daemon mode)')
        parser.add_argument('-n', '--threads', type=int, help='Count threads', default=20)

        parser = parser.parse_args()
        self.file = parser.file

        return parser


unStick = False
helper = Helper()
args = helper.args()


class TestClass(Thread):

    def __init__(self, string, un_stick: bool = False):
        Thread.__init__(self)
        self.string = string
        self.unStick = un_stick

    def run(self):
        """
        :return: None
        """
        if (self.string % 10) < 5:
            time.sleep(self.string/10)

        if self.unStick:
            helper.write(str(time.time()) + str(self.string) + '\n')
        else:
            print('\033[92mchild \033[0m' + str(self.string))


if __name__ == '__main__':

    if args.daemon:
        try:
            pid = os.fork()
            if pid:
                unStick = True
                print('Process forked with PID ' + str(pid))
                sys.exit(0)
        except Exception as e:
            print(e.args)
            exit(1)

    i = 0
    while i < args.threads:
        i += 1
        if args.daemon:
            helper.write(str(time.time()) + str(i) + '\n')
        else:
            print('\033[94mmain \033[0m' + str(i))

        test = TestClass(i, args.daemon)
        test.start()
