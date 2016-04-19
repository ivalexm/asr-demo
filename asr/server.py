import logging
import uuid
from pathlib import Path

import tornado.web

from .decode import schedule_decode

WAV_FILE_DIR = '/tmp/test-asr'
DECODER_PATH = '/decoder'

WAV_DIR = Path(WAV_FILE_DIR)
WAV_DIR.mkdir(exist_ok=True)

LOG = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world.')


class AsrHandler(tornado.web.RequestHandler):
    def post(self):
        asr_id = str(uuid.uuid1())
        wav_file = WAV_DIR / ('%s.wav' % asr_id)

        LOG.info('file received: %s' % wav_file)

        with wav_file.open(mode='bw+') as output:
            output.write(self.request.files['wav'][0]['body'])

        result = schedule_decode(asr_id, wav_file)

        LOG.info('file decoded: %s' % wav_file)

        self.write(result)
