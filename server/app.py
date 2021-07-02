import tornado.web
import tornado.ioloop
from handler.home_search_handler import HomeSearchHandler
from handler.home import HomeSearchGetUserIPHandler

from handler.home import RedictSearchHandler
from handler.home import RedictSearchGetUserIPHandler

from handler.home import InsertExplianFeedbackByUserIPHandler
from handler.home import InsertReExplianFeedbackByUserIPHandler
from handler.home import FeedbackByUserIPHandler

from handler.home import UpExplianZanByUserIPHandler

HANDLERS = [
    (r"/home/searchContent", HomeSearchHandler),
    (r"/home/searchGetUserIp", HomeSearchGetUserIPHandler),
    (r"/home/redictSearchContent", RedictSearchHandler),
    (r"/home/redictSearchGetUserIp", RedictSearchGetUserIPHandler),
    (r"/home/insertExplianFeedback", InsertExplianFeedbackByUserIPHandler),
    (r"/home/insertReExplianFeedback", InsertReExplianFeedbackByUserIPHandler),
    (r"/home/insertFeedback", FeedbackByUserIPHandler),
    (r"/home/upExplianZan", UpExplianZanByUserIPHandler),
]
settings = {
    "cookie_secret": "zkvi2AnRTiG0tEe7PfbHJy+3aMCkh0v2gOxZ5/vIRxo=",
    #"login_url": "/login",
    "debug": True,
    #"xsrf_cookies": True,
}


def make_app():
    return tornado.web.Application(HANDLERS, **settings)


if __name__ == "__main__":
    port = 10301
    app = make_app()
    app.listen(port)
    print('server start on port: {}'.format(port))
    tornado.ioloop.IOLoop.current().start()
