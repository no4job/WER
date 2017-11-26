# EXP_AUDIO_REF = '../WRK/EXP_REF_FILES/AUDIO_REF/'
# EXP_TXT_REF = '../WRK/EXP_REF_FILES/TXT_REF/'

# ***src profiles*****
# src_profile_1 = {
#     "src_audio_ref_file":EXP_AUDIO_REF+'all_text_16_my_voice_cut.wav',
#     "src_txt_ref_file":"EXP_TXT_REF"+"all_text_16_my_voice_cut.txt"
# }

# ***dictor profiles*****
dictor_profile_1 = {
    "id":1,
    "name":"DM",
    "description":"one and only"
}

# ***equipment profiles*****
equipment_profile_1 = [
    { "id":1,
    "name":"Динамики (Realtek High Definition Audio)",
    "description":"выходное аудиоустройство, физическое устройство - встроенная аудиокарта"
      },
    { "id":2,
      "name":"Микрофон (B525 HD Webcam)",
      "description":"входное аудиоустройство, физическое устройство - Веб-камера Logitech HD Webcam B525"
      },
    { "id":3,
      "name":"Акустическая система",
      "description":"акустическая система xyz"
      }
    ]

# ***room profile*****
room_profile_1 =  { "id":1,
      "name":"Помещение 1",
      "description":"комната 2,5*6*2,15"
      }
room_profile_2 =  { "id":1,
                    "name":"Помещение 2",
                    "description":"комната 5*3*3"
                    }

# ***ext playback profile*****
ext_playback_profile_1 =  {"equipment_id":3,
                           "param_set":{"VolumeLevelScalar":0.2}
                    }
# ***ext record profile*****
ext_record_profile_1 =  {}



ext_record_profile = None
asr_profile = None