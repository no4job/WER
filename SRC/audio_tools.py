import winsound
import os
import speech_recognition as sr
import wave
import contextlib
import time
import threading

AUDIO_REF_DIR_PATH = '../REF_AUDIO_IN/'
SAMPLE_RATE = 16000
# DEFAULT_MICROPHONE_NAME = "Микрофон (B525 HD Webcam)"
DEFAULT_MICROPHONE_NAME = "Микрофон (B525 HD Webcam)"
# DEFAULT_MICROPHONE_NAME = "Микрофон (Realtek High Definiti"


RECORD_GUARD_TIME = 0.1

def wav_duration(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    # print(duration)
    return duration

def get_microphone_index_by_name(microphone_name):
    index = None
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        selected = " "
        microphone_name = microphone_name.encode(encoding="1252").decode(encoding="cp1251")
        if microphone_name == "Микрофон (B525 HD Webcam)":
            index = i
            selected = "*"
    return index

def get_microphone_list():
    microphone_list =[]
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        microphone_name = microphone_name.encode(encoding="1252").decode(encoding="cp1251")
        microphone_list.append(tuple([i,microphone_name]))
    return microphone_list

def show_microphone_list(microphone_list,selected_index = None,selected_name = None):
    for i, microphone_name in microphone_list:
        selected = " "
        if selected_index == i or selected_name == microphone_name:
            selected = "*"
        print("{2} Microphone with name \"{1}\" found for microphone(device_index{0})"
              .format(i, microphone_name, selected))

def playback(file):
    time.sleep(RECORD_GUARD_TIME)
    winsound.PlaySound(file, winsound.SND_FILENAME)

def record_playback(playback_audio_file,recorded_file,microphone_name = DEFAULT_MICROPHONE_NAME):
    device_index = get_microphone_index_by_name(microphone_name)
    duration = wav_duration(playback_audio_file)
    r = sr.Recognizer()
    t =  threading.Thread (target = playback,args = (playback_audio_file,))
    t.start()
    with  sr.Microphone(device_index=device_index, sample_rate=SAMPLE_RATE) as source:
        audio = r.record(source, duration = duration+RECORD_GUARD_TIME*2)
        # time.sleep(RECORD_GUARD_TIME)
        # winsound.PlaySound(playback_audio_file, winsound.SND_FILENAME|winsound.SND_ASYNC)
        with open(recorded_file, "wb") as f:
            f.write(audio.get_wav_data())
    t.join()

if __name__ == '__main__':
    show_microphone_list(get_microphone_list(),selected_name = DEFAULT_MICROPHONE_NAME)

    # pass
    '''
    index = None
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        selected = " "
        microphone_name = microphone_name.encode(encoding="1252").decode(encoding="cp1251")
        if microphone_name == "Микрофон (B525 HD Webcam)":
            index = i
            # m = sr.Microphone(device_index=i)
            selected = "*"
        print("{2} Microphone with name \"{1}\" found for microphone(device_index{0})"
              # .format(index,microphone_name.encode(encoding="1252").decode(encoding="cp1251"),selected))
              .format(i, microphone_name, selected))

    r = sr.Recognizer()
    # audio = r.listen(source)
    source = sr.Microphone(device_index=i)
    audio = r.record(source, duration = None, offset = None)
    exit (0)
    audio_ref_file_name = 'all_text_16_my_voice_cut.wav'
    audio_file = os.path.abspath(AUDIO_REF_DIR_PATH+audio_ref_file_name)
    winsound.PlaySound(audio_file, winsound.SND_FILENAME) # winsound.SND_ASYNC
    '''