import subprocess
import sys
import os
import codecs
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
'''
1. pip install click
2. pip install protobuf-3.4.0-py3-none-any.whl - ???
3. from https://github.com/google/protobuf/releases 
    download  protoc-3.4.0-win32.zip
    unpack to xxx\yyy\zzz path
4. download speechkitcloud from github as zip file and unpack it in aaa\bbb\ccc
5.
install speechkitcloud according README.txt:
cd aaa\bbb\ccc\speechkitcloud/python
xxx\yyy\zzz\bin\protoc -I=asrclient --python_out=asrclient asrclient/*.proto
python ./setup.py sdist
cd dist
sudo pip install <generated-file-name>

6. copy asrclient-cli.py to project src folder

7. Change file in installed site package installed file 
C:/virtual_envs/WER/Lib/site-packages/asrclient/basic_pb2.py
change string 16 :  import basic_pb2 as basic__pb2 -> from . import basic_pb2 as basic__pb2 

'''
if __name__ == "__main__":
    AUDIO_IN_DIR_PATH = '../AUDIO_IN/'
    AUDIO_FILE_NAME = 'all_text_16_my_voice.wav'
    RECOGNIZED_DIR_PATH = '../RECOGNIZED_OUT/'
    RECOGNIZED_FILE_NAME = 'recognized.txt'
    API_KEY = '924df669-0866-4524-b2ed-1e6c2eda6867'
    MODEL = 'freeform'
    arg = '--key {} --model {} {}'.format(API_KEY, MODEL, os.path.abspath(AUDIO_IN_DIR_PATH+AUDIO_FILE_NAME))
    # print(sys.executable)
    # sys.stdout = codecs.getwriter('cp866')(sys.stdout,'replace')
    # try:
        # retcode =  subprocess.call(sys.executable + "asrclient-cli.py" + " arg", shell=True)
        #retcode =  subprocess.call(sys.executable + "asrclient-cli.py" + " arg", shell=False)
        # retcode =  subprocess.check_output(sys.executable + "asrclient-cli.py" + " arg", shell=True)
    process = subprocess.Popen(sys.executable + " asrclient-cli.py" + " " + arg, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    print (stdout.decode(encoding="cp866"))
    print (stderr.decode(encoding="cp866"))
    if process.returncode != 0:
        print ("Execution failed, return code: {}".format(process.returncode))
    # except OSError as e:
    #     print("Execution failed:", e)