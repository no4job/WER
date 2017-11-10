import subprocess
import sys
'''
DEFAULT_KEY_VALUE = 'paste-your-own-key'
DEFAULT_SERVER_VALUE = 'asr.yandex.net'
DEFAULT_PORT_VALUE = 80

DEFAULT_FORMAT_VALUE = 'audio/x-pcm;bit=16;rate=16000'
# 'audio/x-pcm;bit=16;rate=8000' # use this format for 8k bitrate wav and pcm

DEFAULT_MODEL_VALUE = 'freeform'
DEFAULT_LANG_VALUE = 'ru-RU'

DEFAULT_UUID_VALUE = randomUuid().hex

DEFAULT_CHUNK_SIZE_VALUE = 1024*32*2
DEFAULT_RECONNECT_DELAY = 0.5
DEFAULT_RECONNECT_RETRY_COUNT = 5
DEFAULT_PENDING_LIMIT = 50

DEFAULT_INTER_UTT_SILENCE = 120
DEFAULT_CMN_LATENCY = 50
'''
if __name__ == "__main__":
    AUDIO_IN_DIR_PATH = '../AUDIO_IN/'
    AUDIO_FILE_NAME = 'all_text_16_my_voice.wav'
    RECOGNIZED_DIR_PATH = '../RECOGNIZED_OUT/'
    RECOGNIZED_FILE_NAME = 'recognized.txt'
    API_KEY = '924df669-0866-4524-b2ed-1e6c2eda6867'
    MODEL = 'freeform'
    arg = '--key {} --model {} {}'.format(API_KEY, MODEL, AUDIO_IN_DIR_PATH+AUDIO_FILE_NAME)
    # print(sys.executable)
    try:
        retcode =  subprocess.call(sys.executable + "asrclient-cli.py" + " arg", shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)