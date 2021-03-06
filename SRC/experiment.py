import os
import ASR
import wer
import time
import audio_tools
import shutil
import ntpath
import experiment_data as ed
import zipfile
import datetime
CALC_DIR = 0
REF_FILE_DIR_PATH = '../WRK/TXT_REF/'
# REF_FILE_NAME = 'ref.txt'
COMPARED_FILE_DIR_PATH = '../WRK/TXT_OUT/'
# COMPARED_FILE_NAME = 'compared.txt'
OUT_CSV_FILE_DIR_PATH = '../WRK/CSV_OUT/'
# OUT_CSV_FILE_NAME = 'out.csv'
AUDIO_REF_DIR_PATH = '../WRK/AUDIO_REF/'
AUDIO_IN_DIR_PATH = '../WRK/AUDIO_IN/'
ASR_ITERATIONS = 5
ASR_ITERATION_DELAY = 0.5
ASR_SELECT_WER = "MIN"
START_GUARD_TIME = 1
RECOGNIZE_AUDIO_REF_FILE = 0
IPC_DIR_PATH = '../WRK/IPC/'
EXP_DIR_LIST =[REF_FILE_DIR_PATH,AUDIO_REF_DIR_PATH,AUDIO_IN_DIR_PATH,COMPARED_FILE_DIR_PATH,OUT_CSV_FILE_DIR_PATH,IPC_DIR_PATH]
EXP_ARCHIVE_DIR_LIST =[REF_FILE_DIR_PATH,AUDIO_REF_DIR_PATH,AUDIO_IN_DIR_PATH,COMPARED_FILE_DIR_PATH,OUT_CSV_FILE_DIR_PATH]
EXP_AUDIO_REF = '../WRK/EXP_REF_FILES/AUDIO_REF/'
EXP_TXT_REF = '../WRK/EXP_REF_FILES/TXT_REF/'
EXP_ARCHIVE = '../WRK/EXP_ARCHIVE/'
EXP_WRK_DIR = '../WRK/'
EQIOMENT_PROFILE =[ {"id":"1","name":"name1","type":"type1","description":"test equipment 1"},
                      {"id":"2","name":"name2","type":"type2","description":"test equipment 2"}
                    ]
ROOM_PROFILE = {"id":"id1","name":"name1","type":"type1","description":"test room profile 1"}


def prepare_exp_dir(dir_list):
    for dir in dir_list:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)

# **** all experiment data known  before the experiment begins ****
def default_exp_data(src_profile,dictor_profile,equipment_profile,room_profile,exp_common,activity,
                     ext_playback_profile,ext_record_profile,asr_profile):
    exp_data = ed.exp_data()

    # ******common section******
    exp_data.set_exp_common(group_id = exp_common["group_id"],group_description = exp_common["group_description"],
                        exp_id = exp_common["exp_id"],exp_description = exp_common["exp_description"])

    # ******source section******
    wcp=audio_tools.wav_params(src_profile["src_audio_ref_file"])
    duration = audio_tools.wav_duration(src_profile["src_audio_ref_file"])
    w_count = wer.word_count(src_profile["src_txt_ref_file"])
    if duration == None or duration == 0:
        speech_tempo = 0
    else:
        speech_tempo = w_count/duration

    exp_data.set_source_audio(
        file_name =  ntpath.basename(src_profile["src_audio_ref_file"]),
        file_path = src_profile["src_audio_ref_file"],
        record_description = "",
        duration = duration,
        format_description ="{}kbit/s, {}kHz, {}bits, {}channel, ".format(wcp["flow_rate"],
                                                                          wcp["sample_rate"],wcp["bits_per_channel"],
                                                                          wcp["number_of_channels"],wcp["compression"]),
        speech_tempo = speech_tempo,
        speaker_id = dictor_profile["id"],
        speaker_name = dictor_profile["name"],
        speaker_description = dictor_profile["description"],
        )

    exp_data.set_source_text(
        file_name =  ntpath.basename(src_profile["src_txt_ref_file"]),
        file_path = src_profile["src_txt_ref_file"],
        text_description  ="",
        word_number = w_count
    )
    # ******activity section******

    exp_data.set_activity(
        activity_decription =  activity["decription"],
        activity_repetition_number = activity["repetition_number"]
    )

    # ******installation section******
    exp_data.set_equipment(equipment_profile)
    exp_data.set_room(**room_profile)

    # ******settings section******
    exp_data.set_playback(ext_playback_profile)
    ext_record_profile(ext_record_profile)
    selected_devices = audio_tools.get_selected_devices()
    playback_profile = dict.fromkeys("equipment_id","param_set")
    playback_profile["equipment_name"] =  selected_devices["out"]["Name"]
    playback_profile["equipment_type"] =  "out audio device"
    playback_profile["param_set"] = {}
    playback_profile["param_set"]["MasterVolumeLevel"] =  selected_devices["out"]["MasterVolumeLevel"]
    playback_profile["param_set"]["VolumeLevelScalar"]=  selected_devices["out"]["VolumeLevelScalar"]
    playback_profile["param_set"]["VolumeRange"] =  selected_devices["out"]["VolumeRange"]

    record_profile = dict.fromkeys("equipment_name","equipment_type","param_set")
    record_profile["equipment_name"] =  selected_devices["out"]["Name"]
    record_profile["equipment_type"] =  "input audio device"
    record_profile["param_set"] = {}
    record_profile["param_set"]["MasterVolumeLevel"] =  selected_devices["in"]["MasterVolumeLevel"]
    record_profile["param_set"]["VolumeLevelScalar"]=  selected_devices["in"]["VolumeLevelScalar"]
    record_profile["param_set"]["VolumeRange"] =  selected_devices["in"]["VolumeRange"]

    exp_data.set_record(playback_profile)
    exp_data.set_record(record_profile)
    exp_data.set_asr(**asr_profile)



def execute_exp(src_audio_ref_file,src_txt_ref_file,exp_data=None,copy_audio = True,playback = True):

    start_time = time.clock()
    time.sleep(START_GUARD_TIME)
    prepare_exp_dir(EXP_DIR_LIST)

    audio_ref_file_name = ntpath.basename(src_audio_ref_file)
    if not copy_audio:
        audio_ref_file = src_audio_ref_file
    else:
        shutil.copy2(src_audio_ref_file,AUDIO_REF_DIR_PATH)
        audio_ref_file = os.path.join(AUDIO_REF_DIR_PATH,audio_ref_file_name)

    # audio_ref_file_name = 'all_text_16_my_voice_cut.wav'
    # audio_ref_file = os.path.abspath(AUDIO_REF_DIR_PATH+audio_ref_file_name)

    audio_file_name = ".".join(audio_ref_file_name.split('.')[:-1:])+".rec.wav"
    audio_file = os.path.abspath(AUDIO_IN_DIR_PATH+audio_file_name)

    # ref_file_name = 'all_text_16_my_voice_cut.ref.txt'
    ref_file_name = ".".join(audio_ref_file_name.split('.')[:-1:])+".ref.txt"
    ref_file =os.path.abspath(REF_FILE_DIR_PATH+ref_file_name)
    shutil.copy2(src_txt_ref_file,ref_file)

    out_csv_file_name = 'out.csv'
    out_csv_file = os.path.abspath(OUT_CSV_FILE_DIR_PATH + out_csv_file_name)

    for root, dirs, files in os.walk(COMPARED_FILE_DIR_PATH, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
    for root, dirs, files in os.walk(AUDIO_IN_DIR_PATH, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
    if RECOGNIZE_AUDIO_REF_FILE == 0:
        print("Start playback file:{}, duration:{:.1f}s".format(audio_ref_file_name,
                                                                audio_tools.wav_duration(audio_ref_file)))
        audio_tools.record_playback(audio_ref_file,audio_file)
        print("End playback")
    else:
        print("Direct reference file recognition:{}, duration:{:.1f}s".format(audio_ref_file_name,
                                                                              audio_tools.wav_duration(audio_ref_file)))
        shutil.copy2(audio_ref_file,audio_file)

    print("Start ASR ")
    all_syncronized_list = []
    min_wer =  1
    max_wer = 0
    min_index = None
    max_index = None
    for i in range(ASR_ITERATIONS):

        compared_file_name = ".".join(ref_file_name.split('.')[:-2:])+"_{}_".format(str(i).zfill(2))+".cmp.txt"
        compared_file = os.path.abspath(COMPARED_FILE_DIR_PATH+compared_file_name)
        compared = ASR.recognize(audio_file)
        syncronized_list =[]
        with open(compared_file,'w',encoding='utf8') as cmp:
            cmp.write(compared)
        with open(ref_file,'r', encoding='utf-8') as ref,open(compared_file,'r',encoding='utf8') as cmp:
            syncronized_list = wer.syncronize_file(ref,cmp)
        if syncronized_list[4] >= max_wer:
            max_wer = syncronized_list[4]
            max_index = i
        if syncronized_list[4] <= min_wer:
            min_wer = syncronized_list[4]
            min_index = i
        all_syncronized_list.append(syncronized_list)
        time.sleep(ASR_ITERATION_DELAY)
        print("ASR iteration({}/{}) WER:{:.4f}".format(i+1,ASR_ITERATIONS,syncronized_list[4]))
    if ASR_SELECT_WER == "MIN":
        selected_list = all_syncronized_list[min_index]
        all_syncronized_list = []
        all_syncronized_list.append(selected_list)
        print("End ASR, MIN(WER) = {:.4f} ".format(selected_list[4]))
    elif ASR_SELECT_WER == "MAX":
        selected_list = all_syncronized_list[max_index]
        all_syncronized_list = []
        all_syncronized_list.append(selected_list)
        print("End ASR, MAX(WER) = {:.4f} ".format(selected_list[4]))
    else:
        print("End ASR")
    finish_time = time.clock()
    print("Duration {:.1f}s".format((finish_time-start_time)))
    ref_syncronized_list,all_compared_syncronized_list=wer.syncronize_all(all_syncronized_list)
    wer.save_csv(ref_syncronized_list,all_compared_syncronized_list,
                 out_csv_file,append = 0)

def generate_test_file_names(src_audio_ref_file_name):
    src_audio_ref_file = os.path.abspath(EXP_AUDIO_REF+src_audio_ref_file_name)
    src_txt_ref_file_name = ".".join(src_audio_ref_file_name.split('.')[:-1:])+".txt"
    src_txt_ref_file = os.path.abspath(EXP_TXT_REF+src_txt_ref_file_name)
    return src_audio_ref_file,src_txt_ref_file_name,src_txt_ref_file

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
def archive_exp(archive_name):
    zipf = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in EXP_ARCHIVE_DIR_LIST:
        zipdir(dir, zipf)
    zipf.close()

def zip_archive():
    zipf = zipfile.ZipFile(EXP_ARCHIVE+'Python.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(EXP_ARCHIVE):
        for file in files:
            zipf.write(os.path.join(root, file))


if __name__ == "__main__":
    # print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()).replace(":","_"))
    # exit (0)
    exp_data = ed.exp_data()
    # exp_data.set_common(group_id = 1,group_description = "test",exp_id = 1,
    #                     exp_description = "playback and recognize all_text_16_my_voice_cut.wav")
    src_audio_ref_file_name = 'all_text_16_my_voice_cut.wav'
    src_audio_ref_file,src_txt_ref_file_name,src_txt_ref_file = generate_test_file_names(src_audio_ref_file_name)

    execute_exp(src_audio_ref_file,src_txt_ref_file,exp_data)
    archive_exp(EXP_ARCHIVE+"exp{:%Y-%m-%d %H:%M:%S}.zip".format(datetime.datetime.now()).replace(":","_"))
    exit(0)

    # dict.fromkeys("group_id","group_description","exp_id","exp_description")

    '''
    start_time = time.clock()
    time.sleep(START_GUARD_TIME)
    audio_ref_file_name = 'all_text_16_my_voice_cut.wav'
    # audio_ref_file_name = 'all_text_16_my_voice.wav'
    audio_ref_file = os.path.abspath(AUDIO_REF_DIR_PATH+audio_ref_file_name)
    audio_file_name = ".".join(audio_ref_file_name.split('.')[:-1:])+".rec.wav"
    audio_file = os.path.abspath(AUDIO_IN_DIR_PATH+audio_file_name)

    # ref_file_name = 'all_text_16_my_voice_cut.ref.txt'
    ref_file_name = ".".join(audio_ref_file_name.split('.')[:-1:])+".ref.txt"
    ref_file =os.path.abspath(REF_FILE_DIR_PATH+ref_file_name)
    out_csv_file_name = 'out.csv'
    out_csv_file = os.path.abspath(OUT_CSV_FILE_DIR_PATH + out_csv_file_name)

    for root, dirs, files in os.walk(COMPARED_FILE_DIR_PATH, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
    for root, dirs, files in os.walk(AUDIO_IN_DIR_PATH, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
    if RECOGNIZE_AUDIO_REF_FILE == 0:
        print("Start playback file:{}, duration:{:.1f}s".format(audio_ref_file_name,audio_tools.wav_duration(audio_ref_file)))
        audio_tools.record_playback(audio_ref_file,audio_file)
        print("End playback")
    else:
        print("Direct reference file recognition:{}, duration:{:.1f}s".format(audio_ref_file_name,audio_tools.wav_duration(audio_ref_file)))
        shutil.copy2(audio_ref_file,audio_file)

    print("Start ASR ")
    all_syncronized_list = []
    min_wer =  1
    max_wer = 0
    min_index = None
    max_index = None
    for i in range(ASR_ITERATIONS):

        compared_file_name = ".".join(ref_file_name.split('.')[:-2:])+"_{}_".format(str(i).zfill(2))+".cmp.txt"
        compared_file = os.path.abspath(COMPARED_FILE_DIR_PATH+compared_file_name)
        compared = ASR.recognize(audio_file)
        syncronized_list =[]
        with open(compared_file,'w',encoding='utf8') as cmp:
            cmp.write(compared)
        with open(ref_file,'r', encoding='utf-8') as ref,open(compared_file,'r',encoding='utf8') as cmp:
            syncronized_list = wer.syncronize_file(ref,cmp)
        if syncronized_list[4] >= max_wer:
            max_wer = syncronized_list[4]
            max_index = i
        if syncronized_list[4] <= min_wer:
            min_wer = syncronized_list[4]
            min_index = i
        all_syncronized_list.append(syncronized_list)
        time.sleep(ASR_ITERATION_DELAY)
        print("ASR iteration({}/{}) WER:{:.4f}".format(i+1,ASR_ITERATIONS,syncronized_list[4]))
    if ASR_SELECT_WER == "MIN":
        selected_list = all_syncronized_list[min_index]
        all_syncronized_list = []
        all_syncronized_list.append(selected_list)
        print("End ASR, MIN(WER) = {:.4f} ".format(selected_list[4]))
    elif ASR_SELECT_WER == "MAX":
        selected_list = all_syncronized_list[max_index]
        all_syncronized_list = []
        all_syncronized_list.append(selected_list)
        print("End ASR, MAX(WER) = {:.4f} ".format(selected_list[4]))
    else:
        print("End ASR")
    finish_time = time.clock()
    
    print("Duration {:.1f}s".format((finish_time-start_time)))
    ref_syncronized_list,all_compared_syncronized_list=wer.syncronize_all(all_syncronized_list)   
    wer.save_csv(ref_syncronized_list,all_compared_syncronized_list,out_csv_file,append = 0)
    '''
