import asyncio

import tornado.platform.asyncio

from asr.server import MainHandler, TaskHandler

if __name__ == '__main__':
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/tasks', TaskHandler),
        (r'/tasks/(.*)', TaskHandler),
    ], debug=True)
    application.listen(8888)

    asyncio.get_event_loop().run_forever()
