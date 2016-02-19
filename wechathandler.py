# -*- coding: utf-8 -*-

"""
@version: ??
@author: caiiiyua
@license: Apache Licence 
@contact: caiiiyua@gmail.com
@site: 
@software: PyCharm
@file: wechathandler.py
@time: 16/2/17 下午11:10
"""

from littlewechat import wechat

def text_handler():
    pass

def handler(body, signature, timestamp, nonce):
    wechat.parse_data(body, signature, timestamp, nonce)
    message = wechat.get_message()

    response = None
    if message.type == 'text':
        response = wechat.response_text(message.content)
    elif message.type == 'image':
        response = wechat.response_text('picture')
    elif message.type == 'audio':
        response = wechat.response_text('audio')
    else:
        response = wechat.response_text('unknown')

    return response