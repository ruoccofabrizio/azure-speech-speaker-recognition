import streamlit as st
import os, json, re
from urllib.error import URLError
from random import randint
from pydub import AudioSegment
from audiorecorder import audiorecorder
import requests

from generateaudio import generate_audio_files
from speakerverification import enroll_profile, verify_profile

def generate_new_auth_code():
    st.session_state['auth_code'] = randint(10000,99999)

def generate_audio_file_with_auth_code(**kwargs):
    st.session_state['used_auth_code'] = st.session_state['auth_code']
    generate_audio_files(**kwargs)

def save_audio_wav(val, prefix, suffix):
    # AudioSegment.converter = r"ffmpeg.exe"
    with open(os.path.join('data',f"{os.environ['language']}-{prefix}Neural{suffix}.mp3"), "wb") as wav_file:
        wav_file.write(val.tobytes())
    sound = AudioSegment.from_file(os.path.join('data',f"{os.environ['language']}-{prefix}Neural{suffix}.mp3"))
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    sound.export(os.path.join('data',f"{os.environ['language']}-{prefix}Neural{suffix}.wav"), format="wav")
    st.audio(os.path.join('data',f"{os.environ['language']}-{prefix}Neural{suffix}.wav"))

def set_activation_phrase_and_voices():
    speech_key = os.environ['Azure_Speech_Key']
    service_region = os.environ['Azure_Speech_Region']
    # Get ActivationPhrase for selected locale
    url = f"https://{service_region}.api.cognitive.microsoft.com/speaker-recognition/verification/text-independent/phrases/{os.environ['language']}?api-version=2021-09-05"
    headers = {"Ocp-Apim-Subscription-Key": speech_key}
    r = requests.get(url, headers=headers)
    os.environ['activation_phrase'] = r.json()['value'][0].get('activationPhrase', "I'll talk for a few seconds so you can recognize my voice in the future.")
    # Get available voices for selected locale
    url = f"https://{service_region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    r = requests.get(url, headers=headers)
    return sorted(list(filter(None,map(lambda x: x['DisplayName'] if x['Locale'].lower() == os.environ['language'] and x['VoiceType'] == 'Neural' else None, r.json()))))


########## START - MAIN ##########
try:
    # Set page layout to wide screen and menu item
    menu_items = {
	'Get help': None,
	'Report a bug': None,
	'About': '''
	 ## Embeddings App

	Azure Speaker Recognition Sample Demo.
	'''
    }
    st.set_page_config(layout="wide", menu_items=menu_items)

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    if 'voice_name' not in st.session_state:
        st.session_state['voice_name'] = None
    if 'auth_code' not in st.session_state:
        st.session_state['auth_code'] = randint(10000,99999)
    if 'verification_voice' not in st.session_state:
        st.session_state['verification_voice'] = None
    if 'used_auth_code' not in st.session_state:
        st.session_state['used_auth_code'] = None

    # Set activation phrase and available voices for specified language
    available_voices = set_activation_phrase_and_voices()

    profile_db = "profiles_db.json"
    with open(profile_db,'r') as f:
        data = json.load(f)   


    # Voice Enrollment
    st.title("Enroll voice")
    col1, col2, col3 = st.columns([1,1,2])

    with col1:
        st.session_state['voice_name'] = st.selectbox("Custom Neural Voice", available_voices)
    
    audio_generated = False
    if os.path.exists(os.path.join('data',f"{os.environ['language']}-{st.session_state['voice_name']}Neural_first.wav")):
        audio_generated = True

    if st.session_state['voice_name']:
        with col2:
            st.write("-")
            st.button("Generate voice sample", on_click=generate_audio_files, kwargs={"name": st.session_state['voice_name'], "person_name": st.session_state['voice_name'], "generate_audio": "Enroll"}, disabled= (audio_generated or st.session_state['voice_name'] == None))
        
        with col3:     
            st.write("-")
            st.button("Enroll voice", on_click=enroll_profile, kwargs= {"profile_name": st.session_state['voice_name']},  disabled= not audio_generated)


        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            st.write("Activation phrase")
            st.write(os.environ['activation_phrase'])
        with col2:
            st.write("-")
            if os.path.exists(os.path.join('data',f"{os.environ['language']}-{st.session_state['voice_name']}Neural_first.wav")):
                st.audio(os.path.join('data',f"{os.environ['language']}-{st.session_state['voice_name']}Neural_first.wav"))
        with col3:
            st.write("Custom audio 20s")
            st.write(os.environ['custom_phrase'])
        with col4:  
            st.write("-")  
            if os.path.exists(os.path.join('data',f"{os.environ['language']}-{st.session_state['voice_name']}Neural.wav")):
                st.audio(os.path.join('data',f"{os.environ['language']}-{st.session_state['voice_name']}Neural.wav"))


    # Voice Recording
    st.title("Record voice")
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    with col1:
        recorded_name = st.text_input("Enter a voice name:")

    col1, col2, col3, col4 = st.columns([1,1,1,1])

    if recorded_name:
        if recorded_name not in data.keys():
            with col1:
                st.header("Activation phrase")
                
                prefix = recorded_name
                suffix = "_first"
                
                if os.path.exists(os.path.join('data',f"{os.environ['language']}-{recorded_name}Neural{suffix}.wav")):
                    st.write("Activation phrase correctly recorded!")
                    st.audio(os.path.join('data',f"{os.environ['language']}-{recorded_name}Neural{suffix}.wav"))
                else:
                    val_first = audiorecorder("Record Activation phrase", "Stop recording")
                    st.write(os.environ['activation_phrase'])
                    if len(val_first) > 0:
                        save_audio_wav(val_first, prefix, suffix)
                            
            with col2: 
                st.header("Custom audio")

                prefix = recorded_name
                suffix = ""

                if os.path.exists(os.path.join('data',f"{os.environ['language']}-{recorded_name}Neural.wav")):
                    st.write("Custom audio correctly recorded!")
                    st.audio(os.path.join('data',f"{os.environ['language']}-{recorded_name}Neural.wav"))
                else:
                    val = audiorecorder("Record Custom audio", "Stop recording")
                    st.write(os.environ['custom_phrase'])
                    if len(val) > 0:
                        save_audio_wav(val, prefix, suffix)
                         
            with col3:
                st.header('Continue Enrollment')
                st.write("To enroll a voice, please record the Activation and Custom Audio")
                if os.path.exists(os.path.join('data',f"{os.environ['language']}-{recorded_name}Neural_first.wav")) and os.path.exists(os.path.join('data',f"os.environ['language']{recorded_name}Neural.wav")):
                    st.button("Enroll", on_click=enroll_profile, kwargs= {"profile_name": recorded_name})
        else:
            st.write(f"{recorded_name} is enrolled! Please choice a different Voice name to enroll it.")
        
                   
    # Voice Verification
    st.title("Verify voice")
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    profiles = [None]
    profiles += data.keys()

    with col1:
        st.session_state['verification_voice'] = st.selectbox("Voice sample", profiles)

    with col4:
        profile = st.selectbox("Enrolled voice", profiles)

    with col2: 
        st.write(f'Auth code: {st.session_state["auth_code"]:05}')
        st.button("Generate New Auth Code", on_click= generate_new_auth_code)
        if st.session_state['verification_voice'] in available_voices:
            st.button("Generate Verification Audio", on_click=generate_audio_file_with_auth_code, kwargs={"name": st.session_state['verification_voice'], "person_name": st.session_state['verification_voice'], "generate_audio": "Verify", "auth_code" :st.session_state['auth_code']})
        else:            
            if not os.path.exists(os.path.join('data',f"{os.environ['language']}-{st.session_state['verification_voice']}Neural_verify{st.session_state['auth_code']}.wav")):
                st.write(f"Record voice: Sono {st.session_state['verification_voice']} ed il mio codice di autorizzazione è {st.session_state['auth_code']:05}")

                prefix = st.session_state["verification_voice"]
                suffix = f'_verify{st.session_state["auth_code"]}'

                val_verify = audiorecorder("Record", "Stop recording")
                if len(val_verify) > 0:
                    save_audio_wav(val_verify, prefix, suffix)

    with col3:
        if st.session_state['verification_voice'] != None and os.path.exists(os.path.join('data',f"{os.environ['language']}-{st.session_state['verification_voice']}Neural_verify{st.session_state['auth_code']}.wav")):
            st.write('Generated Audio')
            st.audio(os.path.join('data', f"{os.environ['language']}-{st.session_state['verification_voice']}Neural_verify{st.session_state['auth_code']}.wav"), format="audio/wav")
            if st.session_state['verification_voice'] != None and profile != None:
                result_json = verify_profile(file_name= st.session_state['verification_voice'], profile_name= profile, auth_code= st.session_state['auth_code'])
                st.write(result_json)

                if result_json['recognitionResult'] == 'Reject':
                    st.write("Voice not recognized")


                regex = r"[0-9]"
                matches = re.finditer(regex, result_json['Text'], re.MULTILINE)
                detected_code = ""
                for matchNum, match in enumerate(matches, start=1):
                    detected_code += match.group()

                if str(st.session_state['auth_code']) == detected_code:
                    st.write(f"Code Successfully Verified")
                else:
                    st.write(f"Code Authorization Failed")


except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
        """
        % e.reason
    )

########## END - MAIN ##########

