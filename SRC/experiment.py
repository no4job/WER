import os
import ASR
import wer
import time
import audio_tools
import shutil
CALC_DIR = 0
REF_FILE_DIR_PATH = '../REF_TXT/'
# REF_FILE_NAME = 'ref.txt'
COMPARED_FILE_DIR_PATH = '../TXT_OUT/'
# COMPARED_FILE_NAME = 'compared.txt'
OUT_CSV_FILE_DIR_PATH = '../CSV_OUT/'
# OUT_CSV_FILE_NAME = 'out.csv'
AUDIO_REF_DIR_PATH = '../AUDIO_REF/'
AUDIO_IN_DIR_PATH = '../AUDIO_IN/'
ASR_ITERATIONS = 5
ASR_ITERATION_DELAY = 0.5
ASR_SELECT_WER = "MIN"
START_GUARD_TIME = 1
RECOGNIZE_AUDIO_REF_FILE = 0

if __name__ == "__main__":
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
    wer.save_csv(ref_syncronized_list,all_compared_syncronized_list,
                 out_csv_file,append = 0)