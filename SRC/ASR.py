import subprocess
import sys
import os
import pickle

IPC_FILE = '..\\IPC\\asr_responce_lst.pickle'

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
3. from https://github.com/google/protobuf/releases 
    download  protoc-3.4.0-win32.zip
    unpack to xxx\yyy\zzz path
4. download speechkitcloud from github as zip file and unpack it in aaa\bbb\ccc
5.
install speechkitcloud according README.txt(https://github.com/yandex/speechkitcloud/tree/master/python):
cd aaa\bbb\ccc\speechkitcloud/python
xxx\yyy\zzz\bin\protoc -I=asrclient --python_out=asrclient asrclient/*.proto
python ./setup.py sdist
cd dist
sudo pip install <generated-file-name>

6. copy asrclient-cli.py to project src folder

7. Change site package  files: 
C:/virtual_envs/WER/Lib/site-packages/asrclient/voiceproxy_pb2.py
change string 16 :  import basic_pb2 as basic__pb2 -> from . import basic_pb2 as basic__pb2 

C:\virtual_envs\WER\Lib\site-packages\asrclient\client.py
change string 264 : 
from:
imported_module = __import__(callback_module, globals(), locals(), [], -1)
to:
imported_module = __import__(callback_module, globals(), locals(), [], 0)
'''
class AsrClientOptions:
    def __init__(self, **kwargs):
        self.option_defaults = {
            'key': ['--key','924df669-0866-4524-b2ed-1e6c2eda6867'],
            'model':['--model','freeform'],
            'callback_module':['--callback-module','advanced_callback'],
            'realtime':['--realtime',False] ,
            'nopunctuation': ['--nopunctuation',True],
            'silent' : ['--silent',True]
        }
        # for (option, default) in option_defaults.items():
        #     setattr(self, option, kwargs.get(option, default))
        self.test_option(kwargs)
        self.options={}
        for (option, default) in self.option_defaults.items():
            self.options[option] = kwargs.get(option, default)


    def option_str(self):
        options_str =""
        for option, value in self.options.items():
            if type(value[1]) != bool:
                options_str =  options_str+" {} {}".format(value[0], value[1])
            else:
                if value[1]:
                    options_str =  options_str+" {}".format(value[0])
                # options_str = " ".join( "{} {}".format(value[0], value[1]) for option, value in self.options.items())
        return options_str

    def test_option(self,kwargs):
        for option, value in kwargs.items():
            if option not in self.option_defaults or type(value) != type( self.option_defaults[option][1]):
                raise ValueError('Bad parameter: {}:{}'.format(option,value))

    def set_option(self,**kwargs):
        self.test_option(kwargs)
        for (option, value) in self.options.items():
            self.options[option][1] = kwargs.get(option, value[1])

    def get_option(self,option):
        return self.options[option][1]

def recognize(file,options=None):
    if not options:
        options = AsrClientOptions().option_str()
    process = subprocess.Popen(sys.executable + " asrclient-cli.py"+ " " + options+ " "+
                               file,
                               shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    print (stderr.decode(encoding="cp866"))
    print (stdout.decode(encoding="utf-8"))
    if process.returncode != 0:
        print ("Execution failed, return code: {}".format(process.returncode))
        exit (process.returncode)
    asr_response_lst = []
    with open(IPC_FILE, 'rb') as f:
        asr_response_lst = pickle.load(f)
    all_text = ""
    for response in asr_response_lst:
        if len(response):
            utterance = " ".join(word['value']  for word in response[0]['word'])
            all_text =  all_text + utterance + "\n"
    # print (all_text)
    return all_text


if __name__ == "__main__":
    AUDIO_IN_DIR_PATH = '../AUDIO_IN/'
    AUDIO_FILE_NAME = 'all_text_16_my_voice.wav'
    file = os.path.abspath(AUDIO_IN_DIR_PATH+AUDIO_FILE_NAME)
    print(recognize(file))
    exit (0)


    '''
    options = AsrClientOptions().option_str()
    print(options)
    # exit(0)
    AUDIO_IN_DIR_PATH = '../AUDIO_IN/'
    AUDIO_FILE_NAME = 'all_text_16_my_voice.wav'
    RECOGNIZED_DIR_PATH = '../RECOGNIZED_OUT/'
    RECOGNIZED_FILE_NAME = 'recognized.txt'
    API_KEY = '924df669-0866-4524-b2ed-1e6c2eda6867'
    MODEL = 'freeform'
    cbck_module  = "advanced_callback"
    # realtime = "--realtime"
    no_punctuation = "--nopunctuation"
    silent = "--silent"
    realtime = ""
    arg = '--key {} --model {} --callback-module {} {} {} {} {}'.format(API_KEY, MODEL, cbck_module,realtime,silent,
                                                no_punctuation,os.path.abspath(AUDIO_IN_DIR_PATH+AUDIO_FILE_NAME))
    # process = subprocess.Popen(sys.executable + " asrclient-cli.py" + " " + arg, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process = subprocess.Popen(sys.executable + " asrclient-cli.py"+ " " + options+ " "+
                                os.path.abspath(AUDIO_IN_DIR_PATH+AUDIO_FILE_NAME),
                               shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    print (stderr.decode(encoding="cp866"))
    print (stdout.decode(encoding="utf-8"))
    if process.returncode != 0:
        print ("Execution failed, return code: {}".format(process.returncode))
        exit (process.returncode)
    asr_response_lst = []
    with open(IPC_FILE, 'rb') as f:
        asr_response_lst = pickle.load(f)
    all_text = ""
    for response in asr_response_lst:
      if len(response):
          utterance = " ".join(word['value']  for word in response[0]['word'])
          all_text =  all_text + utterance + "\n"

    print (all_text)
    '''
