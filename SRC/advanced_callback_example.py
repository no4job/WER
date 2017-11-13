from asrclient.voiceproxy_pb2 import AddDataResponse as AsrResponse
import pickle
import dill
import sys
"""
use it like
./asrclient-cli.py -k <your-key> --callback-module advanced_callback_example --silent <path-to-your-sound.wav>
"""

asr_response_lst = []
call_count = 0
session_id = "not-set"
def advanced_callback(asr_response, correction = 0):

    if not dill.pickles(asr_response):
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print (asr_response)
        print("recursionlimit: {}".format(sys.getrecursionlimit()))
        # sys.setrecursionlimit(10000)
        # print("asr_response.responseCode:  "+dill.pickles(asr_response.responseCode))
        print("recognition:  "+dill.pickles(asr_response.recognition["confidence"]))
        # print (dill.detect.badtypes(asr_response, depth=1).keys())

    global asr_response_lst
    asr_response_lst.append(asr_response)
    print ("******************************************************************")
    # print (asr_response_lst)
    global call_count
    with open('..\\IPC\\asr_responce_lst_{}.pickle'.format(call_count), 'wb') as f:
        # pickle.dump(asr_responce_lst, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(asr_response, f)
        # pickle.dump({"confidence": 0.0,"value": "\321\217","align_info":{"start_time": 42.21000289916992,"end_time": 42.27000427246094,"acoustic_score": 0.0}}, f)
    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    call_count+=1

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


def advanced_utterance_callback(asr_response, data_chunks):
    data_length = 0
    for chunk in data_chunks:
        data_length += len(chunk) if chunk else 0
    print("Got complete utterance, for {0} data_chunks, session_id = {1}".format(len(data_chunks), session_id))
    print("Metainfo", asr_response.metainfo.minBeam, asr_response.metainfo.maxBeam)
    print("Data length = {0}".format(data_length))
