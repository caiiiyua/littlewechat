# -*- coding: utf-8 -*-
from flask import Flask, request
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
import wechathandler
import leancloud

import logging
from logging import handlers
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wechat')
loghandler = logging.StreamHandler()
loghandler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]'))
logger.addHandler(loghandler)

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

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
