# -*- coding: utf-8 -*-
from flask import Flask, request
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic

app = Flask(__name__)

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

@app.route('/little')
def little_wechat():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    if wechat.check_signature(signature, timestamp, nonce):
        return echostr
    else:
        return "validate failed"

if __name__ == '__main__':
    app.run()
