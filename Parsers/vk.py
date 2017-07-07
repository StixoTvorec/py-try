#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser as p
from requests import Session
import json
from os import (
    listdir,
    getcwd
)
from os.path import (
    isfile,
    isdir,
    join,
    splitext
)

apiVersion = '5.65'
oauthUrl = 'https://oauth.vk.com/authorize?client_id={}&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v={}&scope={}'
apiUrl = 'https://api.vk.com/method/{}?v={}&access_token={}&{}'

access = (
    #notify
    1
    #friends
    + 2
    #protos
    + 4
    #audio
    + 8
    #video
    + 16
    #pages
    + 128
    #status
    + 1024
    #notes
    # -- messages
    # + 4096
    #offline
    + 65536
    #docs
    + 131072
    #groups
    + 262144
)

vk_config = p.get_content('./vk_key.json')
if len(vk_config) < 1:
    print('Error. No config file!')
    exit(0)

vk_config = json.loads(vk_config.decode('utf-8'))

if not (
        isinstance(vk_config, object)
        and 'secret_key' in vk_config
        and 'service_key' in vk_config
        and 'app_id' in vk_config
    ):
    print('error parse config')
    exit(1)

secretKey = vk_config['secret_key']
serviceKey = vk_config['service_key']
appId = vk_config['app_id']

user = vk_config['user_id'] #int(input("Input you user id: \n"))

if user < 0:
    print('Error!')
    exit(1)

code = p.get_db().query('SELECT id, token FROM vk WHERE user = %s LIMIT 1', (user,)).fetch(1)

if not isinstance(code, tuple):
    db = p.get_db().execute('INSERT INTO vk (user, token) VALUES (%s, "")', (user,))
    id = db.insert_id()
    db.close()
    code = oauthUrl.format(appId, apiVersion, access,)
    code = input("Please, go to {} and paste code here\n".format(code,))
    p.get_db().execute('UPDATE vk SET token = %s WHERE user = %s', (code, user,)).close()
    token = code
else:
    id = code[0]
    token = code[1]


def request(method: str, more: str = ""):
    url = apiUrl.format(method, apiVersion, token, more)
    return p.Http().get(url)

print("User: {}\nToken: {}\nUserId: {}\n".format(id, token, user,))

class User:

    albums = dict()

    def _upload(self, url: str, files, album_id: int, user_id: int):
        # print(url)
        # print(files)
        # print(album_id)
        # print(user_id)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        # url = 'http://httpbin.org/post';
        p = Session()
        q = p.request('POST', url, files=files, headers=headers)

        if q.status_code == 200:
            j = q.json()
            # print('J:')
            # print(j)
            # print('')
            server = str(j['server'])
            aid = str(j['aid'])
            hash = str(j['hash'])
            photos_list = str(bytearray(j['photos_list'], 'utf-8').decode('unicode_escape'))
            params = 'server=' + server + '&album_id=' + aid + '&hash=' + hash + '&photos_list=' + photos_list
            request('photos.save', params)

    def photosGetAlbums(self):
        data = request('photos.getAlbums', '')
        self.albums = json.loads(data)
        return data

    def photos(self):
        if not (isinstance(self.albums, object) and 'response' in self.albums and 'items' in self.albums.get('response')):
            return False
        url = ','.join(map(lambda a: str(a.get('id'))+':6000', self.albums.get('response').get('items')))
        print(url)
        exit()
        data = request('execute.getAllUserPhotos', '')
        return data

    def uploadPhotos(self):
        album = vk_config['album']
        data = request('photos.getUploadServer', 'album_id=' + str(album))
        data = json.loads(data)
        # print(data)
        if not (isinstance(data, object) and 'response' in data and 'upload_url' in data.get('response')):
            return False
        data = data.get('response')
        url = data.get('upload_url')
        album = data.get('album_id')
        user_id = data.get('user_id')
        path = join(getcwd(), 'vk_upload_files')
        if not isdir(path):
            return False
        _files = [f for f in listdir(path) if isfile(join(path, f))]
        # print(_files)
        files = []
        for f in _files:
            _, ext = splitext(f)
            if ext in ['.jpeg', '.jpg', '.png']:
                files.append(f)
        i = 0
        _list = []
        for f in files:
            if i == 5:
                self._upload(url, _list, album, user_id)
                i = 0
                _list = []
            index = 'file' + str(i+1)
            _list.append((index, open(join(path, f), 'rb')))
            i += 1
        if i != 5:
            self._upload(url, _list, album, user_id)

newUser = User()
# newUser.photosGetAlbums()
# newUser.photos()
newUser.uploadPhotos()
exit()

while True:
    method = input("Method: \n")
    # moreParams = input("More params: \n")
    if method == -1:
        break
    m = getattr(newUser, method)
    print(json.dumps(json.loads(m()), sort_keys=True, indent=4))
