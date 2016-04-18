import logging
import subprocess
import uuid
from pathlib import Path

import tornado.ioloop

import tornado.web

WAV_FILE_DIR = '/tmp/test-asr'
DECODER_PATH = '/decoder'

WAV_DIR = Path(WAV_FILE_DIR)
WAV_DIR.mkdir(exist_ok=True)

LOG = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world.')


def make_cmd(wav_file):
    return 'cd /vagrant/kaldi/egs/twasr-thchs30/s5; ' \
           'local/decode_single.sh %s' % str(wav_file.resolve())


def decode(wav_file):
    file_name = wav_file.name.split('.')[0]
    cmd_result = subprocess.run(
        ['/bin/sh', '-c', make_cmd(wav_file)],
        stderr=subprocess.PIPE
    )

    decoded = cmd_result.stderr.decode('utf-8')

    for line in decoded.splitlines():
        if line.startswith(file_name):
            return line[len(file_name):]


class WavHandler(tornado.web.RequestHandler):
    def post(self):
        file_name = str(uuid.uuid1())
        wav_file = WAV_DIR / ('%s.wav' % file_name)

        LOG.info('file received: %s' % wav_file)

        with wav_file.open(mode='bw+') as output:
            output.write(self.request.files['wav'][0]['body'])

        result = decode(wav_file)

        LOG.info('file decoded: %s' % wav_file)

        self.write(result)


application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/upload', WavHandler),
], debug=True)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
