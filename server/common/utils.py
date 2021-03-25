# -*- coding: utf-8 -*-

import datetime
import time
import hashlib
import uuid
import requests
import pymysql
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
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
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = ''
    USERNAME = ""
    PASSWORD = "BLCUicall12!@"
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
    width = 100
    height = 60
    print(text)
    generator = ImageCaptcha(width=width, height=height) 
    img = generator.generate_image(text)
    output = io.BytesIO()
    img.save(output, format='JPEG')
    hex_data = output.getvalue()
    return hex_data


def get_captcha_text():
    characters = "0123456789abcdefghijklmnopqrstuvwxyz"
    text = ""
    for j in range(4):
        text += random.choice(characters)
    return text


def clean_space(text):
    match_regex = re.compile(u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(should_replace_list,key=lambda i:len(i),reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()
        text = text.replace(i,new_i)
    return text


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


def deleteFullpointOfChinaExplain(s1):
    clear_list = '[。]'
    s2 = re.sub(clear_list,"",s1)
    return s2
