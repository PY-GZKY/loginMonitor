# -*- coding: utf-8 -*
# @Time : 2020/10/30 9:48
import os
import sys

from logger.logger import log_v
from send_msg.config import message, weixin_notice_enable, weixin_sckey

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import requests


class Send_msg(object):
    __slots__ = ('weixin', 'email')

    def send_weixin(self, title, content):
        if not weixin_notice_enable:
            log_v.warning("未开启微信通知")
            return
        url = f"https://sc.ftqq.com/{weixin_sckey}.send"
        r = requests.post(url, data={"text": f'{title}', "desp": content})

        if r.status_code == requests.codes.ok:
            log_v.debug("微信通知发送成功")
        else:
            log_v.warning("微信通知发送失败")

# S = Send_msg()
# S.send_weixin(title="你好啊", content="这不是扯淡吗 ？？")
