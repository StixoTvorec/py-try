#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gtts import gTTS
import pygame
import time
from os import remove
from argparse import ArgumentParser

_args = ArgumentParser()
_args.add_argument('-s', help='Skip lines', type=int, required=False, default=0)
_args.add_argument('--temp-file', help='Temp file', type=str, required=False, default='/tmp/tts.mp3')
_args.add_argument('-f', help='File', type=str, required=False, default='tts.txt')
args = _args.parse_args()


def play(file):
    pygame.mixer.pre_init(28000, 16, 2, 2048)
    pygame.init()

    n = 0
    with open(file, 'r') as text:
        for t in text:
            _t = t.strip()
            if len(_t) < 2 or _t == '<br>':
                continue
            n += 1
            if n < args.s:
                continue

            while pygame.mixer.music.get_busy():
                time.sleep(.5)

            tts = gTTS(text=t, lang='ru', slow=False)
            tts.save(args.temp_file)

            print('playing {}'.format(n))

            try:
                pygame.mixer.music.load(args.temp_file)
                pygame.mixer.music.play()
            except pygame.error:
                print('err')

    remove(args.temp_file)


if __name__ == '__main__':
    try:
        play(args.f)
    except KeyboardInterrupt:
        remove(args.temp_file)
        pass
