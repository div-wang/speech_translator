'''
Author: Div gh110827@gmail.com
Date: 2025-02-11 21:47:59
LastEditors: Div gh110827@gmail.com
LastEditTime: 2025-02-11 21:49:01
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
import requests
import json
import hashlib
import random
import time

class BaiduTranslator:
    def __init__(self, app_id, secret_key):
        self.app_id = app_id
        self.secret_key = secret_key
        self.url = "http://api.fanyi.baidu.com/api/trans/vip/translate"

    def translate(self, text, from_lang='auto', to_lang='jp'):
        salt = str(random.randint(32768, 65536))
        sign = self.app_id + text + salt + self.secret_key
        sign = hashlib.md5(sign.encode()).hexdigest()

        params = {
            'appid': self.app_id,
            'q': text,
            'from': from_lang,
            'to': to_lang,
            'salt': salt,
            'sign': sign
        }

        try:
            response = requests.get(self.url, params=params)
            result = response.json()
            return result['trans_result'][0]['dst']
        except Exception as e:
            print(f"翻译错误: {e}")
            return None 