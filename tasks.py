# coding=utf-8
from __future__ import absolute_import
import os
import sys
from db.redisCurd import RedisQueue
from send_msg.weinxin import Send_msg

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from logger.logger import log_v
from celery import Task

from platLogin.jdLogin.login import JDLogin  # 京东登陆

from celery import Celery

randomQueue = RedisQueue("jd_cookie")

celery_app = Celery('task')
celery_app.config_from_object('celeryConfig')

S = Send_msg()

dl_dict = {
    'jd': {
        'cookie': '',
        'loginClass': 'JDLogin',
    },

}


# 三种运行的状态
class task_status(Task):
    def on_success(self, retval, task_id, args, kwargs):
        log_v.info('任务信息 -> id:{} , arg:{} , successful ..... Done'.format(task_id, args))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log_v.error('task id:{} , arg:{} , failed ! error : {}'.format(task_id, args, exc))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        log_v.warning('task id:{} , arg:{} , retry !  info: {}'.format(task_id, args, exc))


# 轮询, celery6.0 在 win10 系统可能不太稳定,有时候会有连接断开的情况
@celery_app.task(base=task_status)
def get_cookie_status(platName="Erp"):
    try:
        randomQueue.get_hash(platName).decode()
        log_v.debug(f'[+] 轮询 {platName} 成功 ..... Done')
        return "Erp 轮询成功"
    except:
        return "Erp 轮询失败"


@celery_app.task(base=task_status)
def set_plat_cookie(platName, shopId=None):
    log_v.debug(f"[+] {platName} 正在登陆")
    core = eval(dl_dict[platName]['loginClass'])(shopId=shopId)
    result = core.run()
    return result
