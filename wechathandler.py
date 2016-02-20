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

def get_question_url(appid, qid):
    qurl = 'http://inaiping.wang/questions/' + str(qid)
    authorize_url = str.format('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' %
                               (appid, qurl))
    logger.debug(authorize_url)
    return authorize_url
def text_handler(content, userid):
    resp = content
    if 'survey' == content:
        userinfo = wechat.get_user_info(userid)
        q = {}
        q['title'] = 'questionnaire'
        q['description'] = userinfo
        q['url'] = get_question_url(wechat.conf.appid, 1)
        return  wechat.response_news([q])
    elif 'test' == content:
        articles = [{
            'title': u'第一条新闻标题',
            'description': u'第一条新闻描述，这条新闻没有预览图',
            'url': u'http://www.baidu.com/',
        }, {
            'title': u'第二条新闻标题, 这条新闻无描述',
            'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
            'url': u'http://www.github.com/',
        }, {
            'title': u'第三条新闻标题',
            'description': u'第三条新闻描述',
            'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
            'url': u'http://www.v2ex.com/',
        }]
        return wechat.response_news(articles)
    return wechat.response_text(resp)

def handler(body, signature, timestamp, nonce):
    logger.debug("request body: %s", body)
    wechat.parse_data(body, signature, timestamp, nonce)
    message = wechat.get_message()

    id = wechat.message.id          # 对应于 XML 中的 MsgId
    target = wechat.message.target  # 对应于 XML 中的 ToUserName
    source = wechat.message.source  # 对应于 XML 中的 FromUserName
    time = wechat.message.time      # 对应于 XML 中的 CreateTime
    type = wechat.message.type      # 对应于 XML 中的 MsgType
    raw = wechat.message.raw        # 原始 XML 文本，方便进行其他分析

    response = None
    if isinstance(message, TextMessage):
        logger.debug("handling: %s", message.content)
        content = message.content
        response = text_handler(content, source)
    elif isinstance(message, ImageMessage):
        logger.debug("handling: mediaId: %s, picurl: %s", message.media_id, message.picurl)
        response = wechat.response_image(message.media_id)
    elif isinstance(message, EventMessage):
        logger.debug("handling eventMessage: %s", message.type)
        key = None
        if wechat.message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            key = wechat.message.key                        # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
            ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
            if source:
                userinfo = wechat.get_user_info(source)
                logger.debug("typeof(%s) is %s", userinfo, type(userinfo))
                from weuser.weusers import WeUsers
                wuser = WeUsers()
                wuser.openid = userinfo.get('openid')
                wuser.city = userinfo.get('city')
                wuser.nickname = userinfo.get('nickname')
                wuser.headimgurl = userinfo.get('headimgurl')
                wuser.province = userinfo.get('province')
                wuser.sex = userinfo.get('sex')
                wuser.unionid = userinfo.get('unionid')
                wuser.save()
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