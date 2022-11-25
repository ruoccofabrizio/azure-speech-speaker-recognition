from ntpath import join
import azure.cognitiveservices.speech as speechsdk
from random import randint
from os import path
import os

def synt_text (text, scope, voice_name): 
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = os.environ['Azure_Speech_Key']
    service_region = os.environ['Azure_Speech_Region']

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voice_name

    audio_config = speechsdk.audio.AudioOutputConfig(filename= path.join('.','data',f'{voice_name}{scope}.wav'))
    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def generate_audio_files(**kwargs):
    name = kwargs.get('name', 'Cataldo')
    person_name = kwargs.get('name', 'Pierina Bianchi')
    generate_audio= kwargs.get('generate_audio', ["Enroll","Verify"])
    auth_code= kwargs.get('auth_code', randint(0,99999))
    print(auth_code)
    voice_name = f"{os.environ['language']}-{name}Neural"

    text_first = os.environ['activation_phrase']
    text = os.environ['custom_phrase']
    text_verify = f"Sono {person_name} ed il mio codice di conferma per l'operazione è {auth_code:05}"

    if "Enroll" in generate_audio:
        synt_text(text_first, "_first", voice_name)
        synt_text(text, "", voice_name)
    if "Verify" in generate_audio:
        synt_text(text_verify, "_verify", voice_name)