#!/usr/bin/python3
# -*- coding: utf-8 -*-

import iparser as p
from requests import Session
import json
from time import sleep
from os import (
    listdir,
    getcwd,
    mkdir,
    rename,
)
from os.path import (
    isfile,
    isdir,
    join,
    splitext,
    basename,
)

configFile = './vk_key.json'
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

vk_config = p.get_content(configFile)
if len(vk_config) < 1:
    print('Error. No config file!')
    exit(0)

vk_config = json.loads(vk_config.decode('utf-8'))

if not (
        isinstance(vk_config, object)
    ):
    print('error parse config')
    exit(1)

secretKey = vk_config['secret_key']
serviceKey = vk_config['service_key']
appId = vk_config['app_id']
token = vk_config['token']
uploadAlbumId = vk_config['album']

user = vk_config['user_id'] #int(input("Input you user id: \n"))

if int(user) < 0:
    print('Error!')
    exit(1)

if token == '':
    code = oauthUrl.format(appId, apiVersion, access,)
    token = input("Please, go to {} and paste code here\n".format(code,))
    if token == '':
        print('token is empty!')
        exit(1)
    data = {
      "app_id": appId,
      "secret_key": secretKey,
      "service_key": serviceKey,
      "user_id": user,
      "album": uploadAlbumId,
      "token": token
    }
    _ = open(configFile, 'wb')
    _.write(json.dumps(data))
    _.close()


def request(method: str, more: str = ""):
    url = apiUrl.format(method, apiVersion, token, more)
    return p.Http().get(url)

print("User: {}\nToken: {}\nUserId: {}\n".format(id, token, user,))

class User:

    albums = dict()

    def _upload(self, url: str, files):

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
            server = str(j['server'])
            aid = str(j['aid'])
            hash = str(j['hash'])
            photos_list = str(bytearray(j['photos_list'], 'utf-8').decode('unicode_escape'))
            params = 'server=' + server + '&album_id=' + aid + '&hash=' + hash + '&photos_list=' + photos_list
            request('photos.save', params)

    def deleteAllPhotos(self, album):
        return False # standalone access need
        album = str(album)
        list = request('photos.get', 'album_id=' + album)
        list = json.loads(list).get('response').get('items')
        print(' start deleted ' + str(len(list)) + ' photos')
        sleep(1)
        for f in list:
            sleep(.2)
            id = f.get('id')
            data = 'owner_id=' + str(user) + '&photo_id=' + str(id)
            # print('deleting ' + str(id))
            # print(data)
            _ = request('photos.delete', data)
            print(_)

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
        if uploadAlbumId == '':
            print('upload_album_id is empty')
            return False

        # if need delete old uploaded photos
        self.deleteAllPhotos(uploadAlbumId)

        data = request('photos.getUploadServer', 'album_id=' + str(uploadAlbumId))
        data = json.loads(data)
        # print(data)
        if not (isinstance(data, object) and 'response' in data and 'upload_url' in data.get('response')):
            return False
        data = data.get('response')
        url = data.get('upload_url')
        path = join(getcwd(), 'vk_upload_files')
        if not isdir(path):
            return False
        uploadedPath = join(path, 'uploaded')
        if not isdir(uploadedPath):
            mkdir(uploadedPath, 0o777)
        _files = [f for f in listdir(path) if isfile(join(path, f))]
        files = []
        for f in _files:
            _, ext = splitext(f)
            if ext in ['.jpeg', '.jpg', '.png']:
                files.append(f)
        i = 0
        n = 0
        countFiles = len(files)
        _list = []
        _move = []
        if countFiles > 0:
            print('uploading start')
            for f in files:
                if i == 5:
                    n += 5
                    self._upload(url, _list)
                    sleep(1) # на всякий случай
                    for _ in _move:
                        _[1].close()
                        rename(_[0], join(uploadedPath, basename(_[0])))
                    print('uploaded ' + str(n) + '/' + str(countFiles))
                    i = 0
                    _list = []
                    _move = []
                index = 'file' + str(i+1)
                fileName = join(path, f)
                d = open(fileName, 'rb')
                _list.append((index, ('image.png', d,)))
                _move.append((fileName, d,))
                i += 1
            if i != 5:
                self._upload(url, _list)
                for _ in _move:
                    _[1].close()
                    rename(_[0], join(uploadedPath, basename(_[0])))
            print('uploaded finish')

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
