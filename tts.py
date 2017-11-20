#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gtts import gTTS
import pygame
import time
from os import remove
from argparse import ArgumentParser

import re, requests, warnings
from six.moves import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning

_args = ArgumentParser()
_args.add_argument('-s', help='Skip lines', type=int, required=False, default=0)
_args.add_argument('--temp-file', help='Temp file', type=str, required=False, default='/tmp/tts.mp3')
_args.add_argument('-f', help='File', type=str, required=False, default='tts.txt')
args = _args.parse_args()


class TTS(gTTS):
    MAX_CHARS = 200
    TIMEOUT = 2

    def write_to_fp(self, fp):
        """ Do the Web request and save to a file-like object """
        for idx, part in enumerate(self.text_parts):
            payload = { 'ie': 'UTF-8',
                        'q': part,
                        'tl': self.lang,
                        'ttsspeed': self.speed,
                        'total': len(self.text_parts),
                        'idx': idx,
                        'client': 'tw-ob',
                        'textlen': self._len(part),
                        'tk': self.token.calculate_token(part)}
            headers = {
                "Referer" : "http://translate.google.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
            }
            if self.debug: print(payload)
            try:
                # Disable requests' ssl verify to accomodate certain proxies and firewalls
                # Filter out urllib3's insecure warnings. We can live without ssl verify here
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                    while True:
                        try:
                            r = requests.get(self.GOOGLE_TTS_URL,
                                             params=payload,
                                             headers=headers,
                                             proxies=urllib.request.getproxies(),
                                             timeout=self.TIMEOUT,
                                             verify=False)
                            break
                        except requests.exceptions.ReadTimeout:
                            break
                if self.debug:
                    print("Headers: {}".format(r.request.headers))
                    print("Request url: {}".format(r.request.url))
                    print("Response: {}, Redirects: {}".format(r.status_code, r.history))
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024):
                    fp.write(chunk)
            except Exception as e:
                raise

    def _tokenize(self, text, max_size):
        """ Tokenizer on basic punctuation """

        punc = "¡!()[]¿?.،;:—。、：？！\n"
        punc_list = [re.escape(c) for c in punc]
        pattern = '|'.join(punc_list)
        parts = re.split(pattern, text)

        min_parts = []
        for p in parts:
            min_parts += self._minimize(p, " ", max_size)
        return min_parts


def play(file):
    pygame.mixer.pre_init(28000, 16, 2, 2048)
    pygame.init()

    n = 1
    with open(file, 'r') as text:
        for t in text:
            _t = t.strip()
            if len(_t) < 2 or _t == '<br>':
                continue
            n += 1
            if n <= args.s:
                continue

            while pygame.mixer.music.get_busy():
                time.sleep(1)

            tts = TTS(text=t, lang='ru', slow=False, debug=True)
            tts.save(args.temp_file)

            print('playing {}'.format(n))

            try:
                pygame.mixer.music.load(args.temp_file)
                pygame.mixer.music.play()
            except pygame.error:
                print('err')

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    remove(args.temp_file)


if __name__ == '__main__':
    try:
        play(args.f)
    except KeyboardInterrupt:
        remove(args.temp_file)
        pass
