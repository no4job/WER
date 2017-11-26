import collections
import copy


class exp_data:
    def __init__(self):
        self.current_repetition = None
        self.repetition_id = 0
        self.data = dict.fromkeys(["exp_common","source","final_result","activity","installation","settings",
                                  "final_log","comment","repetition"])
        self.get_common()
        self.get_source()
        self.get_final_result()
        self.get_activity()
        self.get_installation()
        self.get_settings()
        self.get_final_log()
        self.get_comment()
        self.get_repetition()
        # self.data_r = copy.deepcopy(self.data)
    
        
    def get_common(self):
        if self.data["exp_common"] != None:
            return self.data["exp_common"]
        self.data["exp_common"] = dict.fromkeys(["group_id","group_description","exp_id","exp_description"])
        return self.data["exp_common"]

    def set_exp_common(self,**kwargs):
        for k,v in kwargs.items():
            # if k not in self.data["group"]:
            #     raise ValueError('Bad parameter in {}: {}:{}'.format("group",k,v))
            self.data["exp_common"][k] = v


    def get_source(self):
        if self.data["source"] != None:
            return self.data["source"]
        source_audio = dict.fromkeys(["file_name","file_path","record_description","duration","format_description",
                                     "speech_tempo","speaker_id","speaker_name","speaker_description"])
        source_text = dict.fromkeys(["file_name","file_path","text_description","word_number"])
        source =  dict(audio = source_audio,text = source_text)
        self.data["source"] = source
        return self.data["source"]

    def set_source_audio(self,**kwargs):
        for k,v in kwargs.items():
            self.data["source"]["audio"][k] = v
    def set_source_text(self,**kwargs):
        for k,v in kwargs.items():
            self.data["source"]["text"][k] = v

    def set_source(self,source_audio,source_text):
        self.set_source_audio(**source_audio)
        self.set_source_text(**source_text)

    def get_final_result(self):
        if self.data["final_result"] != None:
            return self.data["final_result"]
        final_result = dict.fromkeys(["wer_min","wer_max","wer_avg"])
        self.data["final_result"]=final_result
        return self.data["final_result"]

    def set_final_result(self,**kwargs):
        for k,v in kwargs.items():
            self.data["final_result"][k] = v

    def get_activity(self):
        if self.data["activity"] != None:
            return self.data["activity"]
        self.data["activity"] = dict.fromkeys(["activity_decription","activity_repetition_number"])

    def set_activity(self,**kwargs):
        for k,v in kwargs.items():
            self.data["activity"][k] = v


    def get_installation(self):
        if self.data["installation"] != None:
            return self.data["installation"]
        equipment = list([dict.fromkeys(["id","name","type","description"])])
        room = dict.fromkeys(["id","name","type","description"])
        installation = dict(equipment = equipment,room = room)
        self.data["installation"]=installation
        return self.data["installation"]

    def set_equipment(self,equipment_lst):
        for equipment in equipment_lst:
            equipment_ = copy.deepcopy(self.data["installation"]["equipment"][0])
            for k,v in equipment.items():
                equipment_[k] = v
            self.data["installation"]["equipment"].append([equipment_])
        del self.data["installation"]["equipment"][0]

    def set_room(self,**kwargs):
        for k,v in kwargs.items():
            self.data["room"][k] = v

    def get_settings(self):
        if self.data["settings"] != None:
            return self.data["settings"]
        playback_stage = dict.fromkeys(["equipment_id","param_set"])
        playback = list([playback_stage])
        record_stage = dict.fromkeys(["equipment_id","param_set"])
        record = list([record_stage])
        asr = dict.fromkeys(["options","asr_repetition_number","selection_type"])
        settings = dict(playback = playback,record = record,asr = asr)
        self.data["settings"]=settings
        return self.data["settings"]

    def set_playback(self,playback):
        for playback_stage in playback:
            playback_stage_ = copy.deepcopy(self.data["settings"]["playback"][0])
            for k,v in playback_stage.items():
                if k == "param_set":
                    playback_stage_[k] = copy.deepcopy(v)
                else:
                    playback_stage_[k] = v
            self.data["settings"]["playback"].append([playback_stage_])
        del self.data["settings"]["playback"][0]

    def set_record(self,record):
        for record_stage in record:
            record_stage_ = copy.deepcopy(self.data["settings"]["record"][0])
            for k,v in record_stage.items():
                if k == "param_set":
                    record_stage_[k] = copy.deepcopy(v)
                else:
                    record_stage_[k] = v
            self.data["settings"]["record"].append([record_stage_])
        del self.data["settings"]["record"][0]

    def set_asr(self,**kwargs):
        for k,v in kwargs.items():
            self.data["asr"][k] = v

    def get_final_log(self):
        if self.data["final_log"] != None:
            return self.data["final_log"]
        final_log = dict.fromkeys(["exp_start_time","exp_end_time","success","return_code","executed_repetitions",
                                  "final_description"])
        self.data["final_log"]=final_log
        return self.data["final_log"]

    def set_final_log(self,**kwargs):
        for k,v in kwargs.items():
            self.data["final_log"][k] = v


    def get_comment(self):
        if self.data["comment"] != None:
            return self.data["comment"]
        self.data["comment"]=""
        return self.data["comment"]

    def set_comment(self,**kwargs):
        for k,v in kwargs.items():
            self.data["comment"][k] = v


    def get_new_repetition(self):
        if self.current_repetition != None:
            self.current_repetition = None
            return self.get_repetition()
        return None

    def get_repetition(self):
        if self.current_repetition != None:
            return self.current_repetition
        if self.data["repetition"] == None:
            self.data["repetition"] = []
        repetition = dict.fromkeys(["repetition_result","repetition_log"])
        self.data["repetition"].append([repetition])
        repetition["repetition_result"] = self.get_repetition_result(repetition)
        repetition["repetition_log"] = self.get_repetition_log(repetition)
        self.current_repetition = repetition
        return repetition
        
    def get_repetition_result(self,repetition):
        if repetition["repetition_result"] != None:
            return repetition["repetition_result"]
        result_audio = dict.fromkeys(["file_name","source_path","record_description","duration","format_description",
                                     "speech_tempo","speaker_id","speaker_name","speaker_description"])
        result_text = dict.fromkeys(["file_name","source_path","text_description","word_number"])
        wer = dict.fromkeys(["wer_all","wer_min","wer_max"])
        repetition_result = dict(audio = result_audio,text = result_text,wer = wer)
        return repetition_result
        
    
    def set_result_audio(self,repetition,**kwargs):
        for k,v in kwargs.items():
            repetition["repetition_result"]["audio"][k] = v

    def set_result_text(self,repetition,**kwargs):
        for k,v in kwargs.items():
            repetition["repetition_result"]["text"][k] = v
            
    def set_result_wer(self,repetition,**kwargs):
        for k,v in kwargs.items():
            repetition["repetition_result"]["wer"][k] = v
            
    def set_repetition_result(self,repetition,audio,text,wer):
        self.set_result_audio(repetition,**audio)
        self.set_result_text(repetition,**text)
        self.set_result_wer(repetition,**wer)


    def get_repetition_log(self,repetition):
        if repetition["repetition_log"] != None:
            return repetition["repetition_log"]
        repetition_log = dict.fromkeys(["repetition_id","repetition_start_time","repetition_end_time","success",
                                       "return_code","description","repetition_event_log"])
        repetition_event_log = list([dict.fromkeys(["time","event_id","event_type","event_description"])])
        repetition_log["repetition_event_log"] = repetition_event_log
        return repetition_log


    def set_repetition_log(self,repetition,**kwargs):
        for k,v in kwargs.items():
            repetition["repetition_log"][k] = v
        repetition_event_log = []
        for event in repetition["repetition_log"]["repetition_event_log"]:
            repetition_event_log_ = copy.deepcopy(repetition["repetition_log"]["repetition_event_log"][0])
            for k,v in event.items():
                repetition_event_log_[k] = v
            repetition_event_log.append([repetition_event_log_])
        repetition["repetition_log"]["repetition_event_log"][0]=repetition_event_log