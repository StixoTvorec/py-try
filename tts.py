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
_args.add_argument('-a', help='Save all to files', action='store_const', required=False, const=True, default=False)
_args.add_argument('--temp-file', help='Temp file', type=str, required=False, default='/tmp/tts.mp3')
_args.add_argument('-f', help='File', type=str, required=False, default='tts.txt')
args = _args.parse_args()

"""
vk functions:

# getAllUserPhotos
var user = Args.user;
var maxCount = 1000;
// принимает строку вида: 1:40,2:45,4:455
// где первый параметр - альбом, а второй - количество фоток в нем
// преобразуется в: [['1', '40'], ['2', '45'], ['4', '455']]
var albums = Args.albums;
if(!albums) {
    return null;
}
albums = albums.split(",")@.split(":");
var i = 0;
var photos = [];
var api;
while(i < albums.length) {
    var offset = 0;
    //todo %1000
    while(offset < albums[i][1]) {
        api = API.photos.get({
            owner_id: user,
            album_id: albums[i][0],
            offset: offset,
            count: maxCount
        });
        var _photos = api.items@.id;
        photos.push(_photos);
        offset = offset + maxCount;
    }
    i=i+1;
}
return photos;
# getAllUserPhotos

# photosMove
var photos = Args.photos.split(",");
var to = Args.to;
var owner = Args.owner_id;
if(!photos || !to) {
    return null;
}
var i = 0;
while(i < photos.length) {
    API.photos.move({
        owner_id: owner,
        target_album_id: to,
        photo_id: photos[i],
    });
    i = i + 1;
}
return i;
# photosMove

"""


class TTS(gTTS):
    MAX_CHARS = 199
    TIMEOUT = 10

    def write_to_fp(self, fp):
        """ Do the Web request and save to a file-like object """
        for idx, part in enumerate(self.text_parts):
            payload = {'ie': 'UTF-8',
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
            while True:
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
                    break
                except Exception as e:
                    if self.debug:
                        print('Retry')
                    continue

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
    pygame.mixer.pre_init(30000, -16, 2, 2048)
    pygame.init()

    n = 1
    with open(file, 'r') as text:
        for i, t in enumerate(text):
            _t = t.strip()
            if len(_t) < 2 or _t == '<br>':
                continue
            n += 1
            if n <= args.s:
                continue

            _temp_file = '{}-{}.mp3'.format(args.temp_file, i)
            if args.a:
                _temp_file = args.temp_file

                while pygame.mixer.music.get_busy():
                    time.sleep(1)

            tts = TTS(text=t, lang='ru', slow=False, debug=False)
            tts.save(_temp_file)

            print('playing {}'.format(n - 1))

            if args.a:
                try:
                    pygame.mixer.music.load(_temp_file)
                    pygame.mixer.music.play()
                except pygame.error:
                    print('err')

    while pygame.mixer.music.get_busy():
        time.sleep(1)


if __name__ == '__main__':
    try:
        play(args.f)
    except KeyboardInterrupt:
        exit(1)
