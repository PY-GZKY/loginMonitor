# -*- coding: utf-8 -*
# @Time : 2020/10/30 9:55
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 是否开启微信通知
weixin_notice_enable = True

# server酱key
weixin_sckey = ""
message = {
    "subject": "登陆通知",
    "content": "<h1>上次登陆已失效，已重新登陆成功.</h1>"
}
