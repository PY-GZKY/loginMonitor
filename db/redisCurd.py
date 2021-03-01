# -*- coding: utf-8 -*-
# @Time : 2020-11-18 13:56
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import redis

class RedisQueue(object):

    def __init__(self, name, **redis_kwargs):
        self.pool = redis.ConnectionPool(host='127.0.0.1',username='root',password=None,port=6379, db=1, max_connections=10)
        self.__db = redis.Redis(connection_pool=self.pool, decode_responses=True)
        self.key = name

    # 返回队列大小
    def qsize(self):
        return self.__db.llen(self.key)

    # 判断队列用尽
    def empty(self):
        return self.qsize() == 0

    def put_hash(self, key, value):
        self.__db.hset(self.key, key, value)

    def get_hash(self, key):
        return self.__db.hget(self.key, key)

    def get_all_hash(self):
        return self.__db.hkeys(self.key)

    def delete_hash(self, key):
        return self.__db.hdel(self.key, key)




