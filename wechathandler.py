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
import json
import requests

from littlewechat import wechat
from littlewechat import logger
from wechat_sdk.messages import TextMessage, ImageMessage, EventMessage
from leancloud import Query
from weuser.weusers import WeUsers
from question import questionnaire
import datetime

def get_question_url(appid, qid):
    qurl = 'http://inaiping.wang/questions/' + str(qid)
    authorize_url = str.format('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect' %
                               (appid, qurl))
    logger.debug(authorize_url)
    return authorize_url

def get_question_info_url(appid, qid):
    qurl = 'http://inaiping.wang/questions/' + str(qid)
    authorize_url = str.format('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' %
                               (appid, qurl))
    logger.debug(authorize_url)
    return authorize_url

def generate_question(userinfo, title, description):
    question = questionnaire.Questionnaires()
    question.creator = userinfo.get('nickname')
    question.answer_count = 0
    question.category = "default"
    question.expired_at = datetime.datetime.now() + datetime.timedelta(hours=24)
    question.modify_answer = True
    question.show_details = True
    question.description = description
    question.title = title
    question.status = "open"
    question.save()
    return question


def text_handler(content, userid):
    resp = content
    if 'survey' == content:
        userinfo = wechat.get_user_info(userid)
        question = generate_question(userinfo, "周末约吗?", "周五晚上去打麻将吗?")
        q = {}
        q['title'] = '周末约吗?'
        q['description'] = "周五晚上去打麻将吗?"
        q['url'] = get_question_url(wechat.conf.appid, question.id)
        return  wechat.response_news([q])
    elif 'test2' == content:
        userinfo = wechat.get_user_info(userid)
        question = generate_question(userinfo, "周末约吗?", "周六晚上去打麻将吗?")
        q = {}
        q['title'] = '周末约吗?'
        q['description'] = "周六晚上去打麻将吗?"
        q['url'] = get_question_info_url(wechat.conf.appid, question.id)
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
                retrieve_weuser(source)
                response = wechat.response_text('Welcome to playground :-)')
        elif wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
            logger.debug('%s unsubscribe', source)
        elif wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
            key = wechat.message.key                        # 对应于 XML 中的 EventKey
            ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket
        elif wechat.message.type == 'location':  # 上报地理位置事件
            latitude = wechat.message.latitude              # 对应于 XML 中的 Latitude
            longitude = wechat.message.longitude            # 对应于 XML 中的 Longitude
            precision = wechat.message.precision            # 对应于 XML 中的 Precision
            response = wechat.response_text('Welcome to playground :-)')
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
    if not response:
        response = wechat.response_text('unsupported yet :-(')
    return response

def get_user_info(openid, access_token):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + access_token + '&openid=' + openid + '&lang=zh_CN'
    resp = requests.get(url)
    logger.debug(type(resp.text))
    authorize_result = json.loads(resp.text)
    logger.debug("get user info: %s", str(authorize_result))

def retrieve_weuser(openid):
    userinfo = wechat.get_user_info(openid)
    logger.debug(userinfo)
    query = Query(WeUsers)
    query.equal_to('openid', userinfo.get('openid'))
    wuser = query.find()
    logger.debug(wuser)
    if len(wuser) <= 0:
        wuser = WeUsers()
        wuser.openid = userinfo.get('openid')
        wuser.city = userinfo.get('city')
        wuser.nickname = userinfo.get('nickname')
        wuser.headimgurl = userinfo.get('headimgurl')
        wuser.province = userinfo.get('province')
        wuser.sex = userinfo.get('sex')
        wuser.unionid = userinfo.get('unionid')
        wuser.save()
        return wuser
    else:
        wuser = wuser[0]
        logger.debug('%s had already been subscribed', userinfo.get('nickname'))
        return wuser
