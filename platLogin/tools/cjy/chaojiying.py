# -*- coding: utf-8 -*-
# @Time : 2020-11-23 22:32
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import requests
from hashlib import md5


class CJYClient(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def use_cjy(filename):
    username = ""  # 用户名
    password = ""  # 密码
    app_id = "897448"  # 软件ID
    cjy = CJYClient(username, password, app_id)  # 用户中心>>软件ID
    im = open(filename, 'rb').read()  # 本地图片文件路径
    return cjy.PostPic(im, 1006)  # 9004->验证码类型

# res = use_cjy("l.jpg")
# print(res)
