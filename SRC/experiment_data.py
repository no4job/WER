import collections

class FixedDict(collections.MutableMapping):
    def __init__(self, data):
        self.__data = data

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __setitem__(self, k, v):
        if k not in self.__data:
            raise KeyError(k)

        self.__data[k] = v

    def __delitem__(self, k):
        raise NotImplementedError

    def __getitem__(self, k):
        return self.__data[k]

    def __contains__(self, k):
        return k in self.__data

class exp_data:
    def __init__(self):
        self.data = dict.fromkeys("group","source","result","action","installation","settings","log","comments")

        self.group = dict.fromkeys("id","description")
        self.result = dict.fromkeys("repetion_result","final_result")
        self.repetion_result = dict.fromkeys("repetion_id","audio","text","wer")
        self.final_result = dict.fromkeys("wer_min","wer_min_repetion_id","wer_max","wer_max_repetion_id","wer_avg")
        self.action = dict.fromkeys("decription","exp_repetition_number")
        self.installation = dict.fromkeys("equipment","room")
        self.settings = dict.fromkeys("playback","record","asr")

        self.audio = dict.fromkeys("file_name","source_path","record_description","duration","format_description",
                                        "speech_tempo","speaker_id","speaker_name","speaker_description")
        self.text = dict.fromkeys("file_name","source_path","text_description","word_number")
        self.equipment = dict.fromkeys("id","name","type","description")
        self.room = dict.fromkeys("id","name","type","description")
        self.playback_stage = dict.fromkeys("id","equipment_id","name","type","gain","gain_name")
        self.record_stage = dict.fromkeys("id","equipment_id","name","type","gain","gain_name")
        self.asr = dict.fromkeys("options","asr_repetition_number","selection_type")

        self.wer = dict.fromkeys("wer_all","wer_min","wer_max")
