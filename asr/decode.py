import subprocess


def make_cmd(wav_file):
    return 'cd /vagrant/kaldi/egs/twasr-thchs30/s5; ' \
           'local/decode_single.sh %s' % str(wav_file.resolve())


def schedule_decode(asr_id, wav_file):
    cmd_result = subprocess.run(
        ['/bin/sh', '-c', make_cmd(wav_file)],
        stderr=subprocess.PIPE
    )

    decoded = cmd_result.stderr.decode('utf-8')

    for line in decoded.splitlines():
        if line.startswith(asr_id):
            return line[len(asr_id):]
