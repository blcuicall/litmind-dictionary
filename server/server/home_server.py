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

    def insert_userIp(self, ipStr, wordStr, sentenceStr,explainStr,typeidStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(insert_time)
        table = Table('t_history', metadata, autoload=True)
        i = table.insert()
        result = conn.execute(i, user_ip=ipStr, word=wordStr, sentence=sentenceStr,explain=explainStr,praise="0",step_on="0",modify="0",type_id=typeidStr, create_time=insert_time)
        # result = conn.execute(i, user_ip=ipStr, sentence=exampleStr)
        close_mysql_conn(db, conn)
        return result.rowcount

    # 正向词典 获取 解析当前数据
    def get_explain_info_by_use_ip(self,ipStr,explain):
        db, conn, metadata = get_mysql_conn()
        print("#####################")
        print(ipStr)
        sql = "SELECT * FROM t_history where user_ip='144.52.166.105'"
        # SELECT * FROM t_history where user_ip='144.52.166.105' and `explain`='性本善 形容具有慈爱、友善等正面特质的' ORDER BY praise LIMIT 1;
        # sql = "SELECT * FROM t_history WHERE  user_ip  like :userIp and explain  like :explain"
        s = text(sql)
        result = conn.execute(s)
        
        data = sqlalchemy_result_to_dict(result)
        close_mysql_conn(db, conn)
        return data
    # 正向词典 更新 userip 解析下的  赞
    def updata_praise_search_info(self,useripStr,explain,praiseStr):
        db,conn,metadata = get_mysql_conn()
        # 获取更新时间
        update_time = get_current_time()
        table = Table('t_history', metadata, autoload=True)
        u = table.update().values(praise = praiseStr,updata_time=update_time).where(table.c.user_ip == useripStr and table.c.explain == explainStr)
        result = conn.execute(u)
        close_mysql_conn(db,conn)
        return result.rowcount
    # 正向词典 更新 userip 解析下的  踩
    def updata_stepon_search_info(self,useripStr,explain,steponStr):
        db,conn,metadata = get_mysql_conn()
        # 获取更新时间
        update_time = get_current_time()
        table = Table('t_history', metadata, autoload=True)
        u = table.update().values(step_on=steponStr,updata_time=update_time).where(table.c.user_ip == useripStr and table.c.explain == explainStr)
        result = conn.execute(u)
        close_mysql_conn(db,conn)
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
    def insert_redict_userIp(self, ipStr, sentenceStr,explainStr,typeidStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(insert_time)
        table = Table('t_redict_history', metadata, autoload=True)
        i = table.insert()

        result = conn.execute(i, user_ip=ipStr, sentence=sentenceStr,explain=explainStr,praise="0",step_on="0",modify="0",type_id=typeidStr, create_time=insert_time)
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

    # 正向词典 解析 插入反馈意见
    def insert_explain_feedback_by_userIp(self,ipStr,searchWordStr,searchSententStr,explainContentStr,feedStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        print(ipStr)
        print(searchWordStr)
        print(searchSententStr)
        print(explainContentStr)
        print(feedStr)
        table = Table('t_explain_feedback', metadata, autoload=True)
        i = table.insert()
        result = conn.execute(i, user_ip=ipStr,search_word=searchWordStr,search_sentent=searchSententStr,explain_content=explainContentStr, feed_content=feedStr, create_time=insert_time)
        # result = conn.execute(i, user_ip=ipStr, sentence=exampleStr)
        close_mysql_conn(db, conn)
        return result.rowcount

    # 反正向词典 解析 插入反馈意见
    def insert_re_explain_feedback_by_userIp(self, ipStr,searchSententStr,explainContentStr, feedStr):
        db, conn, metadata = get_mysql_conn()
        # 获取插入时间
        insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(insert_time)
        table = Table('t_re_explain_feedback', metadata, autoload=True)
        i = table.insert()
        result = conn.execute(i, user_ip=ipStr,search_sentent=searchSententStr,explain_content=explainContentStr, feed_content=feedStr, create_time=insert_time)
        # result = conn.execute(i, user_ip=ipStr, sentence=exampleStr)
        close_mysql_conn(db, conn)
        return result.rowcount












