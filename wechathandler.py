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
from littlewechat import logger
from wechat_sdk.messages import TextMessage, ImageMessage, EventMessage
import json

def text_handler(content):
    resp = content
    if 'survey' == content:
        q = {}
        q['title'] = 'questionnaire'
        q['description'] = 'This is a questionnaire sample'
        q['url'] = 'http://inaiping.wang'
        logger.debug(json.dump([q]))
        return  wechat.response_news(json.dump([q]))
    return wechat.response_text(resp)

def handler(body, signature, timestamp, nonce):
    logger.debug("request body: %s", body)
    wechat.parse_data(body, signature, timestamp, nonce)
    message = wechat.get_message()

    response = None
    if isinstance(message, TextMessage):
        logger.debug("handling: %s", message.content)
        content = message.content
        response = text_handler(content)
    elif isinstance(message, ImageMessage):
        logger.debug("handling: mediaId: %s, picurl: %s", message.media_id, message.picurl)
        response = wechat.response_image(message.media_id)
    elif isinstance(message, EventMessage):
        key = None
        if wechat.message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            key = wechat.message.key                        # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
            ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
        elif wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
            pass
        elif wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
            key = wechat.message.key                        # 对应于 XML 中的 EventKey
            ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket
        elif wechat.message.type == 'location':  # 上报地理位置事件
            latitude = wechat.message.latitude              # 对应于 XML 中的 Latitude
            longitude = wechat.message.longitude            # 对应于 XML 中的 Longitude
            precision = wechat.message.precision            # 对应于 XML 中的 Precision
        elif wechat.message.type == 'click':  # 自定义菜单点击事件
            key = wechat.message.key                        # 对应于 XML 中的 EventKey
        elif wechat.message.type == 'view':  # 自定义菜单跳转链接事件
            key = wechat.message.key                        # 对应于 XML 中的 EventKey
        elif wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
            status = wechat.message.status                  # 对应于 XML 中的 Status
        elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                                     'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
            key = wechat.message.key                       # 对应于 XML 中的 EventKey
        logger.debug("eventmessage: %s", key)

    else:
        response = wechat.response_text('unsupported yet :-(')

    return response