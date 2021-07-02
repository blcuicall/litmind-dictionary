import datetime
import time
import hashlib


# 　UUID: 通用唯一标识符 ( Universally Unique Identifier ), 对于所有的UUID它可以保证在空间和时间上的唯一性. 它是通过MAC地址, 时间戳, 命名空间, 随机数, 伪随机数来保证生成ID的唯一性, 有着固定的大小( 128 bit ).  它的唯一性和一致性特点使得可以无需注册过程就能够产生一个新的UUID
import uuid
import requests
import pymysql
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re


# 用captcha.image下的 ImageCaptcha 生成字符验证码图片, 只需三行代码
from captcha.image import ImageCaptcha


import os

import io
import random
import numpy as np


APP_KEY = '0173f43b3aeb7b75b8195eecbb88f3cd'
APP_SECRET = '295db878ace5'
cursor = None
client = None


def get_text_len():
    return random.randint(300, 500)


def get_sent_avg_len():
    return random.randint(5, 20)


def get_sent_max_len():
    return random.randint(21, 30)


def get_word_difficuly():
    return random.random()


def get_syntactic_complexity():
    return random.randint(1, 7)


def split_sentence(sentence):
    resentencesp = re.compile('([﹒﹔﹖﹗．；。！？]["’”」』]{0,2}|：(?=["‘“「『]{1,2}|$))')
    s = sentence
    slist = []
    for i in resentencesp.split(s):
        if resentencesp.match(i) and slist:
            slist[-1] += i
        elif i:
            slist.append(i)
    return slist


""" 链接数据库 """


def get_mysql_conn():
    # 1.连接数据库   服务器用户：zxp 密码：yfb217     数据目录：/data/private/zxp
    HOSTNAME = '127.0.0.1'  # ip地址 本地:127.0.0.1  服务器: 202.112.194.62
    PORT = '3306'  # 端口号
    DATABASE = 'new_wenxin_dictionary'  # 数据库名
    USERNAME = "wenxin_dictionary_admin"  # 用户名  本地:root   服务器: wenxin_dictionary_admin
    PASSWORD = "BLCUicall12!@"  # 用户登录密码  本地:123456    服务器: BLCUicall12!@
    DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    db = create_engine(DB_URL, echo=True)
    conn = db.connect()
    metadata = MetaData(db)
    return db, conn, metadata


def close_mysql_conn(db, conn):
    conn.close()
    db.dispose()


def sqlalchemy_result_to_dict(result):
    # return [dict(zip(r.keys(), r)) for r in result]
    data = []
    for r in result:
        d = dict(r.items())
        for key, value in d.items():
            if isinstance(value, datetime.datetime):
                d[key] = str(value)
        data.append(d)
    return data


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_nonce():
    return uuid.uuid4().hex


def get_curtime():
    return str(int(time.time()))


nonce = get_nonce()
curtime = get_curtime()


def get_checksum():
    s = "{}{}{}".format(APP_SECRET, nonce, curtime).encode(encoding="utf-8")
    return hashlib.sha1(s).hexdigest()


checksum = get_checksum()


def get_verification_code(mobile):
    headers = {
        "AppKey": APP_KEY,
        "CurTime": curtime,
        "Nonce": nonce,
        "CheckSum": checksum,
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    data = {
        "mobile": mobile
    }
    url = 'https://api.netease.im/sms/sendcode.action'
    r = requests.post(url, data=data, headers=headers)
    return r.json()


def gen_special_img(text):
    # 设置图片大小和宽度
    width = 100
    height = 60
    print(text)
    # 生成img文件
    generator = ImageCaptcha(width=width, height=height)  # 指定大小
    img = generator.generate_image(text)  # 生成图片
    output = io.BytesIO()
    img.save(output, format='JPEG')
    hex_data = output.getvalue()
    return hex_data


def get_captcha_text():
    # 验证码字符
    characters = "0123456789abcdefghijklmnopqrstuvwxyz"
    #生成验证码
    text = ""
    for j in range(4):
        text += random.choice(characters)
    return text


def clean_space(text):
    """"
    处理多余的空格
    """
    match_regex = re.compile(u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(should_replace_list,key=lambda i:len(i),reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()
        text = text.replace(i,new_i)
    return text
# 查找字符串s2 在另一个字符串s1中的位置
def index_of_str(s1, s2):
    res = []
    index = 0
    if s1 == "" or s2 == "":
        return -1
    split_list = s1.split(s2)
    for i in range(len(split_list) - 1):
        index += len(split_list[i])
        res.append(index)
        index += len(s2)
    return res if res else -1
# 删除中文解析中的句号 。
def deleteFullpointOfChinaExplain(s1):
    clear_list = '[。]'
    s2 = re.sub(clear_list,"",s1)
    return s2