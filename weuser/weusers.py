# -*- coding: utf-8 -*-

"""
@version: ??
@author: caiiiyua
@license: Apache Licence 
@contact: caiiiyua@gmail.com
@site: 
@software: PyCharm
@file: weusers.py.py
@time: 16/2/21 上午1:47
"""

from leancloud import Object

class WeUsers(Object):
    @property
    def openid(self):
        return self.get('openid')
    @openid.setter
    def openid(self, openid):
        return self.set('opendid', openid)

    @property
    def nickname(self):
        return self.get('nickname')
    @nickname.setter
    def nickname(self, name):
        return self.set('nickname', name)

    @property
    def sex(self):
        return self.get('sex')
    @sex.setter
    def sex(self, sex):
        return self.set('sex', sex)

    @property
    def headimgurl(self):
        return self.get('headimgurl')
    @headimgurl.setter
    def headimgurl(self, url):
        return self.set('headimgurl', url)

    @property
    def province(self):
        return self.get('province')
    @province.setter
    def province(self, province):
        return self.set('province', province)

    @property
    def city(self):
        return self.get('city')
    @city.setter
    def city(self, city):
        return self.set('city', city)

    @property
    def unionid(self):
        return self.get('unionid')
    @unionid.setter
    def unionid(self, uid):
        return self.set('unionid', uid)