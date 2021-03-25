# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
from handler.home import HomeSearchHandler
from handler.home import HomeSearchGetUserIPHandler

from handler.home import RedictSearchHandler
from handler.home import RedictSearchGetUserIPHandler

from handler.home import UpdataExplianByUserIPHandler
from handler.home import FeedbackByUserIPHandler

HANDLERS = [

    (r"/home/searchContent", HomeSearchHandler),
    (r"/home/searchGetUserIp", HomeSearchGetUserIPHandler),

    (r"/home/redictSearchContent", RedictSearchHandler),
    (r"/home/redictSearchGetUserIp", RedictSearchGetUserIPHandler),

    (r"/home/updataExplain", UpdataExplianByUserIPHandler),
    (r"/home/insertFeedback", FeedbackByUserIPHandler),

]
settings = {
    "cookie_secret": "zkvi2AnRTiG0tEe7PfbHJy+3aMCkh0v2gOxZ5/vIRxo=",
    "debug": True,
}


def make_app():
    return tornado.web.Application(
        HANDLERS, **settings
    )


if __name__ == "__main__":
    port = 10400
    app = make_app()
    app.listen(port)
    print('server start on port: {}'.format(port))
    tornado.ioloop.IOLoop.current().start()
