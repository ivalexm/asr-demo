import subprocess
import os
import tornado.gen
import tornado.process

tasks = {}


def make_cmd(wav_file):
    return 'cd %s; local/decode_single.sh %s' \
           % (os.environ['KALDI_SCRIPT_DIR'], str(wav_file.resolve()))


class DecodeTask(object):
    def __init__(self):
        self.status = 'pending'
        self.result = ''

    def to_dict(self):
        return {
            'status': self.status,
            'result': self.result
        }


@tornado.gen.coroutine
def schedule_decode(task_id, wav_file):
    proc = tornado.process.Subprocess(['/bin/sh', '-c', make_cmd(wav_file)],
                                      stderr=tornado.process.Subprocess.STREAM)
    yield proc.wait_for_exit(raise_error=False)
    pipe = yield proc.stderr.read_until_close()
    decoded = pipe.decode('utf-8')

    result_line = [line for line in decoded.splitlines() if line.startswith(task_id)]
    if result_line:
        tasks[task_id].status = 'finished'
        tasks[task_id].result = result_line[0][len(task_id):]
    else:
        tasks[task_id].status = 'failed'
        tasks[task_id].result = decoded


def push_task(asr_id):
    tasks[asr_id] = DecodeTask()


def get_task(task_id):
    return tasks.get(task_id, {})
