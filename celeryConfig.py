from __future__ import absolute_import
import datetime
from kombu import Exchange, Queue
from celery.schedules import crontab
from urllib import parse

BROKER_URL = f'redis://root:{parse.quote("不规则密码")}@127.0.0.1:6379/15'

# 导入任务，如tasks.py
CELERY_IMPORTS = ('loginMonitor.tasks',)

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# 定时和计划任务
CELERYBEAT_SCHEDULE = {
    'add-every-60-seconds': {
        'task': 'tasks.get_cookie_status',
        'schedule': datetime.timedelta(minutes=1),  # 每 1 分钟执行一次
        'args': ()  # 任务函数参数
    },
}
