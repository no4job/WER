from asrclient.voiceproxy_pb2 import AddDataResponse as AsrResponse
import pickle
# import dill
# import sys
import os
IPC_FILE = '..\\WRK\\IPC\\asr_responce_lst.pickle'
"""
use it like
./asrclient-cli.py -k <your-key> --callback-module advanced_callback_example --silent <path-to-your-sound.wav>
"""

try:
    os.remove(IPC_FILE)
except OSError:
    pass
asr_response_lst = []
call_count = 0
session_id = "not-set"
def advanced_callback(asr_response, correction = 0):
    global asr_response_lst
    if asr_response.endOfUtt:
        r_count = 0
        response = []
        for r in asr_response.recognition:
            hyp = {}
            # word = {}
            hyp['confidence']= r.confidence
            hyp['normalized']= r.normalized
            hyp['start_time']= r.align_info.start_time+correction
            hyp['end_time']= r.align_info.end_time+correction
            # print("recognition[{}] = {}; confidence = {}".format(r_count, r.normalized, r.confidence))
            # print("utterance timings: from {} to {}".format(r.align_info.start_time+correction,r.align_info.end_time+correction))
            hyp['word'] = []
            w_count = 0
            for w in r.words:
                word ={}
                word['confidence']= w.confidence
                word['value']= w.value
                word['start_time']= w.align_info.start_time+correction
                word['end_time']= w.align_info.end_time+correction
                # print("word[{}] = {}; confidence = {}".format(w_count, w.value.encode("utf-8"), w.confidence))
                # print("word[{}] = {}; confidence = {}".format(w_count, w.value, w.confidence))
                # print("word timings: from {} to {}".format(w.align_info.start_time+correction,w.align_info.end_time+correction))
                hyp['word'].append(word)
                w_count += 1
            r_count += 1
            response.append(hyp)
        asr_response_lst.append(response)
        # with open('..\\IPC\\asr_responce_lst_{}.pickle'.format(call_count), 'wb') as f:
        with open(IPC_FILE, 'wb') as f:
            pickle.dump(asr_response_lst, f)
'''
    print("Got response:")
    print("end-of-utterance = {}".format(asr_response.endOfUtt))
    r_count = 0
    for r in asr_response.recognition:
        # print("recognition[{}] = {}; confidence = {}".format(r_count, r.normalized.encode("utf-8"), r.confidence))
        print("recognition[{}] = {}; confidence = {}".format(r_count, r.normalized, r.confidence))
        # print("recognition[{}] = {}; confidence = {}".format(r_count, r.normalized.encode("utf-8"), r.confidence))
        print("utterance timings: from {} to {}".format(r.align_info.start_time+correction,r.align_info.end_time+correction))
        w_count = 0
        for w in r.words:
            # print("word[{}] = {}; confidence = {}".format(w_count, w.value.encode("utf-8"), w.confidence))
            print("word[{}] = {}; confidence = {}".format(w_count, w.value, w.confidence))
            print("word timings: from {} to {}".format(w.align_info.start_time+correction,w.align_info.end_time+correction))
            w_count += 1
        r_count += 1
'''
def advanced_utterance_callback(asr_response, data_chunks):
    pass

# def advanced_utterance_callback(asr_response, data_chunks):
#     data_length = 0
#     for chunk in data_chunks:
#         data_length += len(chunk) if chunk else 0
#     print("Got complete utterance, for {0} data_chunks, session_id = {1}".format(len(data_chunks), session_id))
#     print("Metainfo", asr_response.metainfo.minBeam, asr_response.metainfo.maxBeam)
#     print("Data length = {0}".format(data_length))
