# -*- coding: utf-8 -*-

"""
@version: ??
@author: caiiiyua
@license: Apache Licence 
@contact: caiiiyua@gmail.com
@site: 
@software: PyCharm
@file: questionnaire.py
@time: 16/2/20 下午4:28
"""

from leancloud import Object

class Questionnaires(Object):
    @property
    def creator(self):
        return self.get('creator')
    @creator.setter
    def creator(self, creator):
        return self.set('creator', creator)

    @property
    def title(self):
        return self.get('title')
    @title.setter
    def title(self, title):
        return self.set('title', title)

    @property
    def description(self):
        return self.get('description')
    @description.setter
    def description(self, descip):
        return self.set('description', descip)

    @property
    def category(self):
        return self.get('category')
    @category.setter
    def category(self, cate):
        return self.set('category', cate)

    @property
    def modify_answer(self):
        return self.get('modify_answer')
    @modify_answer.setter
    def modify_answer(self, canmodify):
        return self.set('modify_answer', canmodify)

    @property
    def expired_at(self):
        return self.get('expired_at')
    @expired_at.setter
    def expired_at(self, expired):
        return self.set('expired_at', expired)

    @property
    def status(self):
        return self.get('status')
    @status.setter
    def status(self, stat):
        return self.set('status', stat)

    @property
    def answer_count(self):
        return self.get('answer_count')
    @answer_count.setter
    def answer_count(self, count):
        return self.set('answer_count', count)

    @property
    def show_details(self):
        return self.get('show_details')
    @show_details.setter
    def show_details(self, show):
        return self.set('show_details', show)

    def __repr__(self):
        return "[" + self.title + ", " + self.creator + ", " + self.status + ", " + self.expired_at + "]"