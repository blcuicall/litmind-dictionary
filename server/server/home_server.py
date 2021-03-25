import re
import sys

from common.utils import close_mysql_conn
from common.utils import get_mysql_conn
from common.utils import sqlalchemy_result_to_dict, get_current_time
import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

sys.path.append('../')


class HomeService(object):

    def insert_userIp(self, ipStr, wordStr, sentenceStr, explainStr, typeidStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(insert_time)
        table = Table('t_history', metadata, autoload=True)
        i = table.insert()
        result = conn.execute(i, user_ip=ipStr, word=wordStr, sentence=sentenceStr, explain=explainStr, praise="0",
                              step_on="0", modify="0", type_id=typeidStr, create_time=insert_time)
        # result = conn.execute(i, user_ip=ipStr, sentence=exampleStr)
        close_mysql_conn(db, conn)
        return result.rowcount
        # 更新 userip 解析下的  赞  踩  修改意见

    def updata_search_info(self, useripStr, explain, praiseStr, steponStr, modifyStr):
        db, conn, metadata = get_mysql_conn()
        # 获取更新时间
        update_time = get_current_time()
        table = Table('t_history', metadata, autoload=True)
        u = table.update().values(praise=praiseStr, step_on=steponStr, modify=modifyStr, updata_time=update_time).where(
            table.c.user_ip == useripStr and table.c.explain == explainStr)
        result = conn.execute(u)
        close_mysql_conn(db, conn)
        return result.rowcount

    # 获取访问ip 列表
    def get_use_ip(self):
        db, conn, metadata = get_mysql_conn()
        sql = "SELECT * FROM t_history order by id desc"
        s = text(sql)
        result = conn.execute(s)
        data = sqlalchemy_result_to_dict(result)
        close_mysql_conn(db, conn)
        return data

    # 获取反向词典 访问ip 插入
    def insert_redict_userIp(self, ipStr, sentenceStr, explainStr, typeidStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(insert_time)
        table = Table('t_redict_history', metadata, autoload=True)
        i = table.insert()

        result = conn.execute(i, user_ip=ipStr, sentence=sentenceStr, explain=explainStr, praise="0", step_on="0",
                              modify="0", type_id=typeidStr, create_time=insert_time)
        # result = conn.execute(i, user_ip=ipStr, sentence=exampleStr)

        close_mysql_conn(db, conn)
        return result.rowcount

    # 获取反向词典 访问ip 列表
    def get_redict_use_ip(self):
        db, conn, metadata = get_mysql_conn()
        sql = "SELECT * FROM t_redict_history order by id desc"
        s = text(sql)
        result = conn.execute(s)
        data = sqlalchemy_result_to_dict(result)
        close_mysql_conn(db, conn)
        return data

    # 插入反馈意见
    def insert_feedback_by_userIp(self, ipStr, feedStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(insert_time)
        table = Table('t_feedback', metadata, autoload=True)
        i = table.insert()
        result = conn.execute(i, user_ip=ipStr, feed_content=feedStr, create_time=insert_time)
        # result = conn.execute(i, user_ip=ipStr, sentence=exampleStr)
        close_mysql_conn(db, conn)
        return result.rowcount












