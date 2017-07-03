#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser as p
import json

apiVersion = '5.65'
oauthUrl = 'https://oauth.vk.com/authorize?client_id={}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52&scope={}'
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

user = int(input("Input you user id: \n"))

if user < 0:
    print('Error!')
    exit(1)

code = p.get_db().query('SELECT id, token FROM vk WHERE user = %s LIMIT 1', (user,)).fetch(1)

if not isinstance(code, tuple):
    db = p.get_db().execute('INSERT INTO vk (user, token) VALUES (%s, "")', (user,))
    id = db.insert_id()
    db.close()
    code = oauthUrl.format(appId, access,)
    code = input("Please, go to {} and paste code here\n".format(code,))
    p.get_db().execute('UPDATE vk SET token = %s WHERE user = %s', (code, user,)).close()
    token = code
else:
    id = code[0]
    token = code[1]


def request(method: str, more: str = ""):
    url = apiUrl.format(method, apiVersion, token, more)
    print(url)
    return p.Http().get(url)

print("User: {}\nToken: {}\n".format(id, token,))

while True:
    method = input("Method: \n")
    moreParams = input("More params: \n")
    if method == -1:
        break
    data = request(method, moreParams)
    print(json.loads(data))
