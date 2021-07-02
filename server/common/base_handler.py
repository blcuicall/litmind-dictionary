import tornado.web
import hashlib
import time
from hashlib import sha1
import os

ALL_USER_DIC = {}
# 随机生成session_id
create_session_id = lambda : sha1(bytes('%s%s' % (os.urandom(16),time.time()),encoding='utf-8')).hexdigest()
class Session:
    infoContainer = {
        # sessionId : {'user': info} --> 通过session保持用户信息，权限等
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
        # 从大字典删除sessionId
        del self.infoContainer[self.randomStr]

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        #self.session = Session(self)
        pass
    def set_default_headers(self):
        # 设置允许请求的方法
        self.set_header('Access-Control-Allow-Methods', 'POST, DELETE, PUT, GET,OPTIONS')
        # Tornado 获取请求的'origin'的方法
        origin = self.request.headers.get('Origin','')
        # 设置允许的'origin'，只设置'*'时某些特定情况下会失败故最好优先获取请求的域加入允许组中
        self.set_header('Access-Control-Allow-Origin', origin or '*')

        # 设置是否允许客户端携带证书式访问。通过对 Credentials 参数的设置，就可以保持跨域 Ajax 时的 Cookie
        self.set_header('Access-Control-Allow-Credentials', 'true')

        self.set_header(
            'Access-Control-Allow-Headers',
            'Origin, X-Requested-With, Content-Type, Accept, client_id, uuid, Authorization'
        )

    def prepare(self):
        pass

    # 重写此方法，记录请求方法，请求url，请求参数，请求客户端的ip,浏览器类型
    def _request_summary(self):
        return "%s^%s^%s^%s^%s" % (
        self.request.method, self.request.uri, self.request.body.decode('utf-8'), self.request.remote_ip,
        self.request.headers["User-Agent"])

