import asyncio

import tornado.platform.asyncio

from asr.server import MainHandler, AsrHandler

if __name__ == '__main__':
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/asrs', AsrHandler),
    ], debug=True)
    application.listen(8888)

    asyncio.get_event_loop().run_forever()
