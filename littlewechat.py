# -*- coding: UTF-8 -*-
from flask import Flask, request, redirect, render_template, make_response
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
import wechathandler
import leancloud
import requests
from leancloud import Query
import json
import sys
from question.questionnaire import Questionnaires
from question.answer import Answers

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
from logging import handlers
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wechat')
loghandler = logging.StreamHandler()
loghandler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]'))
logger.addHandler(loghandler)
logger.debug(sys.getdefaultencoding())

app = Flask(__name__)
# init leancloud sdk
leancloud.init('gbGQrJza12wVi05jnSFejYiB-gzGzoHsz', 'V0obuYelEbFNm2c8Sp81HOrn')

conf = WechatConf(
    token='littlewechat',
    appid='wx6212752719ca7a9f',
    appsecret='c1f99fa01795fca43fd00079d713d013',
    encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='qmsBYxixEpNw8w7ZyangzbytJK0A5pWOcF5FgUDjC9U'  # 如果传入此值则必须保证同时传入 token, appid
)

wechat = WechatBasic(conf=conf)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/little', methods=["GET", "POST"])
def little_wechat():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    msg_signature = request.args.get('msg_signature')
    logger.debug("request with signature:%s timestamp:%s nonce:%s echostr:%s msg_signature:%s",
                 signature, timestamp, nonce, echostr, msg_signature)
    if wechat.check_signature(signature, timestamp, nonce):
        if echostr:
            return echostr
        return wechathandler.handler(request.data, msg_signature, timestamp, nonce)
    else:
        return "validate failed"

@app.route('/questions/<qid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def questions(qid):
    logger.debug(request.args)
    uid = request.cookies.get('uid')
    logger.debug('user id in cookie: ' + str(uid))
    wuser = None
    if uid:
        from weuser.weusers import WeUsers
        query = Query(WeUsers)
        query.get(uid)
        wuser = query.find()
    if not wuser:
        wuser = validate_weuser()
    if wuser:
        logger.debug("questionnaire with id: %s and %s" % (qid, wuser.nickname))
        query = Query(Questionnaires)
        question = query.get(qid)
        if question:
            title = question.title
            logger.debug(question)
            resp = make_response(render_template('question.html',
                                   title=question.title, name=question.creator, qid=qid, question_heading=question.title,
                                   question_content=question.description, status=question.status, expired_at=question.expired_at,
                                   show_details=question.show_details))
            # setcookie for user id
            resp.set_cookie('uid', wuser.id)
            return resp
        else:
            return render_template('question.html', title="Unavailable questionnaire", name="No name", qid=qid)

    else:
        return render_template('question.html', title="Test", name="No name", qid=qid)
        # redirect_url = wechathandler.get_question_info_url(wechat.conf.appid, qid)
        # logger.debug("questionnaire with id: %s and no available user" % qid)
        # return redirect(redirect_url)

@app.route('/answers', methods=["POST"])
def answers():
    uid = request.cookies.get('uid')
    logger.debug('user id in cookie: ' + str(uid))
    logger.debug("request data: %s form: %s", request.data, request.form)
    # answer = Answers()
    # answer.qid = ""
    # answer.userid = ""
    # answer.value = ""
    # answer.save()
    # return json.loads(answer)
    return request.data


def validate_weuser():
    code = request.args.get('code')
    if code:
        url = str.format(
            'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'
            % (wechat.conf.appid, wechat.conf.appsecret, str(code)))
    else:
        return None
    resp = requests.get(url)
    logger.debug(type(resp.text))
    authorize_result = json.loads(resp.text)
    openid = authorize_result.get('openid')
    # userinfo = wechat.get_user_info(openid)
    if openid:
        logger.debug("wechat openId: " + openid)
    else:
        logger.debug("wechat openid invalidated!!!")
    from weuser.weusers import WeUsers
    query = Query(WeUsers)
    query.equal_to('openid', openid)
    wuser = query.find()
    if len(wuser) > 0:
        wuser = wuser[0]
    else:
        logger.debug('try to retrieve userinfo')
        wuser = wechathandler.retrieve_weuser(openid)
    return wuser


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
