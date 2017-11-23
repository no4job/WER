import winsound
import os
import speech_recognition as sr
import wave
import contextlib
import time
import threading
import pycaw
import subprocess
import sys
import pickle


AUDIO_REF_DIR_PATH = '../REF_AUDIO_IN/'
SAMPLE_RATE = 16000
# DEFAULT_MICROPHONE_NAME_CUT = "Микрофон (B525 HD Webcam)"
# DEFAULT_MICROPHONE_NAME_CUT = "Микрофон (Realtek High Definiti"
# DEFAULT_MICROPHONE_NAME_CUT = "DVS Receive  1-2 (Dante Virtual"

# DEFAULT_MICROPHONE_NAME = "Микрофон (B525 HD Webcam)"
DEFAULT_MICROPHONE_NAME = "DVS Receive  1-2 (Dante Virtual Soundcard)"

# DEFAULT_MICROPHONE_NAME = "Микрофон (Steam Streaming Microphone)"

DEFAULT_MICROPHONE_NAME_CUT = DEFAULT_MICROPHONE_NAME[:31]


RECORD_GUARD_TIME = 0.1
PYCAW_IPC_FILE = '..\\WRK\\IPC\\AllDeviceVolume.pickle'

def wav_duration(fname):
    duration = 0
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        if rate == None or rate == 0:
            duration = 0
        else:
            duration = frames / float(rate)
        # print(duration)
    return duration

def wav_params(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        wp = f.getparams()
        wcp ={}
        wcp["flow_rate"]= wp["nchannel"]*wp["sampwidth"]*8*wp["framerate"]/1000.0
        wcp["sample_rate"] = wp["framerate"]/1000.0
        wcp["bits_per_channel"] = wp["sampwidth"]*8
        wcp["number_of_channels"] = wp["nchannel"]
        wcp["compression"] = wp["compnamel"]
        return wcp

def get_microphone_index_by_name(microphone_name):
    index = None
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        # selected = " "
        name = name.encode(encoding="1252").decode(encoding="cp1251")
        if name == microphone_name:
            index = i
            # selected = "*"
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

def record_playback(playback_audio_file,recorded_file,microphone_name = DEFAULT_MICROPHONE_NAME_CUT):
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

def get_device_volume_list():
    all_device_volume = pycaw.AudioUtilities.GetAllDeviceVolume()
    return all_device_volume

def get_device_volume_list_ipc():
    # all_device_volume = pycaw.AudioUtilities.GetAllDeviceVolume()
    '''
    all_device_volume =[None]
    t = threading.Thread(target=pycaw.AudioUtilities.GetAllDeviceVolumeTh, args=(all_device_volume))
    t.start()
    t.join()
    return all_device_volume[0]
    '''
    process = subprocess.Popen(sys.executable + " pycaw.py",
                               shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    if len(stderr)>0:
        print (stderr.decode(encoding="cp866"))
    if len(stdout)>0:
        print (stdout.decode(encoding="utf-8"))
    if process.returncode != 0:
        print ("Execution failed, return code: {}".format(process.returncode))
        exit (process.returncode)
    all_device_volume = {}
    with open(PYCAW_IPC_FILE, 'rb') as f:
        all_device_volume= pickle.load(f)
    # print("ok")
    return all_device_volume

def show_device_list(all_device_volume,selected_name = None):
    out_device = all_device_volume["out"]
    in_device = all_device_volume["in"]
    max_name = max(len(device['Name']) for device in out_device+in_device)
    all = {"Output devices:":out_device,"Input devices:":in_device}
    for device_type,device_list in all.items():
        print ("\n    "+device_type)
        for device in device_list:
            selected = ' '
            default = ' '
            if device["Name"] == selected_name:
                selected = 's'
            if device["GUID"] ==  all_device_volume["default_in"]["GUID"] or \
                device["GUID"] ==  all_device_volume["default_out"]["GUID"] :
                default = 'd'
            if default == 'd' and device_type=="Output devices:":
                selected = 's'

            space = " "*(max_name-len(device['Name']) )
            print("{} {} {}|{}{}: volume {:.2f}dB, slider {:.0%}, volume range min {:g}dB, max {:g}dB, step {:g}dB".format(
                selected,default,
                device["Name"][:31],device["Name"][31:],space,device["MasterVolumeLevel"],
                  device["VolumeLevelScalar"], device["VolumeRange"][0],device["VolumeRange"][1],device["VolumeRange"][2]))

if __name__ == '__main__':
    show_microphone_list(get_microphone_list(),selected_name = DEFAULT_MICROPHONE_NAME_CUT)
    # show_device_list(get_device_volume_list())
    show_device_list(get_device_volume_list_ipc(),DEFAULT_MICROPHONE_NAME)



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