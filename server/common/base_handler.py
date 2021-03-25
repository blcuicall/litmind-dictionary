# -*- coding: utf-8 -*-

import tornado.web
import hashlib
import time
from hashlib import sha1
import os

ALL_USER_DIC = {}
create_session_id = lambda : sha1(bytes('%s%s' % (os.urandom(16),time.time()),encoding='utf-8')).hexdigest()
class Session:
    infoContainer = {
    }
    def __init__(self,handler):
        self.handler = handler
        randomStr = self.handler.get_cookie('session_id')
        if (not randomStr) or (randomStr not in self.infoContainer):
            randomStr = create_session_id()
            self.infoContainer[randomStr] = {}
        self.randomStr = randomStr
        self.handler.setCookie('session_id',randomStr,max_age=3600)

    def __getitem__(self, item):
        return self.infoContainer[self.randomStr].get(item)
    def __setitem__(self, key, value):
        self.infoContainer[self.randomStr][key] = value
    def __delitem__(self, key):
        if self.infoContainer[self.randomStr].get(key):
            del self.infoContainer[self.randomStr][key]
    def delete(self):
        del self.infoContainer[self.randomStr]

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, DELETE, PUT, GET,OPTIONS')
        origin = self.request.headers.get('Origin','')
        self.set_header('Access-Control-Allow-Origin', origin or '*')

        self.set_header('Access-Control-Allow-Credentials', 'true')

        self.set_header(
            'Access-Control-Allow-Headers',
            'Origin, X-Requested-With, Content-Type, Accept, client_id, uuid, Authorization'
        )

    def prepare(self):
        pass

    def _request_summary(self):
        return "%s^%s^%s^%s^%s" % (
        self.request.method, self.request.uri, self.request.body.decode('utf-8'), self.request.remote_ip,
        self.request.headers["User-Agent"])

