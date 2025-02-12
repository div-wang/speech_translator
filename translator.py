'''
Author: Div gh110827@gmail.com
Date: 2025-02-11 21:47:59
LastEditors: Div gh110827@gmail.com
LastEditTime: 2025-02-11 21:49:01
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
import translators as ts

class Translator:
    def __init__(self):
        pass

    def translate(self, text, from_lang='zh', to_lang='en'):
        """翻译文本"""
        try:
            return ts.bing(text, from_language=from_lang, to_language=to_lang)
        except Exception as e:
            print(f"翻译错误: {e}")
            return None 