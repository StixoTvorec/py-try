#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path, makedirs
from argparse import ArgumentParser


_args = ArgumentParser()
_args.add_argument('-d', '--destination', help='Destination', type=int, required=False, default=0)
_args.add_argument('-t', '--target', help='Target dir', type=str, required=False, default='/tmp/tts.mp3')
_args.add_argument('-f', help='File', type=str, required=False, default='tts.txt')
args = _args.parse_args()


class Parser:

    destination = ''

    def __init__(self):
        self.destination = args.destination
        if not len(args.destination):
            self.destination = path.dirname(path.realpath(__file__))
        if not len(args):
            pass

    def _prepareDir(self, url):
        dirName = path.basename(url)
        targetDir = path.join(self.destination, dirName)
        path.isdir(targetDir) or makedirs(targetDir)
        return dirName, targetDir

    def packages(self, url):
        _dirs_ = self._prepareDir(url)





if __name__ == '__main__':
    pass
