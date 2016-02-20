# -*- coding: utf-8 -*-

"""
@version: ??
@author: caiiiyua
@license: Apache Licence 
@contact: caiiiyua@gmail.com
@site: 
@software: PyCharm
@file: answer.py
@time: 16/2/20 下午4:54
"""

from leancloud import Object

class Answers(Object):
    @property
    def userid(self):
        return self.get('userid')
    @userid.setter
    def userid(self, openid):
        return self.set('userid', openid)

    @property
    def qid(self):
        return self.get('qid')
    @qid.setter
    def qid(self, questionid):
        return self.set('qid', questionid)

    @property
    def value(self):
        return self.get('value')
    @value.setter
    def value(self, answer):
        return self.set('value', answer)