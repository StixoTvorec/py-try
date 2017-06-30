#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser as p
import json

vk_config = p.get_content('./vk_key.json')
if len(vk_config) < 1:
    print('Error. No config file!')
    exit(0)

vk_config = json.loads(vk_config)

print(vk_config)
