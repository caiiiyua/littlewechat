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
from weuser.weusers import WeUsers

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
from logging import handlers
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wechat')
loghandler = logging.handlers.TimedRotatingFileHandler('logs/server.log', 'd', 1, 5)
loghandler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]'))
logger.addHandler(loghandler)
# logger.debug(sys.getdefaultencoding())

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
    # uid = request.args.get("uid")
    logger.debug('user id in cookie: ' + str(uid))
    wuser = None
    # if uid:
    #     try:
    #         query = Query(WeUsers)
    #         wuser = query.get(uid)
    #     except leancloud.LeanCloudError:
    #         logger.warning("WeUser not found via uid %s", uid)
    if not wuser:
        wuser = validate_weuser()
    if wuser:
        logger.debug("questionnaire with id: %s and %s" % (qid, wuser.nickname))
        query = Query(Questionnaires)
        question = query.get(qid)
        if question:
            title = question.title
            logger.debug(question)
            answer_query = Query(Answers)
            answer_query.equal_to('qid', qid)
            answers = answer_query.find()
            resp = make_response(render_template('question.html',
                                   title=question.title, name=question.creator, qid=qid, question_heading=question.title,
                                   question_content=question.description, status=question.status, expired_at=question.expired_at,
                                   show_details=question.show_details, answers=answers, answers_count=len(answers)))
            # setcookie for user id
            resp.set_cookie('uid', wuser.id)
            resp.set_cookie('qid', qid)
            return resp
        else:
            return render_template('question.html', title="Unavailable questionnaire", name="No name", qid=qid)

    else:
        return render_template('question.html', title="Test", name="No name", qid=qid)
        # redirect_url = wechathandler.get_question_info_url(wechat.conf.appid, qid)
        # logger.debug("questionnaire with id: %s and no available user" % qid)
        # return redirect(redirect_url)

@app.route('/answers', methods=["GET", "POST"])
def answers():
    uid = request.cookies.get('uid')
    qid = request.cookies.get('qid')
    logger.debug('user id in cookie: ' + str(uid))
    wuser = None
    if uid:
        try:
            query = Query(WeUsers)
            wuser = query.get(uid)
        except leancloud.LeanCloudError:
            logger.warning("WeUser not found via uid %s", uid)
    logger.debug("request data: %s form: %s", request.data, request.form)
    if wuser and qid:
        query = Query(Answers)
        query.equal_to('qid', qid)
        query.equal_to('userid', uid)
        answer = None
        try:
            answer = query.first()
        except leancloud.LeanCloudError:
            logger.debug("Need to create table for answer first")
        if not answer:
            answer = Answers()
            answer.qid = qid
            answer.userid = uid
            answer.value = request.form.get('answer')
            answer.voter = wuser.nickname
            answer.headimg = wuser.headimgurl
            answer.save()
            logger.debug("answered as %s", answer)
        else:
            """
            check modify answer for question
            """
            logger.debug("already answered %s", answer)
        answers_query = Query(Answers)
        answers_query.equal_to('qid', qid)
        answers = answers_query.find()
        answer_count = len(answers)

        return render_template("answers.html", answers=answers, answers_count=answer_count)
    else:
        pass
        answers_query = Query(Answers)
        answers_query.equal_to('qid', "56def37b8ac2470056ece82d")
        answers = answers_query.find()
        answer_count = len(answers)
        return render_template("answers.html", answers=answers, answers_count=answer_count)

def validate_weuser():
    code = request.args.get('code')
    if code:
        url = str.format(
            'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'
            % (wechat.conf.appid, wechat.conf.appsecret, str(code)))
    else:
        return None
    resp = requests.get(url)
    authorize_result = json.loads(resp.text)
    openid = authorize_result.get('openid')
    token = authorize_result.get('access_token')
    # userinfo = wechat.get_user_info(openid)
    if openid:
        logger.debug("wechat openId: %s, token: %s", openid, str(token))
    else:
        logger.debug("wechat openid invalidated!!!")
    try:
        query = Query(WeUsers)
        query.equal_to('openid', openid)
        wuser = query.find()
        if len(wuser) > 0:
            wuser = wuser[0]
        else:
            logger.debug('try to retrieve userinfo')
            wechathandler.get_user_info(openid, token)
            # wuser = wechathandler.retrieve_weuser(openid)
        return wuser
    except leancloud.LeanCloudError:
        logger.warning("WeUser not found")


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
