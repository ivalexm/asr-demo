import json
import logging
import uuid
from pathlib import Path

import tornado.web
from tornado.ioloop import IOLoop

from .decode import schedule_decode, get_task, push_task

WAV_FILE_DIR = '/tmp/test-asr'
DECODER_PATH = '/decoder'

WAV_DIR = Path(WAV_FILE_DIR)
WAV_DIR.mkdir(exist_ok=True)

LOG = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world.')


class TaskHandler(tornado.web.RequestHandler):
    def get(self, task_id):
        self.write(
            json.dumps(get_task(task_id).to_dict(), ensure_ascii=False)
        )

    def post(self):
        task_id = str(uuid.uuid1())
        push_task(task_id)

        wav_file = WAV_DIR / ('%s.wav' % task_id)

        LOG.info('file received: %s' % wav_file)

        with wav_file.open(mode='bw+') as output:
            output.write(self.request.files['wav'][0]['body'])

        IOLoop.current().spawn_callback(schedule_decode, task_id, wav_file)

        LOG.info('file decoded: %s' % wav_file)

        self.write({'id': task_id})
